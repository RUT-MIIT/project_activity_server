"""Репозиторий предрегистрации студентов."""

from __future__ import annotations

from django.db.models import QuerySet

from accounts.models import PreRegisteredStudent


class PreRegisteredStudentRepository:
    """Доступ к данным предрегистрации студентов."""

    def get_by_student_card(self, student_card: str) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию по номеру студенческого билета."""
        return (
            PreRegisteredStudent.objects.select_related("group")
            .filter(student_card=student_card)
            .first()
        )

    def get_by_personnel_number(
        self, personnel_number: str
    ) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию по табельному номеру."""
        return (
            PreRegisteredStudent.objects.select_related("group")
            .filter(personnel_number=personnel_number)
            .first()
        )

    def get_by_snils(self, snils: str) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию по нормализованному СНИЛС."""
        if not snils:
            return None
        return (
            PreRegisteredStudent.objects.select_related("group")
            .filter(snils=snils)
            .first()
        )

    def get_by_id(self, pk: int) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию по первичному ключу."""
        return (
            PreRegisteredStudent.objects.select_related("group").filter(pk=pk).first()
        )

    def delete_unregistered(self) -> int:
        """Удаляет предрегистрации без привязанного пользователя."""
        deleted, _ = PreRegisteredStudent.objects.filter(student__isnull=True).delete()
        return deleted

    def upsert_from_import(
        self,
        *,
        row,
        group_id: int,
        existing: PreRegisteredStudent | None = None,
    ) -> tuple[PreRegisteredStudent, bool]:
        """Создаёт или обновляет предрегистрацию по табельному номеру."""
        defaults = {
            "last_name": row.last_name,
            "first_name": row.first_name,
            "middle_name": row.middle_name,
            "student_card": row.student_card,
            "snils": row.snils,
            "group_id": group_id,
        }
        if existing is not None:
            for field, value in defaults.items():
                setattr(existing, field, value)
            existing.save()
            return existing, False

        return (
            PreRegisteredStudent.objects.create(
                personnel_number=row.personnel_number,
                **defaults,
            ),
            True,
        )

    def link_student(
        self, pre_registered: PreRegisteredStudent, user_id: int
    ) -> PreRegisteredStudent:
        """Привязывает предрегистрацию к созданному пользователю."""
        pre_registered.student_id = user_id
        pre_registered.save(update_fields=["student"])
        return pre_registered

    def list_unregistered(self) -> QuerySet[PreRegisteredStudent]:
        """Возвращает queryset предрегистраций без пользователя."""
        return PreRegisteredStudent.objects.filter(student__isnull=True)
