"""Тесты доменной логики DirectionDomain."""

import pytest

from accounts.models import Department
from showcase.models import Institute
from teams.domain.direction import DirectionDomain
from teams.models import Direction, StudyGroup


@pytest.fixture
def directions(db):
    """Три направления для сценариев фильтрации."""
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
    """Второй институт на другом подразделении."""
    other_dept = Department.objects.create(name="Other Parent", short_name="OP")
    return Institute.objects.create(
        code="OTHER",
        name="Other Institute",
        position=2,
        department=other_dept,
    )


@pytest.mark.django_db
class TestGetFilteredQueryset:
    """Фильтрация queryset направлений по ролям."""

    @pytest.mark.parametrize("role_code", ["admin", "cpds", "user", "mentor"])
    def test_roles_see_all_directions(self, roles, make_user, directions, role_code):
        user = make_user(role_code=role_code)
        queryset = Direction.objects.all()
        filtered = DirectionDomain.get_filtered_queryset(user, queryset)
        assert set(filtered.values_list("code", flat=True)) == {
            directions["d1"].code,
            directions["d2"].code,
            directions["d3"].code,
        }

    def test_staff_sees_all_directions(self, roles, make_user, directions):
        user = make_user(role_code="user")
        user.is_staff = True
        user.save(update_fields=["is_staff"])
        queryset = Direction.objects.all()
        filtered = DirectionDomain.get_filtered_queryset(user, queryset)
        assert filtered.count() == 3

    def test_institute_validator_sees_only_institute_directions(
        self, roles, make_user, departments, institute, directions, other_institute
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        StudyGroup.objects.create(
            name="Группа 1",
            code="g1",
            direction=directions["d1"],
            institute=institute,
        )
        StudyGroup.objects.create(
            name="Группа 2",
            code="g2",
            direction=directions["d2"],
            institute=other_institute,
        )

        queryset = Direction.objects.all()
        filtered = DirectionDomain.get_filtered_queryset(user, queryset)
        codes = set(filtered.values_list("code", flat=True))

        assert directions["d1"].code in codes
        assert directions["d2"].code not in codes
        assert directions["d3"].code not in codes

    def test_direction_without_groups_not_visible_to_validator(
        self, roles, make_user, institute, directions
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        StudyGroup.objects.create(
            name="Группа 1",
            code="g1",
            direction=directions["d1"],
            institute=institute,
        )

        queryset = Direction.objects.all()
        filtered = DirectionDomain.get_filtered_queryset(user, queryset)
        codes = set(filtered.values_list("code", flat=True))

        assert directions["d1"].code in codes
        assert directions["d3"].code not in codes

    def test_institute_validator_without_department_sees_none(
        self, roles, make_user, directions
    ):
        user = make_user(role_code="institute_validator", with_department=False)
        queryset = Direction.objects.all()
        filtered = DirectionDomain.get_filtered_queryset(user, queryset)
        assert filtered.count() == 0

    def test_unauthenticated_sees_none(self, directions):
        queryset = Direction.objects.all()
        filtered = DirectionDomain.get_filtered_queryset(None, queryset)
        assert filtered.count() == 0


@pytest.mark.django_db
class TestGetUserInstituteCodes:
    """Разрешение институтов по подразделению пользователя."""

    def test_child_department_resolves_parent_institute(
        self, make_user, institute, departments
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        codes = DirectionDomain.get_user_institute_codes(user)
        assert institute.code in codes
