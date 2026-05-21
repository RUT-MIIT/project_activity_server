"""Сервис для операций с учебными группами."""

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Department
from teams.domain.study_group import StudyGroupDomain
from teams.models import StudyGroup
from teams.repositories.study_group import StudyGroupRepository

if TYPE_CHECKING:
    from django.db.models import QuerySet

User = get_user_model()


class StudyGroupService:
    """Оркестрация Domain + Repository для StudyGroup."""

    def __init__(self):
        self.repository = StudyGroupRepository()
        self.domain = StudyGroupDomain()

    def list_study_groups(self, user: User) -> "QuerySet[StudyGroup]":
        if user.is_authenticated and user.department_id:
            try:
                department = Department.objects.select_related("parent").get(
                    pk=user.department_id
                )
                user.department = department
            except Department.DoesNotExist:
                pass

        queryset = self.repository.get_all()
        return self.domain.get_filtered_queryset(user, queryset)

    def get_study_group(self, group_id: int, user: User) -> StudyGroup:
        try:
            group = self.repository.get_by_id(group_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Учебная группа с ID {group_id} не найдена") from err

        filtered = self.list_study_groups(user)
        if not filtered.filter(pk=group_id).exists():
            raise ValueError("Нет доступа к этой учебной группе")

        return group
