"""Идемпотентный импорт строк модели Settings из CSV."""

import csv
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from accounts.models import AcademicYear, Semester, Settings

DEFAULT_FILENAME = "app_settings.csv"
REQUIRED_COLUMNS = ("code", "description", "value")


class Command(BaseCommand):
    help = (
        "Импорт настроек (Settings) из CSV: колонки code, description, value. "
        "По умолчанию: accounts/data/app_settings.csv. "
        "Типичные ключи: active_semester_code (pk семестра), "
        "active_academic_year_code (код учебного года)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Путь к CSV (иначе accounts/data/app_settings.csv)",
        )

    def handle(self, *args, **options):
        path = self._resolve_path(options.get("file"))
        if not path.is_file():
            raise CommandError(f"Файл не найден: {path}")

        created = 0
        updated = 0

        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise CommandError("CSV без заголовка")
            missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames)
            if missing:
                raise CommandError("Нет колонок: " + ", ".join(sorted(missing)))

            for line_no, row in enumerate(reader, start=2):
                code = (row.get("code") or "").strip()
                if not code:
                    raise CommandError(f"Строка {line_no}: пустой code")
                description = (row.get("description") or "").strip()
                value = row.get("value")
                if value is None:
                    value = ""
                else:
                    value = str(value).strip()

                _, was_created = Settings.objects.update_or_create(
                    code=code,
                    defaults={"description": description, "value": value},
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        self._validate_known_keys()
        self.stdout.write(
            self.style.SUCCESS(f"Готово: создано {created}, обновлено {updated}")
        )

    def _resolve_path(self, file_arg: str | None) -> Path:
        if file_arg:
            return Path(file_arg).resolve()
        base = Path(apps.get_app_config("accounts").path) / "data"
        return base / DEFAULT_FILENAME

    def _validate_known_keys(self) -> None:
        """Проверка ссылок для active_* ключей (только предупреждение в stdout)."""
        for code, check in (
            ("active_semester_code", self._check_semester_pk),
            ("active_academic_year_code", self._check_year_code),
        ):
            try:
                s = Settings.objects.get(code=code)
            except Settings.DoesNotExist:
                continue
            if not (s.value or "").strip():
                continue
            msg = check(s.value.strip())
            if msg:
                self.stdout.write(self.style.WARNING(f"{code}: {msg}"))

    def _check_semester_pk(self, raw: str) -> str:
        try:
            pk = int(raw)
        except ValueError:
            return f"значение «{raw}» не похоже на pk семестра"
        if not Semester.objects.filter(pk=pk).exists():
            return f"семестр с pk={pk} не найден"
        return ""

    def _check_year_code(self, raw: str) -> str:
        if not AcademicYear.objects.filter(code=raw).exists():
            return f"учебный год с code=«{raw}» не найден"
        return ""
