"""Идемпотентный импорт учебных групп из отчёта контингента 1С (.xls/.xlsx)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
import pandas as pd

from showcase.models import Institute
from teams.domain.study_group_import import (
    REQUIRED_COLUMNS,
    GroupImportRow,
    build_group_import_row,
    normalize_cell,
)
from teams.models import Direction, StudyGroup

DEFAULT_FILE = "data/контингент_14_08.xls"
HEADER_ROW = 1


class Command(BaseCommand):
    help = (
        "Импорт учебных групп из отчёта контингента 1С. "
        "Код группы — «Постоянная группа», название рассчитывается по семестру."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=DEFAULT_FILE,
            help=f"Путь к отчёту (.xls/.xlsx), по умолчанию: {DEFAULT_FILE}",
        )
        parser.add_argument(
            "--semester",
            type=str,
            choices=("autumn", "spring"),
            default="autumn",
            help="Семестр расчёта курса: autumn (осень, по умолчанию) или spring (весна)",
        )
        parser.add_argument(
            "--year",
            type=int,
            default=None,
            help="Календарный год для расчёта курса (по умолчанию — текущий год)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить все учебные группы перед импортом",
        )

    def handle(self, *args, **options):
        path = Path(options["file"]).resolve()
        if not path.is_file():
            raise CommandError(f"Файл не найден: {path}")

        current_year = (
            options["year"] if options["year"] is not None else date.today().year
        )
        semester = options["semester"]

        if options["clear"]:
            deleted, _ = StudyGroup.objects.all().delete()
            self.stdout.write(f"Удалено групп: {deleted}")

        df = self._read_contingent(path)
        rows = self._collect_group_rows(
            df=df,
            current_year=current_year,
            semester=semester,
        )

        created = 0
        updated = 0
        for row in rows.values():
            direction = self._get_or_create_direction(row)
            institute = self._get_institute(row.institute_code)
            _, was_created = StudyGroup.objects.update_or_create(
                code=row.code,
                defaults={
                    "name": row.name,
                    "enrollment_year": row.enrollment_year,
                    "course_number": row.course_number,
                    "direction": direction,
                    "institute": institute,
                    "profile": row.profile,
                    "form": row.form,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {created}, обновлено {updated}, "
                f"уникальных групп {len(rows)} "
                f"(year={current_year}, semester={semester})"
            )
        )

    def _read_contingent(self, path: Path) -> pd.DataFrame:
        """Читает отчёт контингента; заголовок колонок — вторая строка."""
        try:
            df = pd.read_excel(path, header=HEADER_ROW, dtype=object)
        except ValueError as exc:
            raise CommandError(f"Не удалось прочитать файл {path.name}: {exc}") from exc

        if df.empty:
            raise CommandError("Файл не содержит данных")

        missing = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise CommandError(
                "В файле отсутствуют обязательные колонки: "
                + ", ".join(sorted(missing))
            )
        return df

    def _collect_group_rows(
        self,
        *,
        df: pd.DataFrame,
        current_year: int,
        semester: str,
    ) -> dict[str, GroupImportRow]:
        """Дедуплицирует строки по коду постоянной группы."""
        groups: dict[str, GroupImportRow] = {}
        unknown_institutes: set[str] = set()
        skipped = 0

        for line_no, (_, row) in enumerate(df.iterrows(), start=HEADER_ROW + 2):
            permanent_group = normalize_cell(row.get("Постоянная группа"))
            institute_name = normalize_cell(row.get("Институт"))

            if not permanent_group:
                skipped += 1
                continue
            if not institute_name:
                self.stdout.write(
                    self.style.WARNING(
                        f"Строка {line_no}: пропущена — пустой институт "
                        f"(группа «{permanent_group}»)"
                    )
                )
                skipped += 1
                continue

            if permanent_group in groups:
                continue

            try:
                parsed = build_group_import_row(
                    permanent_group_code=permanent_group,
                    institute_name=institute_name,
                    direction_code=normalize_cell(row.get("Код специальности")),
                    direction_name=normalize_cell(row.get("Специальность")),
                    direction_level=normalize_cell(row.get("Вид уровня образования")),
                    profile=normalize_cell(row.get("Профиль/специализация/программа")),
                    form=normalize_cell(row.get("Форма обучения")),
                    current_year=current_year,
                    semester=semester,  # type: ignore[arg-type]
                )
            except ValueError as exc:
                message = str(exc)
                if message.startswith("Неизвестный институт"):
                    unknown_institutes.add(institute_name)
                    continue
                raise CommandError(f"Строка {line_no}: {message}") from exc

            groups[parsed.code] = parsed

        if unknown_institutes:
            names = ", ".join(sorted(unknown_institutes))
            raise CommandError(f"Неизвестные институты в файле: {names}")

        if skipped:
            self.stdout.write(
                self.style.WARNING(f"Пропущено строк без группы/института: {skipped}")
            )

        if not groups:
            raise CommandError("Не найдено ни одной валидной учебной группы")

        return groups

    def _get_or_create_direction(self, row: GroupImportRow) -> Direction:
        """Возвращает направление подготовки, создавая при необходимости."""
        direction, _ = Direction.objects.get_or_create(
            code=row.direction_code,
            defaults={
                "name": row.direction_name,
                "level": row.direction_level,
            },
        )
        return direction

    def _get_institute(self, code: str) -> Institute:
        """Возвращает институт по коду справочника."""
        try:
            return Institute.objects.get(code=code)
        except Institute.DoesNotExist as exc:
            raise CommandError(
                f'Институт с кодом "{code}" не найден (сначала import_institutes)'
            ) from exc
