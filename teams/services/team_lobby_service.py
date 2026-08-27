"""Сервис лобби формирования команд и «Моей команды»."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import QuerySet

from accounts.models import Semester
from showcase.models import ProjectTrack
from teams.domain.team_lobby import TeamLobbyDomain
from teams.dto.team_lobby import (
    LobbyInvitationDTO,
    LobbyJoinRequestDTO,
    LobbyReadDTO,
    LobbyTeamItemDTO,
    LobbyTrackDTO,
    MyTeamMemberDTO,
    MyTeamReadDTO,
)
from teams.models import (
    TeamEventLog,
    TeamInvitation,
    TeamJoinRequest,
    TeamSemester,
    TeamSemesterMember,
)
from teams.repositories.team_lobby import TeamLobbyRepository

if TYPE_CHECKING:
    from accounts.models import User as UserType


class TeamLobbyService:
    """Оркестрация Domain + Repository для студенческого лобби."""

    def __init__(self) -> None:
        self.repository = TeamLobbyRepository()
        self.domain = TeamLobbyDomain()

    def _resolve_semester_id(self, semester_id_raw: str | None) -> int:
        """Резолвит semester_id; по умолчанию actual."""
        return Semester.resolve_list_semester_id(semester_id_raw or "actual")

    def _member_limits_for_team(
        self,
        team_semester: TeamSemester,
        *,
        group_id: int,
        semester_id: int,
        group_tracks: list[ProjectTrack] | None = None,
    ) -> tuple[int, int]:
        """Лимиты команды: свой трек → effective по трекам группы → дефолты."""
        tracks = group_tracks
        if team_semester.project_track_id is None and tracks is None:
            tracks = self.repository.list_group_tracks(
                group_id=group_id, semester_id=semester_id
            )
        return self.domain.resolve_member_limits(
            team_semester.project_track,
            group_tracks=tracks,
        )

    def _my_team_dict(
        self,
        team_semester: TeamSemester,
        *,
        viewer_id: int,
        group_id: int,
        semester_id: int,
        group_tracks: list[ProjectTrack] | None = None,
    ) -> dict:
        """Сериализация «Моей команды» с резолвом лимитов без N+1."""
        min_members, max_members = self._member_limits_for_team(
            team_semester,
            group_id=group_id,
            semester_id=semester_id,
            group_tracks=group_tracks,
        )
        return MyTeamReadDTO(
            team_semester,
            viewer_id=viewer_id,
            min_team_members=min_members,
            max_team_members=max_members,
        ).to_dict()

    def get_lobby(self, user: UserType, semester_id_raw: str | None = None) -> dict:
        """GET лобби: треки группы, команды, заявки/приглашения если без команды."""
        group_id = self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)

        tracks = self.repository.list_group_tracks(
            group_id=group_id, semester_id=semester_id
        )
        team_semesters = self.repository.list_group_team_semesters(
            group_id=group_id,
            semester_id=semester_id,
        )
        by_track = self.repository.group_team_semesters_by_track(team_semesters)
        pending_map = self.repository.map_pending_join_request_ids(
            user_id=user.id,
            team_semester_ids=[ts.id for ts in team_semesters],
        )

        my_team_semester = self.repository.get_user_team_semester(
            user_id=user.id, semester_id=semester_id
        )
        has_team = my_team_semester is not None
        my_team_payload = None
        if my_team_semester is not None:
            min_m, max_m = self.domain.resolve_member_limits(
                my_team_semester.project_track,
                group_tracks=tracks,
            )
            my_team_payload = {
                "id": my_team_semester.id,
                "name": my_team_semester.team.name,
                "status": my_team_semester.status,
                "track_id": my_team_semester.project_track_id,
                "minTeamMembers": min_m,
                "maxTeamMembers": max_m,
                "members": [
                    MyTeamMemberDTO(member).to_dict()
                    for member in my_team_semester.members.all()
                ],
            }

        def _lobby_team_item(ts: TeamSemester) -> dict:
            min_m, max_m = self.domain.resolve_member_limits(
                ts.project_track,
                group_tracks=tracks,
            )
            return LobbyTeamItemDTO(
                ts,
                my_pending_join_request_id=pending_map.get(ts.id),
                min_team_members=min_m,
                max_team_members=max_m,
            ).to_dict()

        teams_payload = [_lobby_team_item(ts) for ts in team_semesters]

        track_dtos: list[dict] = []
        any_can_create = False
        for track in tracks:
            teams_for_track = by_track.get(track.id, [])
            teams_count = len(teams_for_track)
            recommended = int(getattr(track, "recommended_teams_count", 0) or 0)
            can_create = self.domain.can_create_team(
                has_team=has_team,
                teams_count=teams_count,
                recommended_teams_count=recommended,
            )
            if can_create:
                any_can_create = True
            track_teams_payload = [_lobby_team_item(ts) for ts in teams_for_track]
            track_dtos.append(
                LobbyTrackDTO(
                    track,
                    teams=track_teams_payload,
                    teams_count=teams_count,
                    can_create_team=can_create,
                ).to_dict()
            )

        join_requests: list[dict] = []
        invitations: list[dict] = []
        if not has_team:
            join_requests = [
                LobbyJoinRequestDTO(req).to_dict()
                for req in self.repository.list_pending_join_requests_for_user(
                    user_id=user.id, semester_id=semester_id
                )
            ]
            invitations = [
                LobbyInvitationDTO(inv).to_dict()
                for inv in self.repository.list_pending_invitations_for_user(
                    user_id=user.id, semester_id=semester_id
                )
            ]

        return LobbyReadDTO(
            semester_id=semester_id,
            my_team=my_team_payload,
            can_create_team=any_can_create,
            join_requests=join_requests,
            invitations=invitations,
            teams=teams_payload,
            tracks=track_dtos,
        ).to_dict()

    @transaction.atomic
    def create_team(
        self,
        user: UserType,
        *,
        track_id: int | None,
        name: str,
        semester_id_raw: str | None = None,
    ) -> dict:
        """Создаёт команду студента.

        Если track_id не передан и группе доступен ровно один трек —
        он проставляется автоматически.
        """
        group_id = self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)

        if not name or not name.strip():
            raise ValueError("Поле name не может быть пустым")

        if self.repository.user_has_team_in_semester(
            user_id=user.id, semester_id=semester_id
        ):
            raise ValueError("Вы уже состоите в команде в этом семестре")

        if track_id is None:
            available_tracks = self.repository.list_group_tracks(
                group_id=group_id, semester_id=semester_id
            )
            if len(available_tracks) == 1:
                track_id = available_tracks[0].id

        if track_id is not None:
            track = self.repository.get_track_for_group(
                track_id=track_id, group_id=group_id, semester_id=semester_id
            )
            if track is None:
                raise ValueError("Проектный трек не найден для вашей группы")

            teams_count = self.repository.count_group_teams_in_track(
                group_id=group_id, track_id=track_id, semester_id=semester_id
            )
            recommended = int(getattr(track, "recommended_teams_count", 0) or 0)
            if not self.domain.can_create_team(
                has_team=False,
                teams_count=teams_count,
                recommended_teams_count=recommended,
            ):
                raise ValueError("Нет свободных слотов для создания команды в треке")

        team_semester = self.repository.create_team_with_semester(
            name=name,
            group_id=group_id,
            semester_id=semester_id,
            track_id=track_id,
            captain_id=user.id,
        )
        self.repository.mark_user_requests_obsolete(
            user_id=user.id, semester_id=semester_id
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text="Команда создана",
        )
        return self._my_team_dict(
            team_semester,
            viewer_id=user.id,
            group_id=group_id,
            semester_id=semester_id,
        )

    @transaction.atomic
    def create_join_request(
        self,
        user: UserType,
        team_semester_id: int,
        semester_id_raw: str | None = None,
    ) -> dict:
        """Студент подаёт заявку на вступление."""
        group_id = self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)

        if self.repository.user_has_team_in_semester(
            user_id=user.id, semester_id=semester_id
        ):
            raise ValueError("Вы уже состоите в команде")

        team_semester = self.repository.get_team_semester(team_semester_id)
        if team_semester is None:
            raise ValueError("Команда не найдена")
        if team_semester.semester_id != semester_id:
            raise ValueError("Команда относится к другому семестру")
        if team_semester.team.home_study_group_id != group_id:
            raise ValueError("Можно подавать заявку только в команды своей группы")
        self.domain.ensure_team_forming(team_semester)

        if self.repository.map_pending_join_request_ids(
            user_id=user.id, team_semester_ids=[team_semester_id]
        ):
            raise ValueError("Заявка на эту команду уже подана")

        join_request = self.repository.create_join_request(
            team_semester_id=team_semester_id, user_id=user.id
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=(
                f"Подана заявка на вступление от "
                f"{self.domain.user_display_name(user)}"
            ),
        )
        return {"id": join_request.id, "status": join_request.status}

    @transaction.atomic
    def accept_invitation(self, user: UserType, invitation_id: int) -> dict:
        """Студент принимает приглашение."""
        group_id = self.domain.ensure_student_with_group(user)
        invitation = self.repository.get_invitation(invitation_id)
        if invitation is None:
            raise ValueError("Приглашение не найдено")
        if invitation.user_id != user.id:
            raise PermissionError("Это приглашение адресовано другому пользователю")
        self.domain.ensure_invitation_pending(invitation)

        team_semester = invitation.team_semester
        self.domain.ensure_team_forming(team_semester)

        if self.repository.user_has_team_in_semester(
            user_id=user.id, semester_id=team_semester.semester_id
        ):
            raise ValueError("Вы уже состоите в команде")

        self.repository.add_member(
            team_semester_id=team_semester.id,
            user_id=user.id,
            role=invitation.role,
        )
        self.repository.update_invitation_status(
            invitation, status=TeamInvitation.Status.ACCEPTED
        )
        self.repository.mark_user_requests_obsolete(
            user_id=user.id, semester_id=team_semester.semester_id
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=(
                "Принято приглашение; к команде присоединился "
                f"{self.domain.user_display_name(user)}"
            ),
        )
        detail = self.repository.get_my_team_detail(
            user_id=user.id, semester_id=team_semester.semester_id
        )
        return self._my_team_dict(
            detail,
            viewer_id=user.id,
            group_id=group_id,
            semester_id=team_semester.semester_id,
        )

    @transaction.atomic
    def reject_invitation(self, user: UserType, invitation_id: int) -> dict:
        """Студент отклоняет приглашение."""
        self.domain.ensure_student_with_group(user)
        invitation = self.repository.get_invitation(invitation_id)
        if invitation is None:
            raise ValueError("Приглашение не найдено")
        if invitation.user_id != user.id:
            raise PermissionError("Это приглашение адресовано другому пользователю")
        self.domain.ensure_invitation_pending(invitation)
        team_semester = invitation.team_semester
        self.repository.update_invitation_status(
            invitation, status=TeamInvitation.Status.REJECTED
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=(
                "Отклонено приглашение пользователем "
                f"{self.domain.user_display_name(user)}"
            ),
        )
        return {"id": invitation.id, "status": invitation.status}

    def get_my_team(self, user: UserType, semester_id_raw: str | None = None) -> dict:
        """GET «Моя команда»."""
        group_id = self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)
        detail = self.repository.get_my_team_detail(
            user_id=user.id, semester_id=semester_id
        )
        if detail is None:
            raise ValueError("Вы не состоите в команде в этом семестре")
        return self._my_team_dict(
            detail,
            viewer_id=user.id,
            group_id=group_id,
            semester_id=semester_id,
        )

    def get_my_team_event_logs(
        self, user: UserType, semester_id_raw: str | None = None
    ) -> QuerySet[TeamEventLog]:
        """Queryset лога «Моей команды» (новые сверху); 404 если нет команды."""
        self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)
        team_semester = self.repository.get_user_team_semester(
            user_id=user.id, semester_id=semester_id
        )
        if team_semester is None:
            raise ValueError("Вы не состоите в команде в этом семестре")
        return self.repository.list_event_logs(team_semester_id=team_semester.id)

    def _get_captain_team(
        self, user: UserType, semester_id_raw: str | None = None
    ) -> TeamSemester:
        """Возвращает команду капитана или бросает ошибку."""
        self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)
        detail = self.repository.get_my_team_detail(
            user_id=user.id, semester_id=semester_id
        )
        if detail is None:
            raise ValueError("Вы не состоите в команде в этом семестре")
        self.domain.ensure_is_captain(user, detail)
        return detail

    @transaction.atomic
    def approve_join_request(
        self,
        user: UserType,
        join_request_id: int,
        *,
        role: str,
        semester_id_raw: str | None = None,
    ) -> dict:
        """Капитан одобряет заявку и назначает роль."""
        team_semester = self._get_captain_team(user, semester_id_raw)
        self.domain.ensure_team_forming(team_semester)
        self.domain.ensure_approve_role(role)

        join_request = self.repository.get_join_request(join_request_id)
        if join_request is None:
            raise ValueError("Заявка не найдена")
        if join_request.team_semester_id != team_semester.id:
            raise PermissionError("Заявка относится к другой команде")
        self.domain.ensure_join_request_pending(join_request)

        applicant = join_request.user
        if self.repository.user_has_team_in_semester(
            user_id=applicant.id, semester_id=team_semester.semester_id
        ):
            raise ValueError("Заявитель уже состоит в команде")

        self.repository.add_member(
            team_semester_id=team_semester.id,
            user_id=applicant.id,
            role=role,
        )
        self.repository.update_join_request_status(
            join_request,
            status=TeamJoinRequest.Status.APPROVED,
            reviewed_by_id=user.id,
        )
        self.repository.mark_user_requests_obsolete(
            user_id=applicant.id, semester_id=team_semester.semester_id
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=(
                "Одобрена заявка от "
                f"{self.domain.user_display_name(applicant)}; "
                "присоединился к команде"
            ),
        )
        return self.get_my_team(user, semester_id_raw)

    @transaction.atomic
    def reject_join_request(
        self,
        user: UserType,
        join_request_id: int,
        semester_id_raw: str | None = None,
    ) -> dict:
        """Капитан отклоняет заявку."""
        team_semester = self._get_captain_team(user, semester_id_raw)
        self.domain.ensure_team_forming(team_semester)

        join_request = self.repository.get_join_request(join_request_id)
        if join_request is None:
            raise ValueError("Заявка не найдена")
        if join_request.team_semester_id != team_semester.id:
            raise PermissionError("Заявка относится к другой команде")
        self.domain.ensure_join_request_pending(join_request)

        self.repository.update_join_request_status(
            join_request,
            status=TeamJoinRequest.Status.REJECTED,
            reviewed_by_id=user.id,
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=(
                "Отклонена заявка от "
                f"{self.domain.user_display_name(join_request.user)}"
            ),
        )
        return self.get_my_team(user, semester_id_raw)

    @transaction.atomic
    def create_invitation(
        self,
        user: UserType,
        *,
        invitee_user_id: int,
        role: str,
        semester_id_raw: str | None = None,
    ) -> dict:
        """Капитан приглашает одногруппника."""
        group_id = self.domain.ensure_student_with_group(user)
        team_semester = self._get_captain_team(user, semester_id_raw)
        self.domain.ensure_team_forming(team_semester)
        self.domain.ensure_invitation_role(role)

        invitee = self.repository.get_user(invitee_user_id)
        if invitee is None:
            raise ValueError("Пользователь не найден")
        self.domain.ensure_same_study_group(invitee, group_id)

        if self.repository.user_has_team_in_semester(
            user_id=invitee.id, semester_id=team_semester.semester_id
        ):
            raise ValueError("Студент уже состоит в команде")

        if TeamInvitation.objects.filter(
            team_semester_id=team_semester.id,
            user_id=invitee.id,
            status=TeamInvitation.Status.PENDING,
        ).exists():
            raise ValueError("Приглашение этому студенту уже отправлено")

        invitation = self.repository.create_invitation(
            team_semester_id=team_semester.id,
            user_id=invitee.id,
            invited_by_id=user.id,
            role=role,
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=(
                "Отправлено приглашение " f"{self.domain.user_display_name(invitee)}"
            ),
        )
        return {
            "id": invitation.id,
            "status": invitation.status,
            "role": invitation.role,
            "user": {
                "id": invitee.id,
                "full_name": self.domain.user_display_name(invitee),
            },
        }

    @transaction.atomic
    def kick_member(
        self,
        user: UserType,
        member_user_id: int,
        semester_id_raw: str | None = None,
    ) -> dict:
        """Капитан удаляет участника."""
        team_semester = self._get_captain_team(user, semester_id_raw)
        self.domain.ensure_team_forming(team_semester)

        if member_user_id == user.id:
            raise ValueError("Нельзя удалить себя; удалите команду")

        member = next(
            (m for m in team_semester.members.all() if m.user_id == member_user_id),
            None,
        )
        if member is None:
            raise ValueError("Участник не найден в команде")
        if member.role == TeamSemesterMember.Role.LEADER:
            raise ValueError("Нельзя удалить руководителя команды")

        display = self.domain.user_display_name(member.user)
        self.repository.remove_member(
            team_semester_id=team_semester.id, user_id=member_user_id
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=f"Из команды исключён {display}",
        )
        return self.get_my_team(user, semester_id_raw)

    @transaction.atomic
    def leave_team(self, user: UserType, semester_id_raw: str | None = None) -> None:
        """Участник покидает команду."""
        self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)
        detail = self.repository.get_my_team_detail(
            user_id=user.id, semester_id=semester_id
        )
        if detail is None:
            raise ValueError("Вы не состоите в команде в этом семестре")
        if detail.captain_id == user.id:
            raise ValueError("Капитан не может покинуть команду; удалите команду")
        self.domain.ensure_team_forming(detail)

        self.repository.remove_member_force(team_semester_id=detail.id, user_id=user.id)
        self.repository.add_event_log(
            team_id=detail.team_id,
            team_semester_id=detail.id,
            user_id=user.id,
            text=f"Команду покинул {self.domain.user_display_name(user)}",
        )

    @transaction.atomic
    def confirm_composition(
        self, user: UserType, semester_id_raw: str | None = None
    ) -> dict:
        """Капитан подтверждает состав (forming → assembled)."""
        team_semester = self._get_captain_team(user, semester_id_raw)
        self.domain.ensure_team_forming(team_semester)

        members_count = len(list(team_semester.members.all()))
        min_members, max_members = self._member_limits_for_team(
            team_semester,
            group_id=user.study_group_id,
            semester_id=team_semester.semester_id,
        )
        if not self.domain.can_confirm_composition(
            is_captain=True,
            status=team_semester.status,
            members_count=members_count,
            min_team_members=min_members,
            max_team_members=max_members,
        ):
            raise ValueError(
                "Число участников должно быть в пределах "
                f"{min_members}–{max_members}"
            )

        self.repository.set_status(team_semester, TeamSemester.Status.ASSEMBLED)
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text="Состав команды подтверждён",
        )
        return self.get_my_team(user, semester_id_raw)

    @transaction.atomic
    def delete_my_team(
        self, user: UserType, semester_id_raw: str | None = None
    ) -> None:
        """Капитан удаляет команду (только он в составе)."""
        team_semester = self._get_captain_team(user, semester_id_raw)
        self.domain.ensure_team_forming(team_semester)
        members_count = len(list(team_semester.members.all()))
        if not self.domain.can_delete_team(
            is_captain=True,
            status=team_semester.status,
            members_count=members_count,
        ):
            raise ValueError("Перед удалением команды нужно исключить всех участников")
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text="Команда удалена",
        )
        self.repository.delete_team_semester(team_semester)
