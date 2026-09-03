"""Идемпотентный импорт учебных групп из отчёта контингента 1С (.xls/.xlsx)."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
import pandas as pd

from showcase.models import Institute
from teams.domain.study_group_import import (
    OPTIONAL_PERMANENT_EXTERNAL_ID_COLUMN,
    REQUIRED_COLUMNS,
    ExistingGroupCandidate,
    GroupImportRow,
    build_group_import_row,
    get_study_group_override_by_external_id,
    group_ended_by_planned_dates,
    is_external_group_id_remapped_away,
    is_skipped_permanent_group,
    is_skipped_study_group_name,
    is_skipped_teaching_group_name,
    normalize_cell,
    normalize_external_group_id,
    parse_planned_end_date,
    remap_external_group_id,
    resolve_existing_group_for_id,
)
from teams.models import Direction, StudyGroup

DEFAULT_FILE = "data/контингент_29_08.xls"
HEADER_ROW = 1


class Command(BaseCommand):
    help = (
        "Импорт учебных групп из отчёта контингента 1С. "
        "Ключ идемпотентности — ID группы (1С), имя берётся из колонки «Группа»."
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
            help="Устарело: не влияет на identity/имя (оставлено для совместимости CLI)",
        )
        parser.add_argument(
            "--year",
            type=int,
            default=None,
            help="Устарело: не влияет на identity/имя (оставлено для совместимости CLI)",
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

        today = date.today()

        if options["clear"]:
            deleted, _ = StudyGroup.objects.all().delete()
            self.stdout.write(f"Удалено групп: {deleted}")

        df = self._read_contingent(path)
        rows, skipped_by_config, skipped_remap = self._collect_group_rows(
            df=df,
            today=today,
        )

        candidates = [
            ExistingGroupCandidate(
                pk=group.pk,
                code=group.code,
                name=group.name,
                external_group_id=group.external_group_id or "",
            )
            for group in StudyGroup.objects.all().only(
                "pk", "code", "name", "external_group_id"
            )
        ]
        ids_per_permanent: dict[str, set[str]] = {}
        for row in rows.values():
            ids_per_permanent.setdefault(row.code, set()).add(row.external_group_id)

        created = 0
        updated = 0
        claimed = 0
        ended_by_date_count = 0
        claimed_pks: set[int] = set()
        imported_external_ids = set(rows.keys())

        for external_id, row in rows.items():
            direction = self._get_or_create_direction(row)
            institute = self._get_institute(row.institute_code)
            existing = resolve_existing_group_for_id(
                candidates,
                external_id=external_id,
                permanent_code=row.code,
                teaching_name=row.name,
                ids_per_permanent=ids_per_permanent,
                claimed_pks=claimed_pks,
            )
            defaults = {
                "name": row.name,
                "code": row.code,
                "enrollment_year": row.enrollment_year,
                "course_number": row.course_number,
                "direction": direction,
                "institute": institute,
                "profile": row.profile,
                "form": row.form,
                "is_end": row.is_end,
                "external_group_id": row.external_group_id,
                "external_permanent_group_id": row.external_permanent_group_id,
            }
            if row.is_end:
                ended_by_date_count += 1

            if existing is None:
                StudyGroup.objects.create(**defaults)
                created += 1
                continue

            was_claim = not existing.external_group_id
            StudyGroup.objects.filter(pk=existing.pk).update(**defaults)
            claimed_pks.add(existing.pk)
            # Обновляем кандидата в памяти, чтобы повторно не claim'ить.
            for idx, candidate in enumerate(candidates):
                if candidate.pk == existing.pk:
                    candidates[idx] = ExistingGroupCandidate(
                        pk=existing.pk,
                        code=row.code,
                        name=row.name,
                        external_group_id=row.external_group_id,
                    )
                    break
            updated += 1
            if was_claim:
                claimed += 1

        ended_missing_count = 0
        if not options["clear"] and rows:
            ended_missing_count = (
                StudyGroup.objects.exclude(external_group_id__in=imported_external_ids)
                .exclude(external_group_id="")
                .update(is_end=True)
            )
            ended_missing_count += StudyGroup.objects.filter(
                external_group_id=""
            ).update(is_end=True)

        summary = (
            f"Готово: создано {created}, обновлено {updated} "
            f"(из них claim {claimed}), уникальных ID {len(rows)}"
        )
        if skipped_by_config:
            summary += f", пропущено исключённых {skipped_by_config}"
        if skipped_remap:
            summary += f", пропущено слияний ID {skipped_remap}"
        if not options["clear"]:
            summary += (
                f", завершено отсутствующих/без ID {ended_missing_count}, "
                f"завершено по дате {ended_by_date_count}"
            )
        self.stdout.write(self.style.SUCCESS(summary))

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
        today: date,
    ) -> tuple[dict[str, GroupImportRow], int, int]:
        """Дедуплицирует строки по ID группы (после remap)."""
        groups: dict[str, GroupImportRow] = {}
        planned_dates_by_id: dict[str, list[date | None]] = {}
        unknown_institutes: set[str] = set()
        skipped = 0
        skipped_by_config = 0
        skipped_remap = 0
        has_permanent_id_column = OPTIONAL_PERMANENT_EXTERNAL_ID_COLUMN in df.columns

        for line_no, (_, row) in enumerate(df.iterrows(), start=HEADER_ROW + 2):
            permanent_group = normalize_cell(row.get("Постоянная группа"))
            institute_name = normalize_cell(row.get("Институт"))
            raw_external_id = row.get("ID группы")
            external_group_id = normalize_external_group_id(raw_external_id)
            remapped_id = remap_external_group_id(raw_external_id)
            has_id_override = (
                get_study_group_override_by_external_id(remapped_id) is not None
            )

            if not permanent_group:
                skipped += 1
                continue
            if is_external_group_id_remapped_away(raw_external_id):
                skipped_remap += 1
                continue
            if not external_group_id:
                skipped += 1
                continue
            if is_skipped_permanent_group(permanent_group) and not has_id_override:
                skipped_by_config += 1
                continue
            teaching_group = normalize_cell(row.get("Группа"))
            if is_skipped_teaching_group_name(teaching_group) and not has_id_override:
                skipped_by_config += 1
                continue

            try:
                planned_end_date = parse_planned_end_date(
                    row.get("Дата планового окончания")
                )
            except ValueError as exc:
                raise CommandError(f"Строка {line_no}: {exc}") from exc

            permanent_external_id = ""
            if has_permanent_id_column:
                permanent_external_id = normalize_external_group_id(
                    row.get(OPTIONAL_PERMANENT_EXTERNAL_ID_COLUMN)
                )

            try:
                parsed = build_group_import_row(
                    permanent_group_code=permanent_group,
                    teaching_group_name=teaching_group,
                    institute_name=institute_name,
                    direction_code=normalize_cell(row.get("Код специальности")),
                    direction_name=normalize_cell(row.get("Специальность")),
                    direction_level=normalize_cell(row.get("Вид уровня образования")),
                    profile=normalize_cell(row.get("Профиль/специализация/программа")),
                    form=normalize_cell(row.get("Форма обучения")),
                    external_group_id=raw_external_id,
                    course_from_file=row.get("Курс"),
                    external_permanent_group_id=permanent_external_id,
                )
            except ValueError as exc:
                message = str(exc)
                if message.startswith("Неизвестный институт"):
                    unknown_institutes.add(institute_name)
                    continue
                self.stdout.write(
                    self.style.WARNING(f"Строка {line_no}: пропущена — {message}")
                )
                skipped += 1
                continue

            if is_skipped_study_group_name(parsed.name) and not has_id_override:
                skipped_by_config += 1
                continue

            planned_dates_by_id.setdefault(parsed.external_group_id, []).append(
                planned_end_date
            )
            if parsed.external_group_id in groups:
                continue
            groups[parsed.external_group_id] = parsed

        if unknown_institutes:
            names = ", ".join(sorted(unknown_institutes))
            raise CommandError(f"Неизвестные институты в файле: {names}")

        if skipped:
            self.stdout.write(
                self.style.WARNING(
                    f"Пропущено строк без группы/ID/института: {skipped}"
                )
            )
        if skipped_by_config:
            self.stdout.write(
                self.style.WARNING(
                    f"Пропущено строк исключённых групп: {skipped_by_config}"
                )
            )
        if skipped_remap:
            self.stdout.write(
                self.style.WARNING(
                    f"Пропущено строк со слитым ID группы: {skipped_remap}"
                )
            )

        if not groups and not skipped_by_config and not skipped_remap:
            raise CommandError("Не найдено ни одной валидной учебной группы")

        for external_id, group_row in groups.items():
            is_end = group_ended_by_planned_dates(
                planned_dates_by_id.get(external_id, []),
                today=today,
            )
            groups[external_id] = replace(group_row, is_end=is_end)

        return groups, skipped_by_config, skipped_remap

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
