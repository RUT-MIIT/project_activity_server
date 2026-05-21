"""Доменная логика для учебных групп."""

from django.db.models import QuerySet

from accounts.models import User
from teams.domain.institute_access import get_user_institute_codes
from teams.models import StudyGroup


class StudyGroupDomain:
    """Фильтрация учебных групп по роли пользователя."""

    @staticmethod
    def get_filtered_queryset(
        user: User, queryset: QuerySet[StudyGroup]
    ) -> QuerySet[StudyGroup]:
        """institute_validator — только группы своих институтов."""
        if not user or not user.is_authenticated:
            return queryset.none()

        role_code = user.role.code if user.role else None

        if role_code == "institute_validator":
            institute_codes = get_user_institute_codes(user)
            if not institute_codes:
                return queryset.none()
            return queryset.filter(institute_id__in=institute_codes)

        return queryset
