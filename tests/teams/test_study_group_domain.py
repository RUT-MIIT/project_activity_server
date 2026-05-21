"""Тесты доменной логики StudyGroupDomain."""

import pytest

from accounts.models import Department
from showcase.models import Institute
from teams.domain.study_group import StudyGroupDomain
from teams.models import Direction, StudyGroup


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def study_groups(direction, institute, other_institute):
    g1 = StudyGroup.objects.create(
        name="Группа 1",
        code="g1",
        direction=direction,
        institute=institute,
        course_number=1,
    )
    g2 = StudyGroup.objects.create(
        name="Группа 2",
        code="g2",
        direction=direction,
        institute=other_institute,
        course_number=2,
    )
    return {"own": g1, "other": g2}


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
class TestStudyGroupGetFilteredQueryset:
    @pytest.mark.parametrize("role_code", ["admin", "cpds", "user", "mentor"])
    def test_roles_see_all_groups(self, roles, make_user, study_groups, role_code):
        user = make_user(role_code=role_code)
        queryset = StudyGroup.objects.all()
        filtered = StudyGroupDomain.get_filtered_queryset(user, queryset)
        assert set(filtered.values_list("id", flat=True)) == {
            study_groups["own"].id,
            study_groups["other"].id,
        }

    def test_staff_sees_all_groups(self, roles, make_user, study_groups):
        user = make_user(role_code="user")
        user.is_staff = True
        user.save(update_fields=["is_staff"])
        queryset = StudyGroup.objects.all()
        filtered = StudyGroupDomain.get_filtered_queryset(user, queryset)
        assert filtered.count() == 2

    def test_institute_validator_sees_only_own_institute_groups(
        self, roles, make_user, study_groups
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        queryset = StudyGroup.objects.all()
        filtered = StudyGroupDomain.get_filtered_queryset(user, queryset)
        ids = set(filtered.values_list("id", flat=True))
        assert study_groups["own"].id in ids
        assert study_groups["other"].id not in ids

    def test_institute_validator_without_department_sees_none(
        self, roles, make_user, study_groups
    ):
        user = make_user(role_code="institute_validator", with_department=False)
        queryset = StudyGroup.objects.all()
        filtered = StudyGroupDomain.get_filtered_queryset(user, queryset)
        assert filtered.count() == 0

    def test_unauthenticated_sees_none(self, study_groups):
        queryset = StudyGroup.objects.all()
        filtered = StudyGroupDomain.get_filtered_queryset(None, queryset)
        assert filtered.count() == 0
