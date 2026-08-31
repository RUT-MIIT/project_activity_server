"""Назначение групп наставнику при регистрации по данным импорта ПД."""

from __future__ import annotations

from django.contrib.auth import get_user_model

from accounts.models import PreRegisteredStudent, Semester
from teams.domain.mentor_registration import build_mentor_registration_context
from teams.repositories.project_teacher import ProjectTeacherRepository
from teams.repositories.study_group_semester import StudyGroupSemesterRepository

User = get_user_model()


class MentorRegistrationService:
    """Оркестрация назначения групп наставнику из StudyGroupProjectTeacher."""

    def __init__(self) -> None:
        self._project_teacher_repository = ProjectTeacherRepository()
        self._study_group_semester_repository = StudyGroupSemesterRepository()

    def assign_groups_from_project_teachers(
        self,
        *,
        user: User,
        pre_registered: PreRegisteredStudent,
    ) -> int:
        """
        Назначает наставнику группы actual-семестра по импорту преподавателей ПД.

        Returns:
            Число уникальных учебных групп, назначенных наставнику.
        """
        if pre_registered.role_id != "mentor":
            return 0

        semester = Semester.get_active()
        if semester is None:
            return 0

        context = build_mentor_registration_context(pre_registered)
        assignments = self._project_teacher_repository.find_for_mentor(
            semester_id=semester.pk,
            personnel_number=context.personnel_number,
            full_name=context.full_name,
        )
        if not assignments.exists():
            return 0

        self._project_teacher_repository.link_tutor(assignments, user.pk)

        group_ids: set[int] = set()
        for assignment in assignments:
            group_id = assignment.study_group_id
            if group_id in group_ids:
                continue
            group_ids.add(group_id)
            self._study_group_semester_repository.add_mentor(
                study_group_id=group_id,
                semester_id=semester.pk,
                mentor_id=user.pk,
            )

        return len(group_ids)
