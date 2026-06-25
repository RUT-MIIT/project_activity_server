"""Сервис управления пользователями."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from accounts.domain.user_management import UserManagementDomain
from accounts.models import Department, Role
from accounts.repositories.user import UserRepository

if TYPE_CHECKING:
    from django.db.models import QuerySet

User = get_user_model()


class UserManagementService:
    """Оркестрация Domain + Repository для управления пользователями."""

    def __init__(self):
        self.repository = UserRepository()
        self.domain = UserManagementDomain()

    def _ensure_user_department(self, user: User) -> None:
        """Подгружает parent подразделения для корректного resolve институтов."""
        if not user.department_id:
            return
        try:
            department = Department.objects.select_related("parent").get(
                pk=user.department_id
            )
            user.department = department
        except Department.DoesNotExist:
            pass

    def list_users(
        self,
        actor: User,
        *,
        include_authored_projects: bool = False,
    ) -> QuerySet[User]:
        """Список пользователей с учётом роли запрашивающего."""
        can_list, error = self.domain.can_list_users(actor)
        if not can_list:
            raise PermissionError(error)

        self._ensure_user_department(actor)
        department_ids = self.domain.get_department_ids_filter(actor)
        return self.repository.filter_users_queryset(
            department_ids,
            include_authored_projects=include_authored_projects,
        )

    def get_user(
        self,
        actor: User,
        user_id: int,
        *,
        include_authored_projects: bool = False,
    ) -> User:
        """Возвращает пользователя, если он доступен запрашивающему."""
        queryset = self.list_users(
            actor, include_authored_projects=include_authored_projects
        )
        if not self.domain.user_in_accessible_queryset(queryset, user_id):
            raise PermissionError("Нет доступа к этому пользователю")

        return queryset.get(pk=user_id)

    def update_user(
        self,
        actor: User,
        user_id: int,
        *,
        role_code: str | None = None,
        department_id: int | None = None,
        email: str | None = None,
        phone: str | None = None,
        fields_set: set[str],
    ) -> User:
        """Частичное обновление пользователя."""
        can_update, error = self.domain.can_update_users(actor)
        if not can_update:
            raise PermissionError(error)

        queryset = self.list_users(actor)
        if not self.domain.user_in_accessible_queryset(queryset, user_id):
            raise PermissionError("Нет доступа к этому пользователю")

        try:
            target = self.repository.get_by_id(user_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Пользователь с ID {user_id} не найден") from err

        role: Role | None = None
        department: Department | None = None
        update_fields: list[str] = []

        if "role" in fields_set:
            if role_code is None:
                raise ValueError("Поле role не может быть пустым")
            try:
                role = Role.objects.get(code=role_code, is_active=True)
            except Role.DoesNotExist as err:
                raise ValueError(f"Роль '{role_code}' не найдена") from err
            update_fields.append("role")

        if "department_id" in fields_set:
            if department_id is None:
                department = None
            else:
                try:
                    department = Department.objects.get(pk=department_id)
                except Department.DoesNotExist as err:
                    raise ValueError(
                        f"Подразделение с ID {department_id} не найдено"
                    ) from err
            update_fields.append("department")

        if "email" in fields_set:
            if email is None:
                raise ValueError("Поле email не может быть пустым")
            update_fields.append("email")

        if "phone" in fields_set:
            update_fields.append("phone")

        if not update_fields:
            return target

        ok, validation_error = self.domain.validate_update(
            target, role, department, fields_set
        )
        if not ok:
            raise ValueError(validation_error)

        return self.repository.update_user(
            target,
            role=role if "role" in fields_set else None,
            department=department if "department_id" in fields_set else None,
            email=email if "email" in fields_set else None,
            phone=phone if "phone" in fields_set else None,
            update_fields=update_fields,
        )
