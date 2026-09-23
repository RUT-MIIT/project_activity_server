"""DTO статистики проектов для дашборда ответственного."""

from __future__ import annotations

from typing import Any

from accounts.models import User
from showcase.models import ProjectApplication
from teams.domain.team_lobby import TeamLobbyDomain
from teams.models import StudyGroup, TeamSemester, TeamSemesterMember


def _study_group_snapshot(group: StudyGroup | None) -> dict[str, Any] | None:
    """Краткое представление учебной группы."""
    if group is None:
        return None
    return {"id": group.id, "name": group.name}


def _empty_institute() -> dict[str, str]:
    return {"id": "", "name": ""}


def _project_type(application: ProjectApplication) -> str:
    """Тип проекта для stats API: internal / external."""
    return "internal" if application.is_internal_customer else "external"


def _author_dict(application: ProjectApplication) -> dict[str, Any]:
    """Автор заявки в формате IStatsProjectAuthor."""
    author = getattr(application, "author", None)
    if author is not None:
        display_name = (
            author.get_full_name() or TeamLobbyDomain.user_display_name(author)
        )
        return {
            "id": author.id,
            "fullName": display_name,
            "email": author.email or "",
        }
    full_name = (
        f"{application.author_lastname} {application.author_firstname}".strip()
    )
    return {
        "id": 0,
        "fullName": full_name,
        "email": application.author_email or "",
    }


def _member_institute(
    group: StudyGroup | None,
    institute_by_code: dict[str, dict[str, str]],
) -> dict[str, str]:
    """Институт участника по учебной группе."""
    if group is None:
        return _empty_institute()
    code = group.institute_id or ""
    return institute_by_code.get(code, {"id": code, "name": ""})


class ProjectsStatsMemberDTO:
    """Участник команды в детальной карточке проекта."""

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

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fullName": self.full_name,
            "institute": self.institute,
            "studyGroup": self.study_group,
            "course": self.course,
        }


class ProjectsStatsMentorDTO:
    """Наставник команды: id строкой, fullname как на фронте."""

    def __init__(self, mentor: User) -> None:
        self.id = str(mentor.id)
        self.fullname = TeamLobbyDomain.user_display_name(mentor)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fullname": self.fullname,
        }


class ProjectsStatsTeamListDTO:
    """Краткая команда в списке проектов."""

    def __init__(self, team_semester: TeamSemester) -> None:
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.study_group = _study_group_snapshot(team_semester.team.home_study_group)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "studyGroup": self.study_group,
        }


class ProjectsStatsTeamDetailDTO:
    """Команда с участниками и наставниками для detail проекта."""

    def __init__(
        self,
        team_semester: TeamSemester,
        *,
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.study_group = _study_group_snapshot(team_semester.team.home_study_group)
        self.status = team_semester.status
        self.members = [
            ProjectsStatsMemberDTO(
                membership, institute_by_code=institute_by_code
            ).to_dict()
            for membership in team_semester.members.all()
        ]
        mentors = list(team_semester.mentors.all())
        if not mentors and team_semester.mentor_id is not None:
            mentors = [team_semester.mentor]
        self.mentors = [ProjectsStatsMentorDTO(mentor).to_dict() for mentor in mentors]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "studyGroup": self.study_group,
            "status": self.status,
            "members": self.members,
            "mentors": self.mentors,
        }


class ProjectsStatsListItemDTO:
    """Элемент списка проектов дашборда."""

    def __init__(
        self,
        application: ProjectApplication,
        *,
        institute: dict[str, str],
        teams: list[TeamSemester],
    ) -> None:
        self.id = application.id
        self.name = application.title or ""
        self.type = _project_type(application)
        self.customer = application.company or ""
        self.institute = institute
        self.max_teams_count = application.recommended_teams_count
        self.teams = [ProjectsStatsTeamListDTO(team) for team in teams]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "customer": self.customer,
            "institute": self.institute,
            "maxTeamsCount": self.max_teams_count,
            "teams": [team.to_dict() for team in self.teams],
        }


class ProjectsStatsDetailDTO:
    """Детальная карточка проекта дашборда."""

    def __init__(
        self,
        application: ProjectApplication,
        *,
        institute: dict[str, str],
        teams: list[TeamSemester],
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        self.id = application.id
        self.name = application.title or ""
        self.type = _project_type(application)
        self.customer = application.company or ""
        self.institute = institute
        self.max_teams_count = application.recommended_teams_count
        self.current_teams_count = len(teams)
        self.author = _author_dict(application)
        self.print_number = application.print_number or ""
        self.problem_holder = application.problem_holder or ""
        self.goal = application.goal or ""
        self.barrier = application.barrier or ""
        self.existing_solutions = application.existing_solutions or ""
        self.teams = [
            ProjectsStatsTeamDetailDTO(team, institute_by_code=institute_by_code)
            for team in teams
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "customer": self.customer,
            "institute": self.institute,
            "teams": [team.to_dict() for team in self.teams],
            "maxTeamsCount": self.max_teams_count,
            "currentTeamsCount": self.current_teams_count,
            "author": self.author,
            "print_number": self.print_number,
            "problem_holder": self.problem_holder,
            "goal": self.goal,
            "barrier": self.barrier,
            "existing_solutions": self.existing_solutions,
        }
