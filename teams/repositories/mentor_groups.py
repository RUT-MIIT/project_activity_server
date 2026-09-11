"""Репозиторий списка групп наставника в семестре."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import (
    Count,
    Exists,
    F,
    IntegerField,
    OuterRef,
    Q,
    QuerySet,
    Subquery,
)
from django.db.models.functions import Coalesce

from accounts.models import PreRegisteredStudent
from teams.domain.contingent_student import ContingentStudent
from teams.models import StudyGroup, StudyGroupSemester, TeamSemester
from teams.repositories.contingent_student import ContingentStudentRepository
from teams.repositories.team_lobby import TeamLobbyRepository

User = get_user_model()


class MentorGroupsRepository:
    """Выборка учебных групп, где пользователь назначен наставником."""

    def __init__(self) -> None:
        self._team_lobby_repository = TeamLobbyRepository()
        self._contingent_repository = ContingentStudentRepository()

    def _with_counts(
        self, queryset: QuerySet[StudyGroup], semester_id: int
    ) -> QuerySet[StudyGroup]:
        """Добавляет счётчики контингента, регистраций и команд в семестре."""
        teams_count_subquery = (
            TeamSemester.objects.filter(
                team__home_study_group_id=OuterRef("pk"),
                semester_id=semester_id,
            )
            .values("team__home_study_group_id")
            .annotate(count=Count("pk"))
            .values("count")
        )
        assembled_teams_count_subquery = (
            TeamSemester.objects.filter(
                team__home_study_group_id=OuterRef("pk"),
                semester_id=semester_id,
                status=TeamSemester.Status.ASSEMBLED,
            )
            .values("team__home_study_group_id")
            .annotate(count=Count("pk"))
            .values("count")
        )
        direct_students_subquery = (
            User.objects.filter(
                study_group_id=OuterRef("pk"),
                role_id="student",
                is_active=True,
                is_placeholder=False,
            )
            .annotate(
                _linked=Exists(
                    PreRegisteredStudent.objects.filter(
                        group_id=OuterRef("study_group_id"),
                        user_id=OuterRef("pk"),
                    )
                )
            )
            .filter(_linked=False)
            .values("study_group_id")
            .annotate(count=Count("pk"))
            .values("count")
        )
        pr_in_teams_subquery = (
            PreRegisteredStudent.objects.filter(
                group_id=OuterRef("pk"),
                role_id="student",
                user__team_semester_memberships__semester_id=semester_id,
            )
            .values("group_id")
            .annotate(count=Count("pk", distinct=True))
            .values("count")
        )
        direct_in_teams_subquery = (
            User.objects.filter(
                study_group_id=OuterRef("pk"),
                role_id="student",
                is_active=True,
                is_placeholder=False,
                team_semester_memberships__semester_id=semester_id,
            )
            .annotate(
                _linked=Exists(
                    PreRegisteredStudent.objects.filter(
                        group_id=OuterRef("study_group_id"),
                        user_id=OuterRef("pk"),
                    )
                )
            )
            .filter(_linked=False)
            .values("study_group_id")
            .annotate(count=Count("pk", distinct=True))
            .values("count")
        )

        return queryset.annotate(
            _pr_students_count=Count(
                "pre_registered_students",
                filter=Q(pre_registered_students__role_id="student"),
                distinct=True,
            ),
            _direct_students_count=Coalesce(
                Subquery(
                    direct_students_subquery[:1],
                    output_field=IntegerField(),
                ),
                0,
            ),
            _pr_registered_count=Count(
                "pre_registered_students",
                filter=Q(
                    pre_registered_students__role_id="student",
                    pre_registered_students__user_id__isnull=False,
                    pre_registered_students__has_placeholder_user=False,
                ),
                distinct=True,
            ),
            _pr_in_teams_count=Coalesce(
                Subquery(pr_in_teams_subquery[:1], output_field=IntegerField()),
                0,
            ),
            _direct_in_teams_count=Coalesce(
                Subquery(direct_in_teams_subquery[:1], output_field=IntegerField()),
                0,
            ),
            teams_count=Coalesce(Subquery(teams_count_subquery), 0),
            assembled_teams_count=Coalesce(Subquery(assembled_teams_count_subquery), 0),
        ).annotate(
            students_count=F("_pr_students_count") + F("_direct_students_count"),
            registered_students_count=F("_pr_registered_count")
            + F("_direct_students_count"),
            students_in_teams_count=F("_pr_in_teams_count")
            + F("_direct_in_teams_count"),
        )

    def list_for_mentor(self, user_id: int, semester_id: int) -> QuerySet[StudyGroup]:
        """Группы наставника в семестре со счётчиками студентов и команд."""
        mentor_group_ids = StudyGroup.objects.filter(
            is_end=False,
            semester_enrollments__semester_id=semester_id,
            semester_enrollments__mentors__id=user_id,
        ).values("id")

        return self._with_counts(
            StudyGroup.objects.filter(id__in=mentor_group_ids).only("id", "name"),
            semester_id,
        ).order_by("name")

    def list_for_institutes(
        self, institute_codes: list[str], semester_id: int
    ) -> QuerySet[StudyGroup]:
        """Активные группы институтов со счётчиками студентов и команд."""
        if not institute_codes:
            return StudyGroup.objects.none()

        return self._with_counts(
            StudyGroup.objects.filter(
                institute_id__in=institute_codes,
                is_end=False,
            ).only("id", "name"),
            semester_id,
        ).order_by("name")

    def is_mentor(self, user_id: int, group_id: int, semester_id: int) -> bool:
        """Возвращает True, если пользователь — наставник группы в семестре."""
        return StudyGroupSemester.objects.filter(
            study_group_id=group_id,
            semester_id=semester_id,
            mentors__id=user_id,
        ).exists()

    def list_mentor_institute_codes(self, user_id: int, semester_id: int) -> list[str]:
        """Уникальные коды институтов групп, где пользователь — наставник в семестре."""
        return list(
            StudyGroup.objects.filter(
                is_end=False,
                semester_enrollments__semester_id=semester_id,
                semester_enrollments__mentors__id=user_id,
            )
            .order_by("institute_id")
            .values_list("institute_id", flat=True)
            .distinct()
        )

    def get_group_header(self, group_id: int) -> StudyGroup | None:
        """Возвращает заголовок группы (id, name) или None."""
        return (
            StudyGroup.objects.filter(pk=group_id)
            .only("id", "name", "is_end", "institute_id")
            .first()
        )

    def list_students(self, group_id: int, semester_id: int) -> list[ContingentStudent]:
        """Контингент группы: предрегистрация и прямые студенты (без N+1)."""
        return self._contingent_repository.list_for_group(group_id, semester_id)

    def list_teams(self, group_id: int, semester_id: int) -> list[TeamSemester]:
        """Команды группы в семестре с числом участников (без N+1)."""
        return self._team_lobby_repository.list_group_team_semesters(
            group_id=group_id,
            semester_id=semester_id,
        )
