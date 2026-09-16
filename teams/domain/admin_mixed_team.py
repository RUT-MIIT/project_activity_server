"""Доменные правила ручной сборки смешанной команды в admin."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from showcase.constants import DEFAULT_MAX_TEAM_MEMBERS, DEFAULT_MIN_TEAM_MEMBERS
from teams.models import TeamSemester, TeamSemesterMember

if TYPE_CHECKING:
    from accounts.models import User
    from showcase.models import ProjectTrack
    from teams.models import StudyGroup


class AdminMixedTeamDomain:
    """Валидация сборки команды без ограничения по треку/группе."""

    @staticmethod
    def normalize_name(name: str) -> str:
        """Возвращает непустое название команды."""
        cleaned = (name or "").strip()
        if not cleaned:
            raise ValueError("Название команды не может быть пустым")
        return cleaned

    @staticmethod
    def merge_captain_into_members(
        *,
        captain_id: int,
        member_ids: Sequence[int],
    ) -> list[int]:
        """Гарантирует наличие капитана в составе; порядок: капитан, затем остальные."""
        unique: list[int] = []
        seen: set[int] = set()
        for user_id in (captain_id, *member_ids):
            if user_id in seen:
                continue
            seen.add(user_id)
            unique.append(user_id)
        return unique

    @staticmethod
    def ensure_student_users(users: Sequence[User]) -> None:
        """Все участники должны быть студентами."""
        for user in users:
            role_code = user.role.code if user.role else None
            if role_code != "student":
                raise ValueError(
                    f"Пользователь {user.get_full_name() or user.email} "
                    "не является студентом"
                )

    @staticmethod
    def ensure_registered_users(users: Sequence[User]) -> None:
        """Участники должны быть активными и не плейсхолдерами."""
        for user in users:
            if not user.is_active or user.is_placeholder:
                raise ValueError(
                    f"Студент {user.get_full_name() or user.email} "
                    "не зарегистрирован в системе"
                )

    @staticmethod
    def resolve_home_study_group(
        *,
        home_study_group: StudyGroup | None,
        captain: User,
    ) -> StudyGroup:
        """Домашняя группа: явно указанная или группа капитана."""
        if home_study_group is not None:
            return home_study_group
        if captain.study_group_id is None or captain.study_group is None:
            raise ValueError(
                "Укажите домашнюю учебную группу: у капитана группа не задана"
            )
        return captain.study_group

    @staticmethod
    def resolve_member_limits(track: ProjectTrack | None) -> tuple[int, int]:
        """Лимиты размера: из трека или глобальные дефолты."""
        if track is not None:
            return track.min_team_members, track.max_team_members
        return DEFAULT_MIN_TEAM_MEMBERS, DEFAULT_MAX_TEAM_MEMBERS

    @staticmethod
    def ensure_status_member_count(
        *,
        status: str,
        members_count: int,
        min_team_members: int,
        max_team_members: int,
    ) -> None:
        """Для assembled проверяет лимиты; для forming — только верхнюю границу."""
        if members_count < 1:
            raise ValueError("В команде должен быть хотя бы один участник")
        if members_count > max_team_members:
            raise ValueError(
                f"В команде не может быть больше {max_team_members} участников"
            )
        if status == TeamSemester.Status.ASSEMBLED:
            if members_count < min_team_members:
                raise ValueError(
                    f"Для подтверждённого состава нужно не меньше "
                    f"{min_team_members} участников"
                )

    @staticmethod
    def resolve_member_role(*, user_id: int, captain_id: int) -> str:
        """Роль участника: капитан — leader, остальные — member."""
        if user_id == captain_id:
            return TeamSemesterMember.Role.LEADER
        return TeamSemesterMember.Role.MEMBER

    @staticmethod
    def build_created_log_text(*, name: str, members_count: int) -> str:
        """Текст события о ручной сборке в admin."""
        return (
            f"Команда «{name}» собрана вручную в admin "
            f"({members_count} уч., без проверки трека групп)"
        )
