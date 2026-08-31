"""Репозиторий для StudyGroupProjectTeacher."""

from __future__ import annotations

from teams.domain.project_teacher_import import ProjectTeacherImportRow
from teams.models import StudyGroupProjectTeacher


class ProjectTeacherRepository:
    """Доступ к данным преподавателей проектной деятельности групп."""

    def upsert_from_import(
        self,
        *,
        semester_id: int,
        study_group_id: int,
        row: ProjectTeacherImportRow,
        tutor_id: int | None,
    ) -> tuple[StudyGroupProjectTeacher, bool]:
        """Создаёт или обновляет запись по ключу semester/group/teacher."""
        defaults = {
            "tutor_id": tutor_id,
            "mentor_full_name": row.mentor_full_name,
            "external_group_id": row.external_group_id,
            "mentor_short_name": row.mentor_short_name,
            "lesson_count": row.lesson_count,
            "import_status": row.import_status,
        }
        return StudyGroupProjectTeacher.objects.update_or_create(
            semester_id=semester_id,
            study_group_id=study_group_id,
            external_teacher_id=row.external_teacher_id,
            defaults=defaults,
        )
