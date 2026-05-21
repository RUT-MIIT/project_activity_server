"""Разрешения для приложения teams."""

from __future__ import annotations

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from accounts.models import User
from teams.models import Team


class TeamPermission(BasePermission):
    """Чтение — любой аутентифицированный пользователь.

    Изменение — руководитель команды, admin или cpds.
    """

    message = "Недостаточно прав для управления командой"

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view: APIView, obj: Team) -> bool:
        if request.method in SAFE_METHODS:
            return True

        user: User = request.user
        if user.is_staff:
            return True
        if user.role and user.role.code in {"admin", "cpds"}:
            return True
        return obj.leader_id == user.id
