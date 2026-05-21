"""Тесты StudyGroupViewSet."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department
from showcase.models import Institute
from teams.models import Direction, StudyGroup


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


@pytest.fixture
def study_groups(direction, institute, other_institute):
    g1 = StudyGroup.objects.create(
        name="Группа 1",
        code="g1",
        direction=direction,
        institute=institute,
    )
    g2 = StudyGroup.objects.create(
        name="Группа 2",
        code="g2",
        direction=direction,
        institute=other_institute,
    )
    return {"own": g1, "other": g2}


@pytest.mark.django_db
class TestStudyGroupViewSet:
    def test_list_unauthenticated_returns_401(self, study_groups):
        client = APIClient()
        response = client.get("/api/teams/study-groups/")
        assert response.status_code == 401

    def test_list_admin_returns_all(self, roles, make_user, study_groups):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/teams/study-groups/")

        assert response.status_code == 200
        assert len(response.data) == 2
        item = response.data[0]
        assert set(item.keys()) == {
            "id",
            "name",
            "code",
            "course_number",
            "is_end",
            "direction",
            "institute",
        }
        assert set(item["direction"].keys()) == {"code", "level", "name"}
        assert set(item["institute"].keys()) == {"code", "name"}

    def test_list_institute_validator_filtered(self, roles, make_user, study_groups):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/teams/study-groups/")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert ids == {study_groups["own"].id}

    def test_retrieve_admin_success(self, roles, make_user, study_groups):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/teams/study-groups/{study_groups['own'].id}/")

        assert response.status_code == 200
        assert response.data["id"] == study_groups["own"].id
        assert response.data["direction"]["code"] == "38.03.01"
        assert response.data["institute"]["code"] == study_groups["own"].institute_id

    def test_retrieve_validator_forbidden(self, roles, make_user, study_groups):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/teams/study-groups/{study_groups['other'].id}/")

        assert response.status_code == 403

    def test_retrieve_validator_success(self, roles, make_user, study_groups):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/teams/study-groups/{study_groups['own'].id}/")

        assert response.status_code == 200
        assert response.data["name"] == study_groups["own"].name
