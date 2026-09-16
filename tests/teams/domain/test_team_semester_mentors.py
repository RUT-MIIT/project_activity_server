"""Тесты синхронизации наставников TeamSemester."""

from teams.domain.team_semester_mentors import TeamSemesterMentorsDomain


class TestTeamSemesterMentorsDomain:
    def test_resolve_primary_mentor_empty(self):
        assert TeamSemesterMentorsDomain.resolve_primary_mentor([]) is None

    def test_resolve_primary_mentor_min_id(self):
        class _User:
            def __init__(self, pk: int):
                self.id = pk

        primary = TeamSemesterMentorsDomain.resolve_primary_mentor(
            [_User(5), _User(2), _User(9)]
        )
        assert primary is not None
        assert primary.id == 2
