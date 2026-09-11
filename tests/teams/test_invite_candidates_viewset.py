"""Тесты GET /api/teams/my-team/invite-candidates/."""

from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import CaptureQueriesContext
import pytest
from rest_framework.test import APIClient

from accounts.models import (
    ACTIVE_SEMESTER_SETTING_CODE,
    PreRegisteredStudent,
    Semester,
    Settings,
)
from showcase.models import (
    ApplicationInvolvedDepartment,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
)
from teams.models import (
    Direction,
    StudyGroup,
    Team,
    TeamInvitation,
    TeamSemester,
    TeamSemesterMember,
)

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def semester(db):
    semester = Semester.objects.create(code="s1", name="S1", position=1)
    Settings.objects.update_or_create(
        code=ACTIVE_SEMESTER_SETTING_CODE,
        defaults={"value": semester.code, "description": ""},
    )
    return semester


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def invite_setup(
    roles, make_user, semester, direction, institute, statuses, departments
):
    admin = make_user(role_code="admin")
    group_a = StudyGroup.objects.create(
        name="GA",
        code="ga",
        direction=direction,
        institute=institute,
    )
    group_b = StudyGroup.objects.create(
        name="GB",
        code="gb",
        direction=direction,
        institute=institute,
    )
    group_out = StudyGroup.objects.create(
        name="OUT",
        code="out",
        direction=direction,
        institute=institute,
    )

    captain = make_user(role_code="student", email="cap@example.com")
    captain.last_name = "Капитанов"
    captain.first_name = "Кап"
    captain.study_group = group_a
    captain.save(update_fields=["last_name", "first_name", "study_group"])

    same_group = make_user(role_code="student", email="same@example.com")
    same_group.last_name = "Иванов"
    same_group.first_name = "Иван"
    same_group.middle_name = "Иванович"
    same_group.study_group = group_a
    same_group.save(
        update_fields=["last_name", "first_name", "middle_name", "study_group"]
    )

    other_group = make_user(role_code="student", email="other@example.com")
    other_group.last_name = "Иванова"
    other_group.first_name = "Мария"
    other_group.study_group = group_b
    other_group.save(update_fields=["last_name", "first_name", "study_group"])

    outside_track = make_user(role_code="student", email="out@example.com")
    outside_track.last_name = "Ивановский"
    outside_track.first_name = "Пётр"
    outside_track.study_group = group_out
    outside_track.save(update_fields=["last_name", "first_name", "study_group"])

    busy = make_user(role_code="student", email="busy@example.com")
    busy.last_name = "Иваненко"
    busy.first_name = "Busy"
    busy.study_group = group_b
    busy.save(update_fields=["last_name", "first_name", "study_group"])

    pre = PreRegisteredStudent.objects.create(
        last_name="Иванушкин",
        first_name="Незарег",
        middle_name="",
        personnel_number="PR-1",
        group=group_b,
        role_id="student",
    )

    app = ProjectApplication.objects.create(
        title="P",
        company="ООО",
        author_lastname="И",
        author_firstname="И",
        author_email="p@example.com",
        semester=semester,
        status=statuses["approved"],
        goal="Длинная цель проекта больше пятидесяти символов для валидации",
        problem_holder="Носитель",
        barrier="Длинный барьер больше пятидесяти символов для валидации",
        recommended_teams_count=5,
    )
    ApplicationInvolvedDepartment.objects.create(
        application=app, department=departments["child"]
    )
    track = ProjectTrack.objects.create(
        name="Трек",
        department=departments["child"],
        semester=semester,
        author=admin,
        min_team_members=2,
        max_team_members=5,
        recommended_teams_count=5,
    )
    ProjectTrackGroup.objects.create(project_track=track, study_group=group_a)
    ProjectTrackGroup.objects.create(project_track=track, study_group=group_b)
    ProjectTrackApplication.objects.create(project_track=track, project_application=app)

    team = Team.objects.create(name="Alpha", home_study_group=group_a)
    ts = TeamSemester.objects.create(
        team=team,
        semester=semester,
        project_track=track,
        captain=captain,
        status=TeamSemester.Status.FORMING,
    )
    TeamSemesterMember.objects.create(
        team_semester=ts,
        user=captain,
        role=TeamSemesterMember.Role.LEADER,
    )

    busy_team = Team.objects.create(name="BusyTeam", home_study_group=group_b)
    busy_ts = TeamSemester.objects.create(
        team=busy_team,
        semester=semester,
        project_track=track,
        captain=busy,
        status=TeamSemester.Status.FORMING,
    )
    TeamSemesterMember.objects.create(
        team_semester=busy_ts,
        user=busy,
        role=TeamSemesterMember.Role.LEADER,
    )

    return {
        "captain": captain,
        "same_group": same_group,
        "other_group": other_group,
        "outside_track": outside_track,
        "busy": busy,
        "pre": pre,
        "team_semester": ts,
        "track": track,
        "group_a": group_a,
        "group_b": group_b,
        "group_out": group_out,
        "semester": semester,
    }


