"""Доменная логика импорта проектных заявок из Excel."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import re
from typing import Any

import pandas as pd

from showcase.dto.application import ProjectApplicationCreateDTO

COLUMN_ORDER_NUMBER = "Порядковый номер"
COLUMN_CUSTOMER_TYPE = "ТИП Организация-заказчик*"
COLUMN_COMPANY = "Организация-заказчик*"
COLUMN_COMPANY_CONTACTS = "Контактные данные заказчика*"
COLUMN_PROJECT_LEVEL = "Уровень проекта**"
COLUMN_TARGET_INSTITUTES = "Институт/академия"
COLUMN_PROBLEM_HOLDER = "Носитель проблемы"
COLUMN_GOAL = "Цель"
COLUMN_BARRIER = "Барьер"
COLUMN_EXISTING_SOLUTIONS = "Существующие решения"
COLUMN_CONTEXT = "Контекст проекта*"
COLUMN_STAKEHOLDERS = "Другие заинтересованные стороны"
COLUMN_RECOMMENDED_TOOLS = "Рекомендуемые инструменты"
COLUMN_EXPERTS = "Эксперты"
COLUMN_DIRECTION = "Направление проекта"
COLUMN_ADDITIONAL_MATERIALS = "Дополнительные материалы"
COLUMN_TITLE = "Название проекта"

INSTITUTE_NAME_ALIASES: dict[str, str] = {
    "ИМТК": "IMTK",
    "ИУЦТ": "IUCT",
    "ИЖТ": "IZhT",
    "ИЭФ": "IEF",
    "ИСТИ": "ISTI",
    "ИТТСУ": "ITTSY",
    "АВТ": "AVT",
    "АГА": "AGA",
    "АДХ": "ADH",
    "ВИШ": "VISH",
    "ИПСС": "IPSS",
    "ЮИ": "YUI",
    "ПИШ ВСМ": "VSM",
}


@dataclass(frozen=True)
class ApplicationImportRow:
    """Строка Excel, подготовленная к импорту заявки."""

    row_number: int
    dto: ProjectApplicationCreateDTO
    is_external: bool
    is_internal_customer: bool
    tag_name: str | None
    target_institute_codes: list[str]


def normalize_cell(value: Any) -> str:
    """Приводит значение ячейки Excel к нормализованной строке."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def parse_author_name(author: str) -> tuple[str, str]:
    """Разбирает строку вида «Фамилия Имя» на фамилию и имя."""
    parts = author.strip().split(maxsplit=1)
    if not parts:
        raise ValueError("Имя автора не может быть пустым")
    last_name = parts[0]
    first_name = parts[1] if len(parts) > 1 else ""
    if not first_name:
        raise ValueError(
            f"Укажите автора в формате «Фамилия Имя», получено: {author!r}"
        )
    return last_name, first_name


def parse_institute_codes(raw_value: str) -> list[str]:
    """Преобразует значение колонки институтов в коды справочника."""
    if not raw_value:
        return []

    codes: list[str] = []
    for part in re.split(r"[,;]", raw_value):
        token = part.strip()
        if not token:
            continue
        upper_token = token.upper()
        if upper_token in INSTITUTE_NAME_ALIASES:
            codes.append(INSTITUTE_NAME_ALIASES[upper_token])
            continue
        if token in INSTITUTE_NAME_ALIASES.values():
            codes.append(token)
            continue
        raise ValueError(f"Неизвестный институт в файле: {token!r}")
    return codes


def parse_customer_type(raw_value: str) -> tuple[bool, bool]:
    """Возвращает (is_external, is_internal_customer) по типу заказчика."""
    normalized = normalize_cell(raw_value).lower()
    if normalized == "внешний":
        return True, False
    if normalized == "внутренний":
        return False, True
    if not normalized:
        return False, False
    raise ValueError(f"Неизвестный тип организации-заказчика: {raw_value!r}")


