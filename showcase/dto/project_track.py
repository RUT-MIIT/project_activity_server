"""DTO для проектных треков."""

from __future__ import annotations

from typing import Any

from showcase.models import ProjectTrack


class ProjectTrackCreateDTO:
    """DTO для создания проектного трека."""

    def __init__(
        self,
        name: str,
        department_id: int,
        semester_id: int,
        description: str = "",
        max_teams: int = 100,
    ):
        self.name = name
        self.description = description
        self.department_id = department_id
        self.semester_id = semester_id
        self.max_teams = max_teams

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectTrackCreateDTO:
        """Создаёт DTO из словаря."""
        return cls(
            name=data["name"],
            department_id=data["department_id"],
            semester_id=data["semester_id"],
            description=data.get("description", ""),
            max_teams=data.get("max_teams", 100),
        )


class ProjectTrackUpdateDTO:
    """DTO для обновления проектного трека."""

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        department_id: int | None = None,
        semester_id: int | None = None,
        max_teams: int | None = None,
    ):
        self.name = name
        self.description = description
        self.department_id = department_id
        self.semester_id = semester_id
        self.max_teams = max_teams

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectTrackUpdateDTO:
        """Создаёт DTO из словаря."""
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            department_id=data.get("department_id"),
            semester_id=data.get("semester_id"),
            max_teams=data.get("max_teams"),
        )

    def to_update_dict(self) -> dict[str, Any]:
        """Возвращает только переданные поля для обновления."""
        result: dict[str, Any] = {}
        if self.name is not None:
            result["name"] = self.name
        if self.description is not None:
            result["description"] = self.description
        if self.department_id is not None:
            result["department_id"] = self.department_id
        if self.semester_id is not None:
            result["semester_id"] = self.semester_id
        if self.max_teams is not None:
            result["max_teams"] = self.max_teams
        return result


class ProjectTrackGroupItemDTO:
    """DTO группы в проектном треке."""

    def __init__(self, group) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "name": self.name,
            "course_number": self.course_number,
        }


class ProjectTrackApplicationItemDTO:
    """DTO заявки в проектном треке."""

    def __init__(self, application) -> None:
        self.id = application.id
        self.title = application.title or ""
        self.print_number = application.print_number or ""

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "print_number": self.print_number,
        }


class ProjectTrackReadDTO:
    """DTO для чтения проектного трека."""

    def __init__(self, track: ProjectTrack, *, include_relations: bool = True) -> None:
        self.id = track.id
        self.name = track.name
        self.description = track.description
        self.department_id = track.department_id
        self.semester_id = track.semester_id
        self.author_id = track.author_id
        self.max_teams = track.max_teams
        self.groups: list[dict[str, Any]] = []
        self.applications: list[dict[str, Any]] = []

        if include_relations:
            for link in track.group_links.all():
                self.groups.append(ProjectTrackGroupItemDTO(link.study_group).to_dict())

            for link in track.application_links.all():
                self.applications.append(
                    ProjectTrackApplicationItemDTO(link.project_application).to_dict()
                )

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "department_id": self.department_id,
            "semester_id": self.semester_id,
            "author_id": self.author_id,
            "max_teams": self.max_teams,
            "groups": self.groups,
            "applications": self.applications,
        }


class ProjectTrackAddGroupsDTO:
    """DTO для добавления групп в трек."""

    def __init__(self, group_ids: list[int]):
        self.group_ids = group_ids

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectTrackAddGroupsDTO:
        """Создаёт DTO из словаря."""
        return cls(group_ids=data["group_ids"])


class ProjectTrackAddApplicationsDTO:
    """DTO для добавления заявок в трек."""

    def __init__(self, application_ids: list[int]):
        self.application_ids = application_ids

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectTrackAddApplicationsDTO:
        """Создаёт DTO из словаря."""
        return cls(application_ids=data["application_ids"])


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


class ProjectTrackProjectListDTO:
    """DTO проекта со счётчиком назначенных групп."""

    def __init__(self, application) -> None:
        self.id = application.id
        self.title = application.title or ""
        self.print_number = application.print_number or ""
        self.author_name = (
            f"{application.author_lastname} {application.author_firstname}".strip()
        )
        self.assigned_groups_count = application.assigned_groups_count

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "print_number": self.print_number,
            "author_name": self.author_name,
            "assigned_groups_count": self.assigned_groups_count,
        }


class ProjectTrackProjectGroupDTO:
    """DTO группы в деталях проекта."""

    def __init__(self, group) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number
        self.direction = {
            "code": group.direction.code,
            "level": group.direction.level,
            "name": group.direction.name,
        }

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "name": self.name,
            "course_number": self.course_number,
            "direction": self.direction,
        }


class ProjectTrackProjectDetailDTO:
    """DTO деталей проекта с назначенными группами."""

    def __init__(self, application, groups: list) -> None:
        self.id = application.id
        self.title = application.title or ""
        self.print_number = application.print_number or ""
        self.author_name = (
            f"{application.author_lastname} {application.author_firstname}".strip()
        )
        self.groups = [ProjectTrackProjectGroupDTO(group).to_dict() for group in groups]

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "print_number": self.print_number,
            "author_name": self.author_name,
            "groups": self.groups,
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


class ProjectTrackInstituteStatisticsDTO(ProjectTrackStatisticsDTO):
    """DTO статистики по одному институту."""

    def __init__(
        self,
        institute_code: str,
        institute_name: str,
        total_projects: int,
        distributed_projects: int,
        average_projects_per_group: float,
        groups_without_projects: int,
    ) -> None:
        super().__init__(
            total_projects=total_projects,
            distributed_projects=distributed_projects,
            average_projects_per_group=average_projects_per_group,
            groups_without_projects=groups_without_projects,
        )
        self.institute_code = institute_code
        self.institute_name = institute_name

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "institute_code": self.institute_code,
            "institute_name": self.institute_name,
            **super().to_dict(),
        }


class ProjectTrackAggregatedStatisticsDTO:
    """DTO агрегированной статистики по всем институтам."""

    def __init__(
        self,
        overall: dict[str, int | float],
        by_institute: list[dict[str, int | float | str]],
    ) -> None:
        self.overall = overall
        self.by_institute = by_institute

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "overall": ProjectTrackStatisticsDTO(**self.overall).to_dict(),
            "by_institute": [
                ProjectTrackInstituteStatisticsDTO(
                    institute_code=str(item["institute_code"]),
                    institute_name=str(item["institute_name"]),
                    total_projects=int(item["total_projects"]),
                    distributed_projects=int(item["distributed_projects"]),
                    average_projects_per_group=float(
                        item["average_projects_per_group"]
                    ),
                    groups_without_projects=int(item["groups_without_projects"]),
                ).to_dict()
                for item in self.by_institute
            ],
        }
