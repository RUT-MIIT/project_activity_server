"""Пользовательские permissions для приложения accounts."""

from __future__ import annotations

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from accounts.models import User


class RegistrationRequestManagePermission(BasePermission):
    """Разрешает доступ только сотрудникам, администраторам или роли ЦПДС."""

    message = "Недостаточно прав для управления заявками на регистрацию"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Проверяет наличие прав у пользователя.

        Args:
            request: текущий запрос
            view: представление, совершающее проверку

        Returns:
            bool: True, если пользователь имеет доступ.
        """
        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False

        if user.is_staff:
            return True

        if user.role and user.role.code in {"admin", "cpds"}:
            return True

        return False


class IsCpdsUser(BasePermission):
    """Разрешает доступ только пользователям с ролью ЦПДС (код роли `cpds`)."""

    message = "Недостаточно прав: требуется роль ЦПДС"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Проверяет, что у текущего пользователя установлена роль с кодом `cpds`.

        Args:
            request: текущий HTTP‑запрос.
            view: DRF‑представление, выполняющее проверку.

        Returns:
            bool: True, если пользователь аутентифицирован и его роль имеет код `cpds`.
        """
        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False

        return bool(user.role and user.role.code == "cpds")


class IsInstituteValidator(BasePermission):
    """Разрешает доступ только пользователям с ролью institute_validator."""

    message = "Недостаточно прав: требуется роль institute_validator"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Проверяет, что у пользователя роль institute_validator."""
        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False

        return bool(user.role and user.role.code == "institute_validator")


class IsAdminOrCpds(BasePermission):
    """Разрешает доступ только администраторам или пользователям с ролью `cpds`."""

    message = "Недостаточно прав: требуется роль admin или cpds"

    def has_permission(self, request: Request, view: APIView) -> bool:
        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False

        if user.is_staff:
            return True

        return bool(user.role and user.role.code in {"admin", "cpds"})


class DenyStudentPermission(BasePermission):
    """Запрещает доступ пользователям с ролью student."""

    message = "Недостаточно прав: роль student не имеет доступа"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Возвращает False для роли student."""
        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False
        return not bool(user.role and user.role.code == "student")


class ProjectTrackPermission(BasePermission):
    """Разрешает доступ к проектным трекам для admin, cpds и institute_validator."""

    message = "Недостаточно прав для управления проектными треками"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Проверяет наличие прав у пользователя."""
        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False

        if user.is_staff:
            return True

        return bool(
            user.role and user.role.code in {"cpds", "admin", "institute_validator"}
        )


class TagManagePermission(BasePermission):
    """Разрешает доступ к управлению тегами только для ролей cpds, admin и institute_validator."""

    message = "Недостаточно прав для управления тегами"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Проверяет наличие прав у пользователя."""
        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False

        if user.is_staff:
            return True

        return bool(
            user.role and user.role.code in {"cpds", "admin", "institute_validator"}
        )


class ProjectManagementPermission(BasePermission):
    """Разрешает просмотр проектов для admin, cpds и institute_validator."""

    message = "Недостаточно прав для просмотра проектов"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Проверяет наличие прав у пользователя."""
        from showcase.domain.project import ProjectDomain

        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False

        return ProjectDomain.can_list_projects(user)[0]


class UserManagementPermission(BasePermission):
    """Просмотр пользователей — admin/cpds/institute_validator; запись — admin/cpds."""

    message = "Недостаточно прав для управления пользователями"

    LIST_ACTIONS = frozenset({"list", "retrieve"})
    WRITE_ACTIONS = frozenset({"partial_update", "update", "create", "destroy"})

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Проверяет права на чтение или запись пользователей."""
        from accounts.domain.user_management import UserManagementDomain

        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False

        action = getattr(view, "action", None)
        if action in self.LIST_ACTIONS:
            return UserManagementDomain.can_list_users(user)[0]
        if action in self.WRITE_ACTIONS:
            return UserManagementDomain.can_update_users(user)[0]
        return False
