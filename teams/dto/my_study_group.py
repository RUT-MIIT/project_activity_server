"""DTO для эндпоинта «Моя группа»."""

from typing import Any

from accounts.models import User
from showcase.models import InstituteSemesterSettings, ProjectApplication
from teams.domain.contingent_student import ContingentStudent
from teams.domain.institute_responsible import InstituteResponsibleDomain
from teams.domain.team_lobby import TeamLobbyDomain
from teams.models import StudyGroup, TeamSemester, TeamSemesterMember


class StudyGroupMentorDTO:
    """Карточка наставника учебной группы."""

    def __init__(self, mentor: User):
        self.id = mentor.id
        self.last_name = mentor.last_name
        self.first_name = mentor.first_name
        self.middle_name = mentor.middle_name
        self.email = mentor.email
        self.position = mentor.position
        self.academic_degree = mentor.academic_degree
        self.academic_title = mentor.academic_title

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "email": self.email,
            "position": self.position,
            "academic_degree": self.academic_degree,
            "academic_title": self.academic_title,
        }


class StudyGroupMemberDTO:
    """Строка списка группы из контингента."""

    def __init__(
        self,
        student: ContingentStudent,
        include_team: bool = False,
    ):
        self.id = student.id
        self.last_name = student.last_name
        self.first_name = student.first_name
        self.middle_name = student.middle_name
        self.is_registered = student.is_registered
        self.user_id = student.user_id
        self.include_team = include_team
        self.team = self._team_snapshot(student.user) if include_team else None

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
            "id": membership.team_semester.team_id,
            "name": membership.team_semester.team.name,
            "role": membership.role,
        }

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "is_registered": self.is_registered,
            "user_id": self.user_id,
        }
        if self.include_team:
            payload["team"] = self.team
        return payload


class MyStudyGroupTeamMemberDTO:
    """Участник команды текущего студента."""

    def __init__(self, member: TeamSemesterMember) -> None:
        self.id = member.user_id
        self.full_name = TeamLobbyDomain.user_display_name(member.user)
        self.role = member.role

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "role": self.role,
        }


class MyStudyGroupTeamDTO:
    """Снимок команды текущего студента в семестре."""

    def __init__(self, team_semester: TeamSemester, *, viewer_id: int) -> None:
        project: ProjectApplication | None = team_semester.project_application
        members = list(team_semester.members.all())
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.status = team_semester.status
        self.is_captain = team_semester.captain_id == viewer_id
        self.has_project = project is not None
        self.project = (
            {"id": project.id, "title": project.title} if project is not None else None
        )
        self.members = [MyStudyGroupTeamMemberDTO(m).to_dict() for m in members]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "is_captain": self.is_captain,
            "has_project": self.has_project,
            "project": self.project,
            "members": self.members,
        }


class MyStudyGroupRegistrationDTO:
    """Окно записи института на проекты в семестре."""

    def __init__(self, settings: InstituteSemesterSettings | None) -> None:
        is_open = InstituteResponsibleDomain.is_registration_open(settings)
        self.is_open = is_open
        self.opens_at = (
            settings.registration_opens_at.isoformat()
            if settings and settings.registration_opens_at
            else None
        )
        self.closed_by_decision = (
            settings.closed_by_decision if settings is not None else False
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_open": self.is_open,
            "opens_at": self.opens_at,
            "closed_by_decision": self.closed_by_decision,
        }


class MyStudyGroupDTO:
    """Полные данные учебной группы для текущего студента."""

    def __init__(
        self,
        group: StudyGroup,
        members: list[ContingentStudent],
        include_team: bool = False,
        semester_id: int | None = None,
        *,
        viewer_id: int | None = None,
        my_team: TeamSemester | None = None,
        registration_settings: InstituteSemesterSettings | None = None,
        include_semester_context: bool = False,
    ):
        member_dtos = [
            StudyGroupMemberDTO(item, include_team=include_team) for item in members
        ]
        self.id = group.id
        self.name = group.name
        self.code = group.code
        self.course_number = group.course_number
        self.is_end = group.is_end
        self.profile = group.profile
        self.form = group.form
        self.enrollment_year = group.enrollment_year
        self.direction = {
            "code": group.direction.code,
            "level": group.direction.level,
            "name": group.direction.name,
        }
        self.institute = {
            "code": group.institute.code,
            "name": group.institute.name,
        }
        mentor_users = self._resolve_mentors(group, semester_id)
        self.mentors = [
            StudyGroupMentorDTO(mentor).to_dict() for mentor in mentor_users
        ]
        self.members = [member.to_dict() for member in member_dtos]
        self.students_count = len(member_dtos)
        self.registered_students_count = sum(
            1 for member in member_dtos if member.is_registered
        )
        self.include_semester_context = include_semester_context
        self.my_team: dict[str, Any] | None = None
        self.registration: dict[str, Any] | None = None
        if include_semester_context:
            if my_team is not None and viewer_id is not None:
                self.my_team = MyStudyGroupTeamDTO(
                    my_team, viewer_id=viewer_id
                ).to_dict()
            self.registration = MyStudyGroupRegistrationDTO(
                registration_settings
            ).to_dict()

    @staticmethod
    def _resolve_mentors(group: StudyGroup, semester_id: int | None) -> list[User]:
        """Возвращает наставников: из семестра или fallback на StudyGroup.mentor."""
        if semester_id is not None:
            enrollments = getattr(group, "_semester_enrollments_for_semester", None)
            if enrollments:
                return list(enrollments[0].mentors.all())
            return []
        if group.mentor_id:
            return [group.mentor]
        return []

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "course_number": self.course_number,
            "is_end": self.is_end,
            "profile": self.profile,
            "form": self.form,
            "enrollment_year": self.enrollment_year,
            "direction": self.direction,
            "institute": self.institute,
            "mentors": self.mentors,
            "students_count": self.students_count,
            "registered_students_count": self.registered_students_count,
            "members": self.members,
        }
        if self.include_semester_context:
            payload["my_team"] = self.my_team
            payload["registration"] = self.registration
        return payload
