"""Тесты ProjectTrackDomain."""

import pytest

from showcase.domain.project_track import ProjectTrackDomain
from showcase.models import (
    ApplicationInvolvedDepartment,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
)
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


def _create_track(
    *,
    name: str,
    semester,
    department,
    author,
    group=None,
    application=None,
) -> ProjectTrack:
    track = ProjectTrack.objects.create(
        name=name,
        description="",
        department=department,
        semester=semester,
        author=author,
    )
    if group is not None:
        ProjectTrackGroup.objects.create(project_track=track, study_group=group)
    if application is not None:
        ProjectTrackApplication.objects.create(
            project_track=track,
            project_application=application,
        )
    return track


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

    def test_validate_department_access_denied(self):
        ok, error = ProjectTrackDomain.validate_department_access(999, [1, 2])
        assert ok is False

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

    def test_can_view_aggregated_statistics_validator_denied(self, roles, make_user):
        user = make_user(role_code="institute_validator", with_department=True)
        assert ProjectTrackDomain.can_view_aggregated_statistics(user) is False

    def test_can_access_track_validator_own_department(
        self,
        roles,
        make_user,
        statuses,
        institute,
        direction,
        semester,
        departments,
    ):
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
        track = _create_track(
            name="T1",
            semester=semester,
            department=departments["child"],
            author=user,
            group=group,
            application=app,
        )

        accessible_dept_ids = ProjectTrackDomain.get_accessible_department_ids(user)
        ok, _ = ProjectTrackDomain.can_access_track(user, track, accessible_dept_ids)
        assert ok is True

    def test_can_access_track_validator_other_department_denied(
        self,
        roles,
        make_user,
        statuses,
        institute,
        direction,
        semester,
        departments,
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
        admin = make_user(role_code="admin")
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
        track = _create_track(
            name="T2",
            semester=semester,
            department=other_dept,
            author=admin,
            group=group,
            application=app,
        )

        accessible_dept_ids = ProjectTrackDomain.get_accessible_department_ids(user)
        ok, error = ProjectTrackDomain.can_access_track(
            user, track, accessible_dept_ids
        )
        assert ok is False
        assert error
