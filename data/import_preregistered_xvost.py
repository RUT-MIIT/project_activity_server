"""Импорт предрегистрации наставников из data/prerigistered_xvost.xlsx."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

import django
from django.contrib.auth import get_user_model
from django.db import transaction
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.domain.preregistered_mentor_import import (  # noqa: E402
    PreRegisteredMentorImportRow,
    build_user_name_indexes,
    find_user_by_full_name,
)
from accounts.domain.preregistered_xvost_import import (  # noqa: E402
    XVOST_REQUIRED_COLUMNS,
    build_preregistered_xvost_import_row,
    resolve_department_by_institute_label,
)
from accounts.repositories.preregistered_student import (  # noqa: E402
    PreRegisteredStudentRepository,
)
from teams.domain.study_group_import import normalize_cell  # noqa: E402

User = get_user_model()
DATA_DIR = Path(__file__).resolve().parent
DEFAULT_FILE = DATA_DIR / "prerigistered_xvost.xlsx"
HEADER_ROW = 0


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description=(
            "Импорт предрегистрации наставников из prerigistered_xvost.xlsx. "
            "Ключ идемпотентности — табельный номер для регистрации."
        )
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_FILE,
        help=f"Путь к Excel-файлу (по умолчанию: {DEFAULT_FILE})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только отчёт, без записи в БД",
    )
    parser.add_argument(
        "--no-link-users",
        action="store_true",
        help="Не привязывать существующих пользователей по ФИО",
    )
    return parser.parse_args()


def read_xvost_file(path: Path) -> pd.DataFrame:
    """Читает Excel-файл xvost и проверяет обязательные колонки."""
    try:
        df = pd.read_excel(path, header=HEADER_ROW, dtype=object)
    except ValueError as exc:
        raise SystemExit(f"Не удалось прочитать файл {path.name}: {exc}") from exc

    if df.empty:
        raise SystemExit("Файл не содержит данных")

    missing = set(XVOST_REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise SystemExit(
            "В файле отсутствуют обязательные колонки: " + ", ".join(sorted(missing))
        )
    return df


def collect_unique_rows(
    df: pd.DataFrame,
) -> list[tuple[int, PreRegisteredMentorImportRow, str]]:
    """Собирает уникальные строки по табельному номеру (первая запись побеждает)."""
    seen_personnel_numbers: set[str] = set()
    rows: list[tuple[int, PreRegisteredMentorImportRow, str]] = []

    for line_no, (_, row) in enumerate(df.iterrows(), start=HEADER_ROW + 2):
        personnel_number = normalize_cell(row.get("Табельный номер для регистрации"))
        if not personnel_number:
            continue
        if personnel_number in seen_personnel_numbers:
            print(
                f"Строка {line_no}: дубликат табельного номера "
                f"«{personnel_number}» — пропущена"
            )
            continue

        try:
            parsed = build_preregistered_xvost_import_row(
                last_name=normalize_cell(row.get("Фамилия")),
                first_name=normalize_cell(row.get("Имя")),
                middle_name=normalize_cell(row.get("Отчество")),
                personnel_number=personnel_number,
            )
        except ValueError as exc:
            print(f"Строка {line_no}: пропущена — {exc}")
            continue

        institute_label = normalize_cell(row.get("Институт"))
        seen_personnel_numbers.add(parsed.personnel_number)
        rows.append((line_no, parsed, institute_label))

    return rows


def full_name_from_row(parsed: PreRegisteredMentorImportRow) -> str:
    """Собирает полное ФИО из DTO предрегистрации."""
    return " ".join(
        part
        for part in (
            parsed.last_name,
            parsed.first_name,
            parsed.middle_name,
        )
        if part
    )


def should_link_user(
    *,
    user: User,
    import_department,
    line_no: int,
) -> bool:
    """Проверяет, можно ли привязать пользователя без интерактивного выбора."""
    if import_department is None:
        return True

    if user.department_id is None or user.department_id == import_department.pk:
        return True

    user_dept = user.department.name if user.department else "—"
    print(
        f"Строка {line_no}: привязка к {user.email} пропущена "
        f"(подразделение пользователя: {user_dept}, "
        f"из института: {import_department.name})"
    )
    return False


def process_row(
    *,
    line_no: int,
    parsed: PreRegisteredMentorImportRow,
    institute_label: str,
    repository: PreRegisteredStudentRepository,
    by_name: dict,
    by_tokens: dict,
    link_users: bool,
    dry_run: bool,
) -> str:
    """Обрабатывает одну строку импорта. Возвращает код результата."""
    department = None
    result_code = "updated"

    if institute_label:
        try:
            department = resolve_department_by_institute_label(institute_label)
        except ValueError as exc:
            print(f"Строка {line_no}: {exc}")
            result_code = "dept_not_found"
        if department is None and result_code != "dept_not_found":
            print(
                f"Строка {line_no}: у института «{institute_label}» "
                "не задано подразделение в БД"
            )
            result_code = "dept_not_found"
    else:
        print(f"Строка {line_no}: пустой институт")
        result_code = "dept_not_found"

    if dry_run:
        existing = repository.get_by_personnel_number(parsed.personnel_number)
        action = "создана" if existing is None else "обновлена"
        dept_name = department.name if department is not None else "—"
        print(
            f"Строка {line_no}: будет {action} предрегистрация "
            f"«{full_name_from_row(parsed)}» "
            f"({parsed.personnel_number}), подразделение: {dept_name}"
        )
        if result_code == "dept_not_found":
            return "created_no_dept" if existing is None else "updated_no_dept"
        return "created" if existing is None else "updated"

    department_id = department.pk if department is not None else None
    existing = repository.get_by_personnel_number(parsed.personnel_number)
    pre_registered, was_created = repository.upsert_mentor_from_import(
        row=parsed,
        department_id=department_id,
        existing=existing,
    )
    if was_created:
        result_code = (
            "created_no_dept" if result_code == "dept_not_found" else "created"
        )
    elif result_code == "dept_not_found":
        result_code = "updated_no_dept"
    else:
        result_code = "updated"

    if not link_users:
        return result_code

    matched_user = find_user_by_full_name(
        full_name_from_row(parsed),
        by_name=by_name,
        by_tokens=by_tokens,
    )
    if matched_user is None:
        return result_code

    if should_link_user(
        user=matched_user,
        import_department=department,
        line_no=line_no,
    ):
        repository.link_user(pre_registered, matched_user.pk)
        return "linked"

    return result_code


def main() -> None:
    """Точка входа скрипта импорта."""
    args = parse_args()
    path = args.file.resolve()
    if not path.is_file():
        raise SystemExit(f"Файл не найден: {path}")

    df = read_xvost_file(path)
    rows = collect_unique_rows(df)
    repository = PreRegisteredStudentRepository()
    link_users = not args.no_link_users

    users = list(User.objects.select_related("role", "department").all())
    by_name, by_tokens = build_user_name_indexes(users)

    created = 0
    updated = 0
    linked = 0
    skipped = 0
    departments_not_found = 0

    def run_import() -> None:
        nonlocal created, updated, linked, skipped, departments_not_found
        for line_no, parsed, institute_label in rows:
            result = process_row(
                line_no=line_no,
                parsed=parsed,
                institute_label=institute_label,
                repository=repository,
                by_name=by_name,
                by_tokens=by_tokens,
                link_users=link_users,
                dry_run=args.dry_run,
            )
            if result == "created":
                created += 1
            elif result == "updated":
                updated += 1
            elif result == "linked":
                linked += 1
            elif result == "created_no_dept":
                departments_not_found += 1
                created += 1
            elif result == "updated_no_dept":
                departments_not_found += 1
                updated += 1
            else:
                skipped += 1

    if args.dry_run:
        run_import()
    else:
        with transaction.atomic():
            run_import()

    mode = " (dry-run)" if args.dry_run else ""
    print(
        f"Готово{mode}: создано {created}, обновлено {updated}, "
        f"привязано пользователей {linked}, пропущено {skipped}, "
        f"без подразделения {departments_not_found}"
    )


if __name__ == "__main__":
    main()
