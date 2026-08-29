"""Репозиторий для учебных групп."""

from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch, QuerySet

from accounts.models import PreRegisteredStudent
from teams.models import StudyGroup, StudyGroupSemester, TeamSemesterMember

User = get_user_model()


class StudyGroupRepository:
    """Доступ к данным StudyGroup."""

    def get_all(self) -> QuerySet[StudyGroup]:
        return (
            StudyGroup.objects.select_related("direction", "institute")
            .annotate(students_count=Count("pre_registered_students", distinct=True))
            .all()
        )

    def get_by_id(self, group_id: int) -> StudyGroup:
        return (
            StudyGroup.objects.select_related("direction", "institute", "mentor")
            .annotate(students_count=Count("pre_registered_students", distinct=True))
            .get(pk=group_id)
        )

    def get_my_group_detail(
        self, group_id: int, semester_id: int | None = None
    ) -> StudyGroup:
        """Группа с наставником и контингентом без N+1."""
        students_qs = PreRegisteredStudent.objects.select_related("student").order_by(
            "last_name", "first_name"
        )
        if semester_id is not None:
            students_qs = students_qs.prefetch_related(
                Prefetch(
                    "student__team_semester_memberships",
                    queryset=TeamSemesterMember.objects.filter(
                        semester_id=semester_id
                    ).select_related("team_semester__team"),
                    to_attr="_team_membership_for_semester",
                )
            )
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
        return group_qs.prefetch_related(
            Prefetch("pre_registered_students", queryset=students_qs)
        ).get(pk=group_id)
