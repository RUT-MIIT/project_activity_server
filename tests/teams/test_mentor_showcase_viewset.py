"""Тесты GET /api/teams/study-groups/{id}/project-showcase/."""

from __future__ import annotations

from django.db import connection
from django.test.utils import CaptureQueriesContext
import pytest
from rest_framework.test import APIClient

from accounts.models import ACTIVE_SEMESTER_SETTING_CODE, Semester, Settings
from showcase.models import (
    ApplicationInvolvedDepartment,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
    Tag,
)
from teams.models import (
    Direction,
    StudyGroup,
    StudyGroupSemester,
    Team,
    TeamSemester,
    TeamSemesterMember,
)

BASE = "/api/showcase/student-showcase"


def _showcase_url(group_id: int) -> str:
    return f"/api/teams/study-groups/{group_id}/project-showcase/"


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


def _approved_app(
    *,
    semester,
    statuses,
    departments,
    title="Проект",
    teams=3,
    min_members=2,
    max_members=5,
    company="ООО Заказчик",
):
    app = ProjectApplication.objects.create(
        title=title,
        company=company,
        company_contacts="secret@example.com",
        author_lastname="Иванов",
        author_firstname="Иван",
        author_email="a@example.com",
        author_phone="+79990000000",
        semester=semester,
        status=statuses["approved"],
        goal="Цель",
        barrier="Барьер",
        existing_solutions="Решения",
        context="Контекст",
        project_level="L1",
        problem_holder="Носитель",
        recommended_teams_count=teams,
        min_team_members=min_members,
        max_team_members=max_members,
    )
    ApplicationInvolvedDepartment.objects.create(
        application=app, department=departments["child"]
    )
    return app


def _track(*, name, semester, department, author, group, applications):
    total = sum(app.recommended_teams_count for app in applications)
    track = ProjectTrack.objects.create(
        name=name,
        description=f"Описание {name}",
        department=department,
        semester=semester,
        author=author,
        min_team_members=2,
        max_team_members=5,
        recommended_teams_count=total,
    )
    ProjectTrackGroup.objects.create(project_track=track, study_group=group)
    for app in applications:
        ProjectTrackApplication.objects.create(
            project_track=track, project_application=app
        )
    return track


def _create_assembled_team(*, group, semester, track, captain, name, members=None):
    team = Team.objects.create(name=name, home_study_group=group)
    ts = TeamSemester.objects.create(
        team=team,
        semester=semester,
        project_track=track,
        captain=captain,
        status=TeamSemester.Status.ASSEMBLED,
    )
    TeamSemesterMember.objects.create(
        team_semester=ts,
        user=captain,
        role=TeamSemesterMember.Role.LEADER,
    )
    for member in members or []:
        TeamSemesterMember.objects.create(
            team_semester=ts,
            user=member,
            role=TeamSemesterMember.Role.MEMBER,
        )
    return ts


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def semester(db) -> Semester:
    semester = Semester.objects.create(code="s1", name="S1", position=1)
    Settings.objects.update_or_create(
        code=ACTIVE_SEMESTER_SETTING_CODE,
        defaults={"value": semester.code, "description": ""},
    )
    return semester


@pytest.fixture
def direction(db) -> Direction:
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def study_group(direction, institute) -> StudyGroup:
    return StudyGroup.objects.create(
        name="G1",
        code="g1",
        direction=direction,
        institute=institute,
    )


@pytest.fixture
def mentor_showcase_setup(
    roles, make_user, semester, study_group, statuses, departments
):
    admin = make_user(role_code="admin")
    mentor = make_user(role_code="mentor", with_department=True)
    captain = make_user(role_code="student", email="cap@example.com")
    captain.study_group = study_group
    captain.save(update_fields=["study_group"])
    member = make_user(role_code="student", email="mem@example.com")
    member.study_group = study_group
    member.save(update_fields=["study_group"])

    _enrollment_with_mentors(study_group, semester, mentor)

    tag = Tag.objects.create(name="AI", category="Tech")
    app1 = _approved_app(
        semester=semester,
        statuses=statuses,
        departments=departments,
        title="A1",
        teams=2,
    )
    app1.tags.add(tag)
    app2 = _approved_app(
        semester=semester,
        statuses=statuses,
        departments=departments,
        title="A2",
        teams=1,
    )
    track1 = _track(
        name="Трек 1",
        semester=semester,
        department=departments["child"],
        author=admin,
        group=study_group,
        applications=[app1, app2],
    )
    app3 = _approved_app(
        semester=semester,
        statuses=statuses,
        departments=departments,
        title="A3",
        teams=4,
    )
    track2 = _track(
        name="Трек 2",
        semester=semester,
        department=departments["child"],
        author=admin,
        group=study_group,
        applications=[app3],
    )

    return {
        "mentor": mentor,
        "captain": captain,
        "member": member,
        "group": study_group,
        "semester": semester,
        "track1": track1,
        "track2": track2,
        "app1": app1,
        "app2": app2,
        "app3": app3,
        "tag": tag,
        "departments": departments,
        "statuses": statuses,
        "admin": admin,
    }


