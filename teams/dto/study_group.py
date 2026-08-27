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
        self.profile = group.profile
        self.form = group.form
        self.students_count = getattr(group, "students_count", None)
        if self.students_count is None:
            self.students_count = group.pre_registered_students.count()
        self.direction = {
            "code": group.direction.code,
            "level": group.direction.level,
            "name": group.direction.name,
        }
        self.institute = {
            "code": group.institute.code,
            "name": group.institute.name,
        }
        mentor = group.mentor if group.mentor_id else None
        self.mentor = (
            {
                "id": mentor.id,
                "last_name": mentor.last_name,
                "first_name": mentor.first_name,
                "middle_name": mentor.middle_name,
            }
            if mentor is not None
            else None
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "course_number": self.course_number,
            "is_end": self.is_end,
            "profile": self.profile,
            "form": self.form,
            "students_count": self.students_count,
            "direction": self.direction,
            "institute": self.institute,
            "mentor": self.mentor,
        }
