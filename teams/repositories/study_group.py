"""Репозиторий для учебных групп."""

from django.contrib.auth import get_user_model
from django.db.models import (
    Count,
    Exists,
    F,
    IntegerField,
    OuterRef,
    Prefetch,
    Q,
    QuerySet,
    Subquery,
)
from django.db.models.functions import Coalesce

from accounts.models import PreRegisteredStudent
from teams.domain.contingent_student import ContingentStudent
from teams.models import StudyGroup, StudyGroupSemester
from teams.repositories.contingent_student import ContingentStudentRepository

User = get_user_model()


class StudyGroupRepository:
    """Доступ к данным StudyGroup."""

    def __init__(self) -> None:
        self._contingent_repository = ContingentStudentRepository()

    def _with_students_count(
        self, queryset: QuerySet[StudyGroup]
    ) -> QuerySet[StudyGroup]:
        """Добавляет students_count с учётом прямых студентов."""
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
        ).annotate(
            students_count=F("_pr_students_count") + F("_direct_students_count"),
        )

    def get_all(self) -> QuerySet[StudyGroup]:
        return self._with_students_count(
            StudyGroup.objects.select_related("direction", "institute")
        ).all()

    def get_by_id(self, group_id: int) -> StudyGroup:
        return self._with_students_count(
            StudyGroup.objects.select_related("direction", "institute", "mentor")
        ).get(pk=group_id)

    def get_my_group_detail(
        self, group_id: int, semester_id: int | None = None
    ) -> StudyGroup:
        """Группа с наставником без N+1 (контингент — отдельно через list_group_contingent)."""
        group_qs = StudyGroup.objects.select_related(
            "direction",
            "institute",
            "mentor",
            "mentor__role",
        )
        if semester_id is not None:
            group_qs = group_qs.prefetch_related(
                Prefetch(
                    "semester_enrollments",
                    queryset=StudyGroupSemester.objects.filter(
                        semester_id=semester_id
                    ).prefetch_related(
                        Prefetch(
                            "mentors",
                            queryset=User.objects.select_related("role"),
                        )
                    ),
                    to_attr="_semester_enrollments_for_semester",
                )
            )
        return group_qs.get(pk=group_id)

    def list_group_contingent(
        self, group_id: int, semester_id: int | None = None
    ) -> list[ContingentStudent]:
        """Контингент группы: предрегистрация и прямые студенты."""
        return self._contingent_repository.list_for_group(group_id, semester_id)
