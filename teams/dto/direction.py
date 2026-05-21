"""DTO для направлений подготовки."""

from typing import Any

from teams.models import Direction


class DirectionReadDTO:
    """DTO для чтения направления."""

    def __init__(self, direction: Direction):
        self.code = direction.code
        self.level = direction.level
        self.name = direction.name

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "level": self.level,
            "name": self.name,
        }
