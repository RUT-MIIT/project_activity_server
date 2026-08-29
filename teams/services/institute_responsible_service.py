"""Сервис API ответственного по институтам."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Semester
from showcase.models import Institute
from teams.domain.institute_access import get_accessible_institute_codes
from teams.domain.institute_responsible import InstituteResponsibleDomain
from teams.dto.institute_responsible import (
    InstituteResponsibleAssignMentorDTO,
    InstituteResponsibleEmployeeDTO,
    InstituteResponsibleGroupDTO,
    InstituteResponsibleGroupMentorsDTO,
)
from teams.repositories.study_group_semester import StudyGroupSemesterRepository

User = get_user_model()


class InstituteResponsibleService:
    """Оркестрация назначения наставников группам по семестрам."""

    def __init__(self) -> None:
        self.repository = StudyGroupSemesterRepository()
        self.domain = InstituteResponsibleDomain()

    def _check_access(self, user: User) -> None:
        """Проверяет права пользователя."""
        can_access, error = self.domain.can_access(user)
        if not can_access:
            raise PermissionError(error)

    def _resolve_context(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> tuple[int, str, list[str] | None]:
        """Валидирует доступ и возвращает semester_id, institute_code, accessible_codes."""
        self._check_access(user)
        self.domain.ensure_user_department(user)

        resolved_institute_code = self.domain.resolve_institute_code(
            user, institute_code
        )
        if not Institute.objects.filter(code=resolved_institute_code).exists():
            raise ValueError(f"Институт с кодом={resolved_institute_code} не найден")

        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        accessible_codes = get_accessible_institute_codes(user)

        if (
            accessible_codes is not None
            and resolved_institute_code not in accessible_codes
        ):
            raise PermissionError("Недостаточно прав для работы с указанным институтом")

        return semester_id, resolved_institute_code, accessible_codes

    def _resolve_institute_only(
        self,
        user: User,
        institute_code: str | None,
    ) -> tuple[str, set[int]]:
        """Валидирует доступ и возвращает institute_code и department_ids."""
        self._check_access(user)
        self.domain.ensure_user_department(user)

        resolved_institute_code = self.domain.resolve_institute_code(
            user, institute_code
        )
        if not Institute.objects.filter(code=resolved_institute_code).exists():
            raise ValueError(f"Институт с кодом={resolved_institute_code} не найден")

        accessible_codes = get_accessible_institute_codes(user)
        if (
            accessible_codes is not None
            and resolved_institute_code not in accessible_codes
        ):
            raise PermissionError("Недостаточно прав для работы с указанным институтом")

        department_ids = self.domain.get_department_ids_for_user(
            user, resolved_institute_code
        )
        return resolved_institute_code, department_ids

    def _get_validated_group(
        self,
        group_id: int,
        institute_code: str,
        accessible_codes: list[str] | None,
    ):
        """Возвращает группу после проверки доступа."""
        group = self.repository.get_group_by_id(group_id)
        if group is None:
            raise ValueError(f"Учебная группа с id={group_id} не найдена")

        ok, error = self.domain.validate_group_access(
            group, institute_code, accessible_codes
        )
        if not ok:
            raise ValueError(error)

        return group

    def list_groups(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Список активных групп института."""
        _, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        groups = self.repository.list_active_groups(resolved_institute_code)
        return [InstituteResponsibleGroupDTO(group).to_dict() for group in groups]

    def list_employees(
        self,
        user: User,
        institute_code: str | None,
    ) -> list[dict[str, Any]]:
        """Список сотрудников института."""
        _, department_ids = self._resolve_institute_only(user, institute_code)
        employees = self.repository.list_employees(department_ids)
        return [InstituteResponsibleEmployeeDTO(emp).to_dict() for emp in employees]

    def list_group_mentors(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Группы с ID назначенных наставников в семестре."""
        semester_id, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        groups = list(
            self.repository.list_active_groups_with_mentors(
                resolved_institute_code, semester_id
            )
        )
        return InstituteResponsibleGroupMentorsDTO(groups).to_list()

    def assign_mentor(
        self,
        user: User,
        group_id: int,
        mentor_id: int,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> dict[str, Any]:
        """Назначает наставника группе в семестре."""
        semester_id, resolved_institute_code, accessible_codes = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        self._get_validated_group(group_id, resolved_institute_code, accessible_codes)

        department_ids = self.domain.get_department_ids_for_user(
            user, resolved_institute_code
        )
        mentor = self.repository.get_employee_by_id(mentor_id, department_ids)
        if mentor is None:
            raise ValueError(f"Сотрудник с id={mentor_id} не найден в институте")

        with transaction.atomic():
            mentor_ids = self.repository.add_mentor(group_id, semester_id, mentor_id)

        return InstituteResponsibleAssignMentorDTO(
            group_id, semester_id, mentor_ids
        ).to_dict()

    def remove_mentor(
        self,
        user: User,
        group_id: int,
        mentor_id: int,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> dict[str, Any]:
        """Снимает наставника с группы в семестре."""
        semester_id, resolved_institute_code, accessible_codes = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        self._get_validated_group(group_id, resolved_institute_code, accessible_codes)

        department_ids = self.domain.get_department_ids_for_user(
            user, resolved_institute_code
        )
        mentor = self.repository.get_employee_by_id(mentor_id, department_ids)
        if mentor is None:
            raise ValueError(f"Сотрудник с id={mentor_id} не найден в институте")

        with transaction.atomic():
            mentor_ids = self.repository.remove_mentor(group_id, semester_id, mentor_id)

        return InstituteResponsibleAssignMentorDTO(
            group_id, semester_id, mentor_ids
        ).to_dict()
