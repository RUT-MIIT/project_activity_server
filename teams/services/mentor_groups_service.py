"""Сервис эндпоинта «Мои группы» наставника."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model

from accounts.models import Semester
from teams.domain.mentor_groups import MentorGroupsDomain
from teams.dto.mentor_groups import MentorGroupDetailDTO, MentorGroupListDTO
from teams.dto.my_study_group import MyStudyGroupRegistrationDTO
from teams.repositories.institute_responsible import InstituteResponsibleRepository
from teams.repositories.mentor_groups import MentorGroupsRepository

User = get_user_model()


class MentorGroupsService:
    """Возвращает группы, где текущий пользователь — наставник в семестре."""

    def __init__(self) -> None:
        self.repository = MentorGroupsRepository()
        self.domain = MentorGroupsDomain()
        self.institute_repository = InstituteResponsibleRepository()

    def list_my_groups(
        self, user: User, semester_id_raw: str | None
    ) -> list[dict[str, Any]]:
        """Список групп наставника с количеством студентов и команд."""
        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        groups = list(self.repository.list_for_mentor(user.id, semester_id))
        return MentorGroupListDTO(groups).to_list()

    def get_group_detail(
        self,
        user: User,
        group_id: int,
        semester_id_raw: str | None,
    ) -> dict[str, Any]:
        """Детали группы: студенты контингента и команды в семестре."""
        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        group = self.repository.get_group_header(group_id)
        self.domain.ensure_group_exists(group)
        self.domain.ensure_group_active(group)
        is_mentor = self.repository.is_mentor(user.id, group_id, semester_id)
        self.domain.ensure_group_access(user, group, is_mentor)
        students = self.repository.list_students(group_id, semester_id)
        teams = self.repository.list_teams(group_id, semester_id)
        return MentorGroupDetailDTO(group, students, teams).to_dict()

    def get_registration_settings(
        self, user: User, semester_id_raw: str | None
    ) -> dict[str, Any]:
        """Окно записи института на проекты для наставника в семестре."""
        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        institute_codes = self.repository.list_mentor_institute_codes(
            user.id, semester_id
        )
        institute_code = self.domain.resolve_mentor_institute_code(institute_codes)
        settings = self.institute_repository.get_settings(
            institute_code=institute_code,
            semester_id=semester_id,
        )
        return MyStudyGroupRegistrationDTO(settings).to_dict()
