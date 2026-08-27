"""Разрешения для приложения teams."""

from __future__ import annotations

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from accounts.models import User
from teams.models import Team, TeamSemester


def _is_staff_or_admin(user: User) -> bool:
    if user.is_staff:
        return True
    return bool(user.role and user.role.code in {"admin", "cpds"})


class StudentWithStudyGroupPermission(BasePermission):
    """Доступ только студенту с привязанной учебной группой."""

    message = "Доступно только студентам с учебной группой"

    def has_permission(self, request: Request, view: APIView) -> bool:
        user: User | None = request.user if request.user.is_authenticated else None
        if not user:
            return False
        return bool(user.role and user.role.code == "student" and user.study_group_id)


class TeamPermission(BasePermission):
    """Чтение — любой аутентифицированный пользователь.

    Изменение постоянной команды — admin/cpds/staff или капитан любого семестра.
    """

    message = "Недостаточно прав для управления командой"

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view: APIView, obj: Team) -> bool:
        if request.method in SAFE_METHODS:
            return True
        user: User = request.user
        if _is_staff_or_admin(user):
            return True
        return obj.semester_enrollments.filter(captain_id=user.id).exists()


class TeamSemesterPermission(BasePermission):
    """Изменение семестрового контекста — капитан, admin или cpds."""

    message = "Недостаточно прав для управления командой в семестре"

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated

    def has_object_permission(
        self, request: Request, view: APIView, obj: TeamSemester
    ) -> bool:
        if request.method in SAFE_METHODS:
            return True
        user: User = request.user
        if _is_staff_or_admin(user):
            return True
        return obj.captain_id == user.id
