"""Утилиты для работы с подразделениями."""

from typing import Optional

from accounts.models import Department


def get_root_department(department: Optional[Department]) -> Optional[Department]:
    """Находит корневое подразделение в иерархии.

    Поднимается по цепочке parent до тех пор, пока не найдет подразделение
    с parent=None (корневое подразделение верхнего уровня).

    Args:
        department: Подразделение для поиска корневого элемента

    Returns:
        Корневое подразделение или None, если department=None
    """
    if department is None:
        return None

    current = department
    while current.parent is not None:
        current = current.parent

    return current
