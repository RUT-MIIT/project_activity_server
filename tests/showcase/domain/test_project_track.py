"""Тесты ProjectTrackDomain."""

import pytest

from showcase.domain.project_track import ProjectTrackDomain
from showcase.models import ProjectApplication, ProjectTrack
from teams.models import Direction, StudyGroup


@pytest.fixture
def semester(db):
    from accounts.models import Semester

    return Semester.objects.create(code="s1", name="S1", position=1)


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.mark.django_db
class TestProjectTrackDomain:
    def test_can_manage_tracks_admin(self, roles, make_user):
        user = make_user(role_code="admin")
        ok, error = ProjectTrackDomain.can_manage_tracks(user)
        assert ok is True
        assert error == ""

    def test_can_manage_tracks_institute_validator(self, roles, make_user):
        user = make_user(role_code="institute_validator", with_department=True)
        ok, error = ProjectTrackDomain.can_manage_tracks(user)
        assert ok is True

    def test_can_manage_tracks_user_denied(self, roles, make_user):
        user = make_user(role_code="user")
        ok, error = ProjectTrackDomain.can_manage_tracks(user)
        assert ok is False

    def test_get_accessible_institute_codes_admin_returns_none(self, roles, make_user):
        user = make_user(role_code="admin")
        assert ProjectTrackDomain.get_accessible_institute_codes(user) is None

    def test_get_accessible_institute_codes_validator(
        self, roles, make_user, institute
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        codes = ProjectTrackDomain.get_accessible_institute_codes(user)
        assert institute.code in codes

    def test_validate_group_institute_codes_denied(self):
        ok, error = ProjectTrackDomain.validate_group_institute_codes(
            {"OTHER"}, ["INST-1"]
        )
        assert ok is False
        assert "группами" in error

    def test_resolve_institute_code_explicit_validator(
        self, roles, make_user, institute
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        code = ProjectTrackDomain.resolve_institute_code(user, institute.code)
        assert code == institute.code

    def test_resolve_institute_code_default_validator(
        self, roles, make_user, institute
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        code = ProjectTrackDomain.resolve_institute_code(user, None)
        assert code == institute.code

    def test_resolve_institute_code_admin_requires_param(self, roles, make_user):
        user = make_user(role_code="admin")
        with pytest.raises(ValueError, match="institute_code обязателен"):
            ProjectTrackDomain.resolve_institute_code(user, None)

    def test_can_view_aggregated_statistics_admin(self, roles, make_user):
        user = make_user(role_code="admin")
        assert ProjectTrackDomain.can_view_aggregated_statistics(user) is True

    def test_can_view_aggregated_statistics_cpds(self, roles, make_user):
        user = make_user(role_code="cpds")
        assert ProjectTrackDomain.can_view_aggregated_statistics(user) is True

    def test_can_view_aggregated_statistics_validator_denied(self, roles, make_user):
        user = make_user(role_code="institute_validator", with_department=True)
        assert ProjectTrackDomain.can_view_aggregated_statistics(user) is False

    def test_resolve_institute_code_validator_other_denied(
        self, roles, make_user, institute
    ):
        from accounts.models import Department
        from showcase.models import Institute

        other_dept = Department.objects.create(name="Other", short_name="O")
        other_inst = Institute.objects.create(
            code="OTHER",
            name="Other",
            position=2,
            department=other_dept,
        )
        user = make_user(role_code="institute_validator", with_department=True)
        with pytest.raises(PermissionError):
            ProjectTrackDomain.resolve_institute_code(user, other_inst.code)

    def test_can_access_track_validator_own(
        self,
        roles,
        make_user,
        statuses,
        institute,
        direction,
        semester,
        departments,
    ):
        from showcase.models import ApplicationInvolvedDepartment

        user = make_user(role_code="institute_validator", with_department=True)
        group = StudyGroup.objects.create(
            name="Г1",
            code="g1",
            direction=direction,
            institute=institute,
        )
        app = ProjectApplication.objects.create(
            title="Проект",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@b.c",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )
        track = ProjectTrack.objects.create(
            semester=semester,
            study_group=group,
            project_application=app,
        )

        ok, _ = ProjectTrackDomain.can_access_track(user, track, [institute.code])
        assert ok is True

    def test_can_access_track_validator_other_institute_denied(
        self,
        roles,
        make_user,
        statuses,
        institute,
        direction,
        semester,
        departments,
    ):
        from showcase.models import Institute

        other_dept = departments["parent"]
        other_inst = Institute.objects.create(
            code="OTHER",
            name="Other",
            position=2,
            department=other_dept,
        )
        user = make_user(role_code="institute_validator", with_department=True)
        group = StudyGroup.objects.create(
            name="Г2",
            code="g2",
            direction=direction,
            institute=other_inst,
        )
        app = ProjectApplication.objects.create(
            title="Чужой",
            company="ООО",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="p@b.c",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        app.target_institutes.add(other_inst)
        track = ProjectTrack.objects.create(
            semester=semester,
            study_group=group,
            project_application=app,
        )

        ok, error = ProjectTrackDomain.can_access_track(user, track, [institute.code])
        assert ok is False
        assert error
