"""Доменная логика для проектных треков."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accounts.models import User
from teams.domain.institute_access import (
    application_available_for_institute,
    get_accessible_institute_codes,
    get_role_code,
)

if TYPE_CHECKING:
    from showcase.models import ProjectApplication, ProjectTrack


class ProjectTrackDomain:
    """Правила доступа и валидации для проектных треков."""

    MANAGE_ROLES = {"admin", "cpds", "institute_validator"}

    @staticmethod
    def get_role_code(user: User) -> str | None:
        """Код роли пользователя."""
        return get_role_code(user)

    @classmethod
    def can_manage_tracks(cls, user: User) -> tuple[bool, str]:
        """Проверяет, может ли пользователь управлять проектными треками."""
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        if user.is_staff:
            return True, ""

        role_code = cls.get_role_code(user)
        if role_code not in cls.MANAGE_ROLES:
            return False, "Недостаточно прав для управления проектными треками"

        return True, ""

    @classmethod
    def get_accessible_institute_codes(cls, user: User) -> list[str] | None:
        """Коды институтов пользователя; None — без ограничения (admin/cpds)."""
        return get_accessible_institute_codes(user)

    @classmethod
    def can_view_aggregated_statistics(cls, user: User) -> bool:
        """True для admin/cpds/staff — статистика без institute_code."""
        if not user or not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        role_code = cls.get_role_code(user)
        return role_code in {"admin", "cpds"}

    @classmethod
    def resolve_institute_code(cls, user: User, institute_code: str | None) -> str:
        """Определяет код института: из параметра или по умолчанию для validator."""
        accessible_codes = cls.get_accessible_institute_codes(user)

        if institute_code:
            if accessible_codes is not None and institute_code not in accessible_codes:
                raise PermissionError(
                    "Недостаточно прав для просмотра треков указанного института"
                )
            return institute_code

        if accessible_codes is None:
            raise ValueError("Параметр institute_code обязателен")

        if not accessible_codes:
            raise PermissionError("У пользователя нет доступных институтов")

        if len(accessible_codes) > 1:
            raise ValueError(
                "Параметр institute_code обязателен при доступе к нескольким институтам"
            )

        return accessible_codes[0]

    @classmethod
    def validate_group_institute_codes(
        cls,
        group_institute_codes: set[str],
        accessible_codes: list[str] | None,
    ) -> tuple[bool, str]:
        """Проверяет, что все группы доступны пользователю."""
        if accessible_codes is None:
            return True, ""

        if not accessible_codes:
            return False, "У пользователя нет доступных институтов"

        inaccessible = group_institute_codes - set(accessible_codes)
        if inaccessible:
            return False, "Недостаточно прав для работы с указанными учебными группами"

        return True, ""

    @classmethod
    def validate_application_access(
        cls,
        application: ProjectApplication,
        accessible_codes: list[str] | None,
    ) -> tuple[bool, str]:
        """Проверяет, что заявка доступна пользователю по институтам."""
        if accessible_codes is None:
            return True, ""

        if not accessible_codes:
            return False, "У пользователя нет доступных институтов"

        if not application_available_for_institute(application, accessible_codes):
            return False, "Недостаточно прав для работы с указанными проектами"

        return True, ""

    @classmethod
    def can_access_track(
        cls,
        user: User,
        track: ProjectTrack,
        accessible_codes: list[str] | None,
    ) -> tuple[bool, str]:
        """Проверяет доступ к конкретному треку."""
        if accessible_codes is None:
            return True, ""

        group_institute = track.study_group.institute_id
        if group_institute not in accessible_codes:
            return False, "Недостаточно прав для работы с этим треком"

        ok, error = cls.validate_application_access(
            track.project_application, accessible_codes
        )
        if not ok:
            return False, error

        return True, ""
