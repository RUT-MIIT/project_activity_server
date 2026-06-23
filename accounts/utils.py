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


def get_department_subtree_ids(root_department_id: int) -> set[int]:
    """Возвращает id корневого подразделения и всех его потомков."""
    result = {root_department_id}
    queue = [root_department_id]
    while queue:
        children = list(
            Department.objects.filter(parent_id__in=queue).values_list("id", flat=True)
        )
        new_ids = set(children) - result
        result.update(new_ids)
        queue = list(new_ids)
    return result
