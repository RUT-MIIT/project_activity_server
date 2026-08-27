"""Репозиторий лобби формирования команд (без N+1)."""

from __future__ import annotations

from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch, QuerySet
from django.utils import timezone

from showcase.models import ProjectTrack
from teams.models import (
    Team,
    TeamEventLog,
    TeamInvitation,
    TeamJoinRequest,
    TeamSemester,
    TeamSemesterMember,
)

User = get_user_model()


class TeamLobbyRepository:
    """Запросы и записи для студенческого лобби команд."""

    def list_group_tracks(
        self, *, group_id: int, semester_id: int
    ) -> list[ProjectTrack]:
        """Треки группы в семестре (recommended_teams_count уже на модели трека)."""
        return list(
            ProjectTrack.objects.filter(
                semester_id=semester_id,
                group_links__study_group_id=group_id,
            )
            .distinct()
            .order_by("name")
        )

    def get_sole_group_track(
        self, *, group_id: int, semester_id: int
    ) -> ProjectTrack | None:
        """Единственный трек группы в семестре или None (если 0 или >1)."""
        tracks = list(
            ProjectTrack.objects.filter(
                semester_id=semester_id,
                group_links__study_group_id=group_id,
            )
            .distinct()
            .order_by("name")[:2]
        )
        return tracks[0] if len(tracks) == 1 else None

    def list_group_team_semesters(
        self,
        *,
        group_id: int,
        semester_id: int,
    ) -> list[TeamSemester]:
        """Команды учебной группы в семестре (без фильтра по треку)."""
        return list(
            TeamSemester.objects.filter(
                semester_id=semester_id,
                team__home_study_group_id=group_id,
            )
            .select_related("team", "captain", "project_track")
            .annotate(members_count=Count("members", distinct=True))
            .order_by("team__name")
        )

    def get_user_team_semester(
        self, *, user_id: int, semester_id: int
    ) -> TeamSemester | None:
        """Команда пользователя в семестре или None (с составом без N+1)."""
        return (
            TeamSemester.objects.filter(
                semester_id=semester_id,
                members__user_id=user_id,
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
            .distinct()
            .first()
        )

    def get_my_team_detail(
        self, *, user_id: int, semester_id: int
    ) -> TeamSemester | None:
        """Команда пользователя с составом, заявками и приглашениями."""
        return (
            TeamSemester.objects.filter(
                semester_id=semester_id,
                members__user_id=user_id,
            )
            .select_related("team", "captain", "project_track")
            .prefetch_related(
                Prefetch(
                    "members",
                    queryset=TeamSemesterMember.objects.select_related("user").order_by(
                        "role", "joined_at"
                    ),
                ),
                Prefetch(
                    "join_requests",
                    queryset=TeamJoinRequest.objects.filter(
                        status=TeamJoinRequest.Status.PENDING
                    ).select_related("user"),
                ),
                Prefetch(
                    "invitations",
                    queryset=TeamInvitation.objects.filter(
                        status=TeamInvitation.Status.PENDING
                    ).select_related("user", "invited_by"),
                ),
            )
            .distinct()
            .first()
        )

    def list_event_logs(self, *, team_semester_id: int) -> QuerySet[TeamEventLog]:
        """Лог событий команды в семестре (новые сверху)."""
        return TeamEventLog.objects.filter(team_semester_id=team_semester_id).order_by(
            "-created_at"
        )

    def list_pending_join_requests_for_user(
        self, *, user_id: int, semester_id: int
    ) -> list[TeamJoinRequest]:
        """Pending-заявки студента в семестре."""
        return list(
            TeamJoinRequest.objects.filter(
                user_id=user_id,
                status=TeamJoinRequest.Status.PENDING,
                team_semester__semester_id=semester_id,
            )
            .select_related(
                "team_semester__team",
                "team_semester__project_track",
            )
            .order_by("-created_at")
        )

    def list_pending_invitations_for_user(
        self, *, user_id: int, semester_id: int
    ) -> list[TeamInvitation]:
        """Pending-приглашения студента в семестре."""
        return list(
            TeamInvitation.objects.filter(
                user_id=user_id,
                status=TeamInvitation.Status.PENDING,
                team_semester__semester_id=semester_id,
            )
            .select_related(
                "team_semester__team",
                "team_semester__project_track",
                "invited_by",
            )
            .order_by("-created_at")
        )

    def map_pending_join_request_ids(
        self, *, user_id: int, team_semester_ids: list[int]
    ) -> dict[int, int]:
        """Карта team_semester_id → id pending-заявки текущего пользователя."""
        if not team_semester_ids:
            return {}
        rows = TeamJoinRequest.objects.filter(
            user_id=user_id,
            status=TeamJoinRequest.Status.PENDING,
            team_semester_id__in=team_semester_ids,
        ).values_list("team_semester_id", "id")
        return {ts_id: req_id for ts_id, req_id in rows}

    def get_track_for_group(
        self, *, track_id: int, group_id: int, semester_id: int
    ) -> ProjectTrack | None:
        """Трек, доступный группе в семестре."""
        return (
            ProjectTrack.objects.filter(
                pk=track_id,
                semester_id=semester_id,
                group_links__study_group_id=group_id,
            )
            .distinct()
            .first()
        )

    def count_group_teams_in_track(
        self, *, group_id: int, track_id: int, semester_id: int
    ) -> int:
        """Число команд группы в треке в семестре."""
        return TeamSemester.objects.filter(
            semester_id=semester_id,
            project_track_id=track_id,
            team__home_study_group_id=group_id,
        ).count()

    def user_has_team_in_semester(self, *, user_id: int, semester_id: int) -> bool:
        """True, если студент уже в команде в семестре."""
        return TeamSemesterMember.objects.filter(
            user_id=user_id,
            semester_id=semester_id,
        ).exists()

    def get_team_semester(self, team_semester_id: int) -> TeamSemester | None:
        """Команда в семестре с базовыми связями."""
        try:
            return TeamSemester.objects.select_related(
                "team", "captain", "project_track"
            ).get(pk=team_semester_id)
        except TeamSemester.DoesNotExist:
            return None

    def create_team_with_semester(
        self,
        *,
        name: str,
        group_id: int,
        semester_id: int,
        track_id: int | None,
        captain_id: int,
    ) -> TeamSemester:
        """Создаёт Team + TeamSemester + капитана-участника."""
        team = Team.objects.create(name=name.strip(), home_study_group_id=group_id)
        team_semester = TeamSemester.objects.create(
            team=team,
            semester_id=semester_id,
            project_track_id=track_id,
            captain_id=captain_id,
            status=TeamSemester.Status.FORMING,
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user_id=captain_id,
            role=TeamSemesterMember.Role.LEADER,
        )
        return (
            TeamSemester.objects.select_related("team", "captain", "project_track")
            .prefetch_related("members__user")
            .get(pk=team_semester.pk)
        )

    def create_join_request(
        self, *, team_semester_id: int, user_id: int
    ) -> TeamJoinRequest:
        """Создаёт pending-заявку."""
        return TeamJoinRequest.objects.create(
            team_semester_id=team_semester_id,
            user_id=user_id,
            status=TeamJoinRequest.Status.PENDING,
        )

    def get_join_request(self, join_request_id: int) -> TeamJoinRequest | None:
        """Заявка с командой и заявителем."""
        try:
            return TeamJoinRequest.objects.select_related(
                "user",
                "team_semester",
                "team_semester__team",
                "team_semester__captain",
                "team_semester__project_track",
            ).get(pk=join_request_id)
        except TeamJoinRequest.DoesNotExist:
            return None

    def get_invitation(self, invitation_id: int) -> TeamInvitation | None:
        """Приглашение со связями."""
        try:
            return TeamInvitation.objects.select_related(
                "user",
                "invited_by",
                "team_semester",
                "team_semester__team",
                "team_semester__captain",
                "team_semester__project_track",
            ).get(pk=invitation_id)
        except TeamInvitation.DoesNotExist:
            return None

    def create_invitation(
        self,
        *,
        team_semester_id: int,
        user_id: int,
        invited_by_id: int,
        role: str,
    ) -> TeamInvitation:
        """Создаёт pending-приглашение."""
        return TeamInvitation.objects.create(
            team_semester_id=team_semester_id,
            user_id=user_id,
            invited_by_id=invited_by_id,
            role=role,
            status=TeamInvitation.Status.PENDING,
        )

    def add_member(
        self, *, team_semester_id: int, user_id: int, role: str
    ) -> TeamSemesterMember:
        """Добавляет участника в команду семестра."""
        return TeamSemesterMember.objects.create(
            team_semester_id=team_semester_id,
            user_id=user_id,
            role=role,
        )

    def mark_user_requests_obsolete(self, *, user_id: int, semester_id: int) -> None:
        """Все pending-заявки и приглашения студента в семестре → obsolete."""
        now = timezone.now()
        TeamJoinRequest.objects.filter(
            user_id=user_id,
            status=TeamJoinRequest.Status.PENDING,
            team_semester__semester_id=semester_id,
        ).update(status=TeamJoinRequest.Status.OBSOLETE, reviewed_at=now)
        TeamInvitation.objects.filter(
            user_id=user_id,
            status=TeamInvitation.Status.PENDING,
            team_semester__semester_id=semester_id,
        ).update(status=TeamInvitation.Status.OBSOLETE, reviewed_at=now)

    def update_join_request_status(
        self,
        join_request: TeamJoinRequest,
        *,
        status: str,
        reviewed_by_id: int | None = None,
    ) -> TeamJoinRequest:
        """Обновляет статус заявки."""
        join_request.status = status
        join_request.reviewed_at = timezone.now()
        update_fields = ["status", "reviewed_at"]
        if reviewed_by_id is not None:
            join_request.reviewed_by_id = reviewed_by_id
            update_fields.append("reviewed_by")
        join_request.save(update_fields=update_fields)
        return join_request

    def update_invitation_status(
        self, invitation: TeamInvitation, *, status: str
    ) -> TeamInvitation:
        """Обновляет статус приглашения."""
        invitation.status = status
        invitation.reviewed_at = timezone.now()
        invitation.save(update_fields=["status", "reviewed_at"])
        return invitation

    def remove_member(self, *, team_semester_id: int, user_id: int) -> bool:
        """Удаляет участника (не leader); True если был удалён."""
        deleted, _ = (
            TeamSemesterMember.objects.filter(
                team_semester_id=team_semester_id,
                user_id=user_id,
            )
            .exclude(role=TeamSemesterMember.Role.LEADER)
            .delete()
        )
        return deleted > 0

    def remove_member_force(self, *, team_semester_id: int, user_id: int) -> bool:
        """Удаляет участника любой роли (для leave)."""
        deleted, _ = TeamSemesterMember.objects.filter(
            team_semester_id=team_semester_id,
            user_id=user_id,
        ).delete()
        return deleted > 0

    def set_status(self, team_semester: TeamSemester, status: str) -> TeamSemester:
        """Меняет статус состава."""
        team_semester.status = status
        team_semester.save(update_fields=["status", "updated_at"])
        return team_semester

    def delete_team_semester(self, team_semester: TeamSemester) -> None:
        """Удаляет семестровый контекст и постоянную команду, если больше нет семестров."""
        team = team_semester.team
        team_semester.delete()
        if not team.semester_enrollments.exists():
            team.delete()

    def add_event_log(
        self,
        *,
        team_id: int,
        team_semester_id: int | None,
        user_id: int | None,
        text: str,
    ) -> TeamEventLog:
        """Пишет запись в лог команды."""
        return TeamEventLog.objects.create(
            team_id=team_id,
            team_semester_id=team_semester_id,
            user_id=user_id,
            text=text,
        )

    def group_team_semesters_by_track(
        self, team_semesters: list[TeamSemester]
    ) -> dict[int, list[TeamSemester]]:
        """Группирует команды по project_track_id."""
        result: dict[int, list[TeamSemester]] = defaultdict(list)
        for item in team_semesters:
            if item.project_track_id is not None:
                result[item.project_track_id].append(item)
        return result

    def get_user(self, user_id: int) -> User | None:
        """Пользователь по id или None."""
        try:
            return User.objects.select_related("role", "study_group").get(pk=user_id)
        except User.DoesNotExist:
            return None
