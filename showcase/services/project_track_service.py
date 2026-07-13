"""Сервис для операций с проектными треками."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from accounts.models import Department, Semester
from showcase.domain.project_track import ProjectTrackDomain
from showcase.dto.project_track import (
    ProjectTrackAggregatedStatisticsDTO,
    ProjectTrackAssignDTO,
    ProjectTrackAssignResultDTO,
    ProjectTrackDeleteDTO,
    ProjectTrackGroupDetailDTO,
    ProjectTrackGroupListDTO,
    ProjectTrackProjectDetailDTO,
    ProjectTrackProjectListDTO,
    ProjectTrackReadDTO,
    ProjectTrackStatisticsDTO,
)
from showcase.models import Institute, ProjectTrack
from showcase.repositories.project_track import ProjectTrackRepository

if TYPE_CHECKING:
    from accounts.models import User

User = get_user_model()


class ProjectTrackService:
    """Оркестрация Domain + Repository для проектных треков."""

    def __init__(self) -> None:
        self.repository = ProjectTrackRepository()
        self.domain = ProjectTrackDomain()

    def _ensure_user_department(self, user: User) -> None:
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

    def _resolve_institute_semester(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
        *,
        institute_code_required: bool = True,
    ) -> tuple[int, list[str] | None, str]:
        """Валидирует доступ и возвращает semester_id, коды институтов и institute_code."""
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

    def list_tracks(
        self,
        user: User,
        institute_code: str,
        semester_id_raw: str,
    ) -> QuerySet[ProjectTrack]:
        """Список треков по институту и семестру."""
        semester_id, accessible_codes, resolved_institute_code = (
            self._resolve_institute_semester(
                user, institute_code, semester_id_raw, institute_code_required=False
            )
        )

        return self.repository.list_by_institute_and_semester(
            institute_code=resolved_institute_code,
            semester_id=semester_id,
            accessible_institute_codes=accessible_codes,
        )

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
                f"Заявка id={application.pk} не одобрена (статус: {application.status.code})"
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

    def _validate_assign_input(self, dto: ProjectTrackAssignDTO) -> None:
        """Валидирует входные данные для массового назначения."""
        if not dto.group_ids:
            raise ValueError("Список group_ids не может быть пустым")
        if not dto.project_application_ids:
            raise ValueError("Список project_application_ids не может быть пустым")

        if not Semester.objects.filter(pk=dto.semester_id).exists():
            raise ValueError(f"Семестр с id={dto.semester_id} не найден")

    def _validate_groups(
        self,
        group_ids: list[int],
        accessible_codes: list[str] | None,
    ) -> None:
        """Проверяет существование и доступность групп."""
        groups = list(self.repository.get_groups_by_ids(group_ids))
        found_ids = {group.pk for group in groups}
        missing = set(group_ids) - found_ids
        if missing:
            raise ValueError(f"Учебные группы не найдены: {sorted(missing)}")

        group_institute_codes = {group.institute_id for group in groups}
        ok, error = self.domain.validate_group_institute_codes(
            group_institute_codes, accessible_codes
        )
        if not ok:
            raise PermissionError(error)

    def _validate_applications(
        self,
        application_ids: list[int],
        semester_id: int,
        accessible_codes: list[str] | None,
    ) -> None:
        """Проверяет существование и доступность заявок."""
        applications = list(self.repository.get_applications_by_ids(application_ids))
        found_ids = {app.pk for app in applications}
        missing = set(application_ids) - found_ids
        if missing:
            raise ValueError(f"Проектные заявки не найдены: {sorted(missing)}")

        for app in applications:
            if app.status.code != "approved":
                raise ValueError(
                    f"Заявка id={app.pk} не одобрена (статус: {app.status.code})"
                )
            if app.semester_id != semester_id:
                raise ValueError(f"Заявка id={app.pk} относится к другому семестру")

            ok, error = self.domain.validate_application_access(app, accessible_codes)
            if not ok:
                raise PermissionError(error)

    @transaction.atomic
    def bulk_assign(
        self, user: User, dto: ProjectTrackAssignDTO
    ) -> ProjectTrackAssignResultDTO:
        """Массовое назначение групп на проекты."""
        self._check_manage_permission(user)
        self._ensure_user_department(user)
        self._validate_assign_input(dto)

        accessible_codes = self.domain.get_accessible_institute_codes(user)
        self._validate_groups(dto.group_ids, accessible_codes)
        self._validate_applications(
            dto.project_application_ids,
            dto.semester_id,
            accessible_codes,
        )

        total_requested = len(dto.group_ids) * len(dto.project_application_ids)
        existing_pairs = self.repository.get_existing_pairs(
            dto.semester_id,
            dto.group_ids,
            dto.project_application_ids,
        )
        skipped = len(existing_pairs)
        self.repository.bulk_create_tracks(
            dto.semester_id,
            dto.group_ids,
            dto.project_application_ids,
        )
        created = total_requested - skipped

        return ProjectTrackAssignResultDTO(
            created=created,
            skipped=skipped,
            total_requested=total_requested,
        )

    @transaction.atomic
    def delete_track(self, user: User, dto: ProjectTrackDeleteDTO) -> None:
        """Удаляет проектный трек по семестру, группе и заявке."""
        self._check_manage_permission(user)
        self._ensure_user_department(user)

        semester_id = Semester.resolve_list_semester_id(dto.semester_id)
        track = self.repository.get_by_keys(
            semester_id,
            dto.group_id,
            dto.project_application_id,
        )
        if track is None:
            raise ValueError(
                "Проектный трек для указанных semester_id, group_id "
                "и project_application_id не найден"
            )

        accessible_codes = self.domain.get_accessible_institute_codes(user)
        can_access, error = self.domain.can_access_track(user, track, accessible_codes)
        if not can_access:
            raise PermissionError(error)

        self.repository.delete(track)

    @staticmethod
    def serialize_list(tracks: QuerySet[ProjectTrack]) -> list[dict]:
        """Сериализует список треков."""
        return [ProjectTrackReadDTO(track).to_dict() for track in tracks]
