"""DTO для эндпоинта «Мои группы» наставника."""

from __future__ import annotations

from typing import Any

from accounts.models import User
from showcase.models import InstituteSemesterSettings, ProjectApplication
from teams.domain.contingent_student import ContingentStudent
from teams.dto.my_study_group import MyStudyGroupRegistrationDTO
from teams.models import StudyGroup, TeamSemester, TeamSemesterMember


def _project_snapshot(application: ProjectApplication | None) -> dict[str, Any] | None:
    """Краткое представление выбранного проекта команды."""
    if application is None:
        return None
    return {
        "id": application.id,
        "title": application.title or "",
    }


class MentorGroupListItemDTO:
    """Строка списка групп наставника."""

    def __init__(self, group: StudyGroup) -> None:
        self.id = group.id
        self.name = group.name
        self.students_count = int(group.students_count)
        self.registered_students_count = int(
            getattr(group, "registered_students_count", 0) or 0
        )
        self.teams_count = int(group.teams_count)
        self.assembled_teams_count = int(
            getattr(group, "assembled_teams_count", 0) or 0
        )
        self.students_in_teams_count = int(
            getattr(group, "students_in_teams_count", 0) or 0
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "studentsCount": self.students_count,
            "registeredStudentsCount": self.registered_students_count,
            "teamsCount": self.teams_count,
            "assembledTeamsCount": self.assembled_teams_count,
            "studentsInTeamsCount": self.students_in_teams_count,
        }


class MentorGroupListDTO:
    """Список групп наставника."""

    def __init__(self, groups: list[StudyGroup]) -> None:
        self._items = [MentorGroupListItemDTO(group) for group in groups]

    def to_list(self) -> list[dict[str, Any]]:
        return [item.to_dict() for item in self._items]


class MentorGroupStudentDTO:
    """Студент контингента для деталей группы наставника."""

    def __init__(self, student: ContingentStudent) -> None:
        self.id = student.id
        self.last_name = student.last_name
        self.first_name = student.first_name
        self.middle_name = student.middle_name
        self.is_registered = student.is_registered
        self.user_id = student.user_id
        self.team: dict[str, Any] | None = None
        self.project: dict[str, Any] | None = None
        self._fill_team_and_project(student.user)

    def _fill_team_and_project(self, student: User | None) -> None:
        if student is None:
            return
        memberships: list[TeamSemesterMember] = getattr(
            student, "_team_membership_for_semester", []
        )
        if not memberships:
            return
        membership = memberships[0]
        self.team = {
            "id": membership.team_semester_id,
            "name": membership.team_semester.team.name,
            "role": membership.role,
        }
        self.project = _project_snapshot(membership.team_semester.project_application)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "lastName": self.last_name,
            "firstName": self.first_name,
            "middleName": self.middle_name,
            "isRegistered": self.is_registered,
            "userId": self.user_id,
            "team": self.team,
            "project": self.project,
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
        students: list[ContingentStudent],
        teams: list[TeamSemester],
        registration_settings: InstituteSemesterSettings | None = None,
    ) -> None:
        self.id = group.id
        self.name = group.name
        self.students = [MentorGroupStudentDTO(student) for student in students]
        self.teams = [MentorGroupTeamDTO(team) for team in teams]
        self.registration = MyStudyGroupRegistrationDTO(registration_settings).to_dict()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "students": [student.to_dict() for student in self.students],
            "teams": [team.to_dict() for team in self.teams],
            "registration": self.registration,
        }