def is_data_row(row: Mapping[str, Any]) -> bool:
    """Проверяет, что строка содержит данные заявки, а не заголовок/подсказку."""
    order_number = row.get(COLUMN_ORDER_NUMBER)
    if order_number is None or (
        isinstance(order_number, float) and pd.isna(order_number)
    ):
        return False
    if isinstance(order_number, str) and not order_number.strip():
        return False
    try:
        float(order_number)
    except (TypeError, ValueError):
        return False
    return bool(normalize_cell(row.get(COLUMN_COMPANY)))


def build_import_row(
    row: Mapping[str, Any],
    *,
    author_fields: Mapping[str, Any],
    default_institute_code: str,
    main_department_id: int | None,
    semester_id: int | None,
) -> ApplicationImportRow:
    """Собирает DTO и метаданные импорта из строки Excel."""
    row_number = int(float(row[COLUMN_ORDER_NUMBER]))
    is_external, is_internal_customer = parse_customer_type(
        normalize_cell(row.get(COLUMN_CUSTOMER_TYPE))
    )

    target_institute_codes = parse_institute_codes(
        normalize_cell(row.get(COLUMN_TARGET_INSTITUTES))
    )
    if not target_institute_codes:
        target_institute_codes = [default_institute_code]

    dto = ProjectApplicationCreateDTO(
        title=normalize_cell(row.get(COLUMN_TITLE)),
        company=normalize_cell(row.get(COLUMN_COMPANY)),
        company_contacts=normalize_cell(row.get(COLUMN_COMPANY_CONTACTS)),
        project_level=normalize_cell(row.get(COLUMN_PROJECT_LEVEL)),
        problem_holder=normalize_cell(row.get(COLUMN_PROBLEM_HOLDER)),
        goal=normalize_cell(row.get(COLUMN_GOAL)),
        barrier=normalize_cell(row.get(COLUMN_BARRIER)),
        existing_solutions=normalize_cell(row.get(COLUMN_EXISTING_SOLUTIONS)),
        context=normalize_cell(row.get(COLUMN_CONTEXT)) or None,
        stakeholders=normalize_cell(row.get(COLUMN_STAKEHOLDERS)) or None,
        recommended_tools=normalize_cell(row.get(COLUMN_RECOMMENDED_TOOLS)) or None,
        experts=normalize_cell(row.get(COLUMN_EXPERTS)) or None,
        additional_materials=(
            normalize_cell(row.get(COLUMN_ADDITIONAL_MATERIALS)) or None
        ),
        target_institutes=target_institute_codes,
        main_department_id=main_department_id,
        semester_id=semester_id,
        is_internal_customer=is_internal_customer,
        author_lastname=author_fields["author_lastname"],
        author_firstname=author_fields["author_firstname"],
        author_middlename=author_fields.get("author_middlename"),
        author_email=author_fields.get("author_email"),
        author_phone=author_fields.get("author_phone"),
        author_role=author_fields.get("author_role"),
        author_division=author_fields.get("author_division"),
    )

    tag_name = normalize_cell(row.get(COLUMN_DIRECTION)) or None
    return ApplicationImportRow(
        row_number=row_number,
        dto=dto,
        is_external=is_external,
        is_internal_customer=is_internal_customer,
        tag_name=tag_name,
        target_institute_codes=target_institute_codes,
    )


def iter_application_import_rows(
    df: pd.DataFrame,
    *,
    author_fields: Mapping[str, Any],
    default_institute_code: str,
    main_department_id: int | None,
    semester_id: int | None,
) -> list[ApplicationImportRow]:
    """Возвращает список строк импорта из DataFrame."""
    rows: list[ApplicationImportRow] = []
    for _, row in df.iterrows():
        if not is_data_row(row):
            continue
        rows.append(
            build_import_row(
                row,
                author_fields=author_fields,
                default_institute_code=default_institute_code,
                main_department_id=main_department_id,
                semester_id=semester_id,
            )
        )
    return rows
