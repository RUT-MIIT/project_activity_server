"""Формирование Excel-выгрузки комментариев составителю трека."""

from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING, Iterable

from openpyxl import Workbook

from accounts.utils import get_root_department

if TYPE_CHECKING:
    from showcase.models import ProjectApplication

HEADERS: tuple[str, ...] = (
    "Автор заявки",
    "Институт",
    "Название заявки",
    "Комментарий составителю трека",
)

SHEET_FILLED = "Заполненные"
SHEET_EMPTY = "Пустые"

EMPTY_TRACK_COMPOSER_COMMENT_PLACEHOLDERS: frozenset[str] = frozenset(
    {
        "",
        "-",
        "—",
        "–",
        ".",
        "…",
        "нет",
        "н/д",
        "н.д.",
        "n/a",
        "na",
        "нет комментария",
        "без комментария",
    }
)


def is_empty_track_composer_comment(text: str | None) -> bool:
    """Проверяет, что комментарий пустой или условно пустой (placeholder)."""
    normalized = (text or "").strip().casefold()
    return normalized in EMPTY_TRACK_COMPOSER_COMMENT_PLACEHOLDERS


def format_application_author_name(application: ProjectApplication) -> str:
    """Собирает ФИО автора из полей заявки author_* (пустые части пропускаются)."""
    parts = [
        application.author_lastname or "",
        application.author_firstname or "",
        application.author_middlename or "",
    ]
    return " ".join(part for part in parts if part).strip()


def resolve_author_institute_name(application: ProjectApplication) -> str:
    """Возвращает наименование корневого подразделения автора или пустую строку."""
    author = application.author
    if author is None:
        return ""
    department = getattr(author, "department", None)
    root = get_root_department(department)
    if root is None:
        return ""
    return root.name or ""


def application_to_row(application: ProjectApplication) -> tuple[str, ...]:
    """Преобразует заявку в строку Excel-отчёта."""
    return (
        format_application_author_name(application),
        resolve_author_institute_name(application),
        application.title or "",
        application.track_composer_comment or "",
    )


def build_track_composer_comment_xlsx(
    applications: Iterable[ProjectApplication],
) -> bytes:
    """Строит xlsx с двумя листами: заполненные и пустые комментарии."""
    workbook = Workbook()
    filled_sheet = workbook.active
    filled_sheet.title = SHEET_FILLED
    filled_sheet.append(list(HEADERS))

    empty_sheet = workbook.create_sheet(SHEET_EMPTY)
    empty_sheet.append(list(HEADERS))

    for application in applications:
        row = list(application_to_row(application))
        if is_empty_track_composer_comment(application.track_composer_comment):
            empty_sheet.append(row)
        else:
            filled_sheet.append(row)

    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()
