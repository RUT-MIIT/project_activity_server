"""
Подготовка Excel контингента к импорту учебных групп.

Из отчёта 1С (маркеры «Группа : XXX(...)» + строки студентов) собирает
листы students и groups с аббревиатурой и годом приёма — как ИЭФ_01_09_аббр.xlsx.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
from typing import Any

import pandas as pd

STUDENT_COLUMNS = [
    "ФИО (полное)",
    "Специальность",
    "Кафедра",
    "Профиль/специализация/программа",
    "Форма обучения",
    "Курс",
    "Код специальности",
    "Направление специальности",
    "Дата планового окончания",
    "СНИЛС",
    "ID_student",
    "Аббревеатура группа",
    "Год приема",
]

GROUP_COLUMNS = [
    "Специальность",
    "Профиль/специализация/программа",
    "Форма обучения",
    "Курс",
    "Код специальности",
    "Дата планового окончания",
    "Аббревеатура группа",
    "Год приема",
]

# Соответствие заголовков отчёта → колонок выходного листа students
HEADER_ALIASES: dict[str, str] = {
    "фио (полное)": "ФИО (полное)",
    "фио": "ФИО (полное)",
    "специальность": "Специальность",
    "кафедра": "Кафедра",
    "профиль/специализация/программа": "Профиль/специализация/программа",
    "форма обучения": "Форма обучения",
    "курс": "Курс",
    "код специальности": "Код специальности",
    "направление специальности": "Направление специальности",
    "дата планового окончания": "Дата планового окончания",
    "снилс": "СНИЛС",
    "id_student": "ID_student",
}


def _normalize_header(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip().lower()


def _extract_group_abbrev_from_text(text: str) -> str | None:
    """Извлекает аббревиатуру из строки вида «Группа : XXX(...)»."""
    cleaned = text.strip()
    if not cleaned:
        return None
    if "группа" not in cleaned.lower() or ":" not in cleaned:
        return None
    match = re.search(r":\s*([^\(\r\n]+)", cleaned)
    if not match:
        return None
    candidate = match.group(1).strip()
    if not candidate:
        return None
    abbrev = candidate.split()[0].strip()
    return abbrev or None


def _looks_like_student_id(value: Any) -> bool:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        return value.strip().isdigit()
    return False


def _parse_enrollment_year(end_date: object, course: object) -> int | None:
    """Год приёма = год планового окончания − курс."""
    if end_date is None or (isinstance(end_date, float) and pd.isna(end_date)):
        return None
    if course is None or (isinstance(course, float) and pd.isna(course)):
        return None
    try:
        course_number = int(str(course).strip())
    except ValueError:
        return None

    year: int | None = None
    if isinstance(end_date, datetime):
        year = end_date.year
    elif hasattr(end_date, "year"):
        year = int(end_date.year)
    else:
        text = str(end_date).strip()
        for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
            try:
                year = datetime.strptime(text[:10], fmt).year
                break
            except ValueError:
                continue
        if year is None and len(text) >= 4 and text[:4].isdigit():
            # иногда дата приходит как Excel serial — pandas уже мог дать datetime
            try:
                year = int(pd.to_datetime(end_date).year)
            except Exception:
                return None

    if year is None:
        return None
    return year - course_number


def _find_header_row(df: pd.DataFrame) -> tuple[int, dict[str, int]]:
    """
    Находит строку заголовков с ID_student и карту имя_колонки → индекс.
    """
    for r in range(len(df)):
        col_map: dict[str, int] = {}
        for c in range(df.shape[1]):
            norm = _normalize_header(df.iloc[r, c])
            if norm in HEADER_ALIASES:
                col_map[HEADER_ALIASES[norm]] = c
        if "ID_student" in col_map:
            return r, col_map
    raise ValueError("Не найдена строка заголовков с ID_student")


def _cell_str(row: pd.Series, col_idx: int | None) -> str:
    if col_idx is None:
        return ""
    value = row.iloc[col_idx]
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def _fio_from_row(row: pd.Series, col_map: dict[str, int]) -> str:
    """
    ФИО в отчёте часто в колонке 1 (рядом с маркером группы),
    а заголовок «ФИО (полное)» — в колонке 0.
    """
    fio_col = col_map.get("ФИО (полное)")
    # Сначала колонка сразу после заголовка ФИО (обычно index+1)
    if fio_col is not None:
        for candidate in (fio_col + 1, fio_col):
            if 0 <= candidate < len(row):
                text = _cell_str(row, candidate)
                if text and "группа" not in text.lower():
                    return text
    # fallback: первая непустая текстовая ячейка слева от специальности
    spec_col = col_map.get("Специальность", len(row))
    for c in range(spec_col):
        text = _cell_str(row, c)
        if text and text != "-" and "группа" not in text.lower():
            return text
    return ""


def prepare_workbook(input_path: Path, output_path: Path) -> None:
    """Читает отчёт контингента и сохраняет students + groups."""
    engine = "xlrd" if input_path.suffix.lower() == ".xls" else "openpyxl"
    raw = pd.read_excel(
        input_path,
        sheet_name=0,
        header=None,
        dtype=object,
        engine=engine,
    )
    if raw.empty:
        raise ValueError(f"Пустой файл: {input_path}")

    header_row_idx, col_map = _find_header_row(raw)
    id_col = col_map["ID_student"]

    students: list[dict[str, Any]] = []
    current_abbrev: str | None = None

    for r in range(header_row_idx + 1, len(raw)):
        row = raw.iloc[r]

        # Обновляем текущую группу по маркеру в любой ячейке строки
        for c in range(raw.shape[1]):
            value = row.iloc[c]
            if isinstance(value, str) and value.strip():
                maybe = _extract_group_abbrev_from_text(value)
                if maybe:
                    current_abbrev = maybe
                    break

        if not _looks_like_student_id(row.iloc[id_col]):
            continue
        if not current_abbrev:
            continue

        course_raw = row.iloc[col_map["Курс"]] if "Курс" in col_map else None
        end_raw = (
            row.iloc[col_map["Дата планового окончания"]]
            if "Дата планового окончания" in col_map
            else None
        )
        enrollment_year = _parse_enrollment_year(end_raw, course_raw)

        students.append(
            {
                "ФИО (полное)": _fio_from_row(row, col_map),
                "Специальность": _cell_str(row, col_map.get("Специальность")),
                "Кафедра": _cell_str(row, col_map.get("Кафедра")),
                "Профиль/специализация/программа": _cell_str(
                    row, col_map.get("Профиль/специализация/программа")
                ),
                "Форма обучения": _cell_str(row, col_map.get("Форма обучения")),
                "Курс": course_raw,
                "Код специальности": _cell_str(row, col_map.get("Код специальности")),
                "Направление специальности": _cell_str(
                    row, col_map.get("Направление специальности")
                ),
                "Дата планового окончания": end_raw,
                "СНИЛС": _cell_str(row, col_map.get("СНИЛС")),
                "ID_student": row.iloc[id_col],
                "Аббревеатура группа": current_abbrev,
                "Год приема": enrollment_year,
            }
        )

    if not students:
        raise ValueError(
            "Не найдено строк студентов с аббревиатурой группы. "
            "Проверьте формат отчёта (маркеры «Группа : ...»)."
        )

    students_df = pd.DataFrame(students, columns=STUDENT_COLUMNS)

    groups_df = (
        students_df[GROUP_COLUMNS]
        .drop_duplicates()
        .sort_values(
            by=["Аббревеатура группа", "Курс", "Год приема"],
            kind="stable",
        )
        .reset_index(drop=True)
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        students_df.to_excel(writer, sheet_name="students", index=False)
        groups_df.to_excel(writer, sheet_name="groups", index=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Подготовка Excel контингента: листы students и groups "
            "с аббревиатурой группы и годом приёма."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Путь к исходному .xls/.xlsx отчёту.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Путь к выходному .xlsx (students + groups).",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    prepare_workbook(input_path=args.input, output_path=args.output)
    print(f"Сохранено: {args.output}")


if __name__ == "__main__":
    main()
