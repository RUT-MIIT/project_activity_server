"""Доменные правила лобби формирования команд."""

from __future__ import annotations

from typing import TYPE_CHECKING

from showcase.constants import DEFAULT_MAX_TEAM_MEMBERS, DEFAULT_MIN_TEAM_MEMBERS
from teams.models import (
    TeamInvitation,
    TeamJoinRequest,
    TeamSemester,
    TeamSemesterMember,
)

if TYPE_CHECKING:
    from accounts.models import User
    from showcase.models import ProjectTrack


class TeamLobbyDomain:
    """Чистая бизнес-логика лобби и «Моей команды»."""

    @staticmethod
    def resolve_member_limits(
        team_track: ProjectTrack | None,
        *,
        group_tracks: list[ProjectTrack] | None = None,
    ) -> tuple[int, int]:
        """Лимиты размера команды.

        Приоритет:
        1) трек команды;
        2) effective по трекам группы: max(min), min(max);
        3) дефолты, если треков нет или пересечение пустое.
        """
        if team_track is not None:
            return team_track.min_team_members, team_track.max_team_members
        if group_tracks:
            min_members = max(track.min_team_members for track in group_tracks)
            max_members = min(track.max_team_members for track in group_tracks)
            if min_members <= max_members:
                return min_members, max_members
        return DEFAULT_MIN_TEAM_MEMBERS, DEFAULT_MAX_TEAM_MEMBERS

    @staticmethod
    def ensure_student_with_group(user: User) -> int:
        """Проверяет роль student и наличие учебной группы; возвращает group_id."""
        if not user.role or user.role.code != "student":
            raise PermissionError("Доступно только студентам")
        if not user.study_group_id:
            raise ValueError("У студента не указана учебная группа")
        return user.study_group_id

    @staticmethod
    def can_create_team(
        *,
        has_team: bool,
        teams_count: int,
        recommended_teams_count: int,
    ) -> bool:
        """True, если студент без команды и есть свободный слот."""
        if has_team:
            return False
        return teams_count < recommended_teams_count

    @staticmethod
    def ensure_team_forming(team_semester: TeamSemester) -> None:
        """Запрещает изменения состава при подтверждённом составе."""
        if team_semester.status != TeamSemester.Status.FORMING:
            raise ValueError(
                "Состав команды подтверждён: изменения участников недоступны"
            )

    @staticmethod
    def ensure_is_captain(user: User, team_semester: TeamSemester) -> None:
        """Проверяет, что пользователь — капитан команды."""
        if team_semester.captain_id != user.id:
            raise PermissionError("Действие доступно только капитану команды")

    @staticmethod
    def ensure_invitation_role(role: str) -> None:
        """Приглашение не может назначать роль leader."""
        if role == TeamSemesterMember.Role.LEADER:
            raise ValueError("Нельзя пригласить с ролью руководителя")

    @staticmethod
    def ensure_approve_role(role: str) -> None:
        """При одобрении заявки нельзя назначить второго leader."""
        if role == TeamSemesterMember.Role.LEADER:
            raise ValueError("Нельзя назначить роль руководителя при одобрении заявки")

    @staticmethod
    def user_display_name(user: User) -> str:
        """ФИО пользователя для лога."""
        parts = [user.last_name, user.first_name, user.middle_name]
        return " ".join(part for part in parts if part).strip() or user.email

    @staticmethod
    def can_delete_team(*, is_captain: bool, status: str, members_count: int) -> bool:
        """Удаление: капитан, forming, в составе только он."""
        return (
            is_captain and status == TeamSemester.Status.FORMING and members_count <= 1
        )

    @staticmethod
    def can_confirm_composition(
        *,
        is_captain: bool,
        status: str,
        members_count: int,
        min_team_members: int,
        max_team_members: int,
    ) -> bool:
        """Подтверждение состава: капитан, forming, размер в лимитах трека."""
        if not is_captain or status != TeamSemester.Status.FORMING:
            return False
        return min_team_members <= members_count <= max_team_members

    @staticmethod
    def ensure_same_study_group(user: User, group_id: int) -> None:
        """Проверяет, что пользователь из нужной учебной группы."""
        if user.study_group_id != group_id:
            raise ValueError("Студент должен быть из вашей учебной группы")

    @staticmethod
    def ensure_join_request_pending(join_request: TeamJoinRequest) -> None:
        """Заявка должна быть в статусе pending."""
        if join_request.status != TeamJoinRequest.Status.PENDING:
            raise ValueError("Заявка уже рассмотрена или не актуальна")

    @staticmethod
    def ensure_invitation_pending(invitation: TeamInvitation) -> None:
        """Приглашение должно быть в статусе pending."""
        if invitation.status != TeamInvitation.Status.PENDING:
            raise ValueError("Приглашение уже рассмотрено или не актуально")
