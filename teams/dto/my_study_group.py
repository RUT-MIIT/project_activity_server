"""DTO для эндпоинта «Моя группа»."""

from typing import Any

from accounts.models import PreRegisteredStudent, User
from teams.models import StudyGroup, TeamSemesterMember


class StudyGroupMentorDTO:
    """Карточка наставника учебной группы."""

    def __init__(self, mentor: User):
        self.id = mentor.id
        self.last_name = mentor.last_name
        self.first_name = mentor.first_name
        self.middle_name = mentor.middle_name
        self.email = mentor.email
        self.position = mentor.position
        self.academic_degree = mentor.academic_degree
        self.academic_title = mentor.academic_title

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "email": self.email,
            "position": self.position,
            "academic_degree": self.academic_degree,
            "academic_title": self.academic_title,
        }


class StudyGroupMemberDTO:
    """Строка списка группы из контингента."""

    def __init__(
        self,
        pre_registered: PreRegisteredStudent,
        include_team: bool = False,
    ):
        student = pre_registered.student
        self.id = pre_registered.id
        self.last_name = pre_registered.last_name
        self.first_name = pre_registered.first_name
        self.middle_name = pre_registered.middle_name
        self.is_registered = pre_registered.is_registered
        self.user_id = student.id if student is not None else None
        self.email = student.email if student is not None else None
        self.include_team = include_team
        self.team = self._team_snapshot(student) if include_team else None

    @staticmethod
    def _team_snapshot(student: User | None) -> dict[str, Any] | None:
        if student is None:
            return None
        memberships: list[TeamSemesterMember] = getattr(
            student, "_team_membership_for_semester", []
        )
        if not memberships:
            return None
        membership = memberships[0]
        return {
            "id": membership.team_semester.team_id,
            "name": membership.team_semester.team.name,
            "role": membership.role,
        }

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "is_registered": self.is_registered,
            "user_id": self.user_id,
            "email": self.email,
        }
        if self.include_team:
            payload["team"] = self.team
        return payload


class MyStudyGroupDTO:
    """Полные данные учебной группы для текущего студента."""

    def __init__(
        self,
        group: StudyGroup,
        include_team: bool = False,
        semester_id: int | None = None,
    ):
        members = [
            StudyGroupMemberDTO(item, include_team=include_team)
            for item in group.pre_registered_students.all()
        ]
        self.id = group.id
        self.name = group.name
        self.code = group.code
        self.course_number = group.course_number
        self.is_end = group.is_end
        self.profile = group.profile
        self.form = group.form
        self.enrollment_year = group.enrollment_year
        self.direction = {
            "code": group.direction.code,
            "level": group.direction.level,
            "name": group.direction.name,
        }
        self.institute = {
            "code": group.institute.code,
            "name": group.institute.name,
        }
        mentor_users = self._resolve_mentors(group, semester_id)
        self.mentors = [
            StudyGroupMentorDTO(mentor).to_dict() for mentor in mentor_users
        ]
        self.members = [member.to_dict() for member in members]
        self.students_count = len(members)
        self.registered_students_count = sum(
            1 for member in members if member.is_registered
        )

    @staticmethod
    def _resolve_mentors(group: StudyGroup, semester_id: int | None) -> list[User]:
        """Возвращает наставников: из семестра или fallback на StudyGroup.mentor."""
        if semester_id is not None:
            enrollments = getattr(group, "_semester_enrollments_for_semester", None)
            if enrollments:
                return list(enrollments[0].mentors.all())
            return []
        if group.mentor_id:
            return [group.mentor]
        return []

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "course_number": self.course_number,
            "is_end": self.is_end,
            "profile": self.profile,
            "form": self.form,
            "enrollment_year": self.enrollment_year,
            "direction": self.direction,
            "institute": self.institute,
            "mentors": self.mentors,
            "students_count": self.students_count,
            "registered_students_count": self.registered_students_count,
            "members": self.members,
        }
