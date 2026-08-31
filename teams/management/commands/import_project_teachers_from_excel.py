"""Идемпотентный импорт преподавателей проектной деятельности из Excel."""

from __future__ import annotations

from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import pandas as pd

from accounts.domain.preregistered_mentor_import import (
    build_user_name_indexes,
    find_user_by_full_name,
)
from accounts.models import Semester
from teams.domain.project_teacher_import import (
    REQUIRED_COLUMNS,
    ProjectTeacherImportRow,
    build_project_teacher_import_row,
)
from teams.domain.study_group_import import normalize_cell
from teams.models import StudyGroup
from teams.repositories.project_teacher import ProjectTeacherRepository
from teams.repositories.study_group_semester import StudyGroupSemesterRepository

User = get_user_model()

DEFAULT_FILE = "data/project_teachers_marked.xlsx"


class Command(BaseCommand):
    help = (
        "Импорт преподавателей проектной деятельности из Excel. "
        "Ключ идемпотентности — (семестр, группа, ID преподавателя)."
    )

    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self._project_teacher_repository = ProjectTeacherRepository()
        self._study_group_semester_repository = StudyGroupSemesterRepository()

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=DEFAULT_FILE,
            help=f"Путь к Excel (.xlsx), по умолчанию: {DEFAULT_FILE}",
        )

    def handle(self, *args, **options):
        path = Path(options["file"]).resolve()
        if not path.is_file():
            raise CommandError(f"Файл не найден: {path}")

        df = self._read_excel(path)
        users = list(User.objects.only("id", "first_name", "last_name", "middle_name"))
        by_name, by_tokens = build_user_name_indexes(users)

        created = 0
        updated = 0
        skipped = 0
        groups_not_found = 0
        semesters_not_found = 0
        mentors_synced = 0

        with transaction.atomic():
            for line_no, (_, row) in enumerate(df.iterrows(), start=2):
                parsed = self._parse_row(line_no, row)
                if parsed is None:
                    skipped += 1
                    continue

                semester = Semester.objects.filter(code=parsed.semester_code).first()
                if semester is None:
                    semesters_not_found += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Строка {line_no}: семестр с code="
                            f"«{parsed.semester_code}» не найден "
                            f"(из «{parsed.semester_label}»)"
                        )
                    )
                    skipped += 1
                    continue

                study_group = StudyGroup.objects.filter(name=parsed.group_name).first()
                if study_group is None:
                    groups_not_found += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Строка {line_no}: группа «{parsed.group_name}» не найдена"
                        )
                    )
                    skipped += 1
                    continue

                tutor = self._resolve_tutor(
                    parsed, by_name=by_name, by_tokens=by_tokens
                )
                _, was_created = self._project_teacher_repository.upsert_from_import(
                    semester_id=semester.pk,
                    study_group_id=study_group.pk,
                    row=parsed,
                    tutor_id=tutor.pk if tutor is not None else None,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

                if tutor is not None:
                    self._study_group_semester_repository.add_mentor(
                        study_group_id=study_group.pk,
                        semester_id=semester.pk,
                        mentor_id=tutor.pk,
                    )
                    mentors_synced += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {created}, обновлено {updated}, "
                f"пропущено {skipped}, групп не найдено {groups_not_found}, "
                f"семестров не найдено {semesters_not_found}, "
                f"наставников синхронизировано {mentors_synced}"
            )
        )

    def _parse_row(
        self,
        line_no: int,
        row: pd.Series,
    ) -> ProjectTeacherImportRow | None:
        """Парсит строку Excel; возвращает None для пропускаемых строк."""
        mentor_full_name = normalize_cell(row.get("Преподаватель (ФИО)"))
        external_teacher_id = normalize_cell(row.get("ID преподавателя"))
        if not mentor_full_name or not external_teacher_id:
            return None

        try:
            return build_project_teacher_import_row(
                group_name=normalize_cell(row.get("Группа")),
                semester_label=normalize_cell(row.get("Семестр")),
                mentor_full_name=mentor_full_name,
                external_teacher_id=external_teacher_id,
                external_group_id=normalize_cell(row.get("ID группы")),
                mentor_short_name=normalize_cell(row.get("Преподаватель (кратко)")),
                lesson_count=row.get("Кол-во пар"),
                import_status=normalize_cell(row.get("Статус")),
                pd_user_id=row.get("ID в PD"),
            )
        except ValueError as exc:
            self.stdout.write(
                self.style.WARNING(f"Строка {line_no}: пропущена — {exc}")
            )
            return None

    def _resolve_tutor(
        self,
        row: ProjectTeacherImportRow,
        *,
        by_name: dict,
        by_tokens: dict,
    ) -> User | None:
        """Возвращает пользователя PD для строки импорта или None."""
        if row.pd_user_id is not None:
            user = User.objects.filter(pk=row.pd_user_id).first()
            if user is not None:
                return user

        return find_user_by_full_name(
            row.mentor_full_name,
            by_name=by_name,
            by_tokens=by_tokens,
        )

    def _read_excel(self, path: Path) -> pd.DataFrame:
        """Читает Excel с преподавателями проектной деятельности."""
        try:
            df = pd.read_excel(path, header=0, dtype=object)
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
