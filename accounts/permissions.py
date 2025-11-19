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
