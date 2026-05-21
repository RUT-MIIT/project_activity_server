"""Тесты DirectionViewSet."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department
from showcase.models import Institute
from teams.models import Direction, StudyGroup


@pytest.fixture
def directions(db):
    d1 = Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )
    d2 = Direction.objects.create(
        code="38.03.02",
        name="Менеджмент",
        level=Direction.Level.BAKALAVRIAT,
    )
    d3 = Direction.objects.create(
        code="09.03.01",
        name="Информатика",
        level=Direction.Level.BAKALAVRIAT,
    )
    return {"d1": d1, "d2": d2, "d3": d3}


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
class TestDirectionViewSet:
    def test_list_unauthenticated_returns_401(self, directions):
        client = APIClient()
        response = client.get("/api/teams/directions/")
        assert response.status_code == 401

    def test_list_admin_returns_all(self, roles, make_user, directions):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/teams/directions/")

        assert response.status_code == 200
        assert len(response.data) == 3
        codes = {item["code"] for item in response.data}
        assert codes == {
            directions["d1"].code,
            directions["d2"].code,
            directions["d3"].code,
        }
        item = response.data[0]
        assert set(item.keys()) == {"code", "level", "name"}

    def test_list_sorted_by_code(self, roles, make_user, directions):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/teams/directions/")

        codes = [item["code"] for item in response.data]
        assert codes == sorted(codes)

    def test_list_institute_validator_filtered(
        self, roles, make_user, institute, directions, other_institute
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        StudyGroup.objects.create(
            name="G1",
            code="g1",
            direction=directions["d1"],
            institute=institute,
        )
        StudyGroup.objects.create(
            name="G2",
            code="g2",
            direction=directions["d2"],
            institute=other_institute,
        )

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/api/teams/directions/")

        assert response.status_code == 200
        codes = {item["code"] for item in response.data}
        assert codes == {directions["d1"].code}

    def test_retrieve_admin_success(self, roles, make_user, directions):
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/teams/directions/{directions['d1'].code}/")

        assert response.status_code == 200
        assert response.data["code"] == directions["d1"].code
        assert response.data["name"] == directions["d1"].name

    def test_retrieve_validator_forbidden(self, roles, make_user, directions):
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/teams/directions/{directions['d2'].code}/")

        assert response.status_code == 403

    def test_retrieve_validator_success_with_group(
        self, roles, make_user, institute, directions
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        StudyGroup.objects.create(
            name="G1",
            code="g1",
            direction=directions["d1"],
            institute=institute,
        )
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/teams/directions/{directions['d1'].code}/")

        assert response.status_code == 200
        assert response.data["code"] == directions["d1"].code
