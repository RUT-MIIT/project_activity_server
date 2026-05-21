"""Общая логика доступа к институтам по подразделению пользователя."""

from accounts.models import User
from showcase.models import Institute


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
