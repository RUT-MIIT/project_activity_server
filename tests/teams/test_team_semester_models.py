"""Тесты моделей TeamSemester и TeamSemesterMember."""

from django.db import IntegrityError
import pytest

from accounts.models import Semester
from teams.models import Direction, StudyGroup, Team, TeamSemester, TeamSemesterMember


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def study_group(direction, institute):
    return StudyGroup.objects.create(
        name="G1",
        code="g1",
        direction=direction,
        institute=institute,
    )


@pytest.fixture
def semester(db):
    return Semester.objects.create(code="s1", name="Семестр 1", position=1)


@pytest.mark.django_db
class TestTeamSemesterModels:
    def test_unique_team_semester(self, roles, make_user, study_group, semester):
        captain = make_user(role_code="student")
        team = Team.objects.create(name="Alpha", home_study_group=study_group)
        TeamSemester.objects.create(team=team, semester=semester, captain=captain)
        with pytest.raises(IntegrityError):
            TeamSemester.objects.create(team=team, semester=semester, captain=captain)

    def test_member_semester_synced_from_team_semester(
        self, roles, make_user, study_group, semester
    ):
        captain = make_user(role_code="student")
        other = make_user(role_code="student", email="other@example.com")
        team = Team.objects.create(name="Alpha", home_study_group=study_group)
        team_semester = TeamSemester.objects.create(
            team=team, semester=semester, captain=captain
        )
        member = TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=other,
            role=TeamSemesterMember.Role.MEMBER,
        )
        assert member.semester_id == semester.pk

    def test_unique_user_per_semester(self, roles, make_user, study_group, semester):
        captain = make_user(role_code="student")
        other = make_user(role_code="student", email="other@example.com")
        team_a = Team.objects.create(name="A")
        team_b = Team.objects.create(name="B")
        ts_a = TeamSemester.objects.create(
            team=team_a, semester=semester, captain=captain
        )
        ts_b = TeamSemester.objects.create(
            team=team_b,
            semester=semester,
            captain=make_user(role_code="student", email="cap2@example.com"),
        )
        TeamSemesterMember.objects.create(team_semester=ts_a, user=other)
        with pytest.raises(IntegrityError):
            TeamSemesterMember.objects.create(team_semester=ts_b, user=other)
