"""Доменная логика API ответственного по институтам."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from django.utils import timezone

from accounts.models import Department, User
from showcase.domain.project_track import ProjectTrackDomain
from showcase.models import InstituteSemesterSettings
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

    @staticmethod
    def is_registration_opened_by_schedule(
        settings: InstituteSemesterSettings | None,
        *,
        now: datetime | None = None,
    ) -> bool:
        """True, если дата открытия записи наступила (без учёта closed_by_decision)."""
        if settings is None:
            return False
        if settings.registration_opens_at is None:
            return False
        current = now if now is not None else timezone.now()
        return current >= settings.registration_opens_at

    @staticmethod
    def is_registration_open(
        settings: InstituteSemesterSettings | None,
        *,
        now: datetime | None = None,
    ) -> bool:
        """True, если запись на проекты института открыта."""
        if settings is None:
            return False
        if settings.closed_by_decision:
            return False
        return InstituteResponsibleDomain.is_registration_opened_by_schedule(
            settings, now=now
        )

    @staticmethod
    def registration_status(
        settings: InstituteSemesterSettings | None,
        *,
        now: datetime | None = None,
    ) -> str:
        """Строковый статус регистрации: open / closed."""
        if InstituteResponsibleDomain.is_registration_open(settings, now=now):
            return "open"
        return "closed"

    @staticmethod
    def validate_settings_update_payload(
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Проверяет частичный update настроек; возвращает поля для записи.

        Raises:
            ValueError: пустое тело или некорректные типы.
        """
        if not payload:
            raise ValueError("Не передано ни одного параметра для изменения")

        allowed = {"registrationOpensAt", "closedByDecision"}
        unknown = set(payload.keys()) - allowed
        if unknown:
            raise ValueError("Неизвестные поля: " + ", ".join(sorted(unknown)))

        fields: dict[str, Any] = {}
        if "registrationOpensAt" in payload:
            value = payload["registrationOpensAt"]
            if value is not None and not isinstance(value, datetime):
                raise ValueError(
                    "registrationOpensAt должен быть датой/временем или null"
                )
            fields["registration_opens_at"] = value
        if "closedByDecision" in payload:
            value = payload["closedByDecision"]
            if not isinstance(value, bool):
                raise ValueError("closedByDecision должен быть boolean")
            fields["closed_by_decision"] = value

        if not fields:
            raise ValueError("Не передано ни одного параметра для изменения")
        return fields
