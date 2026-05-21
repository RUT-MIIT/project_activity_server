"""Тесты DirectionService."""

import pytest

from teams.models import Direction, StudyGroup
from teams.services.direction_service import DirectionService


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
    return {"d1": d1, "d2": d2}


@pytest.mark.django_db
class TestDirectionService:
    def test_list_directions_admin_sees_all(self, roles, make_user, directions):
        user = make_user(role_code="admin")
        service = DirectionService()
        codes = set(service.list_directions(user).values_list("code", flat=True))
        assert directions["d1"].code in codes
        assert directions["d2"].code in codes

    def test_list_directions_institute_validator_filtered(
        self, roles, make_user, institute, directions
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        StudyGroup.objects.create(
            name="G1",
            code="g1",
            direction=directions["d1"],
            institute=institute,
        )
        service = DirectionService()
        codes = set(service.list_directions(user).values_list("code", flat=True))
        assert directions["d1"].code in codes
        assert directions["d2"].code not in codes

    def test_get_direction_success(self, roles, make_user, directions):
        user = make_user(role_code="admin")
        service = DirectionService()
        direction = service.get_direction(directions["d1"].code, user)
        assert direction.code == directions["d1"].code

    def test_get_direction_forbidden_for_validator(
        self, roles, make_user, directions, institute
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        service = DirectionService()
        with pytest.raises(ValueError, match="Нет доступа"):
            service.get_direction(directions["d2"].code, user)

    def test_get_direction_not_found(self, roles, make_user):
        user = make_user(role_code="admin")
        service = DirectionService()
        with pytest.raises(ValueError, match="не найдено"):
            service.get_direction("99.99.99", user)
