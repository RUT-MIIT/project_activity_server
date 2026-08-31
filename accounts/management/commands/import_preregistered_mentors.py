"""Идемпотентный импорт предрегистрации наставников из отчёта 1С."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import pandas as pd

from accounts.domain.preregistered_mentor_import import (
    MENTOR_REQUIRED_COLUMNS,
    PreRegisteredMentorImportRow,
    build_preregistered_mentor_import_row,
    build_user_name_indexes,
    find_user_by_full_name,
    resolve_department_by_name,
)
from accounts.models import PreRegisteredStudent
from accounts.repositories.preregistered_student import PreRegisteredStudentRepository
from teams.domain.study_group_import import normalize_cell

User = get_user_model()

DEFAULT_FILE = "data/преподаватели.xls"
HEADER_ROW = 1


class DepartmentConflictAction(str, Enum):
    """Действие при расхождении подразделения пользователя и импорта."""

    SKIP = "skip"
    LINK_KEEP_USER_DEPT = "link_keep_user_dept"
    LINK_UPDATE_USER_DEPT = "link_update_user_dept"


class Command(BaseCommand):
    help = (
        "Импорт предрегистрации наставников из отчёта 1С. "
        "Ключ идемпотентности — табельный номер (ID Человека)."
    )

    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self._repository = PreRegisteredStudentRepository()
        self._department_conflict_action: DepartmentConflictAction | None = None

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=DEFAULT_FILE,
            help=f"Путь к отчёту (.xls/.xlsx), по умолчанию: {DEFAULT_FILE}",
        )
        parser.add_argument(
            "--non-interactive",
            action="store_true",
            help="Не спрашивать при конфликте подразделений (пропускать привязку)",
        )

    def handle(self, *args, **options):
        path = Path(options["file"]).resolve()
        if not path.is_file():
            raise CommandError(f"Файл не найден: {path}")

        non_interactive: bool = options["non_interactive"]
        df = self._read_teachers(path)
        rows = self._collect_unique_rows(df)

        users = list(User.objects.select_related("role", "department").all())
        by_name, by_tokens = build_user_name_indexes(users)

        created = 0
        updated = 0
        skipped = 0
        linked = 0
        duplicate_rows = 0
        departments_not_found = 0

        with transaction.atomic():
            for line_no, parsed in rows:
                try:
                    result = self._process_row(
                        line_no=line_no,
                        parsed=parsed,
                        by_name=by_name,
                        by_tokens=by_tokens,
                        non_interactive=non_interactive,
                    )
                except ValueError as exc:
                    self.stdout.write(
                        self.style.WARNING(f"Строка {line_no}: пропущена — {exc}")
                    )
                    skipped += 1
                    continue

                if result == "created":
                    created += 1
                elif result == "updated":
                    updated += 1
                elif result == "linked":
                    linked += 1
                elif result == "duplicate":
                    duplicate_rows += 1
                elif result == "dept_not_found":
                    departments_not_found += 1
                    created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {created}, обновлено {updated}, "
                f"привязано пользователей {linked}, пропущено {skipped}, "
                f"дубликатов строк {duplicate_rows}, "
                f"подразделений не найдено {departments_not_found}"
            )
        )

    def _process_row(
        self,
        *,
        line_no: int,
        parsed: PreRegisteredMentorImportRow,
        by_name: dict,
        by_tokens: dict,
        non_interactive: bool,
    ) -> str:
        """Обрабатывает одну строку импорта. Возвращает код результата."""
        department = resolve_department_by_name(parsed.department_name)
        department_id = department.pk if department is not None else None
        result_code = "updated"

        if parsed.department_name and department is None:
            self.stdout.write(
                self.style.WARNING(
                    f"Строка {line_no}: подразделение «{parsed.department_name}» "
                    "не найдено в БД"
                )
            )
            result_code = "dept_not_found"

        existing = self._repository.get_by_personnel_number(parsed.personnel_number)
        pre_registered, was_created = self._repository.upsert_mentor_from_import(
            row=parsed,
            department_id=department_id,
            existing=existing,
        )
        if was_created:
            result_code = (
                "created" if result_code != "dept_not_found" else "dept_not_found"
            )

        full_name = " ".join(
            part
            for part in (
                parsed.last_name,
                parsed.first_name,
                parsed.middle_name,
            )
            if part
        )
        matched_user = find_user_by_full_name(
            full_name, by_name=by_name, by_tokens=by_tokens
        )
        if matched_user is None:
            return result_code

        if self._link_user_if_appropriate(
            pre_registered=pre_registered,
            user=matched_user,
            import_department=department,
            line_no=line_no,
            non_interactive=non_interactive,
        ):
            return "linked"

        return result_code

    def _link_user_if_appropriate(
        self,
        *,
        pre_registered: PreRegisteredStudent,
        user: User,
        import_department,
        line_no: int,
        non_interactive: bool,
    ) -> bool:
        """Привязывает пользователя к предрегистрации с учётом конфликта подразделений."""
        if import_department is None:
            self._repository.link_user(pre_registered, user.pk)
            return True

        user_department_id = user.department_id
        if (
            user_department_id is not None
            and import_department is not None
            and user_department_id != import_department.pk
        ):
            action = self._resolve_department_conflict(
                line_no=line_no,
                user=user,
                import_department=import_department,
                non_interactive=non_interactive,
            )
            if action == DepartmentConflictAction.SKIP:
                self.stdout.write(
                    self.style.WARNING(
                        f"Строка {line_no}: привязка к {user.email} пропущена "
                        f"(подразделение пользователя: "
                        f"{user.department.name if user.department else '—'}, "
                        f"из файла: {import_department.name})"
                    )
                )
                return False

            self._repository.link_user(pre_registered, user.pk)
            if action == DepartmentConflictAction.LINK_UPDATE_USER_DEPT:
                user.department = import_department
                user.save(update_fields=["department"])
            return True

        self._repository.link_user(pre_registered, user.pk)
        return True

    def _resolve_department_conflict(
        self,
        *,
        line_no: int,
        user: User,
        import_department,
        non_interactive: bool,
    ) -> DepartmentConflictAction:
        """Запрашивает действие при расхождении подразделений."""
        if self._department_conflict_action is not None:
            return self._department_conflict_action

        if non_interactive or not sys.stdin.isatty():
            self.stdout.write(
                self.style.WARNING(
                    f"Строка {line_no}: конфликт подразделений для {user.email} "
                    "(неинтерактивный режим — пропуск привязки)"
                )
            )
            return DepartmentConflictAction.SKIP

        user_dept = user.department.name if user.department else "—"
        self.stdout.write("")
        self.stdout.write(
            f"Строка {line_no}: пользователь {user.get_full_name()} ({user.email}) "
            f"принадлежит подразделению «{user_dept}», "
            f"в файле — «{import_department.name}»."
        )
        self.stdout.write("[1] Пропустить привязку")
        self.stdout.write("[2] Привязать, оставить подразделение пользователя")
        self.stdout.write("[3] Привязать и обновить подразделение пользователя")
        self.stdout.write("[4] Применить выбор ко всем аналогичным конфликтам")

        while True:
            choice = input("Выберите действие [1-4]: ").strip()
            action = self._choice_to_action(choice)
            if action is None:
                self.stdout.write(self.style.WARNING("Некорректный выбор, повторите."))
                continue
            if choice == "4":
                self._department_conflict_action = action
            return action

    @staticmethod
    def _choice_to_action(choice: str) -> DepartmentConflictAction | None:
        """Преобразует ввод пользователя в действие."""
        mapping = {
            "1": DepartmentConflictAction.SKIP,
            "2": DepartmentConflictAction.LINK_KEEP_USER_DEPT,
            "3": DepartmentConflictAction.LINK_UPDATE_USER_DEPT,
        }
        return mapping.get(choice)

    def _collect_unique_rows(
        self, df: pd.DataFrame
    ) -> list[tuple[int, PreRegisteredMentorImportRow]]:
        """Собирает уникальные строки по ID Человека (первая запись побеждает)."""
        seen_personnel_numbers: set[str] = set()
        rows: list[tuple[int, PreRegisteredMentorImportRow]] = []

        for line_no, (_, row) in enumerate(df.iterrows(), start=HEADER_ROW + 2):
            personnel_number = normalize_cell(row.get("ID Человека"))
            if not personnel_number:
                continue
            if personnel_number in seen_personnel_numbers:
                self.stdout.write(
                    self.style.WARNING(
                        f"Строка {line_no}: дубликат ID Человека "
                        f"«{personnel_number}» — пропущена"
                    )
                )
                continue

            try:
                parsed = build_preregistered_mentor_import_row(
                    department_name=normalize_cell(row.get("Подразделение")),
                    full_name=normalize_cell(row.get("ФИО")),
                    personnel_number=personnel_number,
                )
            except ValueError as exc:
                self.stdout.write(
                    self.style.WARNING(f"Строка {line_no}: пропущена — {exc}")
                )
                continue

            seen_personnel_numbers.add(parsed.personnel_number)
            rows.append((line_no, parsed))

        return rows

    def _read_teachers(self, path: Path) -> pd.DataFrame:
        """Читает отчёт преподавателей; заголовок колонок — вторая строка."""
        try:
            df = pd.read_excel(path, header=HEADER_ROW, dtype=object)
        except ValueError as exc:
            raise CommandError(f"Не удалось прочитать файл {path.name}: {exc}") from exc

        if df.empty:
            raise CommandError("Файл не содержит данных")

        missing = set(MENTOR_REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise CommandError(
                "В файле отсутствуют обязательные колонки: "
                + ", ".join(sorted(missing))
            )
        return df
