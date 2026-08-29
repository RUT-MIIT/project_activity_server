"""DTO карточки команды для API наставника."""

from __future__ import annotations

from typing import Any

from teams.domain.team_lobby import TeamLobbyDomain
from teams.models import TeamSemester, TeamSemesterMember


class MentorTeamMemberDTO:
    """Участник команды в карточке наставника."""

    def __init__(self, membership: TeamSemesterMember) -> None:
        user = membership.user
        self.user_id = user.id
        self.full_name = TeamLobbyDomain.user_display_name(user)
        self.role = membership.role
        self.is_placeholder = bool(getattr(user, "is_placeholder", False))

    def to_dict(self) -> dict[str, Any]:
        return {
            "userId": self.user_id,
            "fullName": self.full_name,
            "role": self.role,
            "isPlaceholder": self.is_placeholder,
        }


class MentorTeamDetailDTO:
    """Карточка команды для ответов мутаций наставника."""

    def __init__(self, team_semester: TeamSemester) -> None:
        members = list(team_semester.members.all())
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.status = team_semester.status
        self.members_count = len(members)
        self.members = [MentorTeamMemberDTO(member) for member in members]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "membersCount": self.members_count,
            "members": [member.to_dict() for member in self.members],
        }
