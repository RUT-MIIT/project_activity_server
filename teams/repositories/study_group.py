"""Репозиторий для учебных групп."""

from django.db.models import Count, QuerySet

from teams.models import StudyGroup


class StudyGroupRepository:
    """Доступ к данным StudyGroup."""

    def get_all(self) -> QuerySet[StudyGroup]:
        return (
            StudyGroup.objects.select_related("direction", "institute")
            .annotate(students_count=Count("pre_registered_students", distinct=True))
            .all()
        )

    def get_by_id(self, group_id: int) -> StudyGroup:
        return (
            StudyGroup.objects.select_related("direction", "institute")
            .annotate(students_count=Count("pre_registered_students", distinct=True))
            .get(pk=group_id)
        )
