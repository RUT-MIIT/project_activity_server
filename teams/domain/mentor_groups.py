"""Доменная логика доступа наставника к учебной группе."""

from __future__ import annotations

from accounts.models import User
from teams.domain.institute_access import get_role_code, get_user_institute_codes
from teams.models import StudyGroup


class MentorGroupsDomain:
    """Проверки для API «Мои группы» наставника."""

    @staticmethod
    def ensure_group_exists(group: StudyGroup | None) -> None:
        """Проверяет, что учебная группа существует."""
        if group is None:
            raise LookupError("Учебная группа не найдена")

    @staticmethod
    def ensure_group_active(group: StudyGroup) -> None:
        """Проверяет, что учебная группа не завершила обучение."""
        if group.is_end:
            raise PermissionError("Учебная группа завершила обучение")

    @staticmethod
    def is_institute_validator(user: User) -> bool:
        """Возвращает True, если пользователь — ответственный по институту."""
        return get_role_code(user) == "institute_validator"

    @staticmethod
    def get_institute_codes(user: User) -> list[str]:
        """Коды институтов ответственного по институту."""
        return get_user_institute_codes(user)

    @staticmethod
    def has_group_access(user: User, group: StudyGroup, is_mentor: bool) -> bool:
        """Проверяет доступ к группе: наставник или ответственный по институту."""
        if is_mentor:
            return True
        if not MentorGroupsDomain.is_institute_validator(user):
            return False
        return group.institute_id in MentorGroupsDomain.get_institute_codes(user)

    @staticmethod
    def ensure_group_access(user: User, group: StudyGroup, is_mentor: bool) -> None:
        """Проверяет доступ к группе для списка и деталей."""
        if not MentorGroupsDomain.has_group_access(user, group, is_mentor):
            raise PermissionError("Нет доступа к этой учебной группе")
