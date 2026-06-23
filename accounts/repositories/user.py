"""Репозиторий для управления пользователями."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch, QuerySet

from showcase.models import ProjectApplication

User = get_user_model()


class UserRepository:
    """Доступ к данным пользователей для управления."""

    @staticmethod
    def base_queryset() -> QuerySet:
        """Базовый queryset без администраторов."""
        return (
            User.objects.exclude(role__code="admin")
            .exclude(is_staff=True)
            .select_related("role", "department", "department__parent")
        )

    def filter_users_queryset(
        self,
        department_ids: set[int] | None,
        include_authored_projects: bool = False,
    ) -> QuerySet:
        """Список пользователей с оптимизацией запросов."""
        queryset = (
            self.base_queryset()
            .annotate(
                authored_projects_count=Count("project_applications", distinct=True)
            )
            .order_by("last_name", "first_name", "id")
        )

        if department_ids is not None:
            if not department_ids:
                return User.objects.none()
            queryset = queryset.filter(department_id__in=department_ids)

        if include_authored_projects:
            projects_qs = (
                ProjectApplication.objects.select_related("status")
                .only(
                    "id",
                    "title",
                    "author_id",
                    "status_id",
                    "status__code",
                    "status__name",
                    "creation_date",
                )
                .order_by("-creation_date")
            )
            queryset = queryset.prefetch_related(
                Prefetch(
                    "project_applications",
                    queryset=projects_qs,
                    to_attr="prefetched_authored_projects",
                )
            )

        return queryset

    def get_by_id(self, user_id: int) -> User:
        """Возвращает пользователя по ID."""
        return User.objects.select_related("role", "department").get(pk=user_id)

    def update_user(
        self,
        user: User,
        *,
        role=None,
        department=None,
        update_fields: list[str],
    ) -> User:
        """Сохраняет изменения пользователя."""
        if role is not None:
            user.role = role
        if department is not None:
            user.department = department
        user.save(update_fields=update_fields)
        return user
