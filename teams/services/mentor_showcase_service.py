"""Сервис витрины проектов для наставника."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model

from accounts.models import Semester
from showcase.services.student_showcase_service import StudentShowcaseService
from teams.domain.mentor_groups import MentorGroupsDomain
from teams.repositories.mentor_groups import MentorGroupsRepository

User = get_user_model()


class MentorShowcaseService:
    """Витрина проектов учебной группы для назначенного наставника."""

    def __init__(self) -> None:
        self.mentor_repository = MentorGroupsRepository()
        self.domain = MentorGroupsDomain()
        self.showcase_service = StudentShowcaseService()

    def list_project_showcase(
        self,
        user: User,
        group_id: int,
        semester_id_raw: str | None,
    ) -> list[dict[str, Any]]:
        """Список треков с проектами для группы наставника в семестре."""
        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        group = self.mentor_repository.get_group_header(group_id)
        self.domain.ensure_group_exists(group)
        is_mentor = self.mentor_repository.is_mentor(user.id, group_id, semester_id)
        self.domain.ensure_mentor_access(is_mentor)
        return self.showcase_service.list_tracks_for_group(group_id, semester_id)
