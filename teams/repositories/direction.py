"""Репозиторий для направлений подготовки."""

from django.db.models import QuerySet

from teams.models import Direction


class DirectionRepository:
    """Доступ к данным Direction."""

    def get_all(self) -> QuerySet[Direction]:
        """Все направления (поля модели без связей — prefetch не требуется)."""
        return Direction.objects.all()

    def get_by_code(self, code: str) -> Direction:
        """Направление по коду (PK)."""
        return Direction.objects.get(pk=code)
