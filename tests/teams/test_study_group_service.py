"""Тесты StudyGroupService."""

import pytest

from teams.models import Direction, StudyGroup
from teams.services.study_group_service import StudyGroupService


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def study_groups(direction, institute):
    g1 = StudyGroup.objects.create(
        name="G1",
        code="g1",
        direction=direction,
        institute=institute,
    )
    g2 = StudyGroup.objects.create(
        name="G2",
        code="g2",
        direction=direction,
        institute=institute,
    )
    return {"g1": g1, "g2": g2}


@pytest.mark.django_db
class TestStudyGroupService:
    def test_list_study_groups_admin_sees_all(self, roles, make_user, study_groups):
        user = make_user(role_code="admin")
        service = StudyGroupService()
        ids = set(service.list_study_groups(user).values_list("id", flat=True))
        assert study_groups["g1"].id in ids
        assert study_groups["g2"].id in ids

    def test_list_study_groups_institute_validator_filtered(
        self, roles, make_user, institute, direction, departments
    ):
        from accounts.models import Department
        from showcase.models import Institute

        other_dept = Department.objects.create(name="Other", short_name="OP")
        other_inst = Institute.objects.create(
            code="OTHER",
            name="Other",
            position=2,
            department=other_dept,
        )
        own = StudyGroup.objects.create(
            name="Own",
            code="own",
            direction=direction,
            institute=institute,
        )
        StudyGroup.objects.create(
            name="Other",
            code="other",
            direction=direction,
            institute=other_inst,
        )
        user = make_user(role_code="institute_validator", with_department=True)
        service = StudyGroupService()
        ids = set(service.list_study_groups(user).values_list("id", flat=True))
        assert own.id in ids
        assert len(ids) == 1

    def test_get_study_group_success(self, roles, make_user, study_groups):
        user = make_user(role_code="admin")
        service = StudyGroupService()
        group = service.get_study_group(study_groups["g1"].id, user)
        assert group.id == study_groups["g1"].id

    def test_get_study_group_forbidden(self, roles, make_user, direction, institute):
        from accounts.models import Department
        from showcase.models import Institute

        other_dept = Department.objects.create(name="Other", short_name="OP")
        other_inst = Institute.objects.create(
            code="OTHER",
            name="Other",
            position=2,
            department=other_dept,
        )
        foreign = StudyGroup.objects.create(
            name="Foreign",
            code="foreign",
            direction=direction,
            institute=other_inst,
        )
        user = make_user(role_code="institute_validator", with_department=True)
        service = StudyGroupService()
        with pytest.raises(ValueError, match="Нет доступа"):
            service.get_study_group(foreign.id, user)

    def test_get_study_group_not_found(self, roles, make_user):
        user = make_user(role_code="admin")
        service = StudyGroupService()
        with pytest.raises(ValueError, match="не найдена"):
            service.get_study_group(99999, user)
