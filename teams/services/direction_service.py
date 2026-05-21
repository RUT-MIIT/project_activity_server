"""Сервис для операций с направлениями подготовки."""

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Department
from teams.domain.direction import DirectionDomain
from teams.models import Direction
from teams.repositories.direction import DirectionRepository

if TYPE_CHECKING:
    from django.db.models import QuerySet

User = get_user_model()


class DirectionService:
    """Оркестрация Domain + Repository для Direction."""

    def __init__(self):
        self.repository = DirectionRepository()
        self.domain = DirectionDomain()

    def list_directions(self, user: User) -> "QuerySet[Direction]":
        """Список направлений с фильтрацией по роли."""
        if user.is_authenticated and user.department_id:
            try:
                department = Department.objects.select_related("parent").get(
                    pk=user.department_id
                )
                user.department = department
            except Department.DoesNotExist:
                pass

        queryset = self.repository.get_all()
        return self.domain.get_filtered_queryset(user, queryset)

    def get_direction(self, code: str, user: User) -> Direction:
        """Направление по коду с проверкой доступа."""
        try:
            direction = self.repository.get_by_code(code)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Направление с кодом {code} не найдено") from err

        filtered = self.list_directions(user)
        if not filtered.filter(pk=code).exists():
            raise ValueError("Нет доступа к этому направлению")

        return direction
