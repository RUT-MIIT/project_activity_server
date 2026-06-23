"""Репозиторий для списка проектов."""

from django.db.models import QuerySet

from showcase.models import ProjectApplication
from showcase.repositories.project_track import ProjectTrackRepository


class ProjectRepository:
    """Доступ к данным для списка проектов."""

    def filter_projects_queryset(
        self,
        institute_codes: list[str] | None,
        semester_id: int | None = None,
    ) -> QuerySet[ProjectApplication]:
        """Список заявок с фильтрацией по институту и семестру."""

        queryset = ProjectApplication.objects.all()

        if semester_id is not None:
            queryset = queryset.filter(semester_id=semester_id)

        if institute_codes is not None:
            if not institute_codes:
                return ProjectApplication.objects.none()

            access_q = ProjectTrackRepository._application_institute_access_q(
                institute_codes
            )

            queryset = queryset.filter(access_q)

        return (
            queryset.distinct()
            .select_related(
                "status",
                "main_department",
                "author",
                "author__role",
                "semester",
            )
            .prefetch_related("tags", "target_institutes")
            .order_by("-creation_date")
        )

    def filter_approved_for_institutes_queryset(
        self, semester_id: int, institute_codes: list[str]
    ) -> QuerySet[ProjectApplication]:
        """Одобренные проекты семестра для указанных институтов (legacy)."""

        if not institute_codes:
            return ProjectApplication.objects.none()

        return (
            ProjectApplication.objects.filter(
                status__code="approved",
                semester_id=semester_id,
                target_institutes__code__in=institute_codes,
            )
            .distinct()
            .select_related("status", "semester")
            .prefetch_related("tags")
            .order_by("-creation_date")
        )
