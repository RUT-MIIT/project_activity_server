"""Чистая логика импорта преподавателей проектной деятельности из Excel."""

from __future__ import annotations

from dataclasses import dataclass
import re

from teams.domain.study_group_import import normalize_cell

SEMESTER_LABEL_PATTERN = re.compile(
    r"^(?P<num>\d+)-й\s+семестр\s+(?P<year_start>\d{4})-(?P<year_end>\d{4})$",
    re.IGNORECASE,
)

REQUIRED_COLUMNS = (
    "Группа",
    "Семестр",
    "Преподаватель (ФИО)",
    "ID преподавателя",
)


@dataclass(frozen=True)
class ProjectTeacherImportRow:
    """Строка отчёта, подготовленная к импорту одной связки группа–преподаватель."""

    group_name: str
    semester_label: str
    semester_code: str
    mentor_full_name: str
    external_teacher_id: str
    external_group_id: str
    mentor_short_name: str
    lesson_count: int | None
    import_status: str
    pd_user_id: int | None


def parse_semester_code(semester_label: str) -> str:
    """
    Преобразует подпись семестра из Excel в код модели Semester.

    Пример: «1-й семестр 2026-2027» → «26-27-1».

    Raises:
        ValueError: если формат не распознан.
    """
    cleaned = normalize_cell(semester_label)
    if not cleaned:
        raise ValueError("Пустое название семестра")

    match = SEMESTER_LABEL_PATTERN.match(cleaned)
    if match is None:
        raise ValueError(f"Некорректный формат семестра: «{cleaned}»")

    year_start = int(match.group("year_start"))
    year_end = int(match.group("year_end"))
    semester_num = int(match.group("num"))
    return f"{year_start % 100:02d}-{year_end % 100:02d}-{semester_num}"


def _parse_pd_user_id(value: object) -> int | None:
    """Парсит ID пользователя PD из ячейки Excel."""
    text = normalize_cell(value)
    if not text:
        return None
    try:
        numeric = float(text)
    except ValueError as exc:
        raise ValueError(f"Некорректный ID в PD: «{text}»") from exc
    if numeric != int(numeric):
        raise ValueError(f"Некорректный ID в PD: «{text}»")
    return int(numeric)


def _parse_lesson_count(value: object) -> int | None:
    """Парсит количество пар из ячейки Excel."""
    text = normalize_cell(value)
    if not text:
        return None
    try:
        numeric = float(text)
    except ValueError as exc:
        raise ValueError(f"Некорректное кол-во пар: «{text}»") from exc
    if numeric < 0:
        raise ValueError(f"Некорректное кол-во пар: «{text}»")
    return int(numeric)


def build_project_teacher_import_row(
    *,
    group_name: str,
    semester_label: str,
    mentor_full_name: str,
    external_teacher_id: str,
    external_group_id: str = "",
    mentor_short_name: str = "",
    lesson_count: object = None,
    import_status: str = "",
    pd_user_id: object = None,
) -> ProjectTeacherImportRow:
    """
    Валидирует и нормализует строку импорта преподавателя проектной деятельности.

    Raises:
        ValueError: если обязательные поля пусты или некорректны.
    """
    cleaned_group_name = normalize_cell(group_name)
    cleaned_mentor_full_name = normalize_cell(mentor_full_name)
    cleaned_teacher_id = normalize_cell(external_teacher_id)

    if not cleaned_group_name:
        raise ValueError("Пустое название группы")
    if not cleaned_mentor_full_name:
        raise ValueError("Пустое ФИО преподавателя")
    if not cleaned_teacher_id:
        raise ValueError("Пустой ID преподавателя")

    try:
        teacher_numeric = float(cleaned_teacher_id)
    except ValueError as exc:
        raise ValueError(
            f"Некорректный ID преподавателя: «{cleaned_teacher_id}»"
        ) from exc
    if teacher_numeric != int(teacher_numeric):
        raise ValueError(f"Некорректный ID преподавателя: «{cleaned_teacher_id}»")

    return ProjectTeacherImportRow(
        group_name=cleaned_group_name,
        semester_label=normalize_cell(semester_label),
        semester_code=parse_semester_code(semester_label),
        mentor_full_name=cleaned_mentor_full_name,
        external_teacher_id=str(int(teacher_numeric)),
        external_group_id=normalize_cell(external_group_id),
        mentor_short_name=normalize_cell(mentor_short_name),
        lesson_count=_parse_lesson_count(lesson_count),
        import_status=normalize_cell(import_status),
        pd_user_id=_parse_pd_user_id(pd_user_id),
    )
