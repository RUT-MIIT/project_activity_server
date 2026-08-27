"""Ограничения доступа роли student к staff-сущностям."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Semester
from showcase.models import ProjectApplication

APPLICATION_PAYLOAD = {
    "company": "Test Company",
    "title": "Test Project",
    "company_contacts": "Контакты представителя",
    "existing_solutions": "Описание существующих решений",
    "author_lastname": "Иванов",
    "author_firstname": "Иван",
    "author_email": "test@example.com",
    "author_phone": "+79990000000",
    "goal": "Длинная цель проекта, больше 50 символов для консультации",
    "problem_holder": "Носитель проблемы",
    "barrier": "Длинное описание барьера",
    "project_level": "L1",
}


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestStudentBlockedFromStaffApi:
    def test_student_cannot_create_application(
        self, api_client, roles, make_user, statuses
    ):
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)

        response = api_client.post(
            "/api/showcase/project-applications/", APPLICATION_PAYLOAD, format="json"
        )

        assert response.status_code == 403

    def test_public_simple_create_still_allowed(self, api_client, statuses):
        response = api_client.post(
            "/api/showcase/project-applications/simple/",
            APPLICATION_PAYLOAD,
            format="json",
        )

        assert response.status_code == 201
        assert response.data["is_external"] is True

    def test_student_cannot_list_applications(self, api_client, roles, make_user):
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/showcase/project-applications/")

        assert response.status_code == 403

    def test_student_cannot_list_external_applications(
        self, api_client, roles, make_user
    ):
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/showcase/project-applications/external/")

        assert response.status_code == 403

    def test_student_cannot_comment_on_application(
        self, api_client, roles, make_user, statuses
    ):
        author = make_user(role_code="user", email="author@example.com")
        app = ProjectApplication.objects.create(
            title="App",
            company="Acme",
            author=author,
            status=statuses["await_department"],
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="author@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )
        student = make_user(role_code="student", email="st@example.com")
        api_client.force_authenticate(user=student)

        response = api_client.post(
            f"/api/showcase/project-applications/{app.id}/add_comment/",
            {"field": "goal", "text": "Комментарий"},
            format="json",
        )
        comments = api_client.get(
            f"/api/showcase/project-applications/{app.id}/comments/"
        )

        assert response.status_code == 403
        assert comments.status_code == 403

    def test_student_cannot_manage_department_plans(
        self, api_client, roles, make_user, departments
    ):
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)
        semester = Semester.objects.create(code="s1", name="S1", position=1)

        created = api_client.post(
            "/api/showcase/department-plans/",
            {
                "department_id": departments["parent"].id,
                "semester_id": semester.id,
                "plan": 10,
            },
            format="json",
        )
        listed = api_client.get(
            f"/api/showcase/department-plans/?semester_id={semester.id}"
        )
        my_plan = api_client.get(
            f"/api/showcase/department-plans/my-department-plan/?semester_id={semester.id}"
        )

        assert created.status_code == 403
        assert listed.status_code == 403
        assert my_plan.status_code == 403

    def test_student_cannot_list_project_tracks(self, api_client, roles, make_user):
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/showcase/project-tracks/?semester_id=actual")

        assert response.status_code == 403

    def test_student_cannot_list_projects(self, api_client, roles, make_user):
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/showcase/projects/")

        assert response.status_code == 403


@pytest.mark.django_db
class TestApplicationCommentAccess:
    def test_stranger_cannot_comment_on_foreign_application(
        self, api_client, roles, make_user, statuses
    ):
        author = make_user(role_code="user", email="author@example.com")
        stranger = make_user(role_code="user", email="stranger@example.com")
        app = ProjectApplication.objects.create(
            title="App",
            company="Acme",
            author=author,
            status=statuses["await_department"],
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="author@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )
        api_client.force_authenticate(user=stranger)

        response = api_client.post(
            f"/api/showcase/project-applications/{app.id}/add_comment/",
            {"field": "goal", "text": "Чужой комментарий"},
            format="json",
        )
        comments = api_client.get(
            f"/api/showcase/project-applications/{app.id}/comments/"
        )

        assert response.status_code == 403
        assert comments.status_code == 403

    def test_author_can_comment_on_own_application(
        self, api_client, roles, make_user, statuses
    ):
        author = make_user(role_code="user", email="author@example.com")
        app = ProjectApplication.objects.create(
            title="App",
            company="Acme",
            author=author,
            status=statuses["await_department"],
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="author@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )
        api_client.force_authenticate(user=author)

        response = api_client.post(
            f"/api/showcase/project-applications/{app.id}/add_comment/",
            {"field": "goal", "text": "Уточнение"},
            format="json",
        )

        assert response.status_code == 201
        assert response.data["text"] == "Уточнение"


@pytest.mark.django_db
class TestApplicationDestroyDisabled:
    def test_delete_returns_405(self, api_client, roles, make_user, statuses):
        author = make_user(role_code="admin")
        app = ProjectApplication.objects.create(
            title="App",
            company="Acme",
            author=author,
            status=statuses["approved"],
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="admin@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )
        api_client.force_authenticate(user=author)

        response = api_client.delete(f"/api/showcase/project-applications/{app.id}/")

        assert response.status_code == 405
        assert ProjectApplication.objects.filter(pk=app.id).exists()
