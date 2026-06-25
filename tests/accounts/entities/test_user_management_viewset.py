"""Тесты UserManagementViewSet."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department, Semester
from showcase.models import ProjectApplication


@pytest.mark.django_db
class TestUserManagementViewSet:
    def test_list_unauthenticated_returns_401(self):
        client = APIClient()
        response = client.get("/api/accounts/users/")
        assert response.status_code == 401

    def test_list_regular_user_returns_403(self, make_user):
        user = make_user(role_code="user")
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/api/accounts/users/")
        assert response.status_code == 403

    def test_list_admin_returns_users(self, make_user, roles):
        admin = make_user(role_code="admin")
        target = make_user(role_code="user", email="listed@example.com")
        client = APIClient()
        client.force_authenticate(user=admin)

        response = client.get("/api/accounts/users/")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert target.id in ids
        assert admin.id not in ids
        item = next(x for x in response.data if x["id"] == target.id)
        assert item["full_name"] == target.get_full_name()
        assert item["email"] == target.email
        assert item["role"]["code"] == "user"
        assert "authored_projects_count" in item
        assert "authored_projects" not in item

    def test_list_with_authored_projects(self, make_user, statuses):
        admin = make_user(role_code="admin")
        author = make_user(role_code="user", email="author3@example.com")
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        ProjectApplication.objects.create(
            title="Мой проект",
            company="ООО",
            author=author,
            author_lastname=author.last_name,
            author_firstname=author.first_name,
            author_email=author.email,
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )

        client = APIClient()
        client.force_authenticate(user=admin)
        response = client.get("/api/accounts/users/?include_authored_projects=true")

        assert response.status_code == 200
        item = next(x for x in response.data if x["id"] == author.id)
        assert item["authored_projects_count"] == 1
        assert len(item["authored_projects"]) == 1
        assert item["authored_projects"][0]["title"] == "Мой проект"
        assert item["authored_projects"][0]["status"]["code"] == "approved"

    def test_patch_role_and_department(self, make_user, roles, departments):
        admin = make_user(role_code="admin")
        target = make_user(role_code="user", email="patch@example.com")
        client = APIClient()
        client.force_authenticate(user=admin)

        response = client.patch(
            f"/api/accounts/users/{target.id}/",
            {"role": "department_validator", "department_id": departments["child"].id},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["role"]["code"] == "department_validator"
        assert response.data["department"]["id"] == departments["child"].id

    def test_patch_validator_returns_403(self, make_user, departments):
        validator = make_user(role_code="institute_validator", with_department=True)
        target = make_user(role_code="user", email="patch2@example.com")
        client = APIClient()
        client.force_authenticate(user=validator)

        response = client.patch(
            f"/api/accounts/users/{target.id}/",
            {"role": "mentor"},
            format="json",
        )

        assert response.status_code == 403

    def test_patch_assign_admin_role_returns_400(self, make_user):
        admin = make_user(role_code="admin")
        target = make_user(role_code="user", email="patch3@example.com")
        client = APIClient()
        client.force_authenticate(user=admin)

        response = client.patch(
            f"/api/accounts/users/{target.id}/",
            {"role": "admin"},
            format="json",
        )

        assert response.status_code == 400
        assert "администратора" in response.data["error"]

    def test_patch_email_and_phone(self, make_user):
        admin = make_user(role_code="admin")
        target = make_user(role_code="user", email="old@example.com")
        target.phone = "+79990000001"
        target.save(update_fields=["phone"])
        client = APIClient()
        client.force_authenticate(user=admin)

        response = client.patch(
            f"/api/accounts/users/{target.id}/",
            {"email": "new@example.com", "phone": "+79991112233"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["email"] == "new@example.com"
        assert response.data["phone"] == "+79991112233"
        target.refresh_from_db()
        assert target.email == "new@example.com"
        assert target.phone == "+79991112233"

    def test_patch_duplicate_email_returns_400(self, make_user):
        admin = make_user(role_code="admin")
        make_user(role_code="user", email="taken@example.com")
        target = make_user(role_code="user", email="patch4@example.com")
        client = APIClient()
        client.force_authenticate(user=admin)

        response = client.patch(
            f"/api/accounts/users/{target.id}/",
            {"email": "taken@example.com"},
            format="json",
        )

        assert response.status_code == 400
        assert "email" in response.data

    def test_validator_sees_only_institute_users(
        self, make_user, departments, institute
    ):
        validator = make_user(
            role_code="institute_validator",
            with_department=True,
            email="validator2@example.com",
        )
        own_user = make_user(
            role_code="user",
            with_department=True,
            email="own2@example.com",
        )

        other_parent = Department.objects.create(name="Foreign Root", short_name="FR")
        other_child = Department.objects.create(
            name="Foreign Child", short_name="FC", parent=other_parent
        )
        foreign_user = make_user(role_code="user", email="foreign2@example.com")
        foreign_user.department = other_child
        foreign_user.save(update_fields=["department"])

        client = APIClient()
        client.force_authenticate(user=validator)
        response = client.get("/api/accounts/users/")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert own_user.id in ids
        assert foreign_user.id not in ids
