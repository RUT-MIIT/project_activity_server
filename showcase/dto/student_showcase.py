"""DTO студенческой витрины проектов."""

from __future__ import annotations

from typing import Any

from showcase.models import ProjectApplication, ProjectTrack, Tag
from teams.models import TeamSemester


def _tag_brief(tag: Tag) -> dict[str, Any]:
    return {
        "id": tag.id,
        "name": tag.name,
        "category": tag.category,
    }


class StudentShowcaseProjectListItemDTO:
    """Карточка проекта в списке трека витрины."""

    def __init__(
        self,
        application: ProjectApplication,
        *,
        enrolled_teams_count: int,
    ) -> None:
        self.id = application.id
        self.title = application.title or ""
        self.company = application.company
        self.max_teams = application.recommended_teams_count
        self.enrolled_teams_count = enrolled_teams_count
        self.min_team_members = application.min_team_members
        self.max_team_members = application.max_team_members
        self.tags = [_tag_brief(tag) for tag in application.tags.all()]

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "maxTeams": self.max_teams,
            "enrolledTeamsCount": self.enrolled_teams_count,
            "minTeamMembers": self.min_team_members,
            "maxTeamMembers": self.max_team_members,
            "tags": self.tags,
        }


class StudentShowcaseTrackDTO:
    """Трек с вложенными проектами для витрины."""

    def __init__(self, track: ProjectTrack, projects: list[dict[str, Any]]) -> None:
        self.id = track.id
        self.name = track.name
        self.description = track.description or ""
        self.projects = projects

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "projects": self.projects,
        }


class StudentShowcaseProjectDetailDTO:
    """Детали проекта для студента (без контактов)."""

    def __init__(
        self,
        application: ProjectApplication,
        *,
        track_id: int,
        enrolled_teams_count: int,
        can_enroll: bool,
    ) -> None:
        self.id = application.id
        self.title = application.title or ""
        self.company = application.company
        self.goal = application.goal
        self.barrier = application.barrier
        self.existing_solutions = application.existing_solutions
        self.context = application.context or ""
        self.project_level = application.project_level
        self.tags = [_tag_brief(tag) for tag in application.tags.all()]
        self.max_teams = application.recommended_teams_count
        self.enrolled_teams_count = enrolled_teams_count
        self.min_team_members = application.min_team_members
        self.max_team_members = application.max_team_members
        self.track_id = track_id
        self.can_enroll = can_enroll

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "goal": self.goal,
            "barrier": self.barrier,
            "existingSolutions": self.existing_solutions,
            "context": self.context,
            "projectLevel": self.project_level,
            "tags": self.tags,
            "maxTeams": self.max_teams,
            "enrolledTeamsCount": self.enrolled_teams_count,
            "minTeamMembers": self.min_team_members,
            "maxTeamMembers": self.max_team_members,
            "trackId": self.track_id,
            "canEnroll": self.can_enroll,
        }


class StudentShowcaseEnrollResultDTO:
    """Результат записи команды на проект."""

    def __init__(self, team_semester: TeamSemester) -> None:
        application = team_semester.project_application
        self.team_semester_id = team_semester.id
        self.project_id = application.id if application else None
        self.project_title = (application.title or "") if application else ""

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "teamSemesterId": self.team_semester_id,
            "projectId": self.project_id,
            "projectTitle": self.project_title,
        }
