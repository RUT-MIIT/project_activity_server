"""DTO для API ответственного по институтам."""

from __future__ import annotations

from typing import Any

from accounts.models import User
from teams.models import StudyGroup


class InstituteResponsibleGroupDTO:
    """Компактное представление учебной группы."""

    def __init__(self, group: StudyGroup) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number
        self.direction_code = group.direction.code

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "courseNumber": self.course_number,
            "directionCode": self.direction_code,
        }


class InstituteResponsibleEmployeeDTO:
    """Сотрудник института (id + ФИО)."""

    def __init__(self, user: User) -> None:
        self.id = user.id
        self.full_name = user.get_full_name()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fullName": self.full_name,
        }


class InstituteResponsibleMentorDTO:
    """Назначенный наставник группы (полная карточка)."""

    def __init__(self, mentor: User | None) -> None:
        self.mentor = mentor

    def to_dict(self) -> dict[str, Any] | None:
        if self.mentor is None:
            return None
        return InstituteResponsibleEmployeeDTO(self.mentor).to_dict()


class InstituteResponsibleGroupWithMentorDTO:
    """Учебная группа с ID назначенных наставников в семестре."""

    def __init__(self, group: StudyGroup) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number
        self.direction_code = group.direction.code
        self.mentor_ids = self._mentor_ids_for_group(group)

    @staticmethod
    def _mentor_ids_for_group(group: StudyGroup) -> list[int]:
        enrollments = getattr(group, "_semester_enrollments_for_semester", None)
        if not enrollments:
            return []
        enrollment = enrollments[0]
        return [mentor.id for mentor in enrollment.mentors.all()]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "courseNumber": self.course_number,
            "directionCode": self.direction_code,
            "mentorIds": self.mentor_ids,
        }


class InstituteResponsibleGroupMentorsDTO:
    """Ответ: группы с назначениями наставников."""

    def __init__(self, groups: list[StudyGroup]) -> None:
        self.groups = groups

    def to_list(self) -> list[dict[str, Any]]:
        return [
            InstituteResponsibleGroupWithMentorDTO(group).to_dict()
            for group in self.groups
        ]


class InstituteResponsibleAssignMentorDTO:
    """Ответ после изменения состава наставников."""

    def __init__(self, group_id: int, semester_id: int, mentor_ids: list[int]) -> None:
        self.group_id = group_id
        self.semester_id = semester_id
        self.mentor_ids = mentor_ids

    def to_dict(self) -> dict[str, Any]:
        return {
            "groupId": self.group_id,
            "semesterId": self.semester_id,
            "mentorIds": self.mentor_ids,
        }
