"""Репозиторий выборок API ответственного по институтам (без N+1)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch

from showcase.models import Institute, InstituteSemesterSettings
from teams.domain.contingent_student import ContingentStudent
from teams.domain.institute_access import get_department_ids_by_institute_code
from teams.models import (
    StudyGroup,
    StudyGroupSemester,
    TeamSemester,
    TeamSemesterMember,
)
from teams.repositories.contingent_student import ContingentStudentRepository
from teams.repositories.mentor_groups import MentorGroupsRepository

User = get_user_model()


class InstituteResponsibleRepository:
    """Выборки команд, студентов и настроек регистрации института."""

    def __init__(self) -> None:
        self._mentor_groups_repository = MentorGroupsRepository()
        self._contingent_repository = ContingentStudentRepository()

    def _mentors_only_qs(self):
        """QuerySet наставников с полями для ФИО."""
        return User.objects.only(
            "id", "last_name", "first_name", "middle_name", "email"
        ).order_by("id")

    def _semester_enrollment_qs(self, semester_id: int):
        """StudyGroupSemester семестра с prefetch наставников."""
        return StudyGroupSemester.objects.filter(
            semester_id=semester_id
        ).prefetch_related(Prefetch("mentors", queryset=self._mentors_only_qs()))

    def list_active_institute_codes(self) -> list[str]:
        """Коды всех активных институтов."""
        return list(
            Institute.objects.filter(is_active=True)
            .order_by("position", "code")
            .values_list("code", flat=True)
        )

    def build_department_institute_map(
        self, institute_codes: list[str]
    ) -> dict[int, dict[str, str]]:
        """Карта department_id → {id: code, name} для институтов."""
        if not institute_codes:
            return {}
        by_code = get_department_ids_by_institute_code(institute_codes)
        institutes = {
            item.code: item
            for item in Institute.objects.filter(
                code__in=institute_codes, is_active=True
            ).only("code", "name")
        }
        result: dict[int, dict[str, str]] = {}
        for code, department_ids in by_code.items():
            institute = institutes.get(code)
            if institute is None:
                continue
            snapshot = {"id": institute.code, "name": institute.name}
            for department_id in department_ids:
                result[department_id] = snapshot
        return result

    def list_mentors_by_departments(
        self, department_ids: set[int]
    ) -> list[User]:
        """Пользователи с ролью mentor в указанных подразделениях."""
        if not department_ids:
            return []
        return list(
            User.objects.filter(
                department_id__in=department_ids,
                role__code="mentor",
            )
            .select_related("role")
            .only(
                "id",
                "last_name",
                "first_name",
                "middle_name",
                "email",
                "department_id",
                "role_id",
            )
            .order_by("last_name", "first_name", "id")
        )

    def get_mentor_by_id(self, mentor_id: int) -> User | None:
        """Наставник по id или None."""
        return (
            User.objects.filter(pk=mentor_id, role__code="mentor")
            .select_related("role")
            .only(
                "id",
                "last_name",
                "first_name",
                "middle_name",
                "email",
                "department_id",
                "role_id",
            )
            .first()
        )

    def list_mentor_group_links(
        self, *, mentor_ids: list[int], semester_id: int
    ) -> dict[int, list[int]]:
        """mentor_id → упорядоченный список group_id назначений в семестре."""
        if not mentor_ids:
            return {}
        rows = (
            StudyGroupSemester.objects.filter(
                semester_id=semester_id,
                mentors__id__in=mentor_ids,
                study_group__is_end=False,
            )
            .order_by("study_group__name", "study_group_id")
            .values_list("mentors__id", "study_group_id")
        )
        result: dict[int, list[int]] = defaultdict(list)
        seen: dict[int, set[int]] = defaultdict(set)
        for mentor_id, group_id in rows:
            if group_id in seen[mentor_id]:
                continue
            seen[mentor_id].add(group_id)
            result[mentor_id].append(group_id)
        return dict(result)

    def list_groups_with_counts(
        self, group_ids: set[int] | list[int], semester_id: int
    ) -> list[StudyGroup]:
        """Группы со счётчиками студентов и команд в семестре."""
        ids = set(group_ids)
        if not ids:
            return []
        return list(
            self._mentor_groups_repository._with_counts(
                StudyGroup.objects.filter(id__in=ids).only(
                    "id", "name", "course_number", "institute_id"
                ),
                semester_id,
            ).order_by("name")
        )

    def list_students_for_groups(
        self, group_ids: set[int] | list[int], semester_id: int
    ) -> list[ContingentStudent]:
        """Контингент групп с проектом команды и наставниками группы (батч)."""
        return self._contingent_repository.list_for_groups(
            group_ids,
            semester_id,
            with_project=True,
            enrollment_qs=self._semester_enrollment_qs(semester_id),
        )

    def list_team_semesters_for_groups(
        self, group_ids: set[int] | list[int], semester_id: int
    ) -> list[TeamSemester]:
        """Команды групп в семестре с участниками, проектом и наставниками (без N+1)."""
        ids = set(group_ids)
        if not ids:
            return []
        return list(
            TeamSemester.objects.filter(
                semester_id=semester_id,
                team__home_study_group_id__in=ids,
            )
            .select_related(
                "team",
                "team__home_study_group",
                "project_application",
                "mentor",
            )
            .annotate(members_count=Count("members", distinct=True))
            .prefetch_related(
                Prefetch(
                    "members",
                    queryset=TeamSemesterMember.objects.select_related(
                        "user",
                        "user__study_group",
                    ).order_by("role", "joined_at", "id"),
                ),
                Prefetch("mentors", queryset=self._mentors_only_qs()),
            )
            .order_by("team__home_study_group_id", "team__name", "id")
        )

    def list_team_semesters_for_projects(
        self,
        *,
        project_ids: list[int] | set[int],
        semester_id: int,
    ) -> dict[int, list[TeamSemester]]:
        """Команды по заявкам в семестре: project_id → [TeamSemester] без N+1."""
        ids = set(project_ids)
        if not ids:
            return {}

        mentors_qs = User.objects.only(
            "id", "last_name", "first_name", "middle_name", "email"
        ).order_by("id")
        team_semesters = list(
            TeamSemester.objects.filter(
                semester_id=semester_id,
                project_application_id__in=ids,
            )
            .select_related(
                "team",
                "team__home_study_group",
                "team__home_study_group__institute",
                "mentor",
                "project_application",
            )
            .prefetch_related(
                Prefetch(
                    "members",
                    queryset=TeamSemesterMember.objects.select_related(
                        "user",
                        "user__study_group",
                        "user__study_group__institute",
                    ).order_by("role", "joined_at", "id"),
                ),
                Prefetch("mentors", queryset=mentors_qs),
            )
            .order_by("project_application_id", "team__name", "id")
        )

        result: dict[int, list[TeamSemester]] = defaultdict(list)
        for team_semester in team_semesters:
            result[team_semester.project_application_id].append(team_semester)
        return dict(result)

    def list_institute_team_semesters(
        self,
        *,
        institute_code: str,
        semester_id: int,
    ) -> list[TeamSemester]:
        """Команды института в семестре со счётчиком участников и наставниками."""
        return list(
            TeamSemester.objects.filter(
                semester_id=semester_id,
                team__home_study_group__institute_id=institute_code,
                team__home_study_group__is_end=False,
            )
            .select_related(
                "team",
                "team__home_study_group",
                "project_application",
            )
            .annotate(members_count=Count("members", distinct=True))
            .prefetch_related(
                Prefetch(
                    "team__home_study_group__semester_enrollments",
                    queryset=self._semester_enrollment_qs(semester_id),
                    to_attr="_semester_enrollments_for_semester",
                )
            )
            .order_by("team__name", "id")
        )

    def get_institute_team_semester_detail(
        self,
        *,
        team_semester_id: int,
        institute_code: str,
        semester_id: int,
    ) -> TeamSemester | None:
        """Детали команды института в семестре (капитан, участники) или None."""
        return (
            TeamSemester.objects.filter(
                pk=team_semester_id,
                semester_id=semester_id,
                team__home_study_group__institute_id=institute_code,
                team__home_study_group__is_end=False,
            )
            .select_related(
                "team",
                "team__home_study_group",
                "project_application",
                "captain",
            )
            .annotate(members_count=Count("members", distinct=True))
            .prefetch_related(
                Prefetch(
                    "team__home_study_group__semester_enrollments",
                    queryset=self._semester_enrollment_qs(semester_id),
                    to_attr="_semester_enrollments_for_semester",
                ),
                Prefetch(
                    "members",
                    queryset=TeamSemesterMember.objects.select_related("user").order_by(
                        "role", "joined_at", "id"
                    ),
                ),
            )
            .first()
        )

    def list_institute_students(
        self,
        *,
        institute_code: str,
        semester_id: int,
    ) -> list[ContingentStudent]:
        """Контингент института: предрегистрация и прямые студенты."""
        return ContingentStudentRepository().list_for_institute(
            institute_code=institute_code,
            semester_id=semester_id,
            enrollment_qs=self._semester_enrollment_qs(semester_id),
        )

    def list_active_institutes(self) -> list[Institute]:
        """Активные институты, отсортированные по позиции."""
        return list(
            Institute.objects.filter(is_active=True)
            .only("code", "name", "position")
            .order_by("position", "code")
        )

    def list_semester_settings(
        self, semester_id: int
    ) -> list[InstituteSemesterSettings]:
        """Все настройки институтов для семестра."""
        return list(
            InstituteSemesterSettings.objects.filter(semester_id=semester_id).only(
                "id",
                "institute_id",
                "semester_id",
                "registration_opens_at",
                "closed_by_decision",
            )
        )

    def get_settings(
        self,
        *,
        institute_code: str,
        semester_id: int,
    ) -> InstituteSemesterSettings | None:
        """Настройки института в семестре или None."""
        return (
            InstituteSemesterSettings.objects.filter(
                institute_id=institute_code,
                semester_id=semester_id,
            )
            .only(
                "id",
                "institute_id",
                "semester_id",
                "registration_opens_at",
                "closed_by_decision",
            )
            .first()
        )

    def update_settings(
        self,
        *,
        institute_code: str,
        semester_id: int,
        fields: dict[str, Any],
    ) -> InstituteSemesterSettings:
        """Частичный upsert настроек института в семестре."""
        defaults: dict[str, Any] = {}
        if "registration_opens_at" in fields:
            defaults["registration_opens_at"] = fields["registration_opens_at"]
        if "closed_by_decision" in fields:
            defaults["closed_by_decision"] = fields["closed_by_decision"]

        settings_obj, created = InstituteSemesterSettings.objects.get_or_create(
            institute_id=institute_code,
            semester_id=semester_id,
            defaults={
                "registration_opens_at": defaults.get("registration_opens_at"),
                "closed_by_decision": defaults.get("closed_by_decision", False),
            },
        )
        if created:
            return settings_obj

        update_fields: list[str] = []
        if "registration_opens_at" in fields:
            settings_obj.registration_opens_at = fields["registration_opens_at"]
            update_fields.append("registration_opens_at")
        if "closed_by_decision" in fields:
            settings_obj.closed_by_decision = fields["closed_by_decision"]
            update_fields.append("closed_by_decision")
        if update_fields:
            settings_obj.save(update_fields=update_fields)
        return settings_obj
