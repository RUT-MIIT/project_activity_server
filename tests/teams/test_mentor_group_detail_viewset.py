"""Тесты GET /api/teams/study-groups/{id}/mentor-detail/."""

from __future__ import annotations

from django.db import connection
from django.test.utils import CaptureQueriesContext
import pytest
from rest_framework.test import APIClient

from accounts.models import PreRegisteredStudent, Semester
from teams.dto.mentor_groups import MentorGroupDetailDTO
from teams.models import (
    Direction,
    StudyGroup,
    StudyGroupSemester,
    Team,
    TeamSemester,
    TeamSemesterMember,
)
from teams.repositories.mentor_groups import MentorGroupsRepository


def _detail_url(group_id: int) -> str:
    return f"/api/teams/study-groups/{group_id}/mentor-detail/"


def _enrollment_with_mentors(
    group: StudyGroup, semester: Semester, *mentors
) -> StudyGroupSemester:
    enrollment = StudyGroupSemester.objects.create(
        study_group=group,
        semester=semester,
    )
    if mentors:
        enrollment.mentors.set(mentors)
    return enrollment


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def semester(db) -> Semester:
    return Semester.objects.create(code="s1", name="Семестр 1", position=1)


@pytest.fixture
def direction(db) -> Direction:
    return Direction.objects.create(
        code="09.03.01",
        name="Информатика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def study_group(direction, institute) -> StudyGroup:
    return StudyGroup.objects.create(
        name="ИВТ-101",
        code="IVT-101",
        direction=direction,
        institute=institute,
        is_end=False,
    )


@pytest.mark.django_db
class TestMentorGroupDetailViewSet:
    def test_unauthenticated_returns_401(
        self, api_client: APIClient, study_group: StudyGroup, semester: Semester
    ) -> None:
        response = api_client.get(
            f"{_detail_url(study_group.id)}?semester_id={semester.id}"
        )
        assert response.status_code == 401

    def test_missing_semester_id_returns_400(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        api_client.force_authenticate(user=mentor)

        response = api_client.get(_detail_url(study_group.id))

        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_group_not_found_returns_404(
        self,
        api_client: APIClient,
        roles,
        make_user,
        semester: Semester,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        api_client.force_authenticate(user=mentor)

        response = api_client.get(f"{_detail_url(99999)}?semester_id={semester.id}")

        assert response.status_code == 404

    def test_not_mentor_returns_403(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
        semester: Semester,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        viewer = make_user(role_code="user", with_department=True, email="viewer@x.com")
        _enrollment_with_mentors(study_group, semester, mentor)

        api_client.force_authenticate(user=viewer)
        response = api_client.get(
            f"{_detail_url(study_group.id)}?semester_id={semester.id}"
        )

        assert response.status_code == 403

    def test_institute_validator_can_access_without_mentor_assignment(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
        semester: Semester,
    ) -> None:
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{_detail_url(study_group.id)}?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert response.data["id"] == study_group.id

    def test_ended_group_returns_403(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
        semester: Semester,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        study_group.is_end = True
        study_group.save(update_fields=["is_end"])
        _enrollment_with_mentors(study_group, semester, mentor)

        api_client.force_authenticate(user=mentor)
        response = api_client.get(
            f"{_detail_url(study_group.id)}?semester_id={semester.id}"
        )

        assert response.status_code == 403
        assert "завершила обучение" in response.data["error"]

    def test_success_returns_students_and_teams(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
        semester: Semester,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        _enrollment_with_mentors(study_group, semester, mentor)

        registered = make_user(role_code="student", email="ivan@example.com")
        registered.study_group = study_group
        registered.save(update_fields=["study_group"])
        PreRegisteredStudent.objects.create(
            last_name="Иванов",
            first_name="Иван",
            middle_name="Иванович",
            student_card="25010001",
            snils="11111111111",
            personnel_number="100001",
            group=study_group,
            user=registered,
        )
        PreRegisteredStudent.objects.create(
            last_name="Петров",
            first_name="Пётр",
            student_card="25010002",
            snils="22222222222",
            personnel_number="100002",
            group=study_group,
        )

        team = Team.objects.create(name="Alpha", home_study_group=study_group)
        team_semester = TeamSemester.objects.create(
            team=team,
            semester=semester,
            captain=registered,
            status=TeamSemester.Status.FORMING,
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=registered,
            semester=semester,
            role=TeamSemesterMember.Role.LEADER,
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=make_user(role_code="student", email="member@example.com"),
            semester=semester,
            role=TeamSemesterMember.Role.MEMBER,
        )

        api_client.force_authenticate(user=mentor)
        response = api_client.get(
            f"{_detail_url(study_group.id)}?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert response.data["id"] == study_group.id
        assert response.data["name"] == study_group.name

        registered_student = next(
            item for item in response.data["students"] if item["lastName"] == "Иванов"
        )
        assert registered_student["isRegistered"] is True
        assert registered_student["userId"] == registered.id
        assert registered_student["team"] == {
            "id": team_semester.id,
            "name": "Alpha",
            "role": TeamSemesterMember.Role.LEADER,
        }

        unregistered_student = next(
            item for item in response.data["students"] if item["lastName"] == "Петров"
        )
        assert unregistered_student["isRegistered"] is False
        assert unregistered_student["userId"] is None
        assert unregistered_student["team"] is None

        assert len(response.data["teams"]) == 1
        team_item = response.data["teams"][0]
        assert team_item["id"] == team_semester.id
        assert team_item["name"] == "Alpha"
        assert team_item["status"] == TeamSemester.Status.FORMING
        assert team_item["membersCount"] == 2


@pytest.mark.django_db
class TestMentorGroupDetailQueryPerformance:
    def test_dto_serialization_has_no_extra_queries(
        self,
        roles,
        make_user,
        semester,
        direction,
        institute,
        django_assert_num_queries,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        group = StudyGroup.objects.create(
            name="perf-group",
            code="perf",
            direction=direction,
            institute=institute,
            is_end=False,
        )
        _enrollment_with_mentors(group, semester, mentor)

        for index in range(8):
            PreRegisteredStudent.objects.create(
                last_name=f"Фамилия{index}",
                first_name=f"Имя{index}",
                student_card=f"SC{index}",
                snils=f"1234567890{index}",
                personnel_number=f"PN{index}",
                group=group,
            )

        for index in range(4):
            team = Team.objects.create(
                name=f"Team-{index}",
                home_study_group=group,
            )
            TeamSemester.objects.create(
                team=team,
                semester=semester,
                captain=mentor,
            )

        repository = MentorGroupsRepository()
        header = repository.get_group_header(group.id)
        students = repository.list_students(group.id, semester.id)
        teams = repository.list_teams(group.id, semester.id)

        with django_assert_num_queries(0):
            payload = MentorGroupDetailDTO(header, students, teams).to_dict()

        assert len(payload["students"]) == 8
        assert len(payload["teams"]) == 4

    def test_detail_query_count_does_not_scale_with_students_and_teams(
        self,
        roles,
        make_user,
        api_client,
        semester,
        direction,
        institute,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        api_client.force_authenticate(user=mentor)

        small_group = StudyGroup.objects.create(
            name="small",
            code="small",
            direction=direction,
            institute=institute,
            is_end=False,
        )
        _enrollment_with_mentors(small_group, semester, mentor)
        for index in range(3):
            PreRegisteredStudent.objects.create(
                last_name=f"S{index}",
                first_name="A",
                student_card=f"S{index}",
                snils=f"1000000000{index}",
                personnel_number=f"S{index}",
                group=small_group,
            )
        for index in range(2):
            team = Team.objects.create(
                name=f"S-Team-{index}", home_study_group=small_group
            )
            TeamSemester.objects.create(team=team, semester=semester, captain=mentor)

        with CaptureQueriesContext(connection) as small_ctx:
            response = api_client.get(
                f"{_detail_url(small_group.id)}?semester_id={semester.id}"
            )
        assert response.status_code == 200
        small_count = len(small_ctx.captured_queries)

        large_group = StudyGroup.objects.create(
            name="large",
            code="large",
            direction=direction,
            institute=institute,
            is_end=False,
        )
        _enrollment_with_mentors(large_group, semester, mentor)
        for index in range(15):
            PreRegisteredStudent.objects.create(
                last_name=f"L{index}",
                first_name="B",
                student_card=f"L{index}",
                snils=f"2000000000{index}",
                personnel_number=f"L{index}",
                group=large_group,
            )
        for index in range(12):
            team = Team.objects.create(
                name=f"L-Team-{index}", home_study_group=large_group
            )
            TeamSemester.objects.create(team=team, semester=semester, captain=mentor)

        with CaptureQueriesContext(connection) as large_ctx:
            response = api_client.get(
                f"{_detail_url(large_group.id)}?semester_id={semester.id}"
            )
        assert response.status_code == 200
        large_count = len(large_ctx.captured_queries)

        assert large_count == small_count
