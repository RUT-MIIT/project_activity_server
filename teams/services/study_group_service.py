"""Сервис для операций с учебными группами."""

from typing import TYPE_CHECKING, Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Department, Semester
from teams.domain.study_group import StudyGroupDomain
from teams.dto.my_study_group import MyStudyGroupDTO
from teams.models import StudyGroup
from teams.repositories.institute_responsible import InstituteResponsibleRepository
from teams.repositories.study_group import StudyGroupRepository
from teams.repositories.team_lobby import TeamLobbyRepository

if TYPE_CHECKING:
    from django.db.models import QuerySet

User = get_user_model()


class StudyGroupService:
    """Оркестрация Domain + Repository для StudyGroup."""

    def __init__(self):
        self.repository = StudyGroupRepository()
        self.domain = StudyGroupDomain()
        self.team_lobby_repository = TeamLobbyRepository()
        self.institute_repository = InstituteResponsibleRepository()

    def list_study_groups(
        self, user: User, is_end: bool | None = None
    ) -> "QuerySet[StudyGroup]":
        if user.is_authenticated and user.department_id:
            try:
                department = Department.objects.select_related("parent").get(
                    pk=user.department_id
                )
                user.department = department
            except Department.DoesNotExist:
                pass

        queryset = self.repository.get_all()
        queryset = self.domain.get_filtered_queryset(user, queryset)
        if is_end is not None:
            queryset = queryset.filter(is_end=is_end)
        return queryset

    def get_study_group(self, group_id: int, user: User) -> StudyGroup:
        try:
            group = self.repository.get_by_id(group_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Учебная группа с ID {group_id} не найдена") from err

        filtered = self.list_study_groups(user)
        if not filtered.filter(pk=group_id).exists():
            raise ValueError("Нет доступа к этой учебной группе")

        return group

    def get_my_study_group(
        self, user: User, semester_id_raw: str | None = None
    ) -> dict[str, Any]:
        """Возвращает данные учебной группы текущего студента."""
        if not self.domain.is_student(user):
            raise PermissionError("Доступ только для студентов")
        if not user.study_group_id:
            raise LookupError("Учебная группа не назначена")

        semester_id: int | None = None
        if semester_id_raw is not None:
            semester_id = Semester.resolve_list_semester_id(semester_id_raw)

        group = self.repository.get_my_group_detail(
            user.study_group_id, semester_id=semester_id
        )
        members = self.repository.list_group_contingent(
            user.study_group_id, semester_id=semester_id
        )

        my_team = None
        registration_settings = None
        include_semester_context = semester_id is not None
        if include_semester_context and semester_id is not None:
            my_team = self.team_lobby_repository.get_user_team_semester_snapshot(
                user_id=user.id,
                semester_id=semester_id,
            )
            institute_code = (
                getattr(group.institute, "code", None) or group.institute_id
            )
            registration_settings = self.institute_repository.get_settings(
                institute_code=institute_code,
                semester_id=semester_id,
            )

        return MyStudyGroupDTO(
            group,
            members,
            include_team=semester_id is not None,
            semester_id=semester_id,
            viewer_id=user.id,
            my_team=my_team,
            registration_settings=registration_settings,
            include_semester_context=include_semester_context,
        ).to_dict()
