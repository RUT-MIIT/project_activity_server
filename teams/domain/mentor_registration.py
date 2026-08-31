"""Чистая логика назначения групп наставнику при регистрации."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from accounts.domain.preregistered_mentor_import import normalize_user_name, token_key
from teams.domain.study_group_import import normalize_cell

if TYPE_CHECKING:
    from accounts.models import PreRegisteredStudent


@dataclass(frozen=True)
class MentorRegistrationContext:
    """Данные наставника для поиска в StudyGroupProjectTeacher."""

    personnel_number: str
    full_name: str


def normalize_personnel_number(value: str | None) -> str:
    """Нормализует табельный номер (ID преподавателя из 1С)."""
    text = normalize_cell(value)
    if not text:
        return ""
    try:
        numeric = float(text)
    except ValueError:
        return text
    if numeric == int(numeric):
        return str(int(numeric))
    return text


def build_mentor_full_name(
    *,
    last_name: str,
    first_name: str,
    middle_name: str = "",
) -> str:
    """Собирает полное ФИО из частей предрегистрации."""
    return " ".join(
        part for part in (last_name, first_name, middle_name) if normalize_cell(part)
    )


def build_mentor_registration_context(
    pre_registered: PreRegisteredStudent,
) -> MentorRegistrationContext:
    """Строит контекст поиска наставника из предрегистрации."""
    return MentorRegistrationContext(
        personnel_number=normalize_personnel_number(pre_registered.personnel_number),
        full_name=build_mentor_full_name(
            last_name=pre_registered.last_name,
            first_name=pre_registered.first_name,
            middle_name=pre_registered.middle_name,
        ),
    )


def mentor_full_name_matches(stored: str, provided: str) -> bool:
    """Сравнивает ФИО наставника (точное или по набору токенов)."""
    stored_norm = normalize_user_name(stored)
    provided_norm = normalize_user_name(provided)
    if not stored_norm or not provided_norm:
        return False
    if stored_norm == provided_norm:
        return True
    return token_key(stored) == token_key(provided) and len(token_key(stored)) > 0
