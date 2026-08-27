"""Тесты доменной логики студенческой витрины."""

import pytest

from showcase.domain.student_showcase import StudentShowcaseDomain
from teams.models import TeamSemester


class _FakeApplication:
    def __init__(self, min_team_members: int = 2, max_team_members: int = 5) -> None:
        self.min_team_members = min_team_members
        self.max_team_members = max_team_members


class _FakeTeamSemester:
    def __init__(
        self,
        *,
        status: str = TeamSemester.Status.ASSEMBLED,
        project_application_id: int | None = None,
        project_track_id: int | None = 1,
    ) -> None:
        self.status = status
        self.project_application_id = project_application_id
        self.project_track_id = project_track_id


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        (
            {
                "is_captain": True,
                "status": TeamSemester.Status.ASSEMBLED,
                "has_project": False,
                "members_count": 3,
                "min_team_members": 2,
                "max_team_members": 5,
                "enrolled_count": 0,
                "max_teams": 2,
                "project_track_id": 1,
                "application_track_id": 1,
            },
            True,
        ),
        (
            {
                "is_captain": False,
                "status": TeamSemester.Status.ASSEMBLED,
                "has_project": False,
                "members_count": 3,
                "min_team_members": 2,
                "max_team_members": 5,
                "enrolled_count": 0,
                "max_teams": 2,
                "project_track_id": 1,
                "application_track_id": 1,
            },
            False,
        ),
        (
            {
                "is_captain": True,
                "status": TeamSemester.Status.FORMING,
                "has_project": False,
                "members_count": 3,
                "min_team_members": 2,
                "max_team_members": 5,
                "enrolled_count": 0,
                "max_teams": 2,
                "project_track_id": 1,
                "application_track_id": 1,
            },
            False,
        ),
        (
            {
                "is_captain": True,
                "status": TeamSemester.Status.ASSEMBLED,
                "has_project": True,
                "members_count": 3,
                "min_team_members": 2,
                "max_team_members": 5,
                "enrolled_count": 0,
                "max_teams": 2,
                "project_track_id": 1,
                "application_track_id": 1,
            },
            False,
        ),
        (
            {
                "is_captain": True,
                "status": TeamSemester.Status.ASSEMBLED,
                "has_project": False,
                "members_count": 3,
                "min_team_members": 2,
                "max_team_members": 5,
                "enrolled_count": 0,
                "max_teams": 2,
                "project_track_id": None,
                "application_track_id": 1,
            },
            False,
        ),
        (
            {
                "is_captain": True,
                "status": TeamSemester.Status.ASSEMBLED,
                "has_project": False,
                "members_count": 3,
                "min_team_members": 2,
                "max_team_members": 5,
                "enrolled_count": 0,
                "max_teams": 2,
                "project_track_id": 1,
                "application_track_id": 2,
            },
            False,
        ),
        (
            {
                "is_captain": True,
                "status": TeamSemester.Status.ASSEMBLED,
                "has_project": False,
                "members_count": 1,
                "min_team_members": 2,
                "max_team_members": 5,
                "enrolled_count": 0,
                "max_teams": 2,
                "project_track_id": 1,
                "application_track_id": 1,
            },
            False,
        ),
        (
            {
                "is_captain": True,
                "status": TeamSemester.Status.ASSEMBLED,
                "has_project": False,
                "members_count": 3,
                "min_team_members": 2,
                "max_team_members": 5,
                "enrolled_count": 2,
                "max_teams": 2,
                "project_track_id": 1,
                "application_track_id": 1,
            },
            False,
        ),
    ],
)
def test_can_enroll(kwargs, expected):
    assert StudentShowcaseDomain.can_enroll(**kwargs) is expected


def test_ensure_team_assembled_rejects_forming():
    with pytest.raises(ValueError, match="подтверждения состава"):
        StudentShowcaseDomain.ensure_team_assembled(
            _FakeTeamSemester(status=TeamSemester.Status.FORMING)
        )


def test_ensure_no_project_yet():
    with pytest.raises(ValueError, match="уже записана"):
        StudentShowcaseDomain.ensure_no_project_yet(
            _FakeTeamSemester(project_application_id=10)
        )


def test_ensure_project_in_team_track_requires_track():
    with pytest.raises(ValueError, match="не указан проектный трек"):
        StudentShowcaseDomain.ensure_project_in_team_track(
            _FakeTeamSemester(project_track_id=None), 1
        )


def test_ensure_project_in_team_track_mismatch():
    with pytest.raises(ValueError, match="не входит в трек"):
        StudentShowcaseDomain.ensure_project_in_team_track(
            _FakeTeamSemester(project_track_id=1), 2
        )


def test_ensure_members_fit_project():
    with pytest.raises(ValueError, match="пределах"):
        StudentShowcaseDomain.ensure_members_fit_project(
            members_count=1,
            application=_FakeApplication(min_team_members=2, max_team_members=5),
        )


def test_ensure_enrollment_slot_available():
    with pytest.raises(ValueError, match="максимальное число"):
        StudentShowcaseDomain.ensure_enrollment_slot_available(
            enrolled_count=3, max_teams=3
        )
