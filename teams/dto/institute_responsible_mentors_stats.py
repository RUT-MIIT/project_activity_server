"""DTO статистики наставников для дашборда ответственного."""

from __future__ import annotations

from typing import Any

from accounts.models import User
from showcase.models import ProjectApplication
from teams.domain.contingent_student import ContingentStudent
from teams.domain.team_lobby import TeamLobbyDomain
from teams.models import StudyGroup, TeamSemester, TeamSemesterMember


def _project_name_snapshot(
    application: ProjectApplication | None,
) -> dict[str, Any] | None:
    """Краткое представление проекта: id + name (из title заявки)."""
    if application is None:
        return None
    return {
        "id": application.id,
        "name": application.title or "",
    }


def _study_group_snapshot(group: StudyGroup | None) -> dict[str, Any] | None:
    """Краткое представление учебной группы."""
    if group is None:
        return None
    return {"id": group.id, "name": group.name}


class MentorsStatsStudentDTO:
    """Полный stats-студент для detail наставника."""

    def __init__(
        self,
        *,
        student_id: int,
        full_name: str,
        institute: dict[str, str],
        study_group: dict[str, Any] | None,
        course: int,
        is_registered: bool,
        team: dict[str, Any] | None,
        project: dict[str, Any] | None,
    ) -> None:
        self.student_id = student_id
        self.full_name = full_name
        self.institute = institute
        self.study_group = study_group
        self.course = course
        self.is_registered = is_registered
        self.team = team
        self.project = project

    @classmethod
    def from_contingent(
        cls,
        student: ContingentStudent,
        institute_by_code: dict[str, dict[str, str]],
    ) -> MentorsStatsStudentDTO:
        """Строит DTO из контингента группы."""
        group = student.group
        institute_code = group.institute_id if group is not None else ""
        institute = institute_by_code.get(
            institute_code, {"id": institute_code or "", "name": ""}
        )
        course = int(group.course_number) if group is not None else 0
        team: dict[str, Any] | None = None
        project: dict[str, Any] | None = None
        user = student.user
        if user is not None:
            memberships: list[TeamSemesterMember] = getattr(
                user, "_team_membership_for_semester", []
            )
            if memberships:
                membership = memberships[0]
                team_semester = membership.team_semester
                team = {
                    "id": team_semester.id,
                    "name": team_semester.team.name,
                }
                project = _project_name_snapshot(team_semester.project_application)
        full_name = " ".join(
            part
            for part in (student.last_name, student.first_name, student.middle_name)
            if part
        ).strip()
        return cls(
            student_id=student.id,
            full_name=full_name,
            institute=institute,
            study_group=_study_group_snapshot(group),
            course=course,
            is_registered=student.is_registered,
            team=team,
            project=project,
        )

    @classmethod
    def from_team_member(
        cls,
        membership: TeamSemesterMember,
        *,
        team_semester: TeamSemester,
        institute_by_code: dict[str, dict[str, str]],
    ) -> MentorsStatsStudentDTO:
        """Строит DTO участника команды."""
        user = membership.user
        group = getattr(user, "study_group", None)
        institute_code = group.institute_id if group is not None else ""
        institute = institute_by_code.get(
            institute_code, {"id": institute_code or "", "name": ""}
        )
        course = int(group.course_number) if group is not None else 0
        return cls(
            student_id=user.id,
            full_name=TeamLobbyDomain.user_display_name(user),
            institute=institute,
            study_group=_study_group_snapshot(group),
            course=course,
            is_registered=True,
            team={"id": team_semester.id, "name": team_semester.team.name},
            project=_project_name_snapshot(team_semester.project_application),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.student_id,
            "fullName": self.full_name,
            "institute": self.institute,
            "studyGroup": self.study_group,
            "course": self.course,
            "isRegistered": self.is_registered,
            "team": self.team,
            "project": self.project,
        }


class MentorsStatsTeamDTO:
    """Полная stats-команда группы наставника."""

    def __init__(
        self,
        team_semester: TeamSemester,
        *,
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        group = team_semester.team.home_study_group
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.status = team_semester.status
        self.project = _project_name_snapshot(team_semester.project_application)
        self.study_group = _study_group_snapshot(group)
        self.members = [
            MentorsStatsStudentDTO.from_team_member(
                membership,
                team_semester=team_semester,
                institute_by_code=institute_by_code,
            ).to_dict()
            for membership in team_semester.members.all()
        ]
        self.members_count = int(getattr(team_semester, "members_count", 0) or 0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "project": self.project,
            "studyGroup": self.study_group,
            "members": self.members,
            "membersCount": self.members_count,
        }


class MentorsStatsGroupListDTO:
    """Лёгкая группа в списке наставников."""

    def __init__(self, group: StudyGroup) -> None:
        self.id = group.id
        self.name = group.name
        self.students_count = int(getattr(group, "students_count", 0) or 0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "studentsCount": self.students_count,
        }


class MentorsStatsListItemDTO:
    """Строка списка наставников."""

    def __init__(
        self,
        mentor: User,
        *,
        institute: dict[str, str],
        groups: list[StudyGroup],
    ) -> None:
        self.id = mentor.id
        self.full_name = mentor.get_full_name()
        self.institute = institute
        self.groups = [MentorsStatsGroupListDTO(group) for group in groups]
        self.teams_count = sum(
            int(getattr(group, "teams_count", 0) or 0) for group in groups
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fullName": self.full_name,
            "institute": self.institute,
            "groups": [group.to_dict() for group in self.groups],
            "teamsCount": self.teams_count,
        }


class MentorsStatsGroupDetailDTO:
    """Детальная группа наставника со студентами и командами."""

    def __init__(
        self,
        group: StudyGroup,
        *,
        students: list[ContingentStudent],
        teams: list[TeamSemester],
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        self.id = group.id
        self.name = group.name
        self.students = [
            MentorsStatsStudentDTO.from_contingent(student, institute_by_code)
            for student in students
        ]
        self.teams = [
            MentorsStatsTeamDTO(team, institute_by_code=institute_by_code)
            for team in teams
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "students": [student.to_dict() for student in self.students],
            "teams": [team.to_dict() for team in self.teams],
        }


class MentorsStatsDetailDTO:
    """Детальная карточка наставника."""

    def __init__(
        self,
        mentor: User,
        *,
        institute: dict[str, str],
        groups: list[StudyGroup],
        students_by_group: dict[int, list[ContingentStudent]],
        teams_by_group: dict[int, list[TeamSemester]],
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        self.id = mentor.id
        self.full_name = mentor.get_full_name()
        self.institute = institute
        self.teams_count = sum(
            int(getattr(group, "teams_count", 0) or 0) for group in groups
        )
        self.groups = [
            MentorsStatsGroupDetailDTO(
                group,
                students=students_by_group.get(group.id, []),
                teams=teams_by_group.get(group.id, []),
                institute_by_code=institute_by_code,
            )
            for group in groups
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fullName": self.full_name,
            "institute": self.institute,
            "teamsCount": self.teams_count,
            "groups": [group.to_dict() for group in self.groups],
        }
