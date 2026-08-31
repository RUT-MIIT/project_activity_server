"""Сравнение имён подразделений Excel и БД (кавычки)."""

from __future__ import annotations

import os
import re
import sys

import django
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.domain.preregistered_mentor_import import resolve_department_by_name
from accounts.models import Department
from teams.domain.study_group_import import normalize_cell

QUOTE_CHARS = "\"'«»„“”‚‘’`"


def normalize_department_name(name: str) -> str:
    """Нормализует имя подразделения для сравнения."""
    text = normalize_cell(name).casefold().replace("ё", "е")
    for char in QUOTE_CHARS:
        text = text.replace(char, "")
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    df = pd.read_excel("data/преподаватели.xls", header=1, dtype=object)
    excel_names = sorted(
        {
            normalize_cell(value)
            for value in df["Подразделение"].dropna()
            if normalize_cell(value)
        }
    )
    db_names = list(Department.objects.values_list("name", flat=True))
    db_norm = {normalize_department_name(name): name for name in db_names}

    exact_missing = [
        name for name in excel_names if resolve_department_by_name(name) is None
    ]
    norm_matches: list[tuple[str, str]] = []
    for name in exact_missing:
        key = normalize_department_name(name)
        if key in db_norm:
            norm_matches.append((name, db_norm[key]))

    print(f"Уникальных в Excel: {len(excel_names)}")
    print(f"В БД: {len(db_names)}")
    print(f"Не найдено (точное сравнение): {len(exact_missing)}")
    print(f"Из них совпало бы после нормализации кавычек: {len(norm_matches)}")
    print()
    for excel_name, db_name in norm_matches[:10]:
        print(f"Excel: {excel_name}")
        print(f"  БД: {db_name}")
        print()

    still_missing = [
        name for name in exact_missing if normalize_department_name(name) not in db_norm
    ]
    print(f"Всё ещё нет в БД (даже с нормализацией): {len(still_missing)}")
    for name in still_missing:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
