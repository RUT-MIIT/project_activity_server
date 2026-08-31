"""Чистая логика импорта предрегистрации наставников из отчёта 1С."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import TYPE_CHECKING

from accounts.domain.preregistered_student_import import parse_full_name
from teams.domain.study_group_import import normalize_cell

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

    from accounts.models import Department

MENTOR_REQUIRED_COLUMNS = (
    "Подразделение",
    "ФИО",
    "ID Человека",
)

_NAME_CLEANUP_PATTERN = re.compile(r"[^a-zа-я0-9\s]")


@dataclass(frozen=True)
class PreRegisteredMentorImportRow:
    """Строка отчёта, подготовленная к импорту одной предрегистрации наставника."""

    last_name: str
    first_name: str
    middle_name: str
    personnel_number: str
    department_name: str


def normalize_user_name(value: str | None) -> str:
    """Нормализует ФИО для сравнения."""
    if not value:
        return ""
    text = str(value).strip().lower().replace("ё", "е")
    text = re.sub(r"\s+", " ", text)
    text = _NAME_CLEANUP_PATTERN.sub("", text)
    return text


def token_key(value: str | None) -> tuple[str, ...]:
    """Ключ из набора слов ФИО (устойчив к перестановке частей)."""
    normalized = normalize_user_name(value)
    if not normalized:
        return tuple()
    return tuple(sorted(normalized.split()))


def build_user_name_indexes(
    users: list[AbstractBaseUser],
) -> tuple[dict[str, AbstractBaseUser], dict[tuple[str, ...], list[AbstractBaseUser]]]:
    """Строит индексы пользователей по ФИО."""
    by_name: dict[str, AbstractBaseUser] = {}
    by_tokens: dict[tuple[str, ...], list[AbstractBaseUser]] = {}
    for user in users:
        full_name = user.get_full_name()
        norm = normalize_user_name(full_name)
        if norm:
            by_name.setdefault(norm, user)
        tokens = token_key(full_name)
        if tokens:
            by_tokens.setdefault(tokens, []).append(user)
    return by_name, by_tokens


def find_user_by_full_name(
    full_name: str | None,
    *,
    by_name: dict[str, AbstractBaseUser],
    by_tokens: dict[tuple[str, ...], list[AbstractBaseUser]],
) -> AbstractBaseUser | None:
    """Ищет пользователя по ФИО."""
    norm = normalize_user_name(full_name)
    if not norm:
        return None
    if norm in by_name:
        return by_name[norm]
    matches = by_tokens.get(token_key(full_name), [])
    if len(matches) == 1:
        return matches[0]
    return None


def resolve_department_by_name(name: str) -> Department | None:
    """Ищет подразделение по имени без учёта регистра."""
    from accounts.models import Department

    cleaned = normalize_cell(name)
    if not cleaned:
        return None
    target = cleaned.casefold()
    for department in Department.objects.all():
        if department.name.casefold() == target:
            return department
    return None


def build_preregistered_mentor_import_row(
    *,
    department_name: str,
    full_name: str,
    personnel_number: str,
) -> PreRegisteredMentorImportRow:
    """Собирает DTO одной предрегистрации наставника из полей строки отчёта."""
    last_name, first_name, middle_name = parse_full_name(full_name)
    tab_number = normalize_cell(personnel_number)
    dept_name = normalize_cell(department_name)

    if not tab_number:
        raise ValueError("Пустой табельный номер (ID Человека)")

    return PreRegisteredMentorImportRow(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        personnel_number=tab_number,
        department_name=dept_name,
    )
