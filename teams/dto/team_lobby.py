"""DTO лобби формирования команд и «Моей команды»."""

from __future__ import annotations

from typing import Any

from showcase.constants import DEFAULT_MAX_TEAM_MEMBERS, DEFAULT_MIN_TEAM_MEMBERS
from showcase.models import ProjectTrack
from teams.domain.team_lobby import TeamLobbyDomain
from teams.models import (
    TeamEventLog,
    TeamInvitation,
    TeamJoinRequest,
    TeamSemester,
    TeamSemesterMember,
)


def _user_brief(user) -> dict[str, Any]:
    return {
        "id": user.id,
        "full_name": TeamLobbyDomain.user_display_name(user),
    }


class LobbyTeamItemDTO:
    """Карточка команды в лобби."""

    def __init__(
        self,
        team_semester: TeamSemester,
        *,
        my_pending_join_request_id: int | None,
        min_team_members: int | None = None,
        max_team_members: int | None = None,
    ) -> None:
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.status = team_semester.status
        self.track_id = team_semester.project_track_id
        self.members_count = int(getattr(team_semester, "members_count", 0) or 0)
        track = team_semester.project_track
        if min_team_members is not None and max_team_members is not None:
            self.min_team_members = min_team_members
            self.max_team_members = max_team_members
        else:
            self.min_team_members = (
                track.min_team_members if track else DEFAULT_MIN_TEAM_MEMBERS
            )
            self.max_team_members = (
                track.max_team_members if track else DEFAULT_MAX_TEAM_MEMBERS
            )
        self.captain = _user_brief(team_semester.captain)
        self.my_pending_join_request_id = my_pending_join_request_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "track_id": self.track_id,
            "membersCount": self.members_count,
            "minTeamMembers": self.min_team_members,
            "maxTeamMembers": self.max_team_members,
            "captain": self.captain,
            "myPendingJoinRequestId": self.my_pending_join_request_id,
        }


class LobbyTrackDTO:
    """Трек в лобби со списком команд."""

    def __init__(
        self,
        track: ProjectTrack,
        *,
        teams: list[dict[str, Any]],
        teams_count: int,
        can_create_team: bool,
    ) -> None:
        self.id = track.id
        self.name = track.name
        self.min_team_members = track.min_team_members
        self.max_team_members = track.max_team_members
        self.recommended_teams_count = int(
            getattr(track, "recommended_teams_count", 0) or 0
        )
        self.teams_count = teams_count
        self.can_create_team = can_create_team
        self.teams = teams

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "minTeamMembers": self.min_team_members,
            "maxTeamMembers": self.max_team_members,
            "recommendedTeamsCount": self.recommended_teams_count,
            "teamsCount": self.teams_count,
            "canCreateTeam": self.can_create_team,
            "teams": self.teams,
        }


class LobbyJoinRequestDTO:
    """Pending-заявка студента в лобби."""

    def __init__(self, join_request: TeamJoinRequest) -> None:
        ts = join_request.team_semester
        track = ts.project_track
        self.id = join_request.id
        self.status = join_request.status
        self.team = {"id": ts.id, "name": ts.team.name}
        self.track = {"id": track.id, "name": track.name} if track else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "team": self.team,
            "track": self.track,
        }


class LobbyInvitationDTO:
    """Pending-приглашение студента в лобби."""

    def __init__(self, invitation: TeamInvitation) -> None:
        ts = invitation.team_semester
        self.id = invitation.id
        self.status = invitation.status
        self.role = invitation.role
        self.team = {"id": ts.id, "name": ts.team.name}
        self.invited_by = _user_brief(invitation.invited_by)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "role": self.role,
            "team": self.team,
            "invitedBy": self.invited_by,
        }


class LobbyReadDTO:
    """Ответ GET /lobby/."""

    def __init__(
        self,
        *,
        semester_id: int,
        my_team: dict[str, Any] | None,
        can_create_team: bool,
        join_requests: list[dict[str, Any]],
        invitations: list[dict[str, Any]],
        teams: list[dict[str, Any]],
        tracks: list[dict[str, Any]],
    ) -> None:
        self.semester_id = semester_id
        self.my_team = my_team
        self.can_create_team = can_create_team
        self.join_requests = join_requests
        self.invitations = invitations
        self.teams = teams
        self.tracks = tracks

    def to_dict(self) -> dict[str, Any]:
        return {
            "semester_id": self.semester_id,
            "myTeam": self.my_team,
            "canCreateTeam": self.can_create_team,
            "joinRequests": self.join_requests,
            "invitations": self.invitations,
            "teams": self.teams,
            "tracks": self.tracks,
        }


