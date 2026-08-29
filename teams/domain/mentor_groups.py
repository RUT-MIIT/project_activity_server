"""Доменная логика доступа наставника к учебной группе."""

from __future__ import annotations

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
    def ensure_mentor_access(is_mentor: bool) -> None:
        """Проверяет, что пользователь назначен наставником группы в семестре."""
        if not is_mentor:
            raise PermissionError("Нет доступа к этой учебной группе")
