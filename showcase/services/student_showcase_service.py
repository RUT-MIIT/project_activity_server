"""Сервис студенческой витрины проектов."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction

from accounts.models import Semester
from showcase.domain.student_showcase import StudentShowcaseDomain
from showcase.dto.student_showcase import (
    StudentShowcaseEnrollResultDTO,
    StudentShowcaseProjectDetailDTO,
    StudentShowcaseProjectListItemDTO,
    StudentShowcaseTrackDTO,
)
from showcase.repositories.student_showcase import StudentShowcaseRepository

if TYPE_CHECKING:
    from accounts.models import User as UserType


class StudentShowcaseService:
    """Оркестрация Domain + Repository для студенческой витрины."""

    def __init__(self) -> None:
        self.repository = StudentShowcaseRepository()
        self.domain = StudentShowcaseDomain()

    def _resolve_semester_id(self, semester_id_raw: str | None) -> int:
        """Резолвит semester_id; по умолчанию actual."""
        return Semester.resolve_list_semester_id(semester_id_raw or "actual")

    def list_tracks(
        self, user: UserType, semester_id_raw: str | None = None
    ) -> list[dict]:
        """Список треков группы студента с проектами и счётчиками записи."""
        group_id = self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)

        tracks = self.repository.list_group_tracks_with_projects(
            group_id=group_id, semester_id=semester_id
        )
        track_ids = [track.id for track in tracks]
        application_ids: list[int] = []
        for track in tracks:
            for link in track.application_links.all():
                application_ids.append(link.project_application_id)

        enrolled_map = self.repository.map_enrolled_teams_counts(
            semester_id=semester_id,
            track_ids=track_ids,
            application_ids=application_ids,
        )

        result: list[dict] = []
        for track in tracks:
            projects: list[dict] = []
            for link in track.application_links.all():
                application = link.project_application
                enrolled = enrolled_map.get((track.id, application.id), 0)
                projects.append(
                    StudentShowcaseProjectListItemDTO(
                        application, enrolled_teams_count=enrolled
                    ).to_dict()
                )
            result.append(StudentShowcaseTrackDTO(track, projects).to_dict())
        return result

    def get_project(
        self,
        user: UserType,
        project_id: int,
        semester_id_raw: str | None = None,
    ) -> dict:
        """Детали проекта, доступного группе студента."""
        group_id = self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)

        accessible = self.repository.get_accessible_project(
            project_id=project_id,
            group_id=group_id,
            semester_id=semester_id,
        )
        if accessible is None:
            raise ValueError(f"Проект с id={project_id} не найден")

        application, track_id = accessible
        enrolled = self.repository.count_enrolled_teams(
            semester_id=semester_id,
            track_id=track_id,
            application_id=application.id,
        )

        team_semester = self.repository.get_user_team_semester(
            user_id=user.id, semester_id=semester_id
        )
        can_enroll = False
        if team_semester is not None:
            members_count = len(list(team_semester.members.all()))
            can_enroll = self.domain.can_enroll(
                is_captain=team_semester.captain_id == user.id,
                status=team_semester.status,
                has_project=team_semester.project_application_id is not None,
                members_count=members_count,
                min_team_members=application.min_team_members,
                max_team_members=application.max_team_members,
                enrolled_count=enrolled,
                max_teams=application.recommended_teams_count,
                project_track_id=team_semester.project_track_id,
                application_track_id=track_id,
            )

        return StudentShowcaseProjectDetailDTO(
            application,
            track_id=track_id,
            enrolled_teams_count=enrolled,
            can_enroll=can_enroll,
        ).to_dict()

    @transaction.atomic
    def enroll(
        self,
        user: UserType,
        project_id: int,
        semester_id_raw: str | None = None,
    ) -> dict:
        """Записывает команду капитана на проект."""
        self.domain.ensure_student_with_group(user)
        semester_id = self._resolve_semester_id(semester_id_raw)

        team_semester = self.repository.get_user_team_semester_for_update(
            user_id=user.id, semester_id=semester_id
        )
        if team_semester is None:
            raise ValueError("Вы не состоите в команде в этом семестре")

        self.domain.ensure_is_captain(user, team_semester)
        self.domain.ensure_team_assembled(team_semester)
        self.domain.ensure_no_project_yet(team_semester)

        if team_semester.project_track_id is None:
            raise ValueError("У команды не указан проектный трек")

        link = self.repository.get_project_track_link(
            project_id=project_id,
            track_id=team_semester.project_track_id,
            semester_id=semester_id,
        )
        if link is None:
            raise ValueError(
                "Проект не найден в треке вашей команды или недоступен для записи"
            )

        application = link.project_application
        self.domain.ensure_project_in_team_track(team_semester, link.project_track_id)

        members_count = len(list(team_semester.members.all()))
        self.domain.ensure_members_fit_project(
            members_count=members_count,
            application=application,
        )

        enrolled = self.repository.count_enrolled_teams_for_update(
            semester_id=semester_id,
            track_id=link.project_track_id,
            application_id=application.id,
        )
        self.domain.ensure_enrollment_slot_available(
            enrolled_count=enrolled,
            max_teams=application.recommended_teams_count,
        )

        team_semester = self.repository.enroll_team(
            team_semester=team_semester,
            application=application,
            actor_id=user.id,
        )
        return StudentShowcaseEnrollResultDTO(team_semester).to_dict()
