"""DTO для проектных треков."""

from __future__ import annotations

from typing import Any

from showcase.constants import DEFAULT_MAX_TEAM_MEMBERS, DEFAULT_MIN_TEAM_MEMBERS
from showcase.models import ProjectTrack


class ProjectTrackCreateDTO:
    """DTO для создания проектного трека."""

    def __init__(
        self,
        name: str,
        department_id: int,
        semester_id: int,
        description: str = "",
        min_team_members: int = DEFAULT_MIN_TEAM_MEMBERS,
        max_team_members: int = DEFAULT_MAX_TEAM_MEMBERS,
    ):
        self.name = name
        self.description = description
        self.department_id = department_id
        self.semester_id = semester_id
        self.min_team_members = min_team_members
        self.max_team_members = max_team_members

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectTrackCreateDTO:
        """Создаёт DTO из словаря."""
        return cls(
            name=data["name"],
            department_id=data["department_id"],
            semester_id=data["semester_id"],
            description=data.get("description", ""),
            min_team_members=data.get("minTeamMembers", DEFAULT_MIN_TEAM_MEMBERS),
            max_team_members=data.get("maxTeamMembers", DEFAULT_MAX_TEAM_MEMBERS),
        )


class ProjectTrackUpdateDTO:
    """DTO для обновления проектного трека."""

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        department_id: int | None = None,
        semester_id: int | None = None,
        min_team_members: int | None = None,
        max_team_members: int | None = None,
    ):
        self.name = name
        self.description = description
        self.department_id = department_id
        self.semester_id = semester_id
        self.min_team_members = min_team_members
        self.max_team_members = max_team_members

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectTrackUpdateDTO:
        """Создаёт DTO из словаря."""
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            department_id=data.get("department_id"),
            semester_id=data.get("semester_id"),
            min_team_members=data.get("minTeamMembers"),
            max_team_members=data.get("maxTeamMembers"),
        )

    def to_update_dict(self) -> dict[str, Any]:
        """Возвращает только переданные поля трека для обновления."""
        result: dict[str, Any] = {}
        if self.name is not None:
            result["name"] = self.name
        if self.description is not None:
            result["description"] = self.description
        if self.department_id is not None:
            result["department_id"] = self.department_id
        if self.semester_id is not None:
            result["semester_id"] = self.semester_id
        if self.min_team_members is not None:
            result["min_team_members"] = self.min_team_members
        if self.max_team_members is not None:
            result["max_team_members"] = self.max_team_members
        return result

    def has_team_member_updates(self) -> bool:
        """True, если переданы лимиты размера команды для заявок трека."""
        return self.min_team_members is not None or self.max_team_members is not None


class ProjectTrackGroupItemDTO:
    """DTO группы в проектном треке."""

    def __init__(self, group) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number
        self.students_count = int(getattr(group, "students_count", 0) or 0)
        self.registered_students_count = int(
            getattr(group, "registered_students_count", 0) or 0
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "name": self.name,
            "course_number": self.course_number,
            "students_count": self.students_count,
            "registered_students_count": self.registered_students_count,
        }


class ProjectTrackApplicationItemDTO:
    """DTO заявки в проектном треке."""

    def __init__(self, application) -> None:
        self.id = application.id
        self.title = application.title or ""
        self.print_number = application.print_number or ""
        self.teams_count = application.recommended_teams_count
        self.min_team_members = application.min_team_members
        self.max_team_members = application.max_team_members

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "print_number": self.print_number,
            "teamsCount": self.teams_count,
            "minTeamMembers": self.min_team_members,
            "maxTeamMembers": self.max_team_members,
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
        self.min_team_members = track.min_team_members
        self.max_team_members = track.max_team_members
        self.recommended_teams_count = track.recommended_teams_count
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
            "minTeamMembers": self.min_team_members,
            "maxTeamMembers": self.max_team_members,
            "recommendedTeamsCount": self.recommended_teams_count,
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


class ProjectTrackAddApplicationItemDTO:
    """Элемент добавления заявки в трек."""

    def __init__(
        self,
        application_id: int,
        teams_count: int,
        min_team_members: int,
        max_team_members: int,
    ):
        self.application_id = application_id
        self.teams_count = teams_count
        self.min_team_members = min_team_members
        self.max_team_members = max_team_members


class ProjectTrackAddApplicationsDTO:
    """DTO для добавления заявок в трек."""

    def __init__(self, items: list[ProjectTrackAddApplicationItemDTO]):
        self.items = items

    @classmethod
    def from_items(cls, items: list[dict[str, int]]) -> ProjectTrackAddApplicationsDTO:
        """Создаёт DTO из списка элементов API."""
        parsed = [
            ProjectTrackAddApplicationItemDTO(
                application_id=int(item["id"]),
                teams_count=int(item["teamsCount"]),
                min_team_members=int(item["minTeamMembers"]),
                max_team_members=int(item["maxTeamMembers"]),
            )
            for item in items
        ]
        return cls(parsed)

    @property
    def application_ids(self) -> list[int]:
        """Список id заявок для валидации и привязки."""
        return [item.application_id for item in self.items]

    def teams_count_by_application_id(self) -> dict[int, int]:
        """Карта id заявки → рекомендуемое число команд."""
        return {item.application_id: item.teams_count for item in self.items}

    def min_team_members_by_application_id(self) -> dict[int, int]:
        """Карта id заявки → минимум участников команды."""
        return {item.application_id: item.min_team_members for item in self.items}

    def max_team_members_by_application_id(self) -> dict[int, int]:
        """Карта id заявки → максимум участников команды."""
        return {item.application_id: item.max_team_members for item in self.items}


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
        self.track_composer_comment = application.track_composer_comment or ""
        self.has_track_composer_comment = bool(self.track_composer_comment.strip())
        self.recommended_teams_count = application.recommended_teams_count
        self.min_team_members = application.min_team_members
        self.max_team_members = application.max_team_members

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "print_number": self.print_number,
            "author_name": self.author_name,
            "assigned_groups_count": self.assigned_groups_count,
            "track_composer_comment": self.track_composer_comment,
            "has_track_composer_comment": self.has_track_composer_comment,
            "recommended_teams_count": self.recommended_teams_count,
            "min_team_members": self.min_team_members,
            "max_team_members": self.max_team_members,
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
        self.track_composer_comment = application.track_composer_comment or ""
        self.has_track_composer_comment = bool(self.track_composer_comment.strip())
        self.recommended_teams_count = application.recommended_teams_count
        self.min_team_members = application.min_team_members
        self.max_team_members = application.max_team_members
        self.groups = [ProjectTrackProjectGroupDTO(group).to_dict() for group in groups]

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "id": self.id,
            "title": self.title,
            "print_number": self.print_number,
            "author_name": self.author_name,
            "track_composer_comment": self.track_composer_comment,
            "has_track_composer_comment": self.has_track_composer_comment,
            "recommended_teams_count": self.recommended_teams_count,
            "min_team_members": self.min_team_members,
            "max_team_members": self.max_team_members,
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
