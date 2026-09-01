"""Идемпотентный импорт предрегистрации студентов из отчёта контингента 1С."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import pandas as pd

from accounts.domain.preregistered_student_import import (
    REQUIRED_COLUMNS,
    StudyGroupLookup,
    StudyGroupRef,
    build_preregistered_student_import_row,
    resolve_study_group_for_student,
)
from accounts.models import PreRegisteredStudent
from teams.domain.study_group_import import normalize_cell
from teams.models import StudyGroup

DEFAULT_FILE = "data/контингент_29_08.xls"
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
        parser.add_argument(
            "--semester",
            type=str,
            choices=("autumn", "spring"),
            default="autumn",
            help="Семестр для определения сходящихся строк: autumn или spring",
        )
        parser.add_argument(
            "--year",
            type=int,
            default=None,
            help="Календарный год для определения сходящихся строк (по умолчанию — текущий)",
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
            deleted, _ = PreRegisteredStudent.objects.filter(user__isnull=True).delete()
            self.stdout.write(f"Удалено предрегистраций: {deleted}")

        df = self._read_contingent(path)
        lookup = self._build_group_lookup()
        self._validate_permanent_groups_exist(df, lookup)

        created = 0
        updated = 0
        skipped_invalid = 0
        skipped_no_group = 0
        imported_personnel_numbers: set[str] = set()
        users_to_sync: dict[int, int] = {}

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
                        teaching_group_name=normalize_cell(row.get("Группа")),
                        external_group_id=normalize_cell(row.get("ID группы")),
                        course_from_file=row.get("Курс"),
                    )
                except ValueError as exc:
                    self.stdout.write(
                        self.style.WARNING(f"Строка {line_no}: пропущена — {exc}")
                    )
                    skipped_invalid += 1
                    continue

                resolve_result = resolve_study_group_for_student(
                    parsed,
                    lookup,
                    current_year=current_year,
                    semester=semester,  # type: ignore[arg-type]
                )
                if resolve_result.group is None:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Строка {line_no}: пропущена — {resolve_result.reason}"
                        )
                    )
                    skipped_no_group += 1
                    continue

                group_pk = resolve_result.group.pk
                imported_personnel_numbers.add(parsed.personnel_number)

                existing = PreRegisteredStudent.objects.filter(
                    personnel_number=parsed.personnel_number
                ).first()
                defaults = {
                    "last_name": parsed.last_name,
                    "first_name": parsed.first_name,
                    "middle_name": parsed.middle_name,
                    "student_card": parsed.student_card,
                    "snils": parsed.snils,
                    "group_id": group_pk,
                    "role_id": "student",
                }
                if existing is not None:
                    for field, value in defaults.items():
                        setattr(existing, field, value)
                    existing.save()
                    updated += 1
                    if existing.user_id is not None:
                        users_to_sync[existing.user_id] = group_pk
                else:
                    created_student = PreRegisteredStudent.objects.create(
                        personnel_number=parsed.personnel_number,
                        **defaults,
                    )
                    created += 1
                    if created_student.user_id is not None:
                        users_to_sync[created_student.user_id] = group_pk

            deleted, _ = (
                PreRegisteredStudent.objects.filter(user__isnull=True)
                .exclude(personnel_number__in=imported_personnel_numbers)
                .delete()
            )

        if users_to_sync:
            user_model = get_user_model()
            users = [
                user_model(pk=user_id, study_group_id=group_id)
                for user_id, group_id in users_to_sync.items()
            ]
            user_model.objects.bulk_update(users, ["study_group"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {created}, обновлено {updated}, "
                f"удалено {deleted}, пропущено невалидных {skipped_invalid}, "
                f"пропущено без группы {skipped_no_group}, "
                f"синхронизировано пользователей {len(users_to_sync)}"
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

    def _build_group_lookup(self) -> StudyGroupLookup:
        """Строит индексы всех учебных групп для резолвинга."""
        groups = StudyGroup.objects.all().only(
            "pk", "code", "name", "external_group_id"
        )
        refs = [
            StudyGroupRef(
                pk=group.pk,
                code=group.code,
                name=group.name,
                external_group_id=group.external_group_id,
            )
            for group in groups
        ]
        return StudyGroupLookup.from_groups(refs)

    def _validate_permanent_groups_exist(
        self, df: pd.DataFrame, lookup: StudyGroupLookup
    ) -> None:
        """Проверяет, что постоянные группы из файла есть в БД."""
        codes = {
            normalize_cell(value)
            for value in df["Постоянная группа"].tolist()
            if normalize_cell(value)
        }
        missing_codes = sorted(codes - set(lookup.by_code))
        if missing_codes:
            preview = ", ".join(missing_codes[:10])
            suffix = "..." if len(missing_codes) > 10 else ""
            raise CommandError(
                f"В БД отсутствуют группы ({len(missing_codes)}): {preview}{suffix}. "
                "Сначала выполните import_study_groups_from_contingent."
            )
