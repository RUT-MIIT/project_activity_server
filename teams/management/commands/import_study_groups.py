"""Идемпотентный импорт учебных групп из CSV."""

import csv
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from showcase.models import Institute
from teams.models import Direction, StudyGroup

DEFAULT_FILENAME = "ief_study_groups.csv"
REQUIRED_COLUMNS = (
    "Институт",
    "Название группы",
    "Курс",
    "Код",
    "Направление обучения",
)


class Command(BaseCommand):
    help = (
        "Импорт учебных групп из CSV. "
        "Колонки: Институт, Название группы, Курс, Код, Направление обучения. "
        "По умолчанию: teams/data/ief_study_groups.csv"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Путь к CSV (иначе teams/data/ief_study_groups.csv)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить группы институтов из CSV перед импортом",
        )

    def handle(self, *args, **options):
        path = self._resolve_path(options.get("file"))
        if not path.is_file():
            raise CommandError(f"Файл не найден: {path}")

        rows = self._read_rows(path)
        if options["clear"]:
            codes = {r["institute_code"] for r in rows}
            deleted, _ = StudyGroup.objects.filter(institute_id__in=codes).delete()
            self.stdout.write(f"Удалено групп: {deleted}")

        created = 0
        updated = 0
        for r in rows:
            _, was_created = StudyGroup.objects.update_or_create(
                code=r["code"],
                defaults={
                    "name": r["name"],
                    "institute_id": r["institute_code"],
                    "direction_id": r["direction_code"],
                    "course_number": r["course_number"],
                    "is_end": False,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Готово: создано {created}, обновлено {updated}")
        )

    def _read_rows(self, path: Path) -> list[dict]:
        parsed: list[dict] = []
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise CommandError("CSV без заголовка")
            missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames)
            if missing:
                raise CommandError("Нет колонок: " + ", ".join(sorted(missing)))
            for line_no, row in enumerate(reader, start=2):
                parsed.append(self._parse_row(line_no, row))
        return parsed

    def _parse_row(self, line_no: int, row: dict[str, str]) -> dict:
        institute_code = (row.get("Институт") or "").strip()
        name = (row.get("Название группы") or "").strip()
        course_raw = (row.get("Курс") or "").strip()
        code = (row.get("Код") or "").strip()
        direction_code = (row.get("Направление обучения") or "").strip()

        if not institute_code or not name or not course_raw or not code:
            raise CommandError(
                f"Строка {line_no}: пустые Институт, Название группы, Курс или Код"
            )
        if not direction_code:
            raise CommandError(f"Строка {line_no}: не указано направление обучения")
        try:
            course_number = int(course_raw)
        except ValueError as exc:
            raise CommandError(
                f"Строка {line_no}: курс «{course_raw}» не число"
            ) from exc
        if course_number < 1:
            raise CommandError(f"Строка {line_no}: курс должен быть >= 1")

        if not Institute.objects.filter(code=institute_code).exists():
            raise CommandError(
                f"Строка {line_no}: институт «{institute_code}» не найден"
            )
        if not Direction.objects.filter(code=direction_code).exists():
            raise CommandError(
                f"Строка {line_no}: направление «{direction_code}» не найдено "
                "(сначала import_directions)"
            )

        return {
            "institute_code": institute_code,
            "name": name,
            "course_number": course_number,
            "code": code,
            "direction_code": direction_code,
        }

    def _resolve_path(self, file_arg: str | None) -> Path:
        if file_arg:
            return Path(file_arg).resolve()
        base = Path(apps.get_app_config("teams").path) / "data"
        return base / DEFAULT_FILENAME
