"""Сервис для операций со списком проектов."""

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

from accounts.models import Department, Semester
from showcase.domain.project import ProjectDomain
from showcase.repositories.project import ProjectRepository

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from showcase.models import ProjectApplication

User = get_user_model()


class ProjectService:
    """Оркестрация Domain + Repository для списка проектов."""

    def __init__(self):
        self.repository = ProjectRepository()
        self.domain = ProjectDomain()

    def _ensure_user_department(self, user: User) -> None:
        """Подгружает parent подразделения пользователя."""
        if not user.department_id:
            return
        try:
            department = Department.objects.select_related("parent").get(
                pk=user.department_id
            )
            user.department = department
        except Department.DoesNotExist:
            pass

    def list_projects(
        self, user: User, semester_id_raw: str | None = None
    ) -> "QuerySet[ProjectApplication]":
        """Список проектов с учётом роли пользователя."""
        can_list, error = self.domain.can_list_projects(user)
        if not can_list:
            raise PermissionError(error)

        self._ensure_user_department(user)

        semester_id: int | None = None
        if semester_id_raw is not None:
            semester_id = Semester.resolve_list_semester_id(semester_id_raw)

        institute_codes = self.domain.get_institute_codes_for_user(user)
        return self.repository.filter_projects_queryset(
            institute_codes=institute_codes,
            semester_id=semester_id,
        )
