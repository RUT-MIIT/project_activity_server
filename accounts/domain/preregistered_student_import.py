"""Чистая логика импорта предрегистрации студентов из отчёта контингента 1С."""

from __future__ import annotations

from dataclasses import dataclass
import re

from teams.domain.study_group_import import normalize_cell

REQUIRED_COLUMNS = (
    "ФИО (полное)",
    "Студенческий билет",
    "СНИЛС",
    "ID_E человека",
    "Постоянная группа",
)

SNILS_DIGITS_PATTERN = re.compile(r"\D+")


@dataclass(frozen=True)
class PreRegisteredStudentImportRow:
    """Строка отчёта, подготовленная к импорту одной предрегистрации."""

    last_name: str
    first_name: str
    middle_name: str
    student_card: str
    snils: str
    personnel_number: str
    group_code: str


def normalize_snils(value: object) -> str:
    """Нормализует СНИЛС до 11 цифр или пустой строки."""
    text = normalize_cell(value)
    if not text:
        return ""
    digits = SNILS_DIGITS_PATTERN.sub("", text)
    if not digits:
        return ""
    if len(digits) != 11:
        raise ValueError(f"Некорректный СНИЛС: «{text}»")
    return digits


def last_names_match(stored: str, provided: str) -> bool:
    """Сравнивает фамилии без учёта регистра и лишних пробелов."""
    return normalize_cell(stored).casefold() == normalize_cell(provided).casefold()


def parse_full_name(full_name: str) -> tuple[str, str, str]:
    """
    Разбирает ФИО из отчёта контингента.

    Returns:
        Кортеж (фамилия, имя, отчество).
    """
    cleaned = normalize_cell(full_name)
    if not cleaned:
        raise ValueError("Пустое ФИО")

    parts = cleaned.split()
    if len(parts) < 2:
        raise ValueError(f"Некорректное ФИО: «{full_name}»")

    last_name = parts[0]
    first_name = parts[1]
    middle_name = " ".join(parts[2:]) if len(parts) > 2 else ""
    return last_name, first_name, middle_name


def build_preregistered_student_import_row(
    *,
    full_name: str,
    student_card: str,
    snils: str,
    personnel_number: str,
    permanent_group_code: str,
) -> PreRegisteredStudentImportRow:
    """Собирает DTO одной предрегистрации из полей строки отчёта."""
    last_name, first_name, middle_name = parse_full_name(full_name)
    card = normalize_cell(student_card)
    tab_number = normalize_cell(personnel_number)
    group_code = normalize_cell(permanent_group_code)

    if not card:
        raise ValueError("Пустой студенческий билет")
    if not tab_number:
        raise ValueError("Пустой табельный номер (ID_E человека)")
    if not group_code:
        raise ValueError("Пустая постоянная группа")

    return PreRegisteredStudentImportRow(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        student_card=card,
        snils=normalize_snils(snils),
        personnel_number=tab_number,
        group_code=group_code,
    )
