"""DTO статистики студентов для дашборда ответственного."""

from __future__ import annotations

from typing import Any

from teams.domain.contingent_student import ContingentStudent
from teams.dto.institute_responsible import InstituteResponsibleEmployeeDTO
from teams.dto.institute_responsible_mentors_stats import MentorsStatsStudentDTO
from teams.models import StudyGroup


def _mentors_from_group(group: StudyGroup | None) -> list[dict[str, Any]]:
    """Список наставников группы из prefetch семестра."""
    if group is None:
        return []
    enrollments = getattr(group, "_semester_enrollments_for_semester", None)
    if not enrollments:
        return []
    enrollment = enrollments[0]
    return [
        InstituteResponsibleEmployeeDTO(mentor).to_dict()
        for mentor in enrollment.mentors.all()
    ]


class StudentsStatsStudentDTO:
    """Stats-студент дашборда: MentorsStatsStudentDTO + mentors группы."""

    def __init__(
        self,
        student: ContingentStudent,
        institute_by_code: dict[str, dict[str, str]],
    ) -> None:
        self._base = MentorsStatsStudentDTO.from_contingent(
            student, institute_by_code
        )
        self.mentors = _mentors_from_group(student.group)

    def to_dict(self) -> dict[str, Any]:
        """JSON в формате IStatsStudent."""
        data = self._base.to_dict()
        data["mentors"] = self.mentors
        return data