class MyTeamMemberDTO:
    """Участник в «Моей команде»."""

    def __init__(self, member: TeamSemesterMember) -> None:
        self.id = member.user_id
        self.full_name = TeamLobbyDomain.user_display_name(member.user)
        self.role = member.role

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "role": self.role,
        }


class MyTeamEventLogDTO:
    """Запись лога команды."""

    def __init__(self, log: TeamEventLog) -> None:
        self.user_id = log.user_id
        self.text = log.text
        self.created_at = log.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "text": self.text,
            "created_at": self.created_at,
        }


class MyTeamJoinRequestDTO:
    """Pending-заявка для капитана."""

    def __init__(self, join_request: TeamJoinRequest) -> None:
        self.id = join_request.id
        self.user = _user_brief(join_request.user)
        self.created_at = join_request.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user": self.user,
            "created_at": self.created_at,
        }


class MyTeamInvitationDTO:
    """Отправленное приглашение капитана."""

    def __init__(self, invitation: TeamInvitation) -> None:
        self.id = invitation.id
        self.user = _user_brief(invitation.user)
        self.role = invitation.role
        self.created_at = invitation.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user": self.user,
            "role": self.role,
            "created_at": self.created_at,
        }


class MyTeamReadDTO:
    """Ответ GET /my-team/."""

    def __init__(
        self,
        team_semester: TeamSemester,
        *,
        viewer_id: int,
        min_team_members: int | None = None,
        max_team_members: int | None = None,
    ) -> None:
        track = team_semester.project_track
        members = list(team_semester.members.all())
        is_captain = team_semester.captain_id == viewer_id
        members_count = len(members)
        if min_team_members is not None and max_team_members is not None:
            min_members = min_team_members
            max_members = max_team_members
        else:
            min_members = track.min_team_members if track else DEFAULT_MIN_TEAM_MEMBERS
            max_members = track.max_team_members if track else DEFAULT_MAX_TEAM_MEMBERS
        status = team_semester.status
        forming = status == TeamSemester.Status.FORMING

        self.id = team_semester.id
        self.name = team_semester.team.name
        self.status = status
        self.min_team_members = min_members
        self.max_team_members = max_members
        self.is_captain = is_captain
        self.members = [MyTeamMemberDTO(m).to_dict() for m in members]
        self.can_leave = (not is_captain) and forming
        self.join_requests: list[dict[str, Any]] = []
        self.sent_invitations: list[dict[str, Any]] = []
        self.can_confirm_composition = False
        self.can_delete_team = False
        self.can_invite = False
        self.can_kick = False

        if is_captain:
            self.join_requests = [
                MyTeamJoinRequestDTO(req).to_dict()
                for req in team_semester.join_requests.all()
            ]
            self.sent_invitations = [
                MyTeamInvitationDTO(inv).to_dict()
                for inv in team_semester.invitations.all()
            ]
            self.can_confirm_composition = TeamLobbyDomain.can_confirm_composition(
                is_captain=True,
                status=status,
                members_count=members_count,
                min_team_members=min_members,
                max_team_members=max_members,
            )
            self.can_delete_team = TeamLobbyDomain.can_delete_team(
                is_captain=True,
                status=status,
                members_count=members_count,
            )
            self.can_invite = forming
            self.can_kick = forming and members_count > 1

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "minTeamMembers": self.min_team_members,
            "maxTeamMembers": self.max_team_members,
            "isCaptain": self.is_captain,
            "members": self.members,
            "canLeave": self.can_leave,
        }
        if self.is_captain:
            payload.update(
                {
                    "joinRequests": self.join_requests,
                    "sentInvitations": self.sent_invitations,
                    "canConfirmComposition": self.can_confirm_composition,
                    "canDeleteTeam": self.can_delete_team,
                    "canInvite": self.can_invite,
                    "canKick": self.can_kick,
                }
            )
        return payload
