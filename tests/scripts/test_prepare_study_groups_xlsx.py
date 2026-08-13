"""Тесты подготовки Excel контингента к импорту групп."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from scripts.prepare_study_groups_xlsx import (
    _extract_group_abbrev_from_text,
    _find_header_row,
    _parse_students_flat_table,
    _parse_students_synthetic,
    _parse_students_with_markers,
    prepare_workbook,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Группа : ЮЮП-261(кафедра 1)", "ЮЮП-261"),
        ("группа : ШЭТ-411", "ШЭТ-411"),
        ("не группа", None),
        ("", None),
    ],
)
def test_extract_group_abbrev_from_text(text: str, expected: str | None) -> None:
    """Извлекает аббревиатуру из маркера группы."""
    assert _extract_group_abbrev_from_text(text) == expected


def test_parse_students_with_markers_on_vish_sample() -> None:
    """Маркерный формат: группа берётся из строки «Группа : ...»."""
    input_path = PROJECT_ROOT / "data" / "ВИШ_01_09.xls"
    if not input_path.is_file():
        pytest.skip("Нет файла data/ВИШ_01_09.xls")

    raw = pd.read_excel(
        input_path, sheet_name=0, header=None, dtype=object, engine="xlrd"
    )
    header_row_idx, col_map = _find_header_row(raw)
    assert "Группа" not in col_map

    students = _parse_students_with_markers(
        raw, header_row_idx, col_map, col_map["ID_student"]
    )
    assert len(students) > 0
    assert all(s["Аббревеатура группа"] for s in students)


def test_parse_students_flat_table_on_yui_sample() -> None:
    """Плоский формат: группа берётся из колонки «Группа»."""
    input_path = PROJECT_ROOT / "raw" / "ЮРИДИЧЕСКИЙ ИНСТИТУТ.xls"
    if not input_path.is_file():
        pytest.skip("Нет файла raw/ЮРИДИЧЕСКИЙ ИНСТИТУТ.xls")

    raw = pd.read_excel(
        input_path, sheet_name=0, header=None, dtype=object, engine="xlrd"
    )
    header_row_idx, col_map = _find_header_row(raw)
    assert "Группа" in col_map

    students = _parse_students_flat_table(
        raw, header_row_idx, col_map, col_map["ID_student"]
    )
    assert len(students) == 2092
    assert {s["Аббревеатура группа"] for s in students if s["Аббревеатура группа"]}


def test_parse_students_synthetic_on_avt_sample() -> None:
    """Синтетический формат: группа из профиля+курса+направления."""
    input_path = PROJECT_ROOT / "raw" / "Академия водного транспорта.xls"
    if not input_path.is_file():
        pytest.skip("Нет файла raw/Академия водного транспорта.xls")

    raw = pd.read_excel(
        input_path, sheet_name=0, header=None, dtype=object, engine="xlrd"
    )
    header_row_idx, col_map = _find_header_row(raw)
    assert "Группа" not in col_map

    students = _parse_students_synthetic(
        raw, header_row_idx, col_map, col_map["ID_student"], "AVT"
    )
    assert len(students) == 536
    codes = {student["Аббревеатура группа"] for student in students}
    assert all(code.startswith("AVT-") for code in codes)
    assert len(codes) == 38


def test_prepare_workbook_yui_creates_groups_sheet(tmp_path: Path) -> None:
    """Полный прогон для ЮИ создаёт лист groups с нужными колонками."""
    input_path = PROJECT_ROOT / "raw" / "ЮРИДИЧЕСКИЙ ИНСТИТУТ.xls"
    if not input_path.is_file():
        pytest.skip("Нет файла raw/ЮРИДИЧЕСКИЙ ИНСТИТУТ.xls")

    output_path = tmp_path / "ЮИ_01_09_аббр.xlsx"
    prepare_workbook(input_path=input_path, output_path=output_path)

    students = pd.read_excel(output_path, sheet_name="students", dtype=object)
    groups = pd.read_excel(output_path, sheet_name="groups", dtype=object)
    assert len(students) == 2092
    assert len(groups) > 100
    assert groups.shape[1] >= 8
    assert groups.iloc[0, 6]  # аббревиатура группы не пустая
