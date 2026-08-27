"""Сервис для операций с проектными треками."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from accounts.models import Department, Semester
from showcase.domain.project_track import ProjectTrackDomain
from showcase.dto.project_track import (
    ProjectTrackAddApplicationsDTO,
    ProjectTrackAddGroupsDTO,
    ProjectTrackAggregatedStatisticsDTO,
    ProjectTrackCreateDTO,
    ProjectTrackGroupDetailDTO,
    ProjectTrackGroupListDTO,
    ProjectTrackProjectDetailDTO,
    ProjectTrackProjectListDTO,
    ProjectTrackReadDTO,
    ProjectTrackStatisticsDTO,
    ProjectTrackUpdateDTO,
)
from showcase.models import Institute, ProjectTrack
from showcase.repositories.project_track import ProjectTrackRepository

if TYPE_CHECKING:
    from accounts.models import User as UserType

User = get_user_model()


class ProjectTrackService:
    """Оркестрация Domain + Repository для проектных треков."""

    def __init__(self) -> None:
        self.repository = ProjectTrackRepository()
        self.domain = ProjectTrackDomain()

    def _ensure_user_department(self, user: UserType) -> None:
        """Подгружает подразделение пользователя для проверки институтов."""
        if user.department_id and not getattr(user.department, "parent", None):
            try:
                department = Department.objects.select_related("parent").get(
                    pk=user.department_id
                )
                user.department = department
            except Department.DoesNotExist:
                pass

    def _check_manage_permission(self, user: User) -> None:
        """Проверяет право управления треками."""
        can_manage, error = self.domain.can_manage_tracks(user)
        if not can_manage:
            raise PermissionError(error)

    def _get_accessible_department_ids(self, user: User) -> list[int] | None:
        """Возвращает доступные подразделения пользователя."""
        self._ensure_user_department(user)
        return self.domain.get_accessible_department_ids(user)

    def _resolve_institute_semester(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
        *,
        institute_code_required: bool = True,
    ) -> tuple[int, list[str] | None, str]:
        """Валидирует доступ; возвращает semester_id, коды институтов и institute_code."""
        self._check_manage_permission(user)
        self._ensure_user_department(user)

        if institute_code_required:
            resolved_institute_code = self.domain.resolve_institute_code(
                user, institute_code
            )
        else:
            if not institute_code:
                raise ValueError("Параметр institute_code обязателен")
            resolved_institute_code = institute_code

        if not Institute.objects.filter(code=resolved_institute_code).exists():
            raise ValueError(f"Институт с кодом={resolved_institute_code} не найден")

        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        accessible_codes = self.domain.get_accessible_institute_codes(user)

        if (
            accessible_codes is not None
            and resolved_institute_code not in accessible_codes
        ):
            raise PermissionError(
                "Недостаточно прав для просмотра треков указанного института"
            )

        return semester_id, accessible_codes, resolved_institute_code

    def _get_track_with_access(self, user: User, track_id: int) -> ProjectTrack:
        """Возвращает трек с проверкой доступа."""
        self._check_manage_permission(user)
        accessible_department_ids = self._get_accessible_department_ids(user)

        track = self.repository.get_by_id(track_id)
        if track is None:
            raise ValueError(f"Проектный трек с id={track_id} не найден")

        can_access, error = self.domain.can_access_track(
            user, track, accessible_department_ids
        )
        if not can_access:
            raise PermissionError(error)

        return track

    def list_tracks(
        self,
        user: User,
        semester_id_raw: str,
        *,
        department_id: int | None = None,
        institute_code: str | None = None,
    ) -> QuerySet[ProjectTrack]:
        """Список треков по фильтрам."""
        self._check_manage_permission(user)
        accessible_department_ids = self._get_accessible_department_ids(user)

        semester_id = Semester.resolve_list_semester_id(semester_id_raw)

        if institute_code:
            accessible_codes = self.domain.get_accessible_institute_codes(user)
            if accessible_codes is not None and institute_code not in accessible_codes:
                raise PermissionError(
                    "Недостаточно прав для просмотра треков указанного института"
                )
            if not Institute.objects.filter(code=institute_code).exists():
                raise ValueError(f"Институт с кодом={institute_code} не найден")

        if department_id is not None:
            ok, error = self.domain.validate_department_access(
                department_id, accessible_department_ids
            )
            if not ok:
                raise PermissionError(error)

        return self.repository.list_tracks(
            semester_id,
            department_id=department_id,
            institute_code=institute_code,
            accessible_department_ids=accessible_department_ids,
        )

    def get_track(self, user: User, track_id: int) -> dict:
        """Возвращает детали трека."""
        track = self._get_track_with_access(user, track_id)
        return ProjectTrackReadDTO(track).to_dict()

    @transaction.atomic
    def create_track(self, user: User, dto: ProjectTrackCreateDTO) -> dict:
        """Создаёт проектный трек."""
        self._check_manage_permission(user)
        accessible_department_ids = self._get_accessible_department_ids(user)

        if not dto.name.strip():
            raise ValueError("Поле name не может быть пустым")

        if not Department.objects.filter(pk=dto.department_id).exists():
            raise ValueError(f"Подразделение с id={dto.department_id} не найдено")

        if not Semester.objects.filter(pk=dto.semester_id).exists():
            raise ValueError(f"Семестр с id={dto.semester_id} не найден")

        ok, error = self.domain.validate_department_access(
            dto.department_id, accessible_department_ids
        )
        if not ok:
            raise PermissionError(error)

        track = self.repository.create(
            name=dto.name.strip(),
            description=dto.description,
            department_id=dto.department_id,
            semester_id=dto.semester_id,
            author_id=user.pk,
            min_team_members=dto.min_team_members,
            max_team_members=dto.max_team_members,
        )
        track = self.repository.get_by_id(track.pk)
        return ProjectTrackReadDTO(track).to_dict()

    def _apply_team_member_limits_to_track(
        self,
        track_id: int,
        min_team_members: int | None,
        max_team_members: int | None,
    ) -> None:
        """Проставляет лимиты размера команды всем заявкам трека."""
        if min_team_members is None and max_team_members is None:
            return

        applications = self.repository.get_linked_applications(track_id)
        for application in applications:
            new_min = (
                min_team_members
                if min_team_members is not None
                else application.min_team_members
            )
            new_max = (
                max_team_members
                if max_team_members is not None
                else application.max_team_members
            )
            if new_min > new_max:
                raise ValueError(
                    "Минимальное количество человек не может быть "
                    f"больше максимального для заявки id={application.pk}"
                )
            application.min_team_members = new_min
            application.max_team_members = new_max

        self.repository.update_team_member_limits(applications)

    @transaction.atomic
    def update_track(
        self, user: User, track_id: int, dto: ProjectTrackUpdateDTO
    ) -> dict:
        """Обновляет основные поля трека и лимиты команд у заявок."""
        track = self._get_track_with_access(user, track_id)
        accessible_department_ids = self._get_accessible_department_ids(user)
        update_data = dto.to_update_dict()

        if not update_data and not dto.has_team_member_updates():
            raise ValueError("Не переданы поля для обновления")

        if "name" in update_data and not update_data["name"].strip():
            raise ValueError("Поле name не может быть пустым")
        if "name" in update_data:
            update_data["name"] = update_data["name"].strip()

        if "department_id" in update_data:
            if not Department.objects.filter(pk=update_data["department_id"]).exists():
                raise ValueError(
                    f"Подразделение с id={update_data['department_id']} не найдено"
                )
            ok, error = self.domain.validate_department_access(
                update_data["department_id"], accessible_department_ids
            )
            if not ok:
                raise PermissionError(error)

        if "semester_id" in update_data:
            if not Semester.objects.filter(pk=update_data["semester_id"]).exists():
                raise ValueError(f"Семестр с id={update_data['semester_id']} не найден")

        if dto.has_team_member_updates():
            new_min = (
                dto.min_team_members
                if dto.min_team_members is not None
                else track.min_team_members
            )
            new_max = (
                dto.max_team_members
                if dto.max_team_members is not None
                else track.max_team_members
            )
            if new_min > new_max:
                raise ValueError(
                    "Минимальное количество человек не может быть "
                    "больше максимального."
                )

        if update_data:
            self.repository.update(track, **update_data)

        self._apply_team_member_limits_to_track(
            track_id,
            dto.min_team_members,
            dto.max_team_members,
        )

        track = self.repository.get_by_id(track_id)
        return ProjectTrackReadDTO(track).to_dict()

    @transaction.atomic
    def delete_track(self, user: User, track_id: int) -> None:
        """Удаляет проектный трек."""
        track = self._get_track_with_access(user, track_id)
        self.repository.delete(track)

    @transaction.atomic
    def add_groups_to_track(
        self, user: User, track_id: int, dto: ProjectTrackAddGroupsDTO
    ) -> dict:
        """Добавляет группы в трек."""
        track = self._get_track_with_access(user, track_id)
        accessible_codes = self.domain.get_accessible_institute_codes(user)

        if not dto.group_ids:
            raise ValueError("Список group_ids не может быть пустым")

        groups = list(self.repository.get_groups_by_ids(dto.group_ids))
        found_ids = {group.pk for group in groups}
        missing = set(dto.group_ids) - found_ids
        if missing:
            raise ValueError(f"Учебные группы не найдены: {sorted(missing)}")

        for group in groups:
            ok, error = self.domain.validate_study_group_for_track(
                group, accessible_codes
            )
            if not ok:
                raise ValueError(error)

        existing_ids = self.repository.get_existing_group_ids(track.pk, dto.group_ids)
        new_group_ids = [gid for gid in dto.group_ids if gid not in existing_ids]

        self.repository.add_groups(track.pk, new_group_ids)
        track = self.repository.get_by_id(track_id)
        return ProjectTrackReadDTO(track).to_dict()

    @transaction.atomic
    def remove_group_from_track(self, user: User, track_id: int, group_id: int) -> dict:
        """Удаляет группу из трека."""
        track = self._get_track_with_access(user, track_id)

        if not self.repository.remove_group(track.pk, group_id):
            raise ValueError(f"Группа id={group_id} не привязана к треку id={track_id}")

        track = self.repository.get_by_id(track_id)
        return ProjectTrackReadDTO(track).to_dict()

    @transaction.atomic
    def add_applications_to_track(
        self, user: User, track_id: int, dto: ProjectTrackAddApplicationsDTO
    ) -> dict:
        """Добавляет заявки в трек."""
        track = self._get_track_with_access(user, track_id)
        accessible_codes = self.domain.get_accessible_institute_codes(user)

        if not dto.items:
            raise ValueError("Список заявок не может быть пустым")

        application_ids = dto.application_ids
        teams_by_id = dto.teams_count_by_application_id()
        min_members_by_id = dto.min_team_members_by_application_id()
        max_members_by_id = dto.max_team_members_by_application_id()

        applications = list(self.repository.get_applications_by_ids(application_ids))
        found_ids = {app.pk for app in applications}
        missing = set(application_ids) - found_ids
        if missing:
            raise ValueError(f"Проектные заявки не найдены: {sorted(missing)}")

        for application in applications:
            ok, error = self.domain.validate_application_for_track(
                application, track, accessible_codes
            )
            if not ok:
                raise ValueError(error)

        for application in applications:
            application.recommended_teams_count = teams_by_id[application.pk]
            application.min_team_members = min_members_by_id[application.pk]
            application.max_team_members = max_members_by_id[application.pk]
        self.repository.update_recommended_teams_counts(applications)

        existing_ids = self.repository.get_existing_application_ids(
            track.pk, application_ids
        )
        new_application_ids = [
            app_id for app_id in application_ids if app_id not in existing_ids
        ]
        self.repository.add_applications(track.pk, new_application_ids)
        self.repository.recalculate_recommended_teams_count(track.pk)

        track = self.repository.get_by_id(track_id)
        return ProjectTrackReadDTO(track).to_dict()

    @transaction.atomic
    def remove_application_from_track(
        self, user: User, track_id: int, application_id: int
    ) -> dict:
        """Удаляет заявку из трека."""
        track = self._get_track_with_access(user, track_id)

        if not self.repository.remove_application(track.pk, application_id):
            raise ValueError(
                f"Заявка id={application_id} не привязана к треку id={track_id}"
            )

        self.repository.recalculate_recommended_teams_count(track.pk)

        track = self.repository.get_by_id(track_id)
        return ProjectTrackReadDTO(track).to_dict()

    def list_groups(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> list[dict]:
        """Список групп института со счётчиком назначенных проектов."""
        semester_id, accessible_codes, resolved_institute_code = (
            self._resolve_institute_semester(user, institute_code, semester_id_raw)
        )

        groups = self.repository.list_groups_with_counts(
            institute_code=resolved_institute_code,
            semester_id=semester_id,
            accessible_institute_codes=accessible_codes,
        )
        return [ProjectTrackGroupListDTO(group).to_dict() for group in groups]

    def list_projects(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> list[dict]:
        """Список проектов семестра со счётчиком назначенных групп."""
        semester_id, accessible_codes, resolved_institute_code = (
            self._resolve_institute_semester(user, institute_code, semester_id_raw)
        )

        applications = self.repository.list_projects_with_counts(
            institute_code=resolved_institute_code,
            semester_id=semester_id,
            accessible_institute_codes=accessible_codes,
        )
        return [ProjectTrackProjectListDTO(app).to_dict() for app in applications]

    def get_group_detail(
        self,
        user: User,
        group_id: int,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> dict:
        """Детали группы с назначенными проектами."""
        self._check_manage_permission(user)
        self._ensure_user_department(user)

        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        accessible_codes = self.domain.get_accessible_institute_codes(user)

        group = self.repository.get_group_by_id(group_id)
        if group is None:
            raise ValueError(f"Учебная группа с id={group_id} не найдена")

        if institute_code is None:
            ok, error = self.domain.validate_group_institute_codes(
                {group.institute_id}, accessible_codes
            )
            if not ok:
                raise PermissionError(error)
            resolved_institute_code = group.institute_id
        else:
            resolved_institute_code = self.domain.resolve_institute_code(
                user, institute_code
            )
            if group.institute_id != resolved_institute_code:
                raise ValueError(
                    f"Учебная группа с id={group_id} не принадлежит институту "
                    f"{resolved_institute_code}"
                )

        applications = list(
            self.repository.get_group_assigned_applications(
                group_id=group_id,
                semester_id=semester_id,
                institute_code=resolved_institute_code,
            )
        )
        return ProjectTrackGroupDetailDTO(group, applications).to_dict()

    def get_project_detail(
        self,
        user: User,
        project_id: int,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> dict:
        """Детали проекта с назначенными группами."""
        semester_id, _, resolved_institute_code = self._resolve_institute_semester(
            user, institute_code, semester_id_raw
        )

        application = self.repository.get_application_by_id(
            project_id, institute_code=resolved_institute_code
        )
        if application is None:
            raise ValueError(f"Проектная заявка с id={project_id} не найдена")
        if application.status.code != "approved":
            raise ValueError(
                f"Заявка id={application.pk} не одобрена "
                f"(статус: {application.status.code})"
            )
        if application.semester_id != semester_id:
            raise ValueError(f"Заявка id={application.pk} относится к другому семестру")

        groups = list(
            self.repository.get_project_assigned_groups(
                project_id=project_id,
                semester_id=semester_id,
                institute_code=resolved_institute_code,
            )
        )
        return ProjectTrackProjectDetailDTO(application, groups).to_dict()

    def get_statistics(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> dict:
        """Статистика распределения проектов по группам."""
        self._check_manage_permission(user)

        if institute_code is None and self.domain.can_view_aggregated_statistics(user):
            semester_id = Semester.resolve_list_semester_id(semester_id_raw)
            overall = self.repository.get_statistics_overall(semester_id)
            by_institute = self.repository.list_statistics_by_institutes(semester_id)
            return ProjectTrackAggregatedStatisticsDTO(
                overall=overall,
                by_institute=by_institute,
            ).to_dict()

        semester_id, accessible_codes, resolved_institute_code = (
            self._resolve_institute_semester(user, institute_code, semester_id_raw)
        )

        stats = self.repository.get_statistics(
            institute_code=resolved_institute_code,
            semester_id=semester_id,
            accessible_institute_codes=accessible_codes,
        )
        return ProjectTrackStatisticsDTO(**stats).to_dict()

    @staticmethod
    def serialize_list(tracks: Iterable[ProjectTrack]) -> list[dict]:
        """Сериализует список треков с группами и заявками."""
        return [ProjectTrackReadDTO(track).to_dict() for track in tracks]
