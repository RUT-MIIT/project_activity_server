"""Формирование Excel-выгрузки студентов института."""

from __future__ import annotations

from io import BytesIO
from typing import Any

from openpyxl import Workbook

HEADERS: tuple[str, ...] = (
    "Студент",
    "Группа",
    "Наставник",
    "Команда",
    "Роль",
    "Проект",
)

_ROLE_LABELS: dict[str, str] = {
    "leader": "Капитан",
    "member": "Участник",
}


def format_student_full_name(student: dict[str, Any]) -> str:
    """Собирает ФИО студента из полей lastName/firstName/middleName."""
    parts = [
        student.get("lastName") or "",
        student.get("firstName") or "",
        student.get("middleName") or "",
    ]
    return " ".join(part for part in parts if part).strip()


def format_mentors(mentors: list[dict[str, Any]] | None) -> str:
    """Объединяет ФИО наставников через точку с запятой."""
    if not mentors:
        return ""
    names = [
        (mentor.get("fullName") or "").strip()
        for mentor in mentors
        if (mentor.get("fullName") or "").strip()
    ]
    return "; ".join(names)


def format_role(role: str | None) -> str:
    """Переводит код роли команды в русскую подпись для Excel."""
    if not role:
        return ""
    return _ROLE_LABELS.get(role, "")


def student_dict_to_row(student: dict[str, Any]) -> tuple[str, ...]:
    """Преобразует словарь студента (как в JSON API) в строку Excel."""
    study_group = student.get("studyGroup") or {}
    project = student.get("project") or {}
    return (
        format_student_full_name(student),
        study_group.get("name") or "",
        format_mentors(student.get("mentors")),
        student.get("teamName") or "",
        format_role(student.get("teamRole")),
        project.get("title") or "",
    )


def build_students_xlsx(students: list[dict[str, Any]]) -> bytes:
    """Строит xlsx-файл со списком студентов и возвращает байты."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Студенты"
    sheet.append(list(HEADERS))
    for student in students:
        sheet.append(list(student_dict_to_row(student)))

    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()
