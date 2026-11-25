"""Доменная логика управления пользователями."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accounts.models import Department, Role, User
from accounts.utils import get_department_subtree_ids
from showcase.models import Institute
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
INSTITUTE_PROTECTED_ROLES = frozenset({"admin", "cpds", "institute_validator"})


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
    def can_update_users(
        user: User, *, allow_institute: bool = False
    ) -> tuple[bool, str]:
        """Проверяет, может ли пользователь изменять пользователей."""
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        if user.is_staff:
            return True, ""

        role_code = get_role_code(user)
        if role_code in WRITE_ROLES or (
            allow_institute and role_code == "institute_validator"
        ):
            return True, ""

        return False, "Недостаточно прав для изменения пользователей"

    @staticmethod
    def validate_institute_update(
        actor: User,
        target: User,
        role: Role | None,
        department: Department | None,
        fields_set: set[str],
    ) -> None:
        """Проверяет ограничения записи ответственного института."""
        if fields_set - {"role", "department_id"}:
            raise PermissionError("Недостаточно прав для изменения этих полей")
        if target.is_staff or get_role_code(target) in INSTITUTE_PROTECTED_ROLES:
            raise PermissionError("Нельзя изменять привилегированного пользователя")
        if role is not None and role.code in INSTITUTE_PROTECTED_ROLES:
            raise PermissionError("Нельзя назначить привилегированную роль")

        destination_id = (
            (department.pk if department else None)
            if "department_id" in fields_set
            else target.department_id
        )
        if not target.department_id or not destination_id:
            raise PermissionError("Подразделение пользователя недоступно")

        codes = get_user_institute_codes(actor)
        institutes = Institute.objects.filter(
            code__in=codes, is_active=True, department__isnull=False
        )
        for institute in institutes:
            department_ids = get_department_subtree_ids(institute.department_id)
            if (
                target.department_id in department_ids
                and destination_id in department_ids
            ):
                return
        raise PermissionError("Подразделение пользователя недоступно")

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
            department if "department_id" in update_fields else target.department
        )

        if effective_role and effective_role.requires_department:
            if effective_department is None:
                return False, "Для выбранной роли необходимо указать подразделение"

        return True, ""

    @staticmethod
    def user_in_accessible_queryset(queryset: QuerySet[User], user_id: int) -> bool:
        """Проверяет, что пользователь доступен в отфильтрованном queryset."""
        return queryset.filter(pk=user_id).exists()
