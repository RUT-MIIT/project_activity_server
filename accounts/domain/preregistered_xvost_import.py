"""Чистая логика импорта предрегистрации наставников из prerigistered_xvost.xlsx."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accounts.domain.preregistered_mentor_import import PreRegisteredMentorImportRow
from showcase.domain.application_import import INSTITUTE_NAME_ALIASES
from showcase.models import Institute
from teams.domain.study_group_import import normalize_cell

if TYPE_CHECKING:
    from accounts.models import Department

XVOST_REQUIRED_COLUMNS = (
    "Фамилия",
    "Имя",
    "Табельный номер для регистрации",
    "Институт",
)


def resolve_institute_code(label: str) -> str:
    """
    Возвращает код института по короткому названию из Excel.

    Raises:
        ValueError: если институт не найден в справочнике маппинга.
    """
    cleaned = normalize_cell(label)
    if not cleaned:
        raise ValueError("Пустой институт")

    if cleaned in INSTITUTE_NAME_ALIASES:
        return INSTITUTE_NAME_ALIASES[cleaned]

    upper_cleaned = cleaned.upper()
    if upper_cleaned in INSTITUTE_NAME_ALIASES.values():
        return upper_cleaned

    raise ValueError(f"Неизвестный институт: «{label}»")


def resolve_department_by_institute_label(label: str) -> Department | None:
    """Возвращает подразделение, связанное с институтом из колонки «Институт»."""
    institute_code = resolve_institute_code(label)
    institute = (
        Institute.objects.select_related("department")
        .filter(code=institute_code)
        .first()
    )
    if institute is None:
        raise ValueError(f"Институт с кодом «{institute_code}» не найден в БД")
    return institute.department


def build_preregistered_xvost_import_row(
    *,
    last_name: str,
    first_name: str,
    middle_name: str,
    personnel_number: str,
) -> PreRegisteredMentorImportRow:
    """Собирает DTO предрегистрации наставника из полей строки xvost-файла."""
    normalized_last_name = normalize_cell(last_name)
    normalized_first_name = normalize_cell(first_name)
    normalized_middle_name = normalize_cell(middle_name)
    tab_number = normalize_cell(personnel_number)

    if not normalized_last_name:
        raise ValueError("Пустая фамилия")
    if not normalized_first_name:
        raise ValueError("Пустое имя")
    if not tab_number:
        raise ValueError("Пустой табельный номер для регистрации")

    return PreRegisteredMentorImportRow(
        last_name=normalized_last_name,
        first_name=normalized_first_name,
        middle_name=normalized_middle_name,
        personnel_number=tab_number,
        department_name="",
    )
