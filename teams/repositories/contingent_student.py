"""Репозиторий контингента: предрегистрация + прямые студенты без N+1."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q

from accounts.models import PreRegisteredStudent
from teams.domain.contingent_student import ContingentStudent, merge_contingent_students
from teams.models import TeamSemesterMember

User = get_user_model()


class ContingentStudentRepository:
    """Выборки студентов группы и института."""

    def _membership_qs(self, semester_id: int, *, with_project: bool = False):
        """QuerySet членства в команде семестра для Prefetch."""
        qs = TeamSemesterMember.objects.filter(semester_id=semester_id)
        if with_project:
            return qs.select_related(
                "team_semester__team",
                "team_semester__project_application",
            )
        return qs.select_related("team_semester__team")

    @staticmethod
    def _case_variants(token: str) -> set[str]:
        """Варианты регистра токена для поиска (SQLite LIKE неfoldит кириллицу)."""
        if not token:
            return set()
        first = token[0]
        rest = token[1:]
        swapped = (first.lower() if first.isupper() else first.upper()) + rest
        titled = first.upper() + rest.lower()
        return {
            token,
            token.lower(),
            token.upper(),
            token.capitalize(),
            token.title(),
            token.casefold(),
            swapped,
            titled,
        }

    @classmethod
    def _name_token_filter(cls, tokens: list[str]) -> Q:
        """AND по токенам: каждый токен ищет в любом из полей ФИО.

        Для каждого токена OR по вариантам регистра: в PostgreSQL хватает
        icontains, в SQLite LIKE/icontains для кириллицы регистрозависим.
        """
        combined = Q()
        for token in tokens:
            token_q = Q()
            for variant in cls._case_variants(token):
                token_q |= (
                    Q(last_name__icontains=variant)
                    | Q(first_name__icontains=variant)
                    | Q(middle_name__icontains=variant)
                )
            combined &= token_q
        return combined

    def list_for_group(
        self,
        group_id: int,
        semester_id: int | None = None,
        *,
        with_project: bool = False,
    ) -> list[ContingentStudent]:
        """Контингент одной группы (предрегистрация + прямые студенты)."""
        pre_qs = PreRegisteredStudent.objects.filter(
            group_id=group_id,
            role_id="student",
        ).select_related("user", "group")
        user_qs = User.objects.filter(
            study_group_id=group_id,
            role_id="student",
            is_active=True,
            is_placeholder=False,
        ).select_related("study_group")

        if semester_id is not None:
            membership_qs = self._membership_qs(semester_id, with_project=with_project)
            pre_qs = pre_qs.prefetch_related(
                Prefetch(
                    "user__team_semester_memberships",
                    queryset=membership_qs,
                    to_attr="_team_membership_for_semester",
                )
            )
            user_qs = user_qs.prefetch_related(
                Prefetch(
                    "team_semester_memberships",
                    queryset=membership_qs,
                    to_attr="_team_membership_for_semester",
                )
            )

        pre_registered = list(pre_qs.order_by("last_name", "first_name", "id"))
        linked_user_ids = [
            item.user_id for item in pre_registered if item.user_id is not None
        ]
        direct_users = list(
            user_qs.exclude(id__in=linked_user_ids).order_by(
                "last_name", "first_name", "id"
            )
        )
        return merge_contingent_students(pre_registered, direct_users)

    def search_for_groups(
        self,
        *,
        group_ids: set[int],
        semester_id: int,
        tokens: list[str],
        limit: int,
    ) -> list[ContingentStudent]:
        """Поиск студентов групп по кускам ФИО (предрегистрация + User)."""
        if not group_ids or not tokens or limit <= 0:
            return []

        name_filter = self._name_token_filter(tokens)
        membership_qs = self._membership_qs(semester_id)

        pre_base = PreRegisteredStudent.objects.filter(
            group_id__in=group_ids,
            role_id="student",
        ).filter(name_filter)
        linked_user_ids = list(
            pre_base.exclude(user_id__isnull=True).values_list("user_id", flat=True)
        )
        pre_registered = list(
            pre_base.select_related("user", "group")
            .prefetch_related(
                Prefetch(
                    "user__team_semester_memberships",
                    queryset=membership_qs,
                    to_attr="_team_membership_for_semester",
                )
            )
            .order_by("last_name", "first_name", "id")[:limit]
        )

        direct_users = list(
            User.objects.filter(
                study_group_id__in=group_ids,
                role_id="student",
                is_active=True,
                is_placeholder=False,
            )
            .filter(name_filter)
            .exclude(id__in=linked_user_ids)
            .select_related("study_group")
            .prefetch_related(
                Prefetch(
                    "team_semester_memberships",
                    queryset=membership_qs,
                    to_attr="_team_membership_for_semester",
                )
            )
            .order_by("last_name", "first_name", "id")[:limit]
        )

        return merge_contingent_students(pre_registered, direct_users)[:limit]

    def list_for_institute(
        self,
        *,
        institute_code: str,
        semester_id: int,
        enrollment_qs,
    ) -> list[ContingentStudent]:
        """Контингент активных групп института с командой и наставниками."""
        membership_qs = self._membership_qs(semester_id, with_project=True)
        pre_registered = list(
            PreRegisteredStudent.objects.filter(
                group__institute_id=institute_code,
                group__is_end=False,
                role_id="student",
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
                    queryset=enrollment_qs,
                    to_attr="_semester_enrollments_for_semester",
                ),
            )
            .order_by("group__name", "last_name", "first_name", "id")
        )
        linked_user_ids = [
            item.user_id for item in pre_registered if item.user_id is not None
        ]
        direct_users = list(
            User.objects.filter(
                study_group__institute_id=institute_code,
                study_group__is_end=False,
                role_id="student",
                is_active=True,
                is_placeholder=False,
            )
            .exclude(id__in=linked_user_ids)
            .select_related("study_group")
            .prefetch_related(
                Prefetch(
                    "team_semester_memberships",
                    queryset=membership_qs,
                    to_attr="_team_membership_for_semester",
                ),
                Prefetch(
                    "study_group__semester_enrollments",
                    queryset=enrollment_qs,
                    to_attr="_semester_enrollments_for_semester",
                ),
            )
            .order_by(
                "study_group__name",
                "last_name",
                "first_name",
                "id",
            )
        )

        def institute_sort_key(row: ContingentStudent) -> tuple:
            group_name = row.group.name if row.group is not None else ""
            return (group_name, row.last_name, row.first_name, row.id)

        return merge_contingent_students(
            pre_registered,
            direct_users,
            sort_key=institute_sort_key,
        )
