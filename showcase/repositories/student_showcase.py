"""Репозиторий студенческой витрины проектов (без N+1)."""

from __future__ import annotations

from django.db.models import Count, Prefetch

from showcase.models import ProjectApplication, ProjectTrack, ProjectTrackApplication
from teams.models import TeamEventLog, TeamSemester, TeamSemesterMember


class StudentShowcaseRepository:
    """Запросы и запись для студенческой витрины проектов."""

    def list_group_tracks_with_projects(
        self, *, group_id: int, semester_id: int
    ) -> list[ProjectTrack]:
        """Треки группы в семестре с одобренными проектами и тегами."""
        approved_links = (
            ProjectTrackApplication.objects.filter(
                project_application__status__code="approved"
            )
            .select_related("project_application", "project_application__status")
            .prefetch_related("project_application__tags")
            .order_by("project_application__title")
        )
        return list(
            ProjectTrack.objects.filter(
                semester_id=semester_id,
                group_links__study_group_id=group_id,
            )
            .distinct()
            .prefetch_related(Prefetch("application_links", queryset=approved_links))
            .order_by("name")
        )

    def map_enrolled_teams_counts(
        self,
        *,
        semester_id: int,
        track_ids: list[int],
        application_ids: list[int],
    ) -> dict[tuple[int, int], int]:
        """Карта (track_id, application_id) → число записанных команд."""
        if not track_ids or not application_ids:
            return {}
        rows = (
            TeamSemester.objects.filter(
                semester_id=semester_id,
                project_track_id__in=track_ids,
                project_application_id__in=application_ids,
            )
            .values("project_track_id", "project_application_id")
            .annotate(enrolled=Count("id"))
        )
        return {
            (row["project_track_id"], row["project_application_id"]): int(
                row["enrolled"]
            )
            for row in rows
            if row["project_application_id"] is not None
        }

    def get_accessible_project(
        self,
        *,
        project_id: int,
        group_id: int,
        semester_id: int,
    ) -> tuple[ProjectApplication, int] | None:
        """Одобренный проект, доступный группе в семестре; (application, track_id)."""
        link = (
            ProjectTrackApplication.objects.filter(
                project_application_id=project_id,
                project_application__status__code="approved",
                project_track__semester_id=semester_id,
                project_track__group_links__study_group_id=group_id,
            )
            .select_related(
                "project_application",
                "project_application__status",
                "project_track",
            )
            .prefetch_related("project_application__tags")
            .distinct()
            .first()
        )
        if link is None:
            return None
        return link.project_application, link.project_track_id

    def count_enrolled_teams(
        self,
        *,
        semester_id: int,
        track_id: int,
        application_id: int,
    ) -> int:
        """Число команд, записанных на проект в треке/семестре."""
        return TeamSemester.objects.filter(
            semester_id=semester_id,
            project_track_id=track_id,
            project_application_id=application_id,
        ).count()

    def get_user_team_semester_for_update(
        self, *, user_id: int, semester_id: int
    ) -> TeamSemester | None:
        """Команда пользователя в семестре с блокировкой строки."""
        team_semester_id = (
            TeamSemester.objects.filter(
                semester_id=semester_id,
                members__user_id=user_id,
            )
            .values_list("id", flat=True)
            .first()
        )
        if team_semester_id is None:
            return None

        try:
            team_semester = (
                TeamSemester.objects.select_for_update()
                .select_related(
                    "team", "captain", "project_track", "project_application"
                )
                .get(pk=team_semester_id)
            )
        except TeamSemester.DoesNotExist:
            return None

        # Участников подгружаем отдельно: FOR UPDATE нельзя сочетать с JOIN prefetch.
        members = list(
            TeamSemesterMember.objects.filter(
                team_semester_id=team_semester.id
            ).select_related("user")
        )
        team_semester._prefetched_objects_cache = {"members": members}  # noqa: SLF001
        return team_semester

    def get_user_team_semester(
        self, *, user_id: int, semester_id: int
    ) -> TeamSemester | None:
        """Команда пользователя в семестре (без блокировки)."""
        return (
            TeamSemester.objects.filter(
                semester_id=semester_id,
                members__user_id=user_id,
            )
            .select_related("team", "captain", "project_track", "project_application")
            .prefetch_related(
                Prefetch(
                    "members",
                    queryset=TeamSemesterMember.objects.select_related("user"),
                )
            )
            .distinct()
            .first()
        )

    def get_project_track_link(
        self, *, project_id: int, track_id: int, semester_id: int
    ) -> ProjectTrackApplication | None:
        """Связь проект↔трек с проверкой семестра и статуса approved."""
        return (
            ProjectTrackApplication.objects.filter(
                project_application_id=project_id,
                project_track_id=track_id,
                project_track__semester_id=semester_id,
                project_application__status__code="approved",
            )
            .select_related("project_application", "project_track")
            .first()
        )

    def count_enrolled_teams_for_update(
        self,
        *,
        semester_id: int,
        track_id: int,
        application_id: int,
    ) -> int:
        """Счётчик записанных команд с блокировкой строк TeamSemester проекта."""
        qs = TeamSemester.objects.filter(
            semester_id=semester_id,
            project_track_id=track_id,
            project_application_id=application_id,
        ).select_for_update()
        return qs.count()

    def enroll_team(
        self,
        *,
        team_semester: TeamSemester,
        application: ProjectApplication,
        actor_id: int,
    ) -> TeamSemester:
        """Привязывает проект к команде и пишет лог."""
        team_semester.project_application = application
        team_semester.save(update_fields=["project_application", "updated_at"])
        title = application.title or f"#{application.pk}"
        TeamEventLog.objects.create(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=actor_id,
            text=f"Команда записана на проект «{title}»",
        )
        return team_semester
