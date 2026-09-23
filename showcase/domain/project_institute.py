"""Резолв института проектной заявки для stats/дашбордов."""

from __future__ import annotations

from showcase.dto.project import ProjectListDTO
from showcase.models import ProjectApplication


def resolve_application_institute(
    application: ProjectApplication,
    department_institute_map: dict[int, dict[str, str]],
) -> dict[str, str]:
    """Институт заявки по верхнему причастному подразделению.

    Использует ту же логику выбора подразделения, что и ProjectListDTO
    (исключая ЦПДС). Если маппинг не найден — пустой снимок.
    """
    department = ProjectListDTO._top_level_involved_department(application)
    if department is None:
        return {"id": "", "name": ""}
    return department_institute_map.get(department.id, {"id": "", "name": ""})
