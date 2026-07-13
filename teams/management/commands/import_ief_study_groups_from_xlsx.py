"""Идемпотентный импорт учебных групп ИЭФ из Excel."""

from __future__ import annotations

from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
import pandas as pd

from showcase.models import Institute
from teams.models import Direction, StudyGroup

DEFAULT_FILENAME = "groups_01_09_with_abbrev.xlsx"
DEFAULT_SHEET = "groups"
DEFAULT_BASE_YEAR = 2027  # учебный год 2026/2027: 1 курс -> 2026, 4 курс -> 2023


class Command(BaseCommand):
    help = (
        "Импорт учебных групп из Excel-листа groups. "
        "Ожидается файл с листом 'groups', содержащим уникальные группы. "
        "Институт фиксированный: IEF."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help=f"Путь к .xlsx (по умолчанию: {DEFAULT_FILENAME} в корне проекта)",
        )
        parser.add_argument(
            "--sheet",
            type=str,
            default=DEFAULT_SHEET,
            help="Имя листа с группами (по умолчанию: groups)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить все группы института IEF перед импортом",
        )
        parser.add_argument(
            "--base-year",
            type=int,
            default=DEFAULT_BASE_YEAR,
            help=(
                "Базовый год для расчёта года набора по курсу. "
                "Формула: год_набора = base_year - курс. "
                "По умолчанию 2027 (1 курс=2026, 2 курс=2025, ...)."
            ),
        )

    def handle(self, *args, **options):
        path = self._resolve_path(options.get("file"))
        if not path.is_file():
            raise CommandError(f"Файл не найден: {path}")

        institute = self._get_institute()
        if options["clear"]:
            deleted, _ = StudyGroup.objects.filter(institute=institute).delete()
            self.stdout.write(f"Удалено групп института {institute.code}: {deleted}")

        df = self._read_groups_sheet(path=path, sheet_name=options["sheet"])
        rows = self._parse_rows(df, base_year=int(options["base_year"]))

        created = 0
        updated = 0
        for r in rows:
            _, was_created = StudyGroup.objects.update_or_create(
                institute=institute,
                code=r["code"],
                defaults={
                    "name": r["name"],
                    "direction_id": r["direction_code"],
                    "course_number": r["course_number"],
                    "enrollment_year": r["enrollment_year"],
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

    def _get_institute(self) -> Institute:
        try:
            return Institute.objects.get(code="IEF")
        except Institute.DoesNotExist as exc:
            raise CommandError(
                'Институт с кодом "IEF" не найден (сначала import_institutes)'
            ) from exc

    def _read_groups_sheet(self, path: Path, sheet_name: str) -> pd.DataFrame:
        try:
            return pd.read_excel(path, sheet_name=sheet_name, dtype=object)
        except ValueError as exc:
            raise CommandError(
                f"Лист '{sheet_name}' не найден в файле {path.name}"
            ) from exc

    def _parse_rows(self, df: pd.DataFrame, base_year: int) -> list[dict]:
        if df.empty:
            raise CommandError("Лист groups пуст")

        # В файле колонок немного и они стабильны по позиции:
        # 0: уровень, 1: направление/спец., 2: форма, 3: курс,
        # 4: код направления, 5: дата окончания, 6: аббревиатура группы, 7: год набора
        if df.shape[1] < 8:
            raise CommandError(
                "Неожиданная структура листа groups: ожидалось >= 8 колонок"
            )

        rows: list[dict] = []
        for idx, row in df.iterrows():
            parsed = self._parse_row(idx=idx, row=row, base_year=base_year)
            if parsed is not None:
                rows.append(parsed)
        return rows

    def _parse_row(self, idx: int, row: pd.Series, base_year: int) -> dict | None:
        line_no = int(idx) + 2  # с учётом заголовка

        direction_name_raw = row.iloc[1]
        course_raw = row.iloc[3]
        direction_code_raw = row.iloc[4]
        group_abbrev_raw = row.iloc[6]

        code = ("" if group_abbrev_raw is None else str(group_abbrev_raw)).strip()
        if not code:
            raise CommandError(f"Строка {line_no}: пустая аббревиатура группы")

        course_number = self._parse_course(line_no=line_no, value=course_raw)

        # Фильтрация: магистратуру и бакалавриат 1 курса не импортируем.
        # Магистратура имеет код направления вида **.04.**
        # Бакалавриат — **.03.**, и нам не нужен 1 курс.
        direction_code_str = (
            "" if direction_code_raw is None else str(direction_code_raw)
        )
        parts = direction_code_str.split(".")
        if len(parts) >= 2:
            level_part = parts[1]
            if level_part == "04":
                # Магистратура — полностью пропускаем.
                return None
            if level_part == "03" and course_number == 1:
                # Бакалавриат 1 курса — пропускаем.
                return None

        direction_code = self._get_or_create_direction(
            line_no=line_no,
            code_value=direction_code_raw,
            name_value=direction_name_raw,
        )
        enrollment_year = self._calc_enrollment_year(
            line_no=line_no, base_year=base_year, course_number=course_number
        )

        return {
            "code": code,
            "name": code,
            "course_number": course_number,
            "direction_code": direction_code,
            "enrollment_year": enrollment_year,
        }

    def _parse_course(self, line_no: int, value: object) -> int:
        try:
            course_number = int(str(value).strip())
        except Exception as exc:
            raise CommandError(f"Строка {line_no}: курс «{value}» не число") from exc
        if course_number < 1:
            raise CommandError(f"Строка {line_no}: курс должен быть >= 1")
        return course_number

    def _get_or_create_direction(
        self,
        line_no: int,
        code_value: object,
        name_value: object,
    ) -> str:
        direction_code = ("" if code_value is None else str(code_value)).strip()
        if not direction_code:
            raise CommandError(f"Строка {line_no}: не указан код направления")

        if Direction.objects.filter(code=direction_code).exists():
            return direction_code

        name = ("" if name_value is None else str(name_value)).strip()
        if not name:
            name = direction_code

        # В исходном Excel текстовые поля могут быть в "битой" кодировке,
        # поэтому уровень подготовки надёжно определить не всегда возможно.
        # Для корректного импорта групп создаём направление с безопасным дефолтом.
        Direction.objects.create(
            code=direction_code,
            level=Direction.Level.BAKALAVRIAT,
            name=name,
        )
        return direction_code

    def _calc_enrollment_year(
        self, line_no: int, base_year: int, course_number: int
    ) -> int:
        enrollment_year = base_year - course_number
        if enrollment_year < 1900:
            raise CommandError(
                f"Строка {line_no}: некорректный год набора {enrollment_year} "
                f"(base_year={base_year}, курс={course_number})"
            )
        return enrollment_year

    def _resolve_path(self, file_arg: str | None) -> Path:
        if file_arg:
            return Path(file_arg).resolve()
        return Path(apps.get_app_config("config").path).parent / DEFAULT_FILENAME
