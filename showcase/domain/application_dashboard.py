"""Доменная логика дашборда проектных заявок."""

from __future__ import annotations

from dataclasses import dataclass

from accounts.models import Department, User
from accounts.utils import get_department_subtree_ids
from teams.domain.institute_access import get_accessible_institute_codes

STATUS_GROUPS: dict[str, list[str]] = {
    "approved": ["approved", "approved_department", "approved_institute"],
    "rejected": [
        "rejected",
        "rejected_department",
        "rejected_institute",
        "rejected_cpds",
    ],
    "pending": [
        "await_department",
        "await_institute",
        "await_cpds",
        "require_assignment",
    ],
    "in_progress": [
        "created",
        "returned_department",
        "returned_institute",
        "returned_cpds",
        "returned_author",
    ],
}

ALL_STATUS_GROUPS: tuple[str, ...] = tuple(STATUS_GROUPS.keys())

FINAL_RESOLUTION_STATUS_CODES: frozenset[str] = frozenset({"approved", "rejected"})

GROUP_LABELS: dict[str, str] = {
    "approved": "Согласовано",
    "rejected": "Отклонено",
    "pending": "На согласовании",
    "in_progress": "В работе",
}

GROUP_COLORS: dict[str, str] = {
    "approved": "green",
    "rejected": "red",
    "pending": "purple",
    "in_progress": "orange",
}

RATING_CHART_SERIES: tuple[str, ...] = ("approved", "in_work", "rejected")

RATING_CHART_SERIES_LABELS: dict[str, str] = {
    "approved": GROUP_LABELS["approved"],
    "in_work": "В работе",
    "rejected": GROUP_LABELS["rejected"],
}

RATING_CHART_SERIES_COLORS: dict[str, str] = {
    "approved": GROUP_COLORS["approved"],
    "in_work": GROUP_COLORS["in_progress"],
    "rejected": GROUP_COLORS["rejected"],
}

VALID_APPLICATION_TYPES: frozenset[str] = frozenset({"all", "external", "internal"})


@dataclass(frozen=True)
class DashboardFilters:
    """Параметры фильтрации дашборда."""

    semester_id: int
    institute_code: str | None
    department_id: int | None
    status_groups: tuple[str, ...]
    application_type: str
    days: int
    accessible_institute_codes: list[str] | None


class ApplicationDashboardDomain:
    """Правила доступа и валидации для дашборда заявок."""

    VIEW_ROLES = frozenset({"admin", "cpds", "institute_validator"})

    @staticmethod
    def status_code_to_group(status_code: str | None) -> str | None:
        """Возвращает группу статуса по коду или None."""
        if not status_code:
            return None
        for group, codes in STATUS_GROUPS.items():
            if status_code in codes:
                return group
        return None

    @classmethod
    def expand_status_filter(cls, groups: tuple[str, ...]) -> frozenset[str]:
        """Разворачивает группы статусов в набор кодов."""
        codes: set[str] = set()
        for group in groups:
            if group not in STATUS_GROUPS:
                raise ValueError(f"Неизвестная группа статусов: {group}")
            codes.update(STATUS_GROUPS[group])
        return frozenset(codes)

    @classmethod
    def parse_status_groups(cls, raw: str | None) -> tuple[str, ...]:
        """Парсит query-параметр status в кортеж групп."""
        if not raw or not raw.strip():
            return ALL_STATUS_GROUPS
        groups = tuple(g.strip() for g in raw.split(",") if g.strip())
        unknown = [g for g in groups if g not in STATUS_GROUPS]
        if unknown:
            raise ValueError(f"Неизвестные группы статусов: {', '.join(unknown)}")
        return groups

    @classmethod
    def parse_application_type(cls, raw: str | None) -> str:
        """Парсит query-параметр application_type."""
        value = (raw or "all").strip().lower()
        if value not in VALID_APPLICATION_TYPES:
            raise ValueError(
                "application_type должен быть одним из: all, external, internal"
            )
        return value

    @staticmethod
    def parse_days(raw: str | None) -> int:
        """Парсит query-параметр days."""
        if raw is None or not str(raw).strip():
            return 30
        try:
            days = int(raw)
        except ValueError as err:
            raise ValueError("Параметр days должен быть целым числом") from err
        if days <= 0:
            raise ValueError("Параметр days должен быть положительным")
        if days > 366:
            raise ValueError("Параметр days не может превышать 366")
        return days

    @staticmethod
    def resolve_department_subtree_ids(department_id: int) -> set[int]:
        """Возвращает id подразделения и всех его потомков."""
        if not Department.objects.filter(pk=department_id).exists():
            raise ValueError(f"Подразделение с id={department_id} не найдено")
        return get_department_subtree_ids(department_id)

    @classmethod
    def can_view_dashboard(cls, user: User) -> tuple[bool, str]:
        """Проверяет право пользователя на просмотр дашборда."""
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"
        if user.is_staff:
            return True, ""
        role_code = user.role.code if user.role else None
        if role_code not in cls.VIEW_ROLES:
            return False, "Недостаточно прав для просмотра дашборда"
        return True, ""

    @classmethod
    def get_accessible_institute_codes(cls, user: User) -> list[str] | None:
        """Коды институтов пользователя; None — без ограничения."""
        return get_accessible_institute_codes(user)

    @classmethod
    def validate_institute_access(
        cls,
        user: User,
        institute_code: str | None,
    ) -> str | None:
        """Проверяет доступ к institute_code; возвращает код или None."""
        accessible = cls.get_accessible_institute_codes(user)
        if (
            institute_code
            and accessible is not None
            and institute_code not in accessible
        ):
            raise PermissionError(
                "Недостаточно прав для просмотра дашборда указанного института"
            )
        return institute_code
