"""Чистая логика импорта предрегистрации студентов из отчёта контингента 1С."""

from __future__ import annotations

from dataclasses import dataclass, field
import re

from teams.domain.study_group_import import (
    Semester,
    is_convergent_contingent_row,
    map_teaching_group_name_for_lookup,
    normalize_cell,
)

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
    teaching_group_name: str
    external_group_id: str
    course_from_file: str


@dataclass(frozen=True)
class StudyGroupRef:
    """Ссылка на учебную группу для резолвера без зависимости от ORM."""

    pk: int
    code: str
    name: str
    external_group_id: str


@dataclass
class StudyGroupLookup:
    """Индексы учебных групп для резолвинга при импорте студентов."""

    by_external_id: dict[str, StudyGroupRef] = field(default_factory=dict)
    by_code: dict[str, StudyGroupRef] = field(default_factory=dict)
    by_name: dict[str, list[StudyGroupRef]] = field(default_factory=dict)

    @classmethod
    def from_groups(cls, groups: list[StudyGroupRef]) -> StudyGroupLookup:
        """Строит lookup из списка групп."""
        lookup = cls()
        for group in groups:
            if group.external_group_id:
                lookup.by_external_id[group.external_group_id] = group
            if group.code:
                lookup.by_code[group.code] = group
            lookup.by_name.setdefault(group.name, []).append(group)
        return lookup


@dataclass(frozen=True)
class StudyGroupResolveResult:
    """Результат поиска учебной группы для строки студента."""

    group: StudyGroupRef | None
    reason: str | None = None


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
    teaching_group_name: str = "",
    external_group_id: str = "",
    course_from_file: object = "",
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
        teaching_group_name=normalize_cell(teaching_group_name),
        external_group_id=normalize_cell(external_group_id),
        course_from_file=normalize_cell(course_from_file),
    )


def resolve_study_group_for_student(
    row: PreRegisteredStudentImportRow,
    lookup: StudyGroupLookup,
    *,
    current_year: int,
    semester: Semester,
) -> StudyGroupResolveResult:
    """
    Определяет учебную группу для строки студента.

    Приоритет: external_group_id → code (сходящаяся строка) → name (отстающие).
    """
    if row.external_group_id:
        group = lookup.by_external_id.get(row.external_group_id)
        if group is not None:
            return StudyGroupResolveResult(group=group)

    is_convergent = is_convergent_contingent_row(
        row.group_code,
        row.teaching_group_name,
        row.course_from_file,
        current_year=current_year,
        semester=semester,
    )

    if is_convergent:
        group = lookup.by_code.get(row.group_code)
        if group is not None:
            return StudyGroupResolveResult(group=group)
        return StudyGroupResolveResult(
            group=None,
            reason=(
                f"постоянная группа «{row.group_code}» не найдена в БД "
                "(сначала import_study_groups_from_contingent)"
            ),
        )

    teaching_name = normalize_cell(row.teaching_group_name)
    if not teaching_name:
        return StudyGroupResolveResult(
            group=None,
            reason=(
                f"отстающий студент без колонки «Группа» "
                f"(постоянная «{row.group_code}»)"
            ),
        )

    lookup_name = map_teaching_group_name_for_lookup(teaching_name)
    matches = lookup.by_name.get(lookup_name, [])
    if len(matches) == 1:
        return StudyGroupResolveResult(group=matches[0])
    if len(matches) > 1:
        return StudyGroupResolveResult(
            group=None,
            reason=(
                f"неоднозначное имя учебной группы «{teaching_name}» "
                f"({len(matches)} совпадений)"
            ),
        )
    return StudyGroupResolveResult(
        group=None,
        reason=f"учебная группа «{teaching_name}» не найдена в БД",
    )
