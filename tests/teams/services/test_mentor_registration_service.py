"""Тесты сервиса назначения групп наставнику при регистрации."""

from __future__ import annotations

import pytest

from accounts.models import PreRegisteredStudent, Semester, Settings
from teams.models import (
    Direction,
    StudyGroup,
    StudyGroupProjectTeacher,
    StudyGroupSemester,
)
from teams.services.mentor_registration_service import MentorRegistrationService


@pytest.fixture
def active_semester(db) -> Semester:
    semester = Semester.objects.create(
        code="26-27-1",
        name="Осень 26/27",
        position=1,
    )
    Settings.objects.update_or_create(
        code="active_semester_code",
        defaults={"description": "Active", "value": semester.code},
    )
    return semester


@pytest.fixture
def direction(db) -> Direction:
    return Direction.objects.create(
        code="26.05.06",
        name="Эксплуатация судов",
        level=Direction.Level.SPECIALITET,
    )


@pytest.fixture
def study_groups(direction, institute) -> dict[str, StudyGroup]:
    return {
        "first": StudyGroup.objects.create(
            name="ВГТ-111",
            code="ВГТ-2025-11",
            direction=direction,
            institute=institute,
        ),
        "second": StudyGroup.objects.create(
            name="ВГТ-112",
            code="ВГТ-2025-12",
            direction=direction,
            institute=institute,
        ),
    }


@pytest.fixture
def mentor_user(make_user, roles):
    user = make_user(role_code="mentor", with_department=True)
    user.first_name = "Маргарита"
    user.last_name = "Ишханян"
    user.middle_name = "Владимировна"
    user.save(update_fields=["first_name", "last_name", "middle_name"])
    return user


@pytest.fixture
def pre_registered_mentor(departments) -> PreRegisteredStudent:
    return PreRegisteredStudent.objects.create(
        last_name="Ишханян",
        first_name="Маргарита",
        middle_name="Владимировна",
        personnel_number="1347607",
        role_id="mentor",
        department=departments["child"],
    )


@pytest.fixture
def pre_registered_student(study_groups, departments) -> PreRegisteredStudent:
    return PreRegisteredStudent.objects.create(
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович",
        personnel_number="1000001",
        student_card="25011884",
        role_id="student",
        group=study_groups["first"],
        department=departments["child"],
    )


@pytest.mark.django_db
class TestMentorRegistrationService:
    def test_assigns_groups_by_personnel_number(
        self,
        active_semester: Semester,
        study_groups: dict[str, StudyGroup],
        mentor_user,
        pre_registered_mentor: PreRegisteredStudent,
    ) -> None:
        StudyGroupProjectTeacher.objects.create(
            semester=active_semester,
            study_group=study_groups["first"],
            mentor_full_name="Ишханян Маргарита Владимировна",
            external_teacher_id="1347607",
        )
        StudyGroupProjectTeacher.objects.create(
            semester=active_semester,
            study_group=study_groups["second"],
            mentor_full_name="Ишханян Маргарита Владимировна",
            external_teacher_id="1347607",
        )

        assigned = MentorRegistrationService().assign_groups_from_project_teachers(
            user=mentor_user,
            pre_registered=pre_registered_mentor,
        )

        assert assigned == 2
        assert StudyGroupProjectTeacher.objects.filter(tutor=mentor_user).count() == 2
        for group in study_groups.values():
            enrollment = StudyGroupSemester.objects.get(
                study_group=group,
                semester=active_semester,
            )
            assert list(enrollment.mentors.values_list("id", flat=True)) == [
                mentor_user.pk
            ]

    def test_fallback_assigns_groups_by_full_name(
        self,
        active_semester: Semester,
        study_groups: dict[str, StudyGroup],
        mentor_user,
        pre_registered_mentor: PreRegisteredStudent,
    ) -> None:
        StudyGroupProjectTeacher.objects.create(
            semester=active_semester,
            study_group=study_groups["first"],
            mentor_full_name="Ишханян Маргарита Владимировна",
            external_teacher_id="9999999",
        )

        assigned = MentorRegistrationService().assign_groups_from_project_teachers(
            user=mentor_user,
            pre_registered=pre_registered_mentor,
        )

        assert assigned == 1
        assignment = StudyGroupProjectTeacher.objects.get(
            study_group=study_groups["first"],
        )
        assert assignment.tutor_id == mentor_user.pk

    def test_returns_zero_without_active_semester(
        self,
        study_groups: dict[str, StudyGroup],
        mentor_user,
        pre_registered_mentor: PreRegisteredStudent,
    ) -> None:
        semester = Semester.objects.create(code="tmp", name="Tmp", position=99)
        StudyGroupProjectTeacher.objects.create(
            semester=semester,
            study_group=study_groups["first"],
            mentor_full_name="Ишханян Маргарита Владимировна",
            external_teacher_id="1347607",
        )

        assigned = MentorRegistrationService().assign_groups_from_project_teachers(
            user=mentor_user,
            pre_registered=pre_registered_mentor,
        )

        assert assigned == 0
        assert StudyGroupSemester.objects.count() == 0

    def test_returns_zero_when_no_assignments(
        self,
        active_semester: Semester,
        mentor_user,
        pre_registered_mentor: PreRegisteredStudent,
    ) -> None:
        assigned = MentorRegistrationService().assign_groups_from_project_teachers(
            user=mentor_user,
            pre_registered=pre_registered_mentor,
        )

        assert assigned == 0

    def test_skips_non_mentor_role(
        self,
        active_semester: Semester,
        study_groups: dict[str, StudyGroup],
        mentor_user,
        pre_registered_student: PreRegisteredStudent,
    ) -> None:
        StudyGroupProjectTeacher.objects.create(
            semester=active_semester,
            study_group=study_groups["first"],
            mentor_full_name="Иванов Иван Иванович",
            external_teacher_id="111",
        )

        assigned = MentorRegistrationService().assign_groups_from_project_teachers(
            user=mentor_user,
            pre_registered=pre_registered_student,
        )

        assert assigned == 0
