"""Тесты ProjectTrackViewSet."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department
from showcase.models import (
    ApplicationInvolvedDepartment,
    Institute,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
)
from teams.models import Direction, StudyGroup


@pytest.fixture
def semester(db):
    from accounts.models import Semester

    return Semester.objects.create(code="s1", name="S1", position=1)


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def other_institute(departments):
    other_dept = Department.objects.create(name="Other Parent", short_name="OP")
    return Institute.objects.create(
        code="OTHER",
        name="Other Institute",
        position=2,
        department=other_dept,
    )


def _create_approved_app(
    *,
    semester,
    statuses,
    involved_department=None,
    title: str = "Проект",
) -> ProjectApplication:
    app = ProjectApplication.objects.create(
        title=title,
        company="ООО Тест",
        author_lastname="Иванов",
        author_firstname="Иван",
        author_email="ivan@example.com",
        semester=semester,
        status=statuses["approved"],
        goal="Длинная цель проекта больше пятидесяти символов для валидации",
        problem_holder="Носитель",
        barrier="Длинный барьер больше пятидесяти символов для валидации",
    )
    if involved_department is not None:
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=involved_department,
        )
    return app


def _create_track_with_links(
    *,
    name: str,
    semester,
    department,
    author,
    group,
    application,
) -> ProjectTrack:
    track = ProjectTrack.objects.create(
        name=name,
        description="",
        department=department,
        semester=semester,
        author=author,
        recommended_teams_count=application.recommended_teams_count,
    )
    ProjectTrackGroup.objects.create(project_track=track, study_group=group)
    ProjectTrackApplication.objects.create(
        project_track=track,
        project_application=application,
    )
    return track


@pytest.fixture
def track_setup(statuses, institute, direction, semester, departments, make_user):
    admin = make_user(role_code="admin")
    own_group = StudyGroup.objects.create(
        name="Группа 1",
        code="g1",
        direction=direction,
        institute=institute,
    )
    own_app = _create_approved_app(
        semester=semester,
        statuses=statuses,
        involved_department=departments["child"],
    )
    track = _create_track_with_links(
        name="Трек 1",
        semester=semester,
        department=departments["child"],
        author=admin,
        group=own_group,
        application=own_app,
    )
    return {
        "admin": admin,
        "own_group": own_group,
        "own_app": own_app,
        "track": track,
    }


@pytest.mark.django_db
class TestProjectTrackViewSet:
    def test_list_unauthenticated_returns_401(self, semester):
        client = APIClient()
        response = client.get(
            f"/api/showcase/project-tracks/?semester_id={semester.id}"
        )
        assert response.status_code == 401

    def test_list_user_returns_403(self, roles, make_user, semester):
        user = make_user(role_code="user")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/?semester_id={semester.id}"
        )
        assert response.status_code == 403

    def test_list_missing_semester_returns_400(self, roles, make_user):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/api/showcase/project-tracks/")
        assert response.status_code == 400

    def test_list_admin_success(self, roles, make_user, semester, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/?semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Трек 1"
        assert len(response.data[0]["groups"]) == 1
        assert len(response.data[0]["applications"]) == 1

    def test_create_track(self, roles, make_user, semester, departments):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            "/api/showcase/project-tracks/",
            {
                "name": "Новый трек",
                "department_id": departments["child"].id,
                "semester_id": semester.id,
            },
            format="json",
        )
        assert response.status_code == 201
        assert response.data["name"] == "Новый трек"
        assert response.data["minTeamMembers"] == 4
        assert response.data["maxTeamMembers"] == 7

    def test_create_track_with_team_limits(
        self, roles, make_user, semester, departments
    ):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            "/api/showcase/project-tracks/",
            {
                "name": "Трек с лимитами",
                "department_id": departments["child"].id,
                "semester_id": semester.id,
                "minTeamMembers": 3,
                "maxTeamMembers": 7,
            },
            format="json",
        )
        assert response.status_code == 201
        assert response.data["minTeamMembers"] == 3
        assert response.data["maxTeamMembers"] == 7
        track = ProjectTrack.objects.get(pk=response.data["id"])
        assert track.min_team_members == 3
        assert track.max_team_members == 7

    def test_retrieve_track(self, roles, make_user, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/{track_setup['track'].id}/"
        )
        assert response.status_code == 200
        assert len(response.data["groups"]) == 1
        assert len(response.data["applications"]) == 1
        assert "minTeamMembers" in response.data
        assert "maxTeamMembers" in response.data

    def test_partial_update_track(self, roles, make_user, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.patch(
            f"/api/showcase/project-tracks/{track_setup['track'].id}/",
            {"name": "Обновлённый"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["name"] == "Обновлённый"

    def test_partial_update_track_application_team_limits(
        self, roles, make_user, track_setup
    ):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.patch(
            f"/api/showcase/project-tracks/{track_setup['track'].id}/",
            {
                "minTeamMembers": 2,
                "maxTeamMembers": 6,
            },
            format="json",
        )
        assert response.status_code == 200
        assert response.data["minTeamMembers"] == 2
        assert response.data["maxTeamMembers"] == 6
        app_item = response.data["applications"][0]
        assert app_item["minTeamMembers"] == 2
        assert app_item["maxTeamMembers"] == 6
        track_setup["own_app"].refresh_from_db()
        assert track_setup["own_app"].min_team_members == 2
        assert track_setup["own_app"].max_team_members == 6
        track_setup["track"].refresh_from_db()
        assert track_setup["track"].min_team_members == 2
        assert track_setup["track"].max_team_members == 6

    def test_destroy_track(self, roles, make_user, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(
            f"/api/showcase/project-tracks/{track_setup['track'].id}/"
        )
        assert response.status_code == 204
        assert not ProjectTrack.objects.filter(pk=track_setup["track"].id).exists()

    def test_add_groups(self, roles, make_user, institute, direction, track_setup):
        group = StudyGroup.objects.create(
            name="Г2",
            code="g2",
            direction=direction,
            institute=institute,
        )
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            f"/api/showcase/project-tracks/{track_setup['track'].id}/groups/",
            {"group_ids": [group.id]},
            format="json",
        )
        assert response.status_code == 200
        assert len(response.data["groups"]) == 2

    def test_remove_group(self, roles, make_user, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(
            f"/api/showcase/project-tracks/{track_setup['track'].id}/"
            f"groups/{track_setup['own_group'].id}/"
        )
        assert response.status_code == 200
        assert response.data["groups"] == []

    def test_add_applications(
        self, roles, make_user, semester, statuses, departments, track_setup
    ):
        app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=departments["child"],
            title="Второй",
        )
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            f"/api/showcase/project-tracks/{track_setup['track'].id}/applications/",
            [
                {
                    "id": app.id,
                    "teamsCount": 4,
                    "minTeamMembers": 2,
                    "maxTeamMembers": 6,
                }
            ],
            format="json",
        )
        assert response.status_code == 200
        assert len(response.data["applications"]) == 2
        added = next(
            item for item in response.data["applications"] if item["id"] == app.id
        )
        assert added["teamsCount"] == 4
        assert added["minTeamMembers"] == 2
        assert added["maxTeamMembers"] == 6
        app.refresh_from_db()
        assert app.recommended_teams_count == 4
        assert app.min_team_members == 2
        assert app.max_team_members == 6
        track_setup["track"].refresh_from_db()
        # own_app default 3 + new app 4
        assert track_setup["track"].recommended_teams_count == 7
        assert response.data["recommendedTeamsCount"] == 7

    def test_remove_application(self, roles, make_user, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(
            f"/api/showcase/project-tracks/{track_setup['track'].id}/"
            f"applications/{track_setup['own_app'].id}/"
        )
        assert response.status_code == 200
        assert response.data["applications"] == []
        track_setup["track"].refresh_from_db()
        assert track_setup["track"].recommended_teams_count == 0
        assert response.data["recommendedTeamsCount"] == 0


@pytest.mark.django_db
class TestProjectTrackGroupsViewSet:
    def test_list_groups(self, roles, make_user, institute, semester, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["assigned_projects_count"] == 1

    def test_retrieve_group(self, roles, make_user, institute, semester, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/{track_setup['own_group'].id}/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data["projects"]) == 1


@pytest.mark.django_db
class TestProjectTrackProjectsViewSet:
    def test_list_projects(self, roles, make_user, institute, semester, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/projects/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["assigned_groups_count"] == 1

    def test_retrieve_project(self, roles, make_user, institute, semester, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/projects/{track_setup['own_app'].id}/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data["groups"]) == 1


@pytest.mark.django_db
class TestProjectTrackStatisticsViewSet:
    def test_statistics(self, roles, make_user, institute, semester, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/statistics/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert response.data["distributed_projects"] == 1