@pytest.mark.django_db
class TestInviteCandidatesViewSet:
    def test_search_includes_other_group_of_track(self, api_client, invite_setup):
        api_client.force_authenticate(user=invite_setup["captain"])
        response = api_client.get(
            "/api/teams/my-team/invite-candidates/",
            {"q": "Ива"},
        )
        assert response.status_code == 200
        assert response.data["scope"] == "track"
        assert response.data["trackId"] == invite_setup["track"].id
        by_user = {
            item["user_id"]: item
            for item in response.data["results"]
            if item["user_id"] is not None
        }
        assert invite_setup["same_group"].id in by_user
        assert invite_setup["other_group"].id in by_user
        assert invite_setup["outside_track"].id not in by_user
        assert invite_setup["captain"].id not in by_user

        other = by_user[invite_setup["other_group"].id]
        assert other["isRegistered"] is True
        assert other["inTeam"] is False
        assert other["canInvite"] is True
        assert other["group"]["id"] == invite_setup["group_b"].id

    def test_preregistered_not_invitable(self, api_client, invite_setup):
        api_client.force_authenticate(user=invite_setup["captain"])
        response = api_client.get(
            "/api/teams/my-team/invite-candidates/",
            {"q": "Ивануш"},
        )
        assert response.status_code == 200
        results = response.data["results"]
        assert len(results) == 1
        item = results[0]
        assert item["id"] == invite_setup["pre"].id
        assert item["user_id"] is None
        assert item["isRegistered"] is False
        assert item["canInvite"] is False

    def test_busy_student_flagged(self, api_client, invite_setup):
        api_client.force_authenticate(user=invite_setup["captain"])
        response = api_client.get(
            "/api/teams/my-team/invite-candidates/",
            {"q": "Иванен"},
        )
        assert response.status_code == 200
        item = next(
            r
            for r in response.data["results"]
            if r["user_id"] == invite_setup["busy"].id
        )
        assert item["inTeam"] is True
        assert item["canInvite"] is False
        assert item["team"]["name"] == "BusyTeam"

    def test_pending_invitation_flagged(self, api_client, invite_setup):
        TeamInvitation.objects.create(
            team_semester=invite_setup["team_semester"],
            user=invite_setup["other_group"],
            invited_by=invite_setup["captain"],
            status=TeamInvitation.Status.PENDING,
        )
        api_client.force_authenticate(user=invite_setup["captain"])
        response = api_client.get(
            "/api/teams/my-team/invite-candidates/",
            {"q": "Иванова"},
        )
        assert response.status_code == 200
        item = next(
            r
            for r in response.data["results"]
            if r["user_id"] == invite_setup["other_group"].id
        )
        assert item["hasPendingInvitation"] is True
        assert item["canInvite"] is False

    def test_non_captain_forbidden(self, api_client, invite_setup):
        api_client.force_authenticate(user=invite_setup["same_group"])
        response = api_client.get(
            "/api/teams/my-team/invite-candidates/",
            {"q": "Ива"},
        )
        assert response.status_code in (400, 403)

    def test_short_query_rejected(self, api_client, invite_setup):
        api_client.force_authenticate(user=invite_setup["captain"])
        response = api_client.get(
            "/api/teams/my-team/invite-candidates/",
            {"q": "И"},
        )
        assert response.status_code == 400

    def test_search_cyrillic_case_insensitive(self, api_client, invite_setup):
        """Кириллица: нижний регистр запроса находит ФИО с заглавной (SQLite)."""
        api_client.force_authenticate(user=invite_setup["captain"])
        upper = api_client.get(
            "/api/teams/my-team/invite-candidates/",
            {"q": "Ива"},
        )
        lower = api_client.get(
            "/api/teams/my-team/invite-candidates/",
            {"q": "ива"},
        )
        assert upper.status_code == 200
        assert lower.status_code == 200
        upper_ids = {item["user_id"] for item in upper.data["results"]}
        lower_ids = {item["user_id"] for item in lower.data["results"]}
        assert invite_setup["same_group"].id in upper_ids
        assert invite_setup["same_group"].id in lower_ids
        assert invite_setup["other_group"].id in lower_ids

    def test_search_no_n_plus_one(self, api_client, invite_setup, roles):
        """Число SQL не растёт с числом кандидатов, в т.ч. уже состоящих в команде."""
        group_b = invite_setup["group_b"]
        role = roles["student"]
        track = invite_setup["track"]
        semester = invite_setup["semester"]
        for i in range(12):
            user = User.objects.create_user(
                email=f"ivanextra{i}@example.com",
                password="pass",
                first_name="Extra",
                last_name=f"ИвановExtra{i}",
                role=role,
                study_group=group_b,
            )
            team = Team.objects.create(name=f"ExtraTeam{i}", home_study_group=group_b)
            ts = TeamSemester.objects.create(
                team=team,
                semester=semester,
                project_track=track,
                captain=user,
            )
            TeamSemesterMember.objects.create(
                team_semester=ts,
                user=user,
                role=TeamSemesterMember.Role.LEADER,
            )

        api_client.force_authenticate(user=invite_setup["captain"])
        with CaptureQueriesContext(connection) as ctx_small:
            small = api_client.get(
                "/api/teams/my-team/invite-candidates/",
                {"q": "Ива", "limit": 5},
            )
        assert small.status_code == 200
        assert any(item["inTeam"] for item in small.data["results"])
        small_q = len(ctx_small.captured_queries)

        with CaptureQueriesContext(connection) as ctx_large:
            large = api_client.get(
                "/api/teams/my-team/invite-candidates/",
                {"q": "Ива", "limit": 20},
            )
        assert large.status_code == 200
        assert len(large.data["results"]) >= len(small.data["results"])
        assert sum(1 for item in large.data["results"] if item["inTeam"]) >= 5
        assert len(ctx_large.captured_queries) <= small_q + 2
        assert len(ctx_large.captured_queries) <= 15
