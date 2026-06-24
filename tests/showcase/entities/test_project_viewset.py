"""Тесты ProjectViewSet."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department, Semester
from showcase.models import (
    ApplicationInvolvedDepartment,
    Institute,
    ProjectApplication,
    Tag,
)


def _create_approved_app(
    *,
    semester: Semester,
    statuses: dict,
    institute: Institute,
    title: str = "Проект",
    author_lastname: str = "Иванов",
    author_firstname: str = "Иван",
    author_email: str = "ivan@example.com",
    print_number: str = "25-00001",
) -> ProjectApplication:
    app = ProjectApplication.objects.create(
        title=title,
        company="ООО Тест",
        author_lastname=author_lastname,
        author_firstname=author_firstname,
        author_email=author_email,
        semester=semester,
        status=statuses["approved"],
        print_number=print_number,
        goal="Длинная цель проекта больше пятидесяти символов для валидации",
        problem_holder="Носитель",
        barrier="Длинный барьер больше пятидесяти символов для валидации",
    )
    app.target_institutes.add(institute)
    return app


@pytest.fixture
def other_institute(departments):
    other_dept = Department.objects.create(name="Other Parent", short_name="OP")
    return Institute.objects.create(
        code="OTHER",
        name="Other Institute",
        position=2,
        department=other_dept,
    )


@pytest.mark.django_db
class TestProjectViewSet:
    def test_list_unauthenticated_returns_401(self, statuses, institute):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        client = APIClient()
        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")
        assert response.status_code == 401

    def test_list_regular_user_returns_403(self, roles, make_user, statuses, institute):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="user")
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 403

    def test_list_admin_without_semester_id_returns_200(
        self, roles, make_user, statuses, institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        admin = make_user(role_code="admin")
        app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=institute,
            title="Все семестры",
        )

        client = APIClient()
        client.force_authenticate(user=admin)
        response = client.get("/api/showcase/projects/")

        assert response.status_code == 200
        assert {item["id"] for item in response.data} == {app.id}

    def test_list_invalid_semester_id_returns_400(
        self, roles, make_user, statuses, institute
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/showcase/projects/?semester_id=bad")

        assert response.status_code == 400

    def test_list_validator_without_institutes_returns_empty(
        self, roles, make_user, statuses
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=False)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 200
        assert response.data == []

    def test_list_returns_approved_for_own_institute_and_semester(
        self, roles, make_user, statuses, institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        other_semester = Semester.objects.create(code="s2", name="S2", position=2)
        user = make_user(role_code="institute_validator", with_department=True)
        tag = Tag.objects.create(name="ИИ", category="tech")

        own_app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=institute,
            title="Свой проект",
        )
        own_app.tags.add(tag)

        _create_approved_app(
            semester=other_semester,
            statuses=statuses,
            institute=institute,
            title="Другой семестр",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 200
        assert len(response.data) == 1
        item = response.data[0]
        assert item["id"] == own_app.id
        assert item["title"] == "Свой проект"
        assert item["company"] == "ООО Тест"
        assert item["author_name"] == "Иванов Иван"
        assert item["author_email"] == "ivan@example.com"
        assert item["print_number"] == "25-00001"
        assert item["img"] == ""
        assert item["tags"] == [{"id": tag.id, "name": "ИИ"}]
        assert item["status"]["code"] == "approved"
        assert "main_department" in item
        assert "author" in item
        assert "creation_date" in item
        assert item["creation_date"] == own_app.creation_date.isoformat()

    def test_list_returns_top_level_involved_department_from_child(
        self, roles, make_user, statuses, institute, departments
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=True)

        app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=institute,
            title="С кафедрой",
        )
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 200
        item = response.data[0]
        assert item["main_department"] == {
            "id": departments["parent"].id,
            "name": departments["parent"].name,
            "short_name": departments["parent"].short_name,
        }

    def test_list_returns_top_level_involved_department_when_parent_involved(
        self, roles, make_user, statuses, institute, departments
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=True)

        app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=institute,
            title="С институтом",
        )
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["parent"],
        )

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 200
        item = response.data[0]
        assert item["main_department"]["id"] == departments["parent"].id

    def test_list_main_department_null_without_involved_departments(
        self, roles, make_user, statuses, institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=True)

        _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=institute,
            title="Без подразделений",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 200
        assert response.data[0]["main_department"] is None

    def test_list_admin_includes_non_approved(
        self, roles, make_user, statuses, institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        admin = make_user(role_code="admin")

        approved_app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=institute,
            title="Одобрен",
        )
        pending = ProjectApplication.objects.create(
            title="В работе",
            company="ООО",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="petr@example.com",
            semester=semester,
            status=statuses["await_cpds"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        pending.target_institutes.add(institute)

        client = APIClient()
        client.force_authenticate(user=admin)
        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert ids == {approved_app.id, pending.id}

    def test_list_excludes_other_institute(
        self, roles, make_user, statuses, institute, other_institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=True)

        own_app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=institute,
            title="Свой",
        )
        other_app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=other_institute,
            title="Чужой",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert ids == {own_app.id}
        assert other_app.id not in ids

    def test_list_validator_includes_non_approved(
        self, roles, make_user, statuses, institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=True)

        approved_app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            institute=institute,
            title="Одобрен",
        )
        pending = ProjectApplication.objects.create(
            title="В работе",
            company="ООО",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="petr@example.com",
            semester=semester,
            status=statuses["await_cpds"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        pending.target_institutes.add(institute)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(f"/api/showcase/projects/?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert ids == {approved_app.id, pending.id}
