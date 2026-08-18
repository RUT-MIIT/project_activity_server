"""Идемпотентный импорт предрегистрации студентов из отчёта контингента 1С."""

from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import pandas as pd

from accounts.domain.preregistered_student_import import (
    REQUIRED_COLUMNS,
    build_preregistered_student_import_row,
)
from accounts.models import PreRegisteredStudent
from teams.domain.study_group_import import normalize_cell
from teams.models import StudyGroup

DEFAULT_FILE = "data/контингент_14_08.xls"
HEADER_ROW = 1


class Command(BaseCommand):
    help = (
        "Импорт предрегистрации студентов из отчёта контингента 1С. "
        "Ключ идемпотентности — табельный номер (ID_E человека)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=DEFAULT_FILE,
            help=f"Путь к отчёту (.xls/.xlsx), по умолчанию: {DEFAULT_FILE}",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить предрегистрации без привязанного пользователя перед импортом",
        )

    def handle(self, *args, **options):
        path = Path(options["file"]).resolve()
        if not path.is_file():
            raise CommandError(f"Файл не найден: {path}")

        if options["clear"]:
            deleted, _ = PreRegisteredStudent.objects.filter(
                student__isnull=True
            ).delete()
            self.stdout.write(f"Удалено предрегистраций: {deleted}")

        df = self._read_contingent(path)
        group_map = self._build_group_map(df)

        created = 0
        updated = 0
        skipped = 0

        with transaction.atomic():
            for line_no, (_, row) in enumerate(df.iterrows(), start=HEADER_ROW + 2):
                try:
                    parsed = build_preregistered_student_import_row(
                        full_name=normalize_cell(row.get("ФИО (полное)")),
                        student_card=normalize_cell(row.get("Студенческий билет")),
                        snils=normalize_cell(row.get("СНИЛС")),
                        personnel_number=normalize_cell(row.get("ID_E человека")),
                        permanent_group_code=normalize_cell(
                            row.get("Постоянная группа")
                        ),
                    )
                except ValueError as exc:
                    self.stdout.write(
                        self.style.WARNING(f"Строка {line_no}: пропущена — {exc}")
                    )
                    skipped += 1
                    continue

                group = group_map.get(parsed.group_code)
                if group is None:
                    raise CommandError(
                        f"Строка {line_no}: группа «{parsed.group_code}» не найдена "
                        "(сначала import_study_groups_from_contingent)"
                    )

                existing = PreRegisteredStudent.objects.filter(
                    personnel_number=parsed.personnel_number
                ).first()
                defaults = {
                    "last_name": parsed.last_name,
                    "first_name": parsed.first_name,
                    "middle_name": parsed.middle_name,
                    "student_card": parsed.student_card,
                    "snils": parsed.snils,
                    "group": group,
                }
                if existing is not None:
                    for field, value in defaults.items():
                        setattr(existing, field, value)
                    existing.save()
                    updated += 1
                else:
                    PreRegisteredStudent.objects.create(
                        personnel_number=parsed.personnel_number,
                        **defaults,
                    )
                    created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {created}, обновлено {updated}, пропущено {skipped}"
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

    def _build_group_map(self, df: pd.DataFrame) -> dict[str, StudyGroup]:
        """Строит карту кодов постоянных групп из файла к объектам StudyGroup."""
        codes = {
            normalize_cell(value)
            for value in df["Постоянная группа"].tolist()
            if normalize_cell(value)
        }
        groups = StudyGroup.objects.filter(code__in=codes)
        group_map = {group.code: group for group in groups}
        missing_codes = sorted(codes - set(group_map))
        if missing_codes:
            preview = ", ".join(missing_codes[:10])
            suffix = "..." if len(missing_codes) > 10 else ""
            raise CommandError(
                f"В БД отсутствуют группы ({len(missing_codes)}): {preview}{suffix}. "
                "Сначала выполните import_study_groups_from_contingent."
            )
        return group_map
