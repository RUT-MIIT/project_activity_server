"""Доменная логика управления пользователями."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accounts.models import Department, Role, User
from teams.domain.institute_access import (
    get_department_ids_for_institute_codes,
    get_role_code,
    get_user_institute_codes,
)

if TYPE_CHECKING:
    from django.db.models import QuerySet

LIST_ROLES = frozenset({"admin", "cpds", "institute_validator"})
WRITE_ROLES = frozenset({"admin", "cpds"})
ADMIN_ROLE_CODE = "admin"


class UserManagementDomain:
    """Правила доступа и валидации для управления пользователями."""

    @staticmethod
    def can_list_users(user: User) -> tuple[bool, str]:
        """Проверяет, может ли пользователь просматривать список пользователей."""
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        if user.is_staff:
            return True, ""

        role_code = get_role_code(user)
        if role_code in LIST_ROLES:
            return True, ""

        return False, "Недостаточно прав для просмотра пользователей"

    @staticmethod
    def can_update_users(user: User) -> tuple[bool, str]:
        """Проверяет, может ли пользователь изменять пользователей."""
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        if user.is_staff:
            return True, ""

        role_code = get_role_code(user)
        if role_code in WRITE_ROLES:
            return True, ""

        return False, "Недостаточно прав для изменения пользователей"

    @staticmethod
    def get_department_ids_filter(user: User) -> set[int] | None:
        """ID подразделений для фильтрации; None — без ограничения."""
        if user.is_staff:
            return None

        role_code = get_role_code(user)
        if role_code in {"admin", "cpds"}:
            return None

        if role_code == "institute_validator":
            institute_codes = get_user_institute_codes(user)
            if not institute_codes:
                return set()
            return get_department_ids_for_institute_codes(institute_codes)

        return set()

    @staticmethod
    def is_protected_user(target: User) -> bool:
        """Проверяет, что пользователь защищён от изменений (админ/staff)."""
        if target.is_staff:
            return True
        return bool(target.role and target.role.code == ADMIN_ROLE_CODE)

    @classmethod
    def validate_update(
        cls,
        target: User,
        role: Role | None,
        department: Department | None,
        update_fields: set[str],
    ) -> tuple[bool, str]:
        """Валидирует частичное обновление пользователя."""
        if cls.is_protected_user(target):
            return False, "Нельзя изменять пользователя с ролью администратора"

        if role is not None and role.code == ADMIN_ROLE_CODE:
            return False, "Нельзя назначить роль администратора"

        effective_role = role if "role" in update_fields else target.role
        effective_department = (
            department if "department" in update_fields else target.department
        )

        if effective_role and effective_role.requires_department:
            if effective_department is None:
                return False, "Для выбранной роли необходимо указать подразделение"

        return True, ""

    @staticmethod
    def user_in_accessible_queryset(queryset: QuerySet[User], user_id: int) -> bool:
        """Проверяет, что пользователь доступен в отфильтрованном queryset."""
        return queryset.filter(pk=user_id).exists()
