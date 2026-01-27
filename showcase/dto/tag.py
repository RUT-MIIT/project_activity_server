"""DTO для работы с тегами."""

from typing import Any, Optional


class TagCreateDTO:
    """DTO для создания тега."""

    def __init__(
        self,
        name: str,
        category: str,
        department_ids: Optional[list[int]] = None,
        is_base: Optional[bool] = None,
        **kwargs,
    ):
        self.name = name
        self.category = category
        self.department_ids = department_ids or []
        self.is_base = is_base

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TagCreateDTO":
        """Создание из словаря."""
        # Поддержка обратной совместимости: если передан department_id, преобразуем в список
        if "department_id" in data and "department_ids" not in data:
            dept_id = data.pop("department_id")
            if dept_id is not None:
                data["department_ids"] = [dept_id]
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь."""
        result = {
            "name": self.name,
            "category": self.category,
        }
        if self.department_ids:
            result["department_ids"] = self.department_ids
        return result


class TagUpdateDTO:
    """DTO для обновления тега."""

    def __init__(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        department_ids: Optional[list[int]] = None,
        **kwargs,
    ):
        self.name = name
        self.category = category
        self.department_ids = department_ids

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TagUpdateDTO":
        """Создание из словаря."""
        # Поддержка обратной совместимости: если передан department_id, преобразуем в список
        if "department_id" in data and "department_ids" not in data:
            dept_id = data.pop("department_id")
            if dept_id is not None:
                data["department_ids"] = [dept_id]
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь, исключая None значения."""
        result = {}
        if self.name is not None:
            result["name"] = self.name
        if self.category is not None:
            result["category"] = self.category
        if self.department_ids is not None:
            result["department_ids"] = self.department_ids
        return result


class TagReadDTO:
    """DTO для чтения тега."""

    def __init__(self, tag):
        """Инициализация из модели Tag."""
        self.id = tag.id
        self.name = tag.name
        self.category = tag.category
        self.is_base = tag.is_base
        self.departments = [
            {
                "id": dept.id,
                "name": dept.name,
                "short_name": dept.short_name,
            }
            for dept in tag.departments.all()
        ]

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "is_base": self.is_base,
            "departments": self.departments,
        }
