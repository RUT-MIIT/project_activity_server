import csv
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from teams.models import Direction

DEFAULT_FILENAME = "fgos_specialitet_napravleniya.csv"
REQUIRED_COLUMNS = ("level", "code", "name")
VALID_LEVELS = {choice.value for choice in Direction.Level}


class Command(BaseCommand):
    help = (
        "Импорт направлений подготовки из CSV (level, code, name). "
        "По умолчанию: teams/data/fgos_specialitet_napravleniya.csv"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Путь к CSV-файлу (переопределяет путь по умолчанию)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить все направления перед импортом",
        )

    def handle(self, *args, **options):
        csv_path = self._resolve_path(options["file"])
        if not csv_path.is_file():
            raise CommandError(f"Файл не найден: {csv_path}")

        if options["clear"]:
            deleted, _ = Direction.objects.all().delete()
            self.stdout.write(f"Удалено записей: {deleted}")

        created_count = 0
        updated_count = 0

        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise CommandError("CSV пуст или без заголовка")
            missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames)
            if missing:
                raise CommandError(f"В CSV нет колонок: {', '.join(sorted(missing))}")

            for line_no, row in enumerate(reader, start=2):
                level, code, name = self._parse_row(line_no, row)
                _, created = Direction.objects.update_or_create(
                    code=code,
                    defaults={"level": level, "name": name},
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

    def _parse_row(self, line_no: int, row: dict[str, str]) -> tuple[str, str, str]:
        level = (row.get("level") or "").strip()
        code = (row.get("code") or "").strip()
        name = (row.get("name") or "").strip()
        if not level or not code or not name:
            raise CommandError(f"Строка {line_no}: пустые level, code или name")
        if level not in VALID_LEVELS:
            raise CommandError(
                f"Строка {line_no}: недопустимый level «{level}» "
                f"(ожидается: {', '.join(sorted(VALID_LEVELS))})"
            )
        return level, code, name

    def _resolve_path(self, file_arg: str | None) -> Path:
        if file_arg:
            return Path(file_arg).resolve()
        teams_path = Path(apps.get_app_config("teams").path)
        return teams_path / "data" / DEFAULT_FILENAME
