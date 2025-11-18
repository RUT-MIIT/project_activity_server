import os
from typing import Iterable

import pandas as pd
from django.core.management.base import BaseCommand

from showcase.models import ApplicationStatus


class Command(BaseCommand):
    """Экспорт возможных статусов заявок в Excel."""

    help = (
        "Экспорт статусов заявок в Excel-файл statuses.xlsx "
        "(файл создаётся рядом с командой)."
    )

    def handle(self, *args, **options) -> None:
        """Считывает статусы из базы и сохраняет в Excel."""
        statuses = self._get_statuses()
        data = [
            {
                "code": status.code,
                "name": status.name,
                "position": status.position,
                "is_active": status.is_active,
            }
            for status in statuses
        ]

        if not data:
            self.stdout.write(self.style.WARNING("Статусов в базе не найдено."))

        file_path = os.path.join(os.path.dirname(__file__), "statuses.xlsx")
        pd.DataFrame(data).to_excel(file_path, index=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Выгружено статусов: {len(data)}. Файл сохранён в {file_path}"
            )
        )

    def _get_statuses(self) -> Iterable[ApplicationStatus]:
        """Возвращает статусы, отсортированные по позиции и коду."""
        return ApplicationStatus.objects.all().order_by("position", "code")
