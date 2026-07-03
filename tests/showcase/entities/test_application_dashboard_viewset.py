"""Тесты ApplicationDashboardViewSet."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Semester
from showcase.models import ApplicationInvolvedDepartment, ProjectApplication


@pytest.fixture
def semester(db):
    return Semester.objects.create(code="s1", name="S1", position=1)


@pytest.fixture
def api_client():
    return APIClient()


DASHBOARD_URL = "/api/showcase/project-applications/dashboard/"


@pytest.mark.django_db
class TestApplicationDashboardViewSet:
    """HTTP-тесты дашборда заявок."""

    def test_requires_authentication(self, api_client, semester):
        """Без авторизации — 401."""
        response = api_client.get(DASHBOARD_URL, {"semester_id": semester.pk})
        assert response.status_code == 401

    def test_requires_semester_id(self, api_client, make_user, semester):
        """Без semester_id — 400."""
        user = make_user(role_code="admin")
        api_client.force_authenticate(user=user)
        response = api_client.get(DASHBOARD_URL)
        assert response.status_code == 400
        assert "semester_id" in response.json()["error"]

    def test_forbidden_for_regular_user(self, api_client, make_user, semester):
        """Обычный пользователь — 403."""
        user = make_user(role_code="user")
        api_client.force_authenticate(user=user)
        response = api_client.get(DASHBOARD_URL, {"semester_id": semester.pk})
        assert response.status_code == 403

    def test_success_for_admin(
        self, api_client, make_user, semester, statuses, departments, institute
    ):
        """Админ получает полную структуру дашборда."""
        app = ProjectApplication.objects.create(
            title="Проект",
            company="ООО Тест",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="ivan@example.com",
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        app.target_institutes.add(institute)
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )

        user = make_user(role_code="admin")
        api_client.force_authenticate(user=user)
        response = api_client.get(DASHBOARD_URL, {"semester_id": semester.pk})

        assert response.status_code == 200
        data = response.json()
        assert data["summary_cards"]["cards"][0]["value"] == 1
        assert data["rating_chart"]["id"] == "rating_chart"
        assert data["external_share_chart"]["id"] == "external_share_chart"
        assert data["status_distribution"]["id"] == "status_distribution"
        assert (
            data["application_type_distribution"]["id"]
            == "application_type_distribution"
        )
        assert data["daily_dynamics"]["id"] == "daily_dynamics"
        assert data["oldest_in_progress"]["id"] == "oldest_in_progress"
        assert data["filters_applied"]["semester_id"] == semester.pk

    def test_department_subtree_filter_via_api(
        self, api_client, make_user, semester, statuses, departments, institute
    ):
        """API: фильтр department_id включает дочернее подразделение."""
        ProjectApplication.objects.create(
            title="Child app",
            company="ООО Тест",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="ivan@example.com",
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )

        user = make_user(role_code="cpds")
        api_client.force_authenticate(user=user)
        response = api_client.get(
            DASHBOARD_URL,
            {
                "semester_id": semester.pk,
                "department_id": departments["parent"].pk,
            },
        )

        assert response.status_code == 200
        assert response.json()["summary_cards"]["cards"][0]["value"] == 1

    def test_invalid_status_group_returns_400(self, api_client, make_user, semester):
        """Неизвестная группа статусов — 400."""
        user = make_user(role_code="admin")
        api_client.force_authenticate(user=user)
        response = api_client.get(
            DASHBOARD_URL,
            {"semester_id": semester.pk, "status": "unknown_group"},
        )
        assert response.status_code == 400
