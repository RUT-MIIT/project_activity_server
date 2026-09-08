"""Репозиторий выборок API ответственного по институтам (без N+1)."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch

from accounts.models import PreRegisteredStudent
from showcase.models import Institute, InstituteSemesterSettings
from teams.models import StudyGroupSemester, TeamSemester, TeamSemesterMember

User = get_user_model()


class InstituteResponsibleRepository:
    """Выборки команд, студентов и настроек регистрации института."""

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
    ) -> list[PreRegisteredStudent]:
        """Контингент института с командой/проектом и наставниками группы."""
        membership_qs = TeamSemesterMember.objects.filter(
            semester_id=semester_id
        ).select_related(
            "team_semester__team",
            "team_semester__project_application",
        )
        return list(
            PreRegisteredStudent.objects.filter(
                group__institute_id=institute_code,
                group__is_end=False,
            )
            .select_related("user", "group")
            .prefetch_related(
                Prefetch(
                    "user__team_semester_memberships",
                    queryset=membership_qs,
                    to_attr="_team_membership_for_semester",
                ),
                Prefetch(
                    "group__semester_enrollments",
                    queryset=self._semester_enrollment_qs(semester_id),
                    to_attr="_semester_enrollments_for_semester",
                ),
            )
            .order_by("group__name", "last_name", "first_name", "id")
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
