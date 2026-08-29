"""Доменная логика API ответственного по институтам."""

from __future__ import annotations

from accounts.models import Department, User
from showcase.domain.project_track import ProjectTrackDomain
from teams.domain.institute_access import (
    MANAGEMENT_ROLES,
    get_department_ids_for_institute_codes,
    get_role_code,
)
from teams.models import StudyGroup


class InstituteResponsibleDomain:
    """Правила доступа и валидации для ответственного по институтам."""

    @staticmethod
    def can_access(user: User) -> tuple[bool, str]:
        """Проверяет, может ли пользователь работать с API ответственного."""
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        if user.is_staff:
            return True, ""

        role_code = get_role_code(user)
        if role_code in MANAGEMENT_ROLES:
            return True, ""

        return False, "Недостаточно прав для управления наставниками институтов"

    @classmethod
    def resolve_institute_code(cls, user: User, institute_code: str | None) -> str:
        """Определяет код института из параметра или по умолчанию."""
        return ProjectTrackDomain.resolve_institute_code(user, institute_code)

    @classmethod
    def get_department_ids_for_user(cls, user: User, institute_code: str) -> set[int]:
        """ID подразделений института для фильтрации сотрудников."""
        return get_department_ids_for_institute_codes([institute_code])

    @classmethod
    def validate_group_access(
        cls,
        group: StudyGroup,
        institute_code: str,
        accessible_codes: list[str] | None,
    ) -> tuple[bool, str]:
        """Проверяет доступ к учебной группе."""
        if group.is_end:
            return False, "Учебная группа завершила обучение"

        if group.institute_id != institute_code:
            return False, "Учебная группа не принадлежит указанному институту"

        ok, error = ProjectTrackDomain.validate_group_institute_codes(
            {group.institute_id}, accessible_codes
        )
        if not ok:
            return False, error

        return True, ""

    @staticmethod
    def ensure_user_department(user: User) -> None:
        """Подгружает parent подразделения для resolve институтов."""
        if not user.department_id:
            return
        try:
            department = Department.objects.select_related("parent").get(
                pk=user.department_id
            )
            user.department = department
        except Department.DoesNotExist:
            pass
