"""Сервис API ответственного по институтам."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Semester
from showcase.models import Institute, ProjectApplication
from teams.domain.contingent_student import ContingentStudent
from teams.domain.institute_access import (
    get_accessible_institute_codes,
    get_department_ids_for_institute_codes,
)
from teams.domain.institute_responsible import InstituteResponsibleDomain
from teams.domain.institute_students_excel import (
    build_students_xlsx,
    format_author_full_name,
)
from teams.dto.institute_responsible import (
    InstituteResponsibleAssignMentorDTO,
    InstituteResponsibleEmployeeDTO,
    InstituteResponsibleGroupDTO,
    InstituteResponsibleGroupMentorsDTO,
    InstituteResponsibleRegistrationSettingsDTO,
    InstituteResponsibleStudentDTO,
    InstituteResponsibleTeamDetailDTO,
    InstituteResponsibleTeamListItemDTO,
)
from showcase.domain.project import ProjectDomain
from showcase.domain.project_institute import resolve_application_institute
from showcase.repositories.project import ProjectRepository
from teams.dto.institute_responsible_mentors_stats import (
    MentorsStatsDetailDTO,
    MentorsStatsListItemDTO,
)
from teams.dto.institute_responsible_groups_stats import (
    GroupsStatsDetailDTO,
    GroupsStatsListItemDTO,
)
from teams.dto.institute_responsible_projects_stats import (
    ProjectsStatsDetailDTO,
    ProjectsStatsListItemDTO,
)
from teams.dto.institute_responsible_students_stats import StudentsStatsStudentDTO
from teams.dto.mentor_groups import MentorGroupListDTO
from teams.models import TeamSemester, TeamSemesterMember
from teams.repositories.institute_responsible import InstituteResponsibleRepository
from teams.repositories.mentor_groups import MentorGroupsRepository
from teams.repositories.study_group_semester import StudyGroupSemesterRepository

User = get_user_model()


class InstituteResponsibleService:
    """Оркестрация назначения наставников группам по семестрам."""

    def __init__(self) -> None:
        self.repository = StudyGroupSemesterRepository()
        self.groups_overview_repository = MentorGroupsRepository()
        self.institute_repository = InstituteResponsibleRepository()
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
        """Валидирует доступ; возвращает semester_id, institute_code, codes."""
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

    def list_groups_overview(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Список активных групп института со счётчиками контингента и команд."""
        semester_id, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        groups = list(
            self.groups_overview_repository.list_for_institutes(
                [resolved_institute_code], semester_id
            )
        )
        return MentorGroupListDTO(groups).to_list()

    def list_employees(
        self,
        user: User,
        institute_code: str | None,
    ) -> list[dict[str, Any]]:
        """Список сотрудников института."""
        _, department_ids = self._resolve_institute_only(user, institute_code)
        employees = self.repository.list_employees(department_ids)
        return [InstituteResponsibleEmployeeDTO(emp).to_dict() for emp in employees]

    def _resolve_accessible_institute_codes(self, user: User) -> list[str]:
        """Коды институтов для multi-institute выборки mentors stats."""
        codes = get_accessible_institute_codes(user)
        if codes is None:
            return self.institute_repository.list_active_institute_codes()
        return list(codes)

    def _resolve_mentors_stats_context(
        self, user: User, semester_id_raw: str
    ) -> tuple[int, list[str], set[int], dict[int, dict[str, str]]]:
        """Семестр, коды институтов, department_ids и карта department→institute."""
        self._check_access(user)
        self.domain.ensure_user_department(user)
        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        institute_codes = self._resolve_accessible_institute_codes(user)
        department_ids = get_department_ids_for_institute_codes(institute_codes)
        department_institute_map = (
            self.institute_repository.build_department_institute_map(institute_codes)
        )
        return semester_id, institute_codes, department_ids, department_institute_map

    @staticmethod
    def _institute_by_code_from_dept_map(
        department_institute_map: dict[int, dict[str, str]],
    ) -> dict[str, dict[str, str]]:
        """Уникальные институты из карты подразделений."""
        result: dict[str, dict[str, str]] = {}
        for snapshot in department_institute_map.values():
            result[snapshot["id"]] = snapshot
        return result

    def list_mentors_stats(
        self,
        user: User,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Лёгкий список наставников по доступным институтам в семестре."""
        (
            semester_id,
            _,
            department_ids,
            department_institute_map,
        ) = self._resolve_mentors_stats_context(user, semester_id_raw)

        mentors = self.institute_repository.list_mentors_by_departments(department_ids)
        mentor_ids = [mentor.id for mentor in mentors]
        links = self.institute_repository.list_mentor_group_links(
            mentor_ids=mentor_ids, semester_id=semester_id
        )
        all_group_ids: set[int] = set()
        for group_ids in links.values():
            all_group_ids.update(group_ids)
        groups = self.institute_repository.list_groups_with_counts(
            all_group_ids, semester_id
        )
        groups_by_id = {group.id: group for group in groups}

        empty_institute = {"id": "", "name": ""}
        result: list[dict[str, Any]] = []
        for mentor in mentors:
            institute = department_institute_map.get(
                mentor.department_id, empty_institute
            )
            mentor_groups = [
                groups_by_id[group_id]
                for group_id in links.get(mentor.id, [])
                if group_id in groups_by_id
            ]
            result.append(
                MentorsStatsListItemDTO(
                    mentor,
                    institute=institute,
                    groups=mentor_groups,
                ).to_dict()
            )
        return result

    def get_mentor_stats_detail(
        self,
        user: User,
        mentor_id: int,
        semester_id_raw: str,
    ) -> dict[str, Any]:
        """Детальная карточка наставника со студентами и командами групп."""
        (
            semester_id,
            _,
            department_ids,
            department_institute_map,
        ) = self._resolve_mentors_stats_context(user, semester_id_raw)

        mentor = self.institute_repository.get_mentor_by_id(mentor_id)
        if mentor is None or mentor.department_id not in department_ids:
            raise LookupError(f"Наставник с id={mentor_id} не найден")

        institute = department_institute_map.get(
            mentor.department_id, {"id": "", "name": ""}
        )
        links = self.institute_repository.list_mentor_group_links(
            mentor_ids=[mentor.id], semester_id=semester_id
        )
        group_ids = links.get(mentor.id, [])
        groups = self.institute_repository.list_groups_with_counts(
            group_ids, semester_id
        )
        groups_by_id = {group.id: group for group in groups}
        ordered_groups = [
            groups_by_id[group_id]
            for group_id in group_ids
            if group_id in groups_by_id
        ]

        students = self.institute_repository.list_students_for_groups(
            group_ids, semester_id
        )
        students_by_group: dict[int, list] = {}
        for student in students:
            if student.group is None:
                continue
            students_by_group.setdefault(student.group.id, []).append(student)

        team_semesters = self.institute_repository.list_team_semesters_for_groups(
            group_ids, semester_id
        )
        teams_by_group: dict[int, list[TeamSemester]] = {}
        for team_semester in team_semesters:
            home_group = team_semester.team.home_study_group
            if home_group is None:
                continue
            teams_by_group.setdefault(home_group.id, []).append(team_semester)

        institute_by_code = self._institute_by_code_from_dept_map(
            department_institute_map
        )
        return MentorsStatsDetailDTO(
            mentor,
            institute=institute,
            groups=ordered_groups,
            students_by_group=students_by_group,
            teams_by_group=teams_by_group,
            institute_by_code=institute_by_code,
        ).to_dict()

    def list_projects_stats(
        self,
        user: User,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Список одобренных проектов семестра с краткими командами."""
        (
            semester_id,
            _,
            _,
            department_institute_map,
        ) = self._resolve_mentors_stats_context(user, semester_id_raw)

        institute_codes = ProjectDomain.get_institute_codes_for_user(user)
        applications = list(
            ProjectRepository().filter_projects_queryset(institute_codes, semester_id)
        )
        project_ids = [application.id for application in applications]
        teams_by_project = self.institute_repository.list_team_semesters_for_projects(
            project_ids=project_ids,
            semester_id=semester_id,
        )

        result: list[dict[str, Any]] = []
        for application in applications:
            institute = resolve_application_institute(
                application, department_institute_map
            )
            result.append(
                ProjectsStatsListItemDTO(
                    application,
                    institute=institute,
                    teams=teams_by_project.get(application.id, []),
                ).to_dict()
            )
        return result

    def get_project_stats_detail(
        self,
        user: User,
        project_id: int,
        semester_id_raw: str,
    ) -> dict[str, Any]:
        """Детальная карточка проекта с командами, участниками и наставниками."""
        (
            semester_id,
            _,
            _,
            department_institute_map,
        ) = self._resolve_mentors_stats_context(user, semester_id_raw)

        institute_codes = ProjectDomain.get_institute_codes_for_user(user)
        application = (
            ProjectRepository()
            .filter_projects_queryset(institute_codes, semester_id)
            .filter(pk=project_id)
            .first()
        )
        if application is None:
            raise LookupError(f"Проект с id={project_id} не найден")

        teams_by_project = self.institute_repository.list_team_semesters_for_projects(
            project_ids=[application.id],
            semester_id=semester_id,
        )
        teams = teams_by_project.get(application.id, [])
        institute = resolve_application_institute(
            application, department_institute_map
        )
        institute_by_code = self._institute_by_code_from_dept_map(
            department_institute_map
        )
        return ProjectsStatsDetailDTO(
            application,
            institute=institute,
            teams=teams,
            institute_by_code=institute_by_code,
        ).to_dict()

    def list_groups_stats(
        self,
        user: User,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Список активных учебных групп по доступным институтам в семестре."""
        (
            semester_id,
            institute_codes,
            _,
            department_institute_map,
        ) = self._resolve_mentors_stats_context(user, semester_id_raw)

        groups = list(
            self.groups_overview_repository.list_for_institutes(
                institute_codes, semester_id
            )
        )
        group_ids = [group.id for group in groups]
        team_semesters = self.institute_repository.list_team_semesters_for_groups(
            group_ids, semester_id
        )
        teams_by_group: dict[int, list[TeamSemester]] = {}
        for team_semester in team_semesters:
            home_group = team_semester.team.home_study_group
            if home_group is None:
                continue
            teams_by_group.setdefault(home_group.id, []).append(team_semester)

        institute_by_code = self._institute_by_code_from_dept_map(
            department_institute_map
        )
        empty_institute = {"id": "", "name": ""}
        result: list[dict[str, Any]] = []
        for group in groups:
            code = group.institute_id or ""
            institute = institute_by_code.get(
                code, {"id": code, "name": ""} if code else empty_institute
            )
            result.append(
                GroupsStatsListItemDTO(
                    group,
                    institute=institute,
                    teams=teams_by_group.get(group.id, []),
                ).to_dict()
            )
        return result

    def get_group_stats_detail(
        self,
        user: User,
        group_id: int,
        semester_id_raw: str,
    ) -> dict[str, Any]:
        """Детальная карточка учебной группы со студентами и командами."""
        (
            semester_id,
            institute_codes,
            _,
            department_institute_map,
        ) = self._resolve_mentors_stats_context(user, semester_id_raw)

        group = self.groups_overview_repository.get_group_header(group_id)
        accessible_codes = set(institute_codes)
        if (
            group is None
            or group.is_end
            or (group.institute_id or "") not in accessible_codes
        ):
            raise LookupError(f"Группа с id={group_id} не найдена")

        institute_by_code = self._institute_by_code_from_dept_map(
            department_institute_map
        )
        code = group.institute_id or ""
        institute = institute_by_code.get(code, {"id": code, "name": ""})

        students = self.institute_repository.list_students_for_groups(
            {group.id}, semester_id
        )
        teams = self.institute_repository.list_team_semesters_for_groups(
            {group.id}, semester_id
        )
        return GroupsStatsDetailDTO(
            group,
            institute=institute,
            students=students,
            teams=teams,
            institute_by_code=institute_by_code,
        ).to_dict()

    def list_students_stats(
        self,
        user: User,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Список студентов контингента по доступным институтам в семестре."""
        (
            semester_id,
            institute_codes,
            _,
            department_institute_map,
        ) = self._resolve_mentors_stats_context(user, semester_id_raw)

        groups = list(
            self.groups_overview_repository.list_for_institutes(
                institute_codes, semester_id
            )
        )
        group_ids = [group.id for group in groups]
        students = self.institute_repository.list_students_for_groups(
            group_ids, semester_id
        )
        institute_by_code = self._institute_by_code_from_dept_map(
            department_institute_map
        )
        return [
            StudentsStatsStudentDTO(student, institute_by_code).to_dict()
            for student in students
        ]

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

    def list_teams(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Список команд института в семестре."""
        semester_id, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        team_semesters = self.institute_repository.list_institute_team_semesters(
            institute_code=resolved_institute_code,
            semester_id=semester_id,
        )
        return [
            InstituteResponsibleTeamListItemDTO(item).to_dict()
            for item in team_semesters
        ]

    def get_team(
        self,
        user: User,
        team_semester_id: int,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> dict[str, Any]:
        """Подробности команды института в семестре."""
        semester_id, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        team_semester = self.institute_repository.get_institute_team_semester_detail(
            team_semester_id=team_semester_id,
            institute_code=resolved_institute_code,
            semester_id=semester_id,
        )
        if team_semester is None:
            raise LookupError(f"Команда с id={team_semester_id} не найдена")
        return InstituteResponsibleTeamDetailDTO(team_semester).to_dict()

    def list_students(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> list[dict[str, Any]]:
        """Список студентов (контингент) института в семестре."""
        semester_id, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        students = self.institute_repository.list_institute_students(
            institute_code=resolved_institute_code,
            semester_id=semester_id,
        )
        return [
            InstituteResponsibleStudentDTO(student).to_dict() for student in students
        ]

    @staticmethod
    def _project_application_for_contingent(
        student: ContingentStudent,
    ) -> ProjectApplication | None:
        """Заявка выбранного проекта команды студента контингента, если есть."""
        user = student.user
        if user is None:
            return None
        memberships: list[TeamSemesterMember] = getattr(
            user, "_team_membership_for_semester", []
        )
        if not memberships:
            return None
        return memberships[0].team_semester.project_application

    def _student_dict_for_excel(self, student: ContingentStudent) -> dict[str, Any]:
        """DTO студента с полями заявки только для Excel (JSON API не затрагивает)."""
        data = InstituteResponsibleStudentDTO(student).to_dict()
        application = self._project_application_for_contingent(student)
        if application is None:
            return data
        project = dict(data.get("project") or {})
        project["company"] = application.company or ""
        project["companyContacts"] = application.company_contacts or ""
        project["authorFullName"] = format_author_full_name(
            last_name=application.author_lastname,
            first_name=application.author_firstname,
            middle_name=application.author_middlename,
        )
        data["project"] = project
        return data

    def export_students(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> tuple[bytes, str]:
        """Выгрузка контингента института в Excel для выбранного семестра."""
        semester_id, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        students = self.institute_repository.list_institute_students(
            institute_code=resolved_institute_code,
            semester_id=semester_id,
        )
        payload = [self._student_dict_for_excel(student) for student in students]
        content = build_students_xlsx(payload)
        filename = f"students_{resolved_institute_code}_{semester_id}.xlsx"
        return content, filename

    def get_registration_settings(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
    ) -> dict[str, Any]:
        """Настройки регистрации текущего и других институтов."""
        semester_id, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        return self._build_registration_settings_response(
            resolved_institute_code, semester_id
        )

    def update_registration_settings(
        self,
        user: User,
        institute_code: str | None,
        semester_id_raw: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Частичное обновление настроек регистрации своего института."""
        semester_id, resolved_institute_code, _ = self._resolve_context(
            user, institute_code, semester_id_raw
        )
        fields = self.domain.validate_settings_update_payload(payload)
        with transaction.atomic():
            self.institute_repository.update_settings(
                institute_code=resolved_institute_code,
                semester_id=semester_id,
                fields=fields,
            )
        return self._build_registration_settings_response(
            resolved_institute_code, semester_id
        )

    def _build_registration_settings_response(
        self,
        institute_code: str,
        semester_id: int,
    ) -> dict[str, Any]:
        """Собирает ответ registration-settings без N+1."""
        institutes = self.institute_repository.list_active_institutes()
        current = next(
            (item for item in institutes if item.code == institute_code),
            None,
        )
        if current is None:
            current = Institute.objects.filter(code=institute_code).first()
            if current is None:
                raise ValueError(f"Институт с кодом={institute_code} не найден")

        settings_list = self.institute_repository.list_semester_settings(semester_id)
        settings_by_code = {item.institute_id: item for item in settings_list}
        others = [item for item in institutes if item.code != institute_code]
        return InstituteResponsibleRegistrationSettingsDTO(
            current_institute=current,
            current_settings=settings_by_code.get(institute_code),
            other_institutes=others,
            settings_by_code=settings_by_code,
        ).to_dict()
