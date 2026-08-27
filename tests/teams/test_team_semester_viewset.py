"""Тесты API TeamSemester."""

import pytest
from rest_framework.test import APIClient

from accounts.models import ACTIVE_SEMESTER_SETTING_CODE, Semester, Settings
from teams.models import Direction, StudyGroup, Team, TeamSemester, TeamSemesterMember


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def study_group(direction, institute):
    return StudyGroup.objects.create(
        name="G1",
        code="g1",
        direction=direction,
        institute=institute,
    )


@pytest.fixture
def semester(db):
    semester = Semester.objects.create(code="s1", name="Семестр 1", position=1)
    Settings.objects.update_or_create(
        code=ACTIVE_SEMESTER_SETTING_CODE,
        defaults={"value": semester.code, "description": ""},
    )
    return semester


@pytest.mark.django_db
class TestTeamSemesterViewSet:
    def test_create_team_and_semester_adds_captain_member(
        self, api_client, roles, make_user, study_group, semester
    ):
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)

        team_resp = api_client.post(
            "/api/teams/teams/",
            {"name": "Alpha", "home_study_group_id": study_group.id},
            format="json",
        )
        assert team_resp.status_code == 201
        team_id = team_resp.data["id"]

        ts_resp = api_client.post(
            "/api/teams/team-semesters/",
            {"team_id": team_id, "semester_id": semester.id},
            format="json",
        )
        assert ts_resp.status_code == 201
        assert ts_resp.data["captain"]["id"] == user.id
        assert len(ts_resp.data["members"]) == 1
        assert ts_resp.data["members"][0]["role"] == "leader"

    def test_add_and_remove_member(
        self, api_client, roles, make_user, study_group, semester
    ):
        captain = make_user(role_code="student", email="cap@example.com")
        member_user = make_user(role_code="student", email="mem@example.com")
        team = Team.objects.create(name="Alpha", home_study_group=study_group)
        team_semester = TeamSemester.objects.create(
            team=team, semester=semester, captain=captain
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=captain,
            role=TeamSemesterMember.Role.LEADER,
        )
        api_client.force_authenticate(user=captain)

        add_resp = api_client.post(
            f"/api/teams/team-semesters/{team_semester.id}/members/",
            {"user_id": member_user.id, "role": "member"},
            format="json",
        )
        assert add_resp.status_code == 201
        member_id = add_resp.data["id"]

        del_resp = api_client.delete(
            f"/api/teams/team-semesters/{team_semester.id}/members/{member_id}/"
        )
        assert del_resp.status_code == 204

    def test_non_captain_cannot_add_member(
        self, api_client, roles, make_user, study_group, semester
    ):
        captain = make_user(role_code="student", email="cap@example.com")
        other = make_user(role_code="student", email="other@example.com")
        team = Team.objects.create(name="Alpha")
        team_semester = TeamSemester.objects.create(
            team=team, semester=semester, captain=captain
        )
        api_client.force_authenticate(user=other)

        response = api_client.post(
            f"/api/teams/team-semesters/{team_semester.id}/members/",
            {"user_id": other.id, "role": "member"},
            format="json",
        )
        assert response.status_code == 403

    def test_my_requires_semester_id(self, api_client, roles, make_user):
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/teams/team-semesters/my/")
        assert response.status_code == 400

    def test_my_returns_user_team_semester(
        self, api_client, roles, make_user, study_group, semester
    ):
        user = make_user(role_code="student")
        team = Team.objects.create(name="Alpha", home_study_group=study_group)
        team_semester = TeamSemester.objects.create(
            team=team, semester=semester, captain=user
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=user,
            role=TeamSemesterMember.Role.LEADER,
        )
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/teams/teams/my/", {"semester_id": "actual"})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == team_semester.id
        assert response.data[0]["team"]["name"] == "Alpha"
