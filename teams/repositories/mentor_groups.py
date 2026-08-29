"""Репозиторий списка групп наставника в семестре."""

from __future__ import annotations

from django.db.models import Count, OuterRef, Prefetch, QuerySet, Subquery
from django.db.models.functions import Coalesce

from accounts.models import PreRegisteredStudent
from teams.models import (
    StudyGroup,
    StudyGroupSemester,
    TeamSemester,
    TeamSemesterMember,
)
from teams.repositories.team_lobby import TeamLobbyRepository


class MentorGroupsRepository:
    """Выборка учебных групп, где пользователь назначен наставником."""

    def __init__(self) -> None:
        self._team_lobby_repository = TeamLobbyRepository()

    def list_for_mentor(self, user_id: int, semester_id: int) -> QuerySet[StudyGroup]:
        """Группы наставника в семестре со счётчиками студентов и команд."""
        mentor_group_ids = StudyGroup.objects.filter(
            is_end=False,
            semester_enrollments__semester_id=semester_id,
            semester_enrollments__mentors__id=user_id,
        ).values("id")

        teams_count_subquery = (
            TeamSemester.objects.filter(
                team__home_study_group_id=OuterRef("pk"),
                semester_id=semester_id,
            )
            .values("team__home_study_group_id")
            .annotate(count=Count("pk"))
            .values("count")
        )

        return (
            StudyGroup.objects.filter(id__in=mentor_group_ids)
            .annotate(
                students_count=Count("pre_registered_students", distinct=True),
                teams_count=Coalesce(Subquery(teams_count_subquery), 0),
            )
            .only("id", "name")
            .order_by("name")
        )

    def is_mentor(self, user_id: int, group_id: int, semester_id: int) -> bool:
        """Возвращает True, если пользователь — наставник группы в семестре."""
        return StudyGroupSemester.objects.filter(
            study_group_id=group_id,
            semester_id=semester_id,
            mentors__id=user_id,
        ).exists()

    def get_group_header(self, group_id: int) -> StudyGroup | None:
        """Возвращает заголовок группы (id, name) или None."""
        return (
            StudyGroup.objects.filter(pk=group_id).only("id", "name", "is_end").first()
        )

    def list_students(
        self, group_id: int, semester_id: int
    ) -> list[PreRegisteredStudent]:
        """Контингент группы с командой студента в семестре (без N+1)."""
        students_qs = (
            PreRegisteredStudent.objects.filter(group_id=group_id)
            .select_related("student")
            .prefetch_related(
                Prefetch(
                    "student__team_semester_memberships",
                    queryset=TeamSemesterMember.objects.filter(
                        semester_id=semester_id
                    ).select_related("team_semester__team"),
                    to_attr="_team_membership_for_semester",
                )
            )
            .order_by("last_name", "first_name", "id")
        )
        return list(students_qs)

    def list_teams(self, group_id: int, semester_id: int) -> list[TeamSemester]:
        """Команды группы в семестре с числом участников (без N+1)."""
        return self._team_lobby_repository.list_group_team_semesters(
            group_id=group_id,
            semester_id=semester_id,
        )
