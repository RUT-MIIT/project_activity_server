"""DTO статистики учебных групп для дашборда ответственного."""

from __future__ import annotations

from typing import Any

from accounts.models import User
from teams.domain.contingent_student import ContingentStudent
from teams.domain.team_lobby import TeamLobbyDomain
from teams.dto.institute_responsible_mentors_stats import MentorsStatsStudentDTO
from teams.models import StudyGroup, TeamSemester, TeamSemesterMember


def _empty_institute() -> dict[str, str]:
    return {"id": "", "name": ""}


def _study_group_snapshot(group: StudyGroup | None) -> dict[str, Any] | None:
    """Краткое представление учебной группы."""
    if group is None:
        return None
    return {"id": group.id, "name": group.name}


def _member_institute(
    group: StudyGroup | None,
    institute_by_code: dict[str, dict[str, str]],
) -> dict[str, str]:
    """Институт участника по учебной группе."""
    if group is None:
        return _empty_institute()
    code = group.institute_id or ""
    return institute_by_code.get(code, {"id": code, "name": ""})


class GroupsStatsTeamListDTO:
    """Краткая команда в списке групп."""

    def __init__(self, team_semester: TeamSemester) -> None:
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.students_count = int(getattr(team_semester, "members_count", 0) or 0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "studentsCount": self.students_count,
        }


class GroupsStatsMemberDTO:
    """Участник команды в детальной карточке группы."""

    def __init__(
        self,
        membership: TeamSemesterMember,
        *,
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        user = membership.user
        group = getattr(user, "study_group", None)
        self.id = user.id
        self.full_name = TeamLobbyDomain.user_display_name(user)
        self.institute = _member_institute(group, institute_by_code)
        self.study_group = _study_group_snapshot(group)
        self.course = int(group.course_number) if group is not None else 0
        self.role = membership.role

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fullName": self.full_name,
            "institute": self.institute,
            "studyGroup": self.study_group,
            "course": self.course,
            "role": self.role,
        }


class GroupsStatsMentorDTO:
    """Наставник команды: id числом, fullName как на фронте Groups."""

    def __init__(self, mentor: User) -> None:
        self.id = mentor.id
        self.full_name = TeamLobbyDomain.user_display_name(mentor)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fullName": self.full_name,
        }


class GroupsStatsTeamDetailDTO:
    """Команда с участниками и наставниками для detail группы."""

    def __init__(
        self,
        team_semester: TeamSemester,
        *,
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.status = team_semester.status
        self.members = [
            GroupsStatsMemberDTO(
                membership, institute_by_code=institute_by_code
            ).to_dict()
            for membership in team_semester.members.all()
        ]
        mentors = list(team_semester.mentors.all())
        if not mentors and team_semester.mentor_id is not None:
            mentors = [team_semester.mentor]
        self.mentors = [GroupsStatsMentorDTO(mentor).to_dict() for mentor in mentors]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "members": self.members,
            "mentors": self.mentors,
        }


class GroupsStatsListItemDTO:
    """Элемент списка групп дашборда."""

    def __init__(
        self,
        group: StudyGroup,
        *,
        institute: dict[str, str],
        teams: list[TeamSemester],
    ) -> None:
        self.id = group.id
        self.name = group.name
        self.institute = institute
        self.students_count = int(getattr(group, "students_count", 0) or 0)
        self.students_in_team_count = int(
            getattr(group, "students_in_teams_count", 0) or 0
        )
        self.course = int(group.course_number)
        self.teams = [GroupsStatsTeamListDTO(team) for team in teams]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "institute": self.institute,
            "studentsCount": self.students_count,
            "studentsInTeamCount": self.students_in_team_count,
            "course": self.course,
            "teams": [team.to_dict() for team in self.teams],
        }


class GroupsStatsDetailDTO:
    """Детальная карточка учебной группы дашборда."""

    def __init__(
        self,
        group: StudyGroup,
        *,
        institute: dict[str, str],
        students: list[ContingentStudent],
        teams: list[TeamSemester],
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        self.id = group.id
        self.name = group.name
        self.institute = institute
        self.course = int(group.course_number)
        self.students = [
            MentorsStatsStudentDTO.from_contingent(student, institute_by_code)
            for student in students
        ]
        self.teams = [
            GroupsStatsTeamDetailDTO(team, institute_by_code=institute_by_code)
            for team in teams
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "institute": self.institute,
            "course": self.course,
            "students": [student.to_dict() for student in self.students],
            "teams": [team.to_dict() for team in self.teams],
        }
