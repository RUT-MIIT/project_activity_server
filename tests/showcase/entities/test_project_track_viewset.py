"""Тесты ProjectTrackViewSet."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department, Semester
from showcase.models import (
    ApplicationInvolvedDepartment,
    Institute,
    ProjectApplication,
    ProjectTrack,
)
from teams.models import Direction, StudyGroup


@pytest.fixture
def semester(db):
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
    semester: Semester,
    statuses: dict,
    involved_department: Department | None = None,
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


@pytest.fixture
def track_setup(statuses, institute, other_institute, direction, semester, departments):
    own_group = StudyGroup.objects.create(
        name="Группа 1",
        code="g1",
        direction=direction,
        institute=institute,
    )
    other_group = StudyGroup.objects.create(
        name="Группа 2",
        code="g2",
        direction=direction,
        institute=other_institute,
    )
    own_app = _create_approved_app(
        semester=semester,
        statuses=statuses,
        involved_department=departments["child"],
    )
    other_child = Department.objects.create(
        name="Other Child",
        short_name="OC",
        parent=other_institute.department,
    )
    other_app = _create_approved_app(
        semester=semester,
        statuses=statuses,
        involved_department=other_child,
        title="Чужой",
    )
    track = ProjectTrack.objects.create(
        semester=semester,
        study_group=own_group,
        project_application=own_app,
    )
    return {
        "own_group": own_group,
        "other_group": other_group,
        "own_app": own_app,
        "other_app": other_app,
        "track": track,
    }


@pytest.mark.django_db
class TestProjectTrackViewSet:
    def test_list_unauthenticated_returns_401(self, institute, semester):
        client = APIClient()
        response = client.get(
            f"/api/showcase/project-tracks/?institute_code={institute.code}"
            f"&semester_id={semester.id}"
        )
        assert response.status_code == 401

    def test_list_user_returns_403(self, roles, make_user, institute, semester):
        user = make_user(role_code="user")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/?institute_code={institute.code}"
            f"&semester_id={semester.id}"
        )
        assert response.status_code == 403

    def test_list_missing_params_returns_400(
        self, roles, make_user, institute, semester
    ):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/api/showcase/project-tracks/")
        assert response.status_code == 400

    def test_list_admin_success(
        self, roles, make_user, institute, semester, track_setup
    ):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/?institute_code={institute.code}"
            f"&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data) == 1
        item = response.data[0]
        assert item["id"] == track_setup["track"].id
        assert item["group_id"] == track_setup["own_group"].id
        assert item["project_application_id"] == track_setup["own_app"].id

    def test_list_validator_own_institute(
        self, roles, make_user, institute, semester, track_setup
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/?institute_code={institute.code}"
            f"&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_post_creates_tracks(
        self, roles, make_user, institute, semester, direction, statuses, departments
    ):
        group = StudyGroup.objects.create(
            name="Новая",
            code="new",
            direction=direction,
            institute=institute,
        )
        app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=departments["child"],
        )
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            "/api/showcase/project-tracks/",
            {
                "semester_id": semester.id,
                "group_ids": [group.id],
                "project_application_ids": [app.id],
            },
            format="json",
        )
        assert response.status_code == 201
        assert response.data["created"] == 1
        assert response.data["skipped"] == 0

    def test_post_idempotent(self, roles, make_user, institute, semester, track_setup):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        payload = {
            "semester_id": semester.id,
            "group_ids": [track_setup["own_group"].id],
            "project_application_ids": [track_setup["own_app"].id],
        }
        response = client.post("/api/showcase/project-tracks/", payload, format="json")
        assert response.status_code == 201
        assert response.data["created"] == 0
        assert response.data["skipped"] == 1
        assert ProjectTrack.objects.count() == 1

    def test_post_validator_other_group_403(
        self, roles, make_user, institute, semester, track_setup
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            "/api/showcase/project-tracks/",
            {
                "semester_id": semester.id,
                "group_ids": [track_setup["other_group"].id],
                "project_application_ids": [track_setup["own_app"].id],
            },
            format="json",
        )
        assert response.status_code == 403

    def test_delete_success(self, roles, make_user, track_setup, semester):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        track_id = track_setup["track"].id
        response = client.delete(
            "/api/showcase/project-tracks/",
            {
                "semester_id": semester.id,
                "group_id": track_setup["own_group"].id,
                "project_application_id": track_setup["own_app"].id,
            },
            format="json",
        )
        assert response.status_code == 204
        assert not ProjectTrack.objects.filter(pk=track_id).exists()

    def test_delete_validator_other_track_403(
        self, roles, make_user, semester, statuses, other_institute, direction
    ):
        other_group = StudyGroup.objects.create(
            name="Чужая",
            code="og",
            direction=direction,
            institute=other_institute,
        )
        other_app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=Department.objects.create(
                name="Other Child",
                short_name="OC",
                parent=other_institute.department,
            ),
        )
        track = ProjectTrack.objects.create(
            semester=semester,
            study_group=other_group,
            project_application=other_app,
        )
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(
            "/api/showcase/project-tracks/",
            {
                "semester_id": semester.id,
                "group_id": other_group.id,
                "project_application_id": other_app.id,
            },
            format="json",
        )
        assert response.status_code == 403

    def test_delete_not_found(self, roles, make_user, semester):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(
            "/api/showcase/project-tracks/",
            {
                "semester_id": semester.id,
                "group_id": 99999,
                "project_application_id": 99999,
            },
            format="json",
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestProjectTrackGroupsViewSet:
    def test_list_groups_missing_semester_returns_400(
        self, roles, make_user, institute, semester
    ):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/?institute_code={institute.code}"
        )
        assert response.status_code == 400

    def test_list_groups_validator_without_institute_code(
        self, roles, make_user, institute, semester, direction, track_setup
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/?semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_list_groups_admin_without_institute_code_returns_400(
        self, roles, make_user, semester
    ):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/?semester_id={semester.id}"
        )
        assert response.status_code == 400
        assert "institute_code" in response.data["error"]

    def test_list_groups_admin_success(
        self, roles, make_user, institute, semester, direction, track_setup
    ):
        empty_group = StudyGroup.objects.create(
            name="Группа пустая",
            code="g-empty",
            direction=direction,
            institute=institute,
        )
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/?institute_code={institute.code}"
            f"&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data) == 2
        by_id = {item["id"]: item for item in response.data}
        assert by_id[track_setup["own_group"].id]["assigned_projects_count"] == 1
        assert by_id[empty_group.id]["assigned_projects_count"] == 0
        assert by_id[track_setup["own_group"].id]["direction"]["code"] == direction.code
        assert by_id[track_setup["own_group"].id]["course_number"] == 1

    def test_list_groups_validator_other_institute_403(
        self, roles, make_user, other_institute, semester, track_setup
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/?institute_code={other_institute.code}"
            f"&semester_id={semester.id}"
        )
        assert response.status_code == 403

    def test_retrieve_group_validator_without_institute_code(
        self, roles, make_user, institute, semester, track_setup
    ):
        track_setup["own_app"].print_number = "25-00001"
        track_setup["own_app"].save(update_fields=["print_number"])
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/{track_setup['own_group'].id}/"
            f"?semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert len(response.data["projects"]) == 1

    def test_retrieve_group_with_projects(
        self, roles, make_user, institute, semester, track_setup
    ):
        track_setup["own_app"].print_number = "25-00001"
        track_setup["own_app"].save(update_fields=["print_number"])
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/{track_setup['own_group'].id}/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert response.data["id"] == track_setup["own_group"].id
        assert response.data["direction"]["level"] == "бакалавриат"
        assert len(response.data["projects"]) == 1
        project = response.data["projects"][0]
        assert project["id"] == track_setup["own_app"].id
        assert project["title"] == track_setup["own_app"].title
        assert project["print_number"] == "25-00001"
        assert project["author_name"] == "Иванов Иван"

    def test_retrieve_group_empty_projects(
        self, roles, make_user, institute, semester, direction
    ):
        group = StudyGroup.objects.create(
            name="Без проектов",
            code="g0",
            direction=direction,
            institute=institute,
        )
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/{group.id}/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert response.data["projects"] == []

    def test_retrieve_group_wrong_institute_returns_404(
        self, roles, make_user, institute, other_institute, semester, track_setup
    ):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/groups/{track_setup['other_group'].id}/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )
        assert response.status_code == 404

    def test_statistics_validator_without_institute_code(
        self, roles, make_user, institute, semester, track_setup
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/statistics/?semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert response.data["total_projects"] == 1

    def test_statistics_admin_success(
        self,
        roles,
        make_user,
        institute,
        semester,
        direction,
        statuses,
        departments,
        track_setup,
    ):
        StudyGroup.objects.create(
            name="Группа без проектов",
            code="g-empty",
            direction=direction,
            institute=institute,
        )
        extra_app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=departments["child"],
            title="Второй проект",
        )
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            f"/api/showcase/project-tracks/statistics/?institute_code={institute.code}"
            f"&semester_id={semester.id}"
        )
        assert response.status_code == 200
        assert response.data["total_projects"] == 2
        assert response.data["distributed_projects"] == 1
        assert response.data["average_projects_per_group"] == 0.5
        assert response.data["groups_without_projects"] == 1

    def test_statistics_missing_params_returns_400(
        self, roles, make_user, institute, semester
    ):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/api/showcase/project-tracks/statistics/")
        assert response.status_code == 400
