"""DTO для учебных групп."""

from typing import Any

from teams.models import StudyGroup


class StudyGroupReadDTO:
    """DTO для чтения учебной группы."""

    def __init__(self, group: StudyGroup):
        self.id = group.id
        self.name = group.name
        self.code = group.code
        self.course_number = group.course_number
        self.is_end = group.is_end
        self.direction = {
            "code": group.direction.code,
            "level": group.direction.level,
            "name": group.direction.name,
        }
        self.institute = {
            "code": group.institute.code,
            "name": group.institute.name,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "course_number": self.course_number,
            "is_end": self.is_end,
            "direction": self.direction,
            "institute": self.institute,
        }
