"""Общая логика доступа к институтам по подразделению пользователя."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accounts.models import User
from accounts.utils import get_department_subtree_ids, get_root_department
from showcase.models import Institute

if TYPE_CHECKING:
    from showcase.models import ProjectApplication


MANAGEMENT_ROLES = frozenset({"admin", "cpds", "institute_validator"})


def get_role_code(user: User) -> str | None:
    """Код роли пользователя."""
    return user.role.code if user.role else None


def get_accessible_institute_codes(user: User) -> list[str] | None:
    """Коды институтов пользователя; None — без ограничения (admin/cpds/staff)."""
    if user.is_staff:
        return None

    role_code = get_role_code(user)
    if role_code in {"admin", "cpds"}:
        return None

    if role_code == "institute_validator":
        return get_user_institute_codes(user)

    return []


def get_user_institute_codes(user: User) -> list[str]:
    """Коды активных институтов, связанных с подразделением пользователя."""
    if not user.department_id:
        return []

    department_ids = [user.department_id]
    parent_id = getattr(user.department, "parent_id", None)
    if parent_id is None and hasattr(user.department, "parent"):
        parent = user.department.parent
        parent_id = parent.id if parent else None
    if parent_id:
        department_ids.append(parent_id)

    return list(
        Institute.objects.filter(
            department_id__in=department_ids,
            is_active=True,
        ).values_list("code", flat=True)
    )


def get_department_ids_for_institute_codes(institute_codes: list[str]) -> set[int]:
    """ID подразделений в деревьях институтов (корень и все потомки)."""
    result: set[int] = set()
    institutes = Institute.objects.filter(
        code__in=institute_codes,
        is_active=True,
    ).select_related("department__parent")
    for institute in institutes:
        if institute.department_id is None:
            continue
        root = get_root_department(institute.department)
        if root is not None:
            result |= get_department_subtree_ids(root.id)
    return result


def application_belongs_to_institutes(
    application: ProjectApplication,
    institute_codes: list[str],
) -> bool:
    """Проверяет принадлежность заявки к институтам по причастным подразделениям.

    Сравниваются причастные подразделения заявки с деревом корневого подразделения
    института. target_institutes не учитываются.
    """
    if not institute_codes:
        return False

    allowed_department_ids = get_department_ids_for_institute_codes(institute_codes)
    if not allowed_department_ids:
        return False

    involved_department_ids = set(
        application.involved_departments.values_list("department_id", flat=True)
    )
    return bool(involved_department_ids & allowed_department_ids)


def application_available_for_institute(
    application: ProjectApplication,
    institute_codes: list[str],
) -> bool:
    """Проверяет доступность заявки институту для проектных треков.

    Заявка доступна, если совпадают причастные подразделения или target_institutes.
    """
    if not institute_codes:
        return False

    if application_belongs_to_institutes(application, institute_codes):
        return True

    return application.target_institutes.filter(code__in=institute_codes).exists()
