"""Тесты GET /api/teams/study-groups/my-groups/."""

from __future__ import annotations

from django.db import connection
from django.test.utils import CaptureQueriesContext
import pytest
from rest_framework.test import APIClient

from accounts.models import PreRegisteredStudent, Semester
from teams.dto.mentor_groups import MentorGroupListDTO
from teams.models import Direction, StudyGroup, StudyGroupSemester, Team, TeamSemester
from teams.repositories.mentor_groups import MentorGroupsRepository

MY_GROUPS_URL = "/api/teams/study-groups/my-groups/"


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
def study_groups(direction, institute) -> dict[str, StudyGroup]:
    return {
        "first": StudyGroup.objects.create(
            name="ИВТ-101",
            code="IVT-101",
            direction=direction,
            institute=institute,
            is_end=False,
        ),
        "second": StudyGroup.objects.create(
            name="ИВТ-102",
            code="IVT-102",
            direction=direction,
            institute=institute,
            is_end=False,
        ),
        "foreign": StudyGroup.objects.create(
            name="ИВТ-999",
            code="IVT-999",
            direction=direction,
            institute=institute,
            is_end=False,
        ),
    }


@pytest.mark.django_db
class TestMentorGroupsViewSet:
    def test_unauthenticated_returns_401(self, api_client: APIClient) -> None:
        response = api_client.get(f"{MY_GROUPS_URL}?semester_id=1")
        assert response.status_code == 401

    def test_missing_semester_id_returns_400(
        self, api_client: APIClient, roles, make_user
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        api_client.force_authenticate(user=mentor)

        response = api_client.get(MY_GROUPS_URL)

        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_returns_only_mentor_groups_in_semester(
        self,
        api_client: APIClient,
        roles,
        make_user,
        semester,
        study_groups,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        other_mentor = make_user(
            role_code="mentor", with_department=True, email="other@x.com"
        )
        _enrollment_with_mentors(study_groups["first"], semester, mentor)
        _enrollment_with_mentors(study_groups["second"], semester, mentor)
        _enrollment_with_mentors(study_groups["foreign"], semester, other_mentor)

        api_client.force_authenticate(user=mentor)
        response = api_client.get(f"{MY_GROUPS_URL}?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert ids == {study_groups["first"].id, study_groups["second"].id}

    def test_excludes_ended_groups(
        self,
        api_client: APIClient,
        roles,
        make_user,
        semester,
        study_groups,
        direction,
        institute,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        ended_group = StudyGroup.objects.create(
            name="ИВТ-103",
            code="IVT-103",
            direction=direction,
            institute=institute,
            is_end=True,
        )
        _enrollment_with_mentors(study_groups["first"], semester, mentor)
        _enrollment_with_mentors(ended_group, semester, mentor)

        api_client.force_authenticate(user=mentor)
        response = api_client.get(f"{MY_GROUPS_URL}?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert ended_group.id not in ids
        assert study_groups["first"].id in ids

    def test_counts_students_and_teams(
        self,
        api_client: APIClient,
        roles,
        make_user,
        semester,
        study_groups,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        group = study_groups["first"]
        _enrollment_with_mentors(group, semester, mentor)

        for index in range(3):
            PreRegisteredStudent.objects.create(
                last_name=f"Фамилия{index}",
                first_name=f"Имя{index}",
                student_card=f"SC{index}",
                snils=f"1234567890{index}",
                personnel_number=f"PN{index}",
                group=group,
            )

        team_one = Team.objects.create(name="Alpha", home_study_group=group)
        team_two = Team.objects.create(name="Beta", home_study_group=group)
        TeamSemester.objects.create(team=team_one, semester=semester, captain=mentor)
        TeamSemester.objects.create(team=team_two, semester=semester, captain=mentor)

        other_group_team = Team.objects.create(
            name="Other", home_study_group=study_groups["second"]
        )
        TeamSemester.objects.create(
            team=other_group_team, semester=semester, captain=mentor
        )

        api_client.force_authenticate(user=mentor)
        response = api_client.get(f"{MY_GROUPS_URL}?semester_id={semester.id}")

        assert response.status_code == 200
        item = next(row for row in response.data if row["id"] == group.id)
        assert item["name"] == group.name
        assert item["studentsCount"] == 3
        assert item["teamsCount"] == 2

    def test_other_semester_assignment_not_listed(
        self,
        api_client: APIClient,
        roles,
        make_user,
        semester,
        study_groups,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        other_semester = Semester.objects.create(
            code="other", name="Other", position=99
        )
        _enrollment_with_mentors(study_groups["first"], semester, mentor)
        _enrollment_with_mentors(study_groups["first"], other_semester)

        api_client.force_authenticate(user=mentor)
        response = api_client.get(f"{MY_GROUPS_URL}?semester_id={other_semester.id}")

        assert response.status_code == 200
        assert response.data == []

    def test_non_mentor_gets_empty_list(
        self,
        api_client: APIClient,
        roles,
        make_user,
        semester,
        study_groups,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        viewer = make_user(role_code="user", with_department=True, email="viewer@x.com")
        _enrollment_with_mentors(study_groups["first"], semester, mentor)

        api_client.force_authenticate(user=viewer)
        response = api_client.get(f"{MY_GROUPS_URL}?semester_id={semester.id}")

        assert response.status_code == 200
        assert response.data == []

    def test_institute_validator_gets_empty_list_without_mentor_assignment(
        self,
        api_client: APIClient,
        roles,
        make_user,
        semester,
        study_groups,
        direction,
        institute,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        validator = make_user(
            role_code="institute_validator",
            with_department=True,
            email="validator@x.com",
        )
        StudyGroup.objects.create(
            name="ИВТ-103",
            code="IVT-103",
            direction=direction,
            institute=institute,
            is_end=False,
        )
        _enrollment_with_mentors(study_groups["first"], semester, mentor)

        api_client.force_authenticate(user=validator)
        response = api_client.get(f"{MY_GROUPS_URL}?semester_id={semester.id}")

        assert response.status_code == 200
        assert response.data == []


@pytest.mark.django_db
class TestMentorGroupsQueryPerformance:
    def _create_groups(
        self,
        direction: Direction,
        institute,
        count: int,
        *,
        prefix: str,
    ) -> list[StudyGroup]:
        return [
            StudyGroup.objects.create(
                name=f"{prefix}-{index}",
                code=f"{prefix}-{index}",
                direction=direction,
                institute=institute,
                is_end=False,
            )
            for index in range(count)
        ]

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
        groups = self._create_groups(direction, institute, 8, prefix="perf")
        for group in groups:
            _enrollment_with_mentors(group, semester, mentor)

        repository = MentorGroupsRepository()
        loaded = list(repository.list_for_mentor(mentor.id, semester.id))

        with django_assert_num_queries(0):
            payload = MentorGroupListDTO(loaded).to_list()

        assert len(payload) == 8
        assert all("teamsCount" in item for item in payload)

    def test_list_query_count_does_not_scale_with_groups(
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

        small_groups = self._create_groups(direction, institute, 3, prefix="small")
        for group in small_groups:
            _enrollment_with_mentors(group, semester, mentor)

        with CaptureQueriesContext(connection) as small_ctx:
            response = api_client.get(f"{MY_GROUPS_URL}?semester_id={semester.id}")
        assert response.status_code == 200
        small_count = len(small_ctx.captured_queries)

        large_groups = self._create_groups(direction, institute, 12, prefix="large")
        for group in large_groups:
            _enrollment_with_mentors(group, semester, mentor)

        with CaptureQueriesContext(connection) as large_ctx:
            response = api_client.get(f"{MY_GROUPS_URL}?semester_id={semester.id}")
        assert response.status_code == 200
        large_count = len(large_ctx.captured_queries)

        assert large_count == small_count
