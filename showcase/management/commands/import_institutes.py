import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import pandas as pd

from showcase.models import Institute

REQUIRED_COLUMNS = ("code", "name", "position")


class Command(BaseCommand):
    help = (
        "Идемпотентный импорт справочника институтов из CSV. "
        "По умолчанию: showcase/management/commands/institutes.csv"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="institutes.csv",
            help="Путь к CSV файлу с данными институтов",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить все институты перед импортом",
        )

    def handle(self, *args, **options):
        file_path = self._resolve_path(options["file"])
        if not os.path.exists(file_path):
            raise CommandError(f"Файл не найден: {file_path}")

        df = pd.read_csv(file_path)
        missing = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise CommandError(
                "В CSV отсутствуют обязательные колонки: " + ", ".join(sorted(missing))
            )

        if options["clear"]:
            deleted, _ = Institute.objects.all().delete()
            self.stdout.write(f"Удалено институтов: {deleted}")

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for line_no, row in enumerate(df.itertuples(index=False), start=2):
                code = str(row.code).strip()
                name = str(row.name).strip()
                position = int(row.position)

                if not code or not name:
                    raise CommandError(f"Строка {line_no}: пустые code или name")

                _, created = Institute.objects.update_or_create(
                    code=code,
                    defaults={
                        "name": name,
                        "position": position,
                        "is_active": True,
                    },
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {created_count}, обновлено {updated_count}"
            )
        )

    def _resolve_path(self, file_path: str) -> str:
        """Возвращает абсолютный путь к CSV (относительный — от папки commands)."""
        if os.path.isabs(file_path):
            return file_path
        commands_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(commands_dir, file_path)
