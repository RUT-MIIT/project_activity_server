"""Чистая логика импорта предрегистрации студентов из отчёта контингента 1С."""

from __future__ import annotations

from dataclasses import dataclass, field
import re

from teams.domain.study_group_import import normalize_cell, remap_external_group_id

REQUIRED_COLUMNS = (
    "ФИО (полное)",
    "Студенческий билет",
    "СНИЛС",
    "ID_E человека",
    "Постоянная группа",
    "ID группы",
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
    is_end: bool = False


@dataclass
class StudyGroupLookup:
    """Индексы учебных групп для резолвинга при импорте студентов."""

    by_external_id: dict[str, StudyGroupRef] = field(default_factory=dict)

    @classmethod
    def from_groups(cls, groups: list[StudyGroupRef]) -> StudyGroupLookup:
        """Строит lookup из списка групп по ID группы 1С."""
        lookup = cls()
        for group in groups:
            if group.external_group_id:
                lookup.by_external_id[group.external_group_id] = group
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
    remapped_id = remap_external_group_id(external_group_id)

    if not card:
        raise ValueError("Пустой студенческий билет")
    if not tab_number:
        raise ValueError("Пустой табельный номер (ID_E человека)")
    if not group_code:
        raise ValueError("Пустая постоянная группа")
    if not remapped_id:
        raise ValueError("Пустой ID группы")

    return PreRegisteredStudentImportRow(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        student_card=card,
        snils=normalize_snils(snils),
        personnel_number=tab_number,
        group_code=group_code,
        teaching_group_name=normalize_cell(teaching_group_name),
        external_group_id=remapped_id,
        course_from_file=normalize_cell(course_from_file),
    )


def resolve_study_group_for_student(
    row: PreRegisteredStudentImportRow,
    lookup: StudyGroupLookup,
) -> StudyGroupResolveResult:
    """
    Определяет учебную группу для строки студента по ID группы 1С.

    ID уже должен быть пропущен через remap_external_group_id.
    """
    if not row.external_group_id:
        return StudyGroupResolveResult(
            group=None,
            reason="не указан ID группы",
        )

    group = lookup.by_external_id.get(row.external_group_id)
    if group is None:
        return StudyGroupResolveResult(
            group=None,
            reason=(
                f"учебная группа с ID «{row.external_group_id}» не найдена в БД "
                "(сначала import_study_groups_from_contingent)"
            ),
        )
    if group.is_end:
        return StudyGroupResolveResult(
            group=None,
            reason=(
                f"учебная группа по ID «{row.external_group_id}» " "завершила обучение"
            ),
        )
    return StudyGroupResolveResult(group=group)
