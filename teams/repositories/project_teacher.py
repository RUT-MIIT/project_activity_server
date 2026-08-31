"""Репозиторий для StudyGroupProjectTeacher."""

from __future__ import annotations

from django.db.models import QuerySet

from teams.domain.mentor_registration import mentor_full_name_matches
from teams.domain.project_teacher_import import ProjectTeacherImportRow
from teams.models import StudyGroupProjectTeacher


class ProjectTeacherRepository:
    """Доступ к данным преподавателей проектной деятельности групп."""

    def find_for_mentor(
        self,
        *,
        semester_id: int,
        personnel_number: str,
        full_name: str,
    ) -> QuerySet[StudyGroupProjectTeacher]:
        """
        Ищет записи преподавателя ПД в семестре.

        Сначала по табельному номеру, затем по ФИО.
        """
        base_qs = StudyGroupProjectTeacher.objects.filter(
            semester_id=semester_id,
        ).select_related("study_group")

        if personnel_number:
            by_number = base_qs.filter(external_teacher_id=personnel_number)
            if by_number.exists():
                return by_number

        if not full_name:
            return StudyGroupProjectTeacher.objects.none()

        matched_ids: list[int] = []
        for assignment in base_qs.iterator():
            if mentor_full_name_matches(assignment.mentor_full_name, full_name):
                matched_ids.append(assignment.pk)

        if not matched_ids:
            return StudyGroupProjectTeacher.objects.none()

        return base_qs.filter(pk__in=matched_ids)

    def link_tutor(
        self,
        assignments: QuerySet[StudyGroupProjectTeacher],
        user_id: int,
    ) -> int:
        """Привязывает пользователя PD к найденным записям импорта."""
        return assignments.update(tutor_id=user_id)

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
