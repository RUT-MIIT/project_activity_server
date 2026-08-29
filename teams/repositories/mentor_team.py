"""Репозиторий управления командой наставником."""

from __future__ import annotations

from django.db.models import Prefetch

from teams.models import Team, TeamSemester, TeamSemesterMember
from teams.repositories.team_lobby import TeamLobbyRepository


class MentorTeamRepository:
    """Запросы и записи для API команд наставника."""

    def __init__(self) -> None:
        self._lobby = TeamLobbyRepository()

    def get_team_semester_detail(
        self,
        *,
        team_semester_id: int,
        group_id: int,
        semester_id: int,
    ) -> TeamSemester | None:
        """Команда в семестре с составом или None."""
        team_semester = (
            TeamSemester.objects.filter(
                pk=team_semester_id,
                semester_id=semester_id,
                team__home_study_group_id=group_id,
            )
            .select_related("team", "captain", "project_track")
            .prefetch_related(
                Prefetch(
                    "members",
                    queryset=TeamSemesterMember.objects.select_related("user").order_by(
                        "role", "joined_at"
                    ),
                )
            )
            .first()
        )
        return team_semester

    def count_members(self, team_semester_id: int) -> int:
        """Число участников команды в семестре."""
        return TeamSemesterMember.objects.filter(
            team_semester_id=team_semester_id
        ).count()

    def update_team_name(self, team_id: int, name: str) -> None:
        """Обновляет название постоянной команды."""
        Team.objects.filter(pk=team_id).update(name=name.strip())

    def transfer_captain(
        self, team_semester: TeamSemester, new_captain_id: int
    ) -> TeamSemester:
        """Назначает нового капитана и синхронизирует роли участников."""
        TeamSemesterMember.objects.filter(
            team_semester_id=team_semester.id,
            role=TeamSemesterMember.Role.LEADER,
        ).update(role=TeamSemesterMember.Role.MEMBER)
        TeamSemesterMember.objects.filter(
            team_semester_id=team_semester.id,
            user_id=new_captain_id,
        ).update(role=TeamSemesterMember.Role.LEADER)
        team_semester.captain_id = new_captain_id
        team_semester.save(update_fields=["captain_id", "updated_at"])
        return self.reload_team_semester(team_semester.id)

    def set_captain_for_first_member(
        self, team_semester: TeamSemester, user_id: int
    ) -> None:
        """Назначает капитана при добавлении первого участника."""
        team_semester.captain_id = user_id
        team_semester.save(update_fields=["captain_id", "updated_at"])

    def reload_team_semester(self, team_semester_id: int) -> TeamSemester:
        """Перезагружает команду с составом."""
        return (
            TeamSemester.objects.filter(pk=team_semester_id)
            .select_related("team", "captain", "project_track")
            .prefetch_related(
                Prefetch(
                    "members",
                    queryset=TeamSemesterMember.objects.select_related("user").order_by(
                        "role", "joined_at"
                    ),
                )
            )
            .get(pk=team_semester_id)
        )

    def add_member(
        self, *, team_semester_id: int, user_id: int, role: str
    ) -> TeamSemesterMember:
        """Добавляет участника в команду семестра."""
        return self._lobby.add_member(
            team_semester_id=team_semester_id,
            user_id=user_id,
            role=role,
        )

    def remove_member_force(self, *, team_semester_id: int, user_id: int) -> bool:
        """Удаляет участника любой роли."""
        return self._lobby.remove_member_force(
            team_semester_id=team_semester_id,
            user_id=user_id,
        )

    def set_status(self, team_semester: TeamSemester, status: str) -> TeamSemester:
        """Меняет статус состава."""
        return self._lobby.set_status(team_semester, status)

    def delete_team_semester(self, team_semester: TeamSemester) -> None:
        """Удаляет семестровый контекст и постоянную команду при необходимости."""
        self._lobby.delete_team_semester(team_semester)

    def add_event_log(
        self,
        *,
        team_id: int,
        team_semester_id: int,
        user_id: int,
        text: str,
    ) -> None:
        """Пишет запись в лог команды."""
        self._lobby.add_event_log(
            team_id=team_id,
            team_semester_id=team_semester_id,
            user_id=user_id,
            text=text,
        )

    def user_has_team_in_semester(self, *, user_id: int, semester_id: int) -> bool:
        """True, если пользователь уже в команде в семестре."""
        return self._lobby.user_has_team_in_semester(
            user_id=user_id,
            semester_id=semester_id,
        )

    def get_user(self, user_id: int):
        """Пользователь по id или None."""
        return self._lobby.get_user(user_id)

    def list_group_tracks(self, *, group_id: int, semester_id: int):
        """Треки группы в семестре."""
        return self._lobby.list_group_tracks(
            group_id=group_id,
            semester_id=semester_id,
        )

    def mark_user_requests_obsolete(self, *, user_id: int, semester_id: int) -> None:
        """Снимает pending-заявки и приглашения студента в семестре."""
        self._lobby.mark_user_requests_obsolete(
            user_id=user_id,
            semester_id=semester_id,
        )
