"""Доменная логика для направлений подготовки."""

from django.db.models import QuerySet

from accounts.models import User
from teams.domain.institute_access import get_user_institute_codes
from teams.models import Direction, StudyGroup


class DirectionDomain:
    """Фильтрация направлений по роли пользователя."""

    get_user_institute_codes = staticmethod(get_user_institute_codes)

    @staticmethod
    def get_filtered_queryset(
        user: User, queryset: QuerySet[Direction]
    ) -> QuerySet[Direction]:
        """Фильтрует направления: institute_validator — только из групп своего института."""
        if not user or not user.is_authenticated:
            return queryset.none()

        role_code = user.role.code if user.role else None

        if role_code == "institute_validator":
            institute_codes = get_user_institute_codes(user)
            if not institute_codes:
                return queryset.none()

            direction_codes = (
                StudyGroup.objects.filter(institute_id__in=institute_codes)
                .values_list("direction_id", flat=True)
                .distinct()
            )
            return queryset.filter(code__in=direction_codes)

        return queryset
