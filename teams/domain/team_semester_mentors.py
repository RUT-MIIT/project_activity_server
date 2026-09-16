"""Доменные правила синхронизации наставников команды в семестре."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from accounts.models import User
    from teams.models import TeamSemester


class TeamSemesterMentorsDomain:
    """Синхронизация M2M mentors и основного FK mentor."""

    @staticmethod
    def resolve_primary_mentor(mentors: list[User]) -> User | None:
        """Основной наставник — с минимальным id (стабильный порядок)."""
        if not mentors:
            return None
        return min(mentors, key=lambda user: user.id)

    @staticmethod
    def ensure_mentor_roles(mentors: list[User]) -> None:
        """Все пользователи должны иметь роль mentor."""
        for user in mentors:
            role_code = user.role.code if user.role else None
            if role_code != "mentor":
                raise ValueError(
                    f"Пользователь {user.get_full_name() or user.email} "
                    "не является наставником"
                )


def sync_team_semester_primary_mentor(team_semester: TeamSemester) -> None:
    """Выставляет FK mentor по первому из M2M mentors (без лишних save)."""
    primary = team_semester.mentors.order_by("id").only("id").first()
    primary_id = primary.id if primary is not None else None
    if team_semester.mentor_id != primary_id:
        type(team_semester).objects.filter(pk=team_semester.pk).update(
            mentor_id=primary_id
        )
        team_semester.mentor_id = primary_id
