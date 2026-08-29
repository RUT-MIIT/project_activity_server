"""Репозиторий для StudyGroupSemester и связанных выборок."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Prefetch, QuerySet

from teams.models import StudyGroup, StudyGroupSemester

User = get_user_model()


class StudyGroupSemesterRepository:
    """Доступ к данным групп в семестре и сотрудников института."""

    def list_active_groups(self, institute_code: str) -> QuerySet[StudyGroup]:
        """Активные группы института."""
        return (
            StudyGroup.objects.filter(
                institute_id=institute_code,
                is_end=False,
            )
            .select_related("direction")
            .order_by("name")
        )

    def list_active_groups_with_mentors(
        self,
        institute_code: str,
        semester_id: int,
    ) -> QuerySet[StudyGroup]:
        """Активные группы с prefetch наставников в семестре."""
        semester_enrollment_qs = StudyGroupSemester.objects.filter(
            semester_id=semester_id
        ).prefetch_related(
            Prefetch(
                "mentors",
                queryset=User.objects.only("id").order_by("id"),
            )
        )
        return self.list_active_groups(institute_code).prefetch_related(
            Prefetch(
                "semester_enrollments",
                queryset=semester_enrollment_qs,
                to_attr="_semester_enrollments_for_semester",
            )
        )

    def get_group_by_id(self, group_id: int) -> StudyGroup | None:
        """Возвращает группу по ID или None."""
        return (
            StudyGroup.objects.filter(pk=group_id)
            .only("id", "institute_id", "is_end")
            .first()
        )

    def list_employees(self, department_ids: set[int]) -> QuerySet[User]:
        """Сотрудники института (не студенты, не админы, не staff)."""
        if not department_ids:
            return User.objects.none()
        return (
            User.objects.filter(department_id__in=department_ids)
            .exclude(role__code__in=("student", "admin"))
            .exclude(is_staff=True)
            .select_related("role")
            .order_by("last_name", "first_name", "id")
        )

    def get_employee_by_id(self, user_id: int, department_ids: set[int]) -> User | None:
        """Возвращает сотрудника института по ID."""
        return self.list_employees(department_ids).filter(pk=user_id).first()

    def get_or_create_enrollment(
        self,
        study_group_id: int,
        semester_id: int,
    ) -> StudyGroupSemester:
        """Возвращает или создаёт запись группы в семестре."""
        enrollment, _ = StudyGroupSemester.objects.get_or_create(
            study_group_id=study_group_id,
            semester_id=semester_id,
        )
        return enrollment

    def add_mentor(
        self,
        study_group_id: int,
        semester_id: int,
        mentor_id: int,
    ) -> list[int]:
        """Добавляет наставника группе в семестре; возвращает актуальные mentorIds."""
        enrollment = self.get_or_create_enrollment(study_group_id, semester_id)
        enrollment.mentors.add(mentor_id)
        return self.get_mentor_ids(study_group_id, semester_id)

    def remove_mentor(
        self,
        study_group_id: int,
        semester_id: int,
        mentor_id: int,
    ) -> list[int]:
        """Снимает наставника с группы в семестре; возвращает актуальные mentorIds."""
        enrollment = StudyGroupSemester.objects.filter(
            study_group_id=study_group_id,
            semester_id=semester_id,
        ).first()
        if enrollment is not None:
            enrollment.mentors.remove(mentor_id)
        return self.get_mentor_ids(study_group_id, semester_id)

    def get_mentor_ids(self, study_group_id: int, semester_id: int) -> list[int]:
        """Возвращает отсортированные ID наставников группы в семестре."""
        enrollment = StudyGroupSemester.objects.filter(
            study_group_id=study_group_id,
            semester_id=semester_id,
        ).first()
        if enrollment is None:
            return []
        return list(enrollment.mentors.order_by("id").values_list("id", flat=True))
