"""Сервис ручной сборки смешанной команды из Django admin."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Semester
from showcase.models import ProjectApplication, ProjectTrack
from teams.domain.admin_mixed_team import AdminMixedTeamDomain
from teams.models import StudyGroup, Team, TeamSemester, TeamSemesterMember
from teams.repositories.team_lobby import TeamLobbyRepository

User = get_user_model()


@dataclass(frozen=True)
class AdminMixedTeamCreateResult:
    """Результат сборки смешанной команды в admin."""

    team: Team
    team_semester: TeamSemester
    members_count: int


class AdminMixedTeamService:
    """Создаёт команду с участниками из любых учебных групп."""

    def __init__(self) -> None:
        self.domain = AdminMixedTeamDomain()
        self.repository = TeamLobbyRepository()

    @transaction.atomic
    def create_mixed_team(
        self,
        *,
        name: str,
        semester: Semester,
        captain: User,
        members: Sequence[User],
        actor_id: int | None = None,
        home_study_group: StudyGroup | None = None,
        project_track: ProjectTrack | None = None,
        project_application: ProjectApplication | None = None,
        mentor: User | None = None,
        status: str = TeamSemester.Status.ASSEMBLED,
    ) -> AdminMixedTeamCreateResult:
        """Собирает команду без проверки принадлежности групп к треку.

        Raises:
            ValueError: при нарушении бизнес-правил состава.
        """
        cleaned_name = self.domain.normalize_name(name)
        member_ids = self.domain.merge_captain_into_members(
            captain_id=captain.id,
            member_ids=[user.id for user in members],
        )
        users_by_id = {user.id: user for user in members}
        users_by_id[captain.id] = captain
        ordered_users = [users_by_id[user_id] for user_id in member_ids]

        self.domain.ensure_student_users(ordered_users)
        self.domain.ensure_registered_users(ordered_users)

        resolved_home = self.domain.resolve_home_study_group(
            home_study_group=home_study_group,
            captain=captain,
        )
        min_members, max_members = self.domain.resolve_member_limits(project_track)
        self.domain.ensure_status_member_count(
            status=status,
            members_count=len(ordered_users),
            min_team_members=min_members,
            max_team_members=max_members,
        )

        if (
            project_application is not None
            and project_application.semester_id is not None
            and project_application.semester_id != semester.id
        ):
            raise ValueError("Проектная заявка относится к другому семестру")
        if project_track is not None and project_track.semester_id != semester.id:
            raise ValueError("Проектный трек относится к другому семестру")

        busy_ids = self._busy_user_ids(
            user_ids=member_ids,
            semester_id=semester.id,
        )
        if busy_ids:
            busy_names = ", ".join(
                users_by_id[user_id].get_full_name() or users_by_id[user_id].email
                for user_id in busy_ids
            )
            raise ValueError(f"Уже состоят в команде в этом семестре: {busy_names}")

        if mentor is not None:
            mentor_role = mentor.role.code if mentor.role else None
            if mentor_role != "mentor":
                raise ValueError("Наставник должен иметь роль mentor")

        team = Team.objects.create(
            name=cleaned_name,
            home_study_group=resolved_home,
        )
        team_semester = TeamSemester.objects.create(
            team=team,
            semester=semester,
            project_track=project_track,
            project_application=project_application,
            mentor=mentor,
            captain=captain,
            status=status,
        )

        for user in ordered_users:
            role = self.domain.resolve_member_role(
                user_id=user.id,
                captain_id=captain.id,
            )
            TeamSemesterMember.objects.create(
                team_semester=team_semester,
                user=user,
                role=role,
            )
            self.repository.mark_user_requests_obsolete(
                user_id=user.id,
                semester_id=semester.id,
            )

        self.repository.add_event_log(
            team_id=team.id,
            team_semester_id=team_semester.id,
            user_id=actor_id,
            text=self.domain.build_created_log_text(
                name=cleaned_name,
                members_count=len(ordered_users),
            ),
        )

        team_semester = (
            TeamSemester.objects.select_related(
                "team",
                "captain",
                "mentor",
                "project_track",
                "project_application",
            )
            .prefetch_related("members__user")
            .get(pk=team_semester.pk)
        )
        return AdminMixedTeamCreateResult(
            team=team_semester.team,
            team_semester=team_semester,
            members_count=len(ordered_users),
        )

    def _busy_user_ids(
        self,
        *,
        user_ids: Sequence[int],
        semester_id: int,
    ) -> list[int]:
        """ID студентов, уже состоящих в команде семестра (с сохранением порядка)."""
        if not user_ids:
            return []
        busy = set(
            TeamSemesterMember.objects.filter(
                user_id__in=user_ids,
                semester_id=semester_id,
            ).values_list("user_id", flat=True)
        )
        return [user_id for user_id in user_ids if user_id in busy]
