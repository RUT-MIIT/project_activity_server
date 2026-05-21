"""Репозиторий для учебных групп."""

from django.db.models import QuerySet

from teams.models import StudyGroup


class StudyGroupRepository:
    """Доступ к данным StudyGroup."""

    def get_all(self) -> QuerySet[StudyGroup]:
        return StudyGroup.objects.select_related("direction", "institute").all()

    def get_by_id(self, group_id: int) -> StudyGroup:
        return StudyGroup.objects.select_related("direction", "institute").get(
            pk=group_id
        )
