"""DTO для эндпоинта «Мои группы» наставника."""

from __future__ import annotations

from typing import Any

from accounts.models import PreRegisteredStudent, User
from teams.models import StudyGroup, TeamSemester, TeamSemesterMember


class MentorGroupListItemDTO:
    """Строка списка групп наставника."""

    def __init__(self, group: StudyGroup) -> None:
        self.id = group.id
        self.name = group.name
        self.students_count = int(group.students_count)
        self.teams_count = int(group.teams_count)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "studentsCount": self.students_count,
            "teamsCount": self.teams_count,
        }


class MentorGroupListDTO:
    """Список групп наставника."""

    def __init__(self, groups: list[StudyGroup]) -> None:
        self._items = [MentorGroupListItemDTO(group) for group in groups]

    def to_list(self) -> list[dict[str, Any]]:
        return [item.to_dict() for item in self._items]


class MentorGroupStudentDTO:
    """Студент контингента для деталей группы наставника."""

    def __init__(self, pre_registered: PreRegisteredStudent) -> None:
        student = pre_registered.student
        self.id = pre_registered.id
        self.last_name = pre_registered.last_name
        self.first_name = pre_registered.first_name
        self.middle_name = pre_registered.middle_name
        self.is_registered = pre_registered.is_registered
        self.user_id = student.id if student is not None else None
        self.team = self._team_snapshot(student)

    @staticmethod
    def _team_snapshot(student: User | None) -> dict[str, Any] | None:
        if student is None:
            return None
        memberships: list[TeamSemesterMember] = getattr(
            student, "_team_membership_for_semester", []
        )
        if not memberships:
            return None
        membership = memberships[0]
        return {
            "id": membership.team_semester_id,
            "name": membership.team_semester.team.name,
            "role": membership.role,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "lastName": self.last_name,
            "firstName": self.first_name,
            "middleName": self.middle_name,
            "isRegistered": self.is_registered,
            "userId": self.user_id,
            "team": self.team,
        }


class MentorGroupTeamDTO:
    """Команда группы в семестре для деталей наставника."""

    def __init__(self, team_semester: TeamSemester) -> None:
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.status = team_semester.status
        self.members_count = int(getattr(team_semester, "members_count", 0) or 0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "membersCount": self.members_count,
        }


class MentorGroupDetailDTO:
    """Детали учебной группы для наставника в семестре."""

    def __init__(
        self,
        group: StudyGroup,
        students: list[PreRegisteredStudent],
        teams: list[TeamSemester],
    ) -> None:
        self.id = group.id
        self.name = group.name
        self.students = [MentorGroupStudentDTO(student) for student in students]
        self.teams = [MentorGroupTeamDTO(team) for team in teams]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "students": [student.to_dict() for student in self.students],
            "teams": [team.to_dict() for team in self.teams],
        }