@pytest.mark.django_db
class TestMentorShowcaseViewSet:
    def test_unauthenticated_returns_401(
        self, api_client: APIClient, mentor_showcase_setup
    ) -> None:
        group = mentor_showcase_setup["group"]
        semester = mentor_showcase_setup["semester"]
        response = api_client.get(
            f"{_showcase_url(group.id)}?semester_id={semester.id}"
        )
        assert response.status_code == 401

    def test_missing_semester_id_returns_400(
        self, api_client: APIClient, roles, make_user, mentor_showcase_setup
    ) -> None:
        mentor = mentor_showcase_setup["mentor"]
        api_client.force_authenticate(user=mentor)
        response = api_client.get(_showcase_url(mentor_showcase_setup["group"].id))
        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_group_not_found_returns_404(
        self, api_client: APIClient, mentor_showcase_setup
    ) -> None:
        mentor = mentor_showcase_setup["mentor"]
        api_client.force_authenticate(user=mentor)
        response = api_client.get(
            f"{_showcase_url(99999)}?semester_id={mentor_showcase_setup['semester'].id}"
        )
        assert response.status_code == 404

    def test_not_mentor_returns_403(
        self, api_client: APIClient, roles, make_user, mentor_showcase_setup
    ) -> None:
        viewer = make_user(role_code="user", with_department=True, email="viewer@x.com")
        api_client.force_authenticate(user=viewer)
        group = mentor_showcase_setup["group"]
        semester = mentor_showcase_setup["semester"]
        response = api_client.get(
            f"{_showcase_url(group.id)}?semester_id={semester.id}"
        )
        assert response.status_code == 403

    def test_institute_validator_can_access_without_mentor_assignment(
        self, api_client: APIClient, roles, make_user, mentor_showcase_setup
    ) -> None:
        validator = make_user(
            role_code="institute_validator",
            with_department=True,
            email="validator@x.com",
        )
        api_client.force_authenticate(user=validator)
        group = mentor_showcase_setup["group"]
        semester = mentor_showcase_setup["semester"]

        response = api_client.get(
            f"{_showcase_url(group.id)}?semester_id={semester.id}"
        )

        assert response.status_code == 200
        tracks = {t["id"]: t for t in response.data}
        assert mentor_showcase_setup["track1"].id in tracks
        assert mentor_showcase_setup["app1"].id in {
            p["id"] for p in tracks[mentor_showcase_setup["track1"].id]["projects"]
        }

    def test_mentor_can_retrieve_project_application_from_group_track(
        self, api_client: APIClient, mentor_showcase_setup
    ) -> None:
        mentor = mentor_showcase_setup["mentor"]
        app = mentor_showcase_setup["app1"]
        api_client.force_authenticate(user=mentor)

        response = api_client.get(f"/api/showcase/project-applications/{app.id}/")

        assert response.status_code == 200
        assert response.data["id"] == app.id

    def test_unrelated_mentor_cannot_retrieve_project_application(
        self, api_client: APIClient, roles, make_user, mentor_showcase_setup
    ) -> None:
        other_mentor = make_user(
            role_code="mentor", with_department=True, email="other@x.com"
        )
        app = mentor_showcase_setup["app1"]
        api_client.force_authenticate(user=other_mentor)

        response = api_client.get(f"/api/showcase/project-applications/{app.id}/")

        assert response.status_code == 403

    def test_lists_tracks_with_same_fields_as_student_showcase(
        self, api_client: APIClient, mentor_showcase_setup
    ) -> None:
        mentor = mentor_showcase_setup["mentor"]
        api_client.force_authenticate(user=mentor)
        group = mentor_showcase_setup["group"]
        semester = mentor_showcase_setup["semester"]

        response = api_client.get(
            f"{_showcase_url(group.id)}?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert response["Cache-Control"] == "private, max-age=30"
        tracks = {t["id"]: t for t in response.data}
        assert mentor_showcase_setup["track1"].id in tracks
        assert mentor_showcase_setup["track2"].id in tracks
        assert len(tracks) == 2
        assert tracks[mentor_showcase_setup["track1"].id]["name"] == "Трек 1"
        assert (
            tracks[mentor_showcase_setup["track1"].id]["description"]
            == "Описание Трек 1"
        )
        projects = {
            p["id"]: p for p in tracks[mentor_showcase_setup["track1"].id]["projects"]
        }
        assert projects[mentor_showcase_setup["app1"].id]["title"] == "A1"
        assert projects[mentor_showcase_setup["app1"].id]["company"] == "ООО Заказчик"
        assert projects[mentor_showcase_setup["app1"].id]["maxTeams"] == 2
        assert projects[mentor_showcase_setup["app1"].id]["enrolledTeamsCount"] == 0
        assert projects[mentor_showcase_setup["app1"].id]["minTeamMembers"] == 2
        assert projects[mentor_showcase_setup["app1"].id]["maxTeamMembers"] == 5
        assert projects[mentor_showcase_setup["app1"].id]["tags"] == [
            {
                "id": mentor_showcase_setup["tag"].id,
                "name": "AI",
                "category": "Tech",
            }
        ]

    def test_enrolled_teams_count(
        self, api_client: APIClient, mentor_showcase_setup
    ) -> None:
        setup = mentor_showcase_setup
        _create_assembled_team(
            group=setup["group"],
            semester=setup["semester"],
            track=setup["track1"],
            captain=setup["captain"],
            name="Alpha",
            members=[setup["member"]],
        )
        ts = TeamSemester.objects.get(captain=setup["captain"])
        ts.project_application = setup["app1"]
        ts.save(update_fields=["project_application"])

        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.get(
            f"{_showcase_url(setup['group'].id)}?semester_id={setup['semester'].id}"
        )
        assert response.status_code == 200
        tracks = {t["id"]: t for t in response.data}
        projects = {p["id"]: p for p in tracks[setup["track1"].id]["projects"]}
        assert projects[setup["app1"].id]["enrolledTeamsCount"] == 1
        assert projects[setup["app2"].id]["enrolledTeamsCount"] == 0

    def test_matches_student_showcase_for_same_group(
        self, api_client: APIClient, mentor_showcase_setup
    ) -> None:
        setup = mentor_showcase_setup
        api_client.force_authenticate(user=setup["mentor"])
        mentor_response = api_client.get(
            f"{_showcase_url(setup['group'].id)}?semester_id={setup['semester'].id}"
        )
        api_client.force_authenticate(user=setup["captain"])
        student_response = api_client.get(f"{BASE}/?semester_id={setup['semester'].id}")
        assert mentor_response.status_code == 200
        assert student_response.status_code == 200
        assert mentor_response.data == student_response.data


@pytest.mark.django_db
class TestMentorShowcaseQueryPerformance:
    def test_list_query_count_stable(
        self, api_client: APIClient, mentor_showcase_setup
    ) -> None:
        setup = mentor_showcase_setup
        api_client.force_authenticate(user=setup["mentor"])
        url = f"{_showcase_url(setup['group'].id)}?semester_id={setup['semester'].id}"

        with CaptureQueriesContext(connection) as ctx_small:
            response_small = api_client.get(url)
        assert response_small.status_code == 200
        queries_small = len(ctx_small.captured_queries)

        extra_apps = [
            _approved_app(
                semester=setup["semester"],
                statuses=setup["statuses"],
                departments=setup["departments"],
                title=f"Extra{i}",
                teams=1,
            )
            for i in range(5)
        ]
        for app in extra_apps:
            ProjectTrackApplication.objects.create(
                project_track=setup["track1"],
                project_application=app,
            )

        with CaptureQueriesContext(connection) as ctx_large:
            response_large = api_client.get(url)
        assert response_large.status_code == 200
        queries_large = len(ctx_large.captured_queries)
        assert queries_large <= queries_small + 1
