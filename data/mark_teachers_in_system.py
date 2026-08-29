"""Сверка преподавателей из Excel со списком пользователей prod API."""

from __future__ import annotations

import json
from pathlib import Path
import re

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

DATA_DIR = Path(__file__).resolve().parent
USERS_JSON = DATA_DIR / "prod_users.json"
SOURCE_XLSX = DATA_DIR / "project_teachers.xlsx"
OUTPUT_XLSX = DATA_DIR / "project_teachers_marked.xlsx"
SHEET_NAME = "Проектная деятельность"

COL_TEACHER_FIO = 9  # I
COL_IN_SYSTEM = 14  # N
COL_USER_ID = 15  # O
COL_USER_EMAIL = 16  # P


def normalize_name(value: str | None) -> str:
    """Нормализует ФИО для сравнения."""
    if not value:
        return ""
    text = str(value).strip().lower().replace("ё", "е")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zа-я0-9\s]", "", text)
    return text


def token_key(value: str | None) -> tuple[str, ...]:
    """Ключ из набора слов ФИО (устойчив к перестановке частей)."""
    normalized = normalize_name(value)
    if not normalized:
        return tuple()
    return tuple(sorted(normalized.split()))


def build_user_indexes(
    users: list[dict],
) -> tuple[dict[str, dict], dict[tuple[str, ...], list[dict]]]:
    """Строит индексы пользователей по ФИО."""
    by_name: dict[str, dict] = {}
    by_tokens: dict[tuple[str, ...], list[dict]] = {}
    for user in users:
        full_name = user.get("full_name") or ""
        norm = normalize_name(full_name)
        if norm:
            by_name.setdefault(norm, user)
        tokens = token_key(full_name)
        if tokens:
            by_tokens.setdefault(tokens, []).append(user)
    return by_name, by_tokens


def find_user(
    teacher_name: str | None,
    *,
    by_name: dict[str, dict],
    by_tokens: dict[tuple[str, ...], list[dict]],
) -> dict | None:
    """Ищет пользователя по ФИО преподавателя."""
    norm = normalize_name(teacher_name)
    if not norm:
        return None
    if norm in by_name:
        return by_name[norm]
    matches = by_tokens.get(token_key(teacher_name), [])
    if len(matches) == 1:
        return matches[0]
    return None


def main() -> None:
    """Отмечает преподавателей из Excel, которые есть в prod."""
    users = json.loads(USERS_JSON.read_text(encoding="utf-8"))
    by_name, by_tokens = build_user_indexes(users)

    workbook = load_workbook(SOURCE_XLSX)
    sheet = workbook[SHEET_NAME]

    header_font = Font(bold=True)
    header_fill = PatternFill(fill_type="solid", fgColor="FFE2EFDA")
    yes_fill = PatternFill(fill_type="solid", fgColor="FFC6EFCE")
    no_fill = PatternFill(fill_type="solid", fgColor="FFFFC7CE")

    sheet.cell(row=1, column=COL_IN_SYSTEM, value="В системе PD")
    sheet.cell(row=1, column=COL_USER_ID, value="ID в PD")
    sheet.cell(row=1, column=COL_USER_EMAIL, value="Email в PD")
    for col in (COL_IN_SYSTEM, COL_USER_ID, COL_USER_EMAIL):
        cell = sheet.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill

    found = 0
    missing = 0
    empty = 0

    for row in range(2, sheet.max_row + 1):
        teacher_name = sheet.cell(row=row, column=COL_TEACHER_FIO).value
        if not teacher_name or not str(teacher_name).strip():
            empty += 1
            continue

        user = find_user(str(teacher_name), by_name=by_name, by_tokens=by_tokens)
        in_system_cell = sheet.cell(row=row, column=COL_IN_SYSTEM)
        id_cell = sheet.cell(row=row, column=COL_USER_ID)
        email_cell = sheet.cell(row=row, column=COL_USER_EMAIL)

        if user:
            found += 1
            in_system_cell.value = "да"
            id_cell.value = user["id"]
            email_cell.value = user.get("email") or ""
            in_system_cell.fill = yes_fill
        else:
            missing += 1
            in_system_cell.value = "нет"
            id_cell.value = ""
            email_cell.value = ""
            in_system_cell.fill = no_fill

    workbook.save(OUTPUT_XLSX)
    print(f"Пользователей в API: {len(users)}")
    print(f"Строк с преподавателем: {found + missing}")
    print(f"Найдено в системе: {found}")
    print(f"Не найдено: {missing}")
    print(f"Пустых строк (без ФИО): {empty}")
    print(f"Сохранено: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
