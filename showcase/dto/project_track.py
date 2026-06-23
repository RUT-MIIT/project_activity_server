"""DTO для проектных треков."""

from __future__ import annotations

from typing import Any

from showcase.models import ProjectTrack


class ProjectTrackAssignDTO:
    """DTO для массового назначения групп на проекты."""

    def __init__(
        self,
        semester_id: int,
        group_ids: list[int],
        project_application_ids: list[int],
    ):
        self.semester_id = semester_id
        self.group_ids = group_ids
        self.project_application_ids = project_application_ids

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectTrackAssignDTO:
        """Создаёт DTO из словаря."""
        return cls(
            semester_id=data["semester_id"],
            group_ids=data["group_ids"],
            project_application_ids=data["project_application_ids"],
        )


class ProjectTrackReadDTO:
    """DTO для чтения проектного трека."""

    def __init__(self, track: ProjectTrack):
        self.id = track.id
        self.semester_id = track.semester_id
        self.group_id = track.study_group_id
        self.group_name = track.study_group.name
        self.project_application_id = track.project_application_id
        self.project_title = track.project_application.title or ""

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "semester_id": self.semester_id,
            "group_id": self.group_id,
            "group_name": self.group_name,
            "project_application_id": self.project_application_id,
            "project_title": self.project_title,
        }


class ProjectTrackDeleteDTO:
    """DTO для удаления связки группа — проект."""

    def __init__(
        self,
        semester_id: int,
        group_id: int,
        project_application_id: int,
    ):
        self.semester_id = semester_id
        self.group_id = group_id
        self.project_application_id = project_application_id

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectTrackDeleteDTO:
        """Создаёт DTO из словаря."""
        return cls(
            semester_id=data["semester_id"],
            group_id=data["group_id"],
            project_application_id=data["project_application_id"],
        )


class ProjectTrackAssignResultDTO:
    """DTO результата массового назначения."""

    def __init__(self, created: int, skipped: int, total_requested: int):
        self.created = created
        self.skipped = skipped
        self.total_requested = total_requested

    def to_dict(self) -> dict[str, int]:
        """Преобразует DTO в словарь для API."""
        return {
            "created": self.created,
            "skipped": self.skipped,
            "total_requested": self.total_requested,
        }


class ProjectTrackGroupListDTO:
    """DTO группы со счётчиком назначенных проектов."""

    def __init__(self, group) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number
        self.direction = {
            "code": group.direction.code,
            "name": group.direction.name,
        }
        self.assigned_projects_count = group.assigned_projects_count

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "name": self.name,
            "course_number": self.course_number,
            "direction": self.direction,
            "assigned_projects_count": self.assigned_projects_count,
        }


class ProjectTrackGroupProjectDTO:
    """DTO проекта в деталях группы."""

    def __init__(self, application) -> None:
        self.id = application.id
        self.title = application.title or ""
        self.print_number = application.print_number or ""
        self.author_name = (
            f"{application.author_lastname} {application.author_firstname}".strip()
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "print_number": self.print_number,
            "author_name": self.author_name,
        }


class ProjectTrackGroupDetailDTO:
    """DTO деталей группы с назначенными проектами."""

    def __init__(self, group, applications: list) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number
        self.direction = {
            "code": group.direction.code,
            "level": group.direction.level,
            "name": group.direction.name,
        }
        self.projects = [
            ProjectTrackGroupProjectDTO(app).to_dict() for app in applications
        ]

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "name": self.name,
            "course_number": self.course_number,
            "direction": self.direction,
            "projects": self.projects,
        }


class ProjectTrackStatisticsDTO:
    """DTO статистики распределения проектов по группам."""

    def __init__(
        self,
        total_projects: int,
        distributed_projects: int,
        average_projects_per_group: float,
        groups_without_projects: int,
    ) -> None:
        self.total_projects = total_projects
        self.distributed_projects = distributed_projects
        self.average_projects_per_group = average_projects_per_group
        self.groups_without_projects = groups_without_projects

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "total_projects": self.total_projects,
            "distributed_projects": self.distributed_projects,
            "average_projects_per_group": self.average_projects_per_group,
            "groups_without_projects": self.groups_without_projects,
        }
