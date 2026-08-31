"""Репозиторий предрегистрации студентов."""

from __future__ import annotations

from django.db.models import QuerySet

from accounts.models import PreRegisteredStudent


class PreRegisteredStudentRepository:
    """Доступ к данным предрегистрации студентов."""

    def get_by_student_card(self, student_card: str) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию по номеру студенческого билета."""
        return (
            PreRegisteredStudent.objects.select_related("group", "department", "role")
            .filter(student_card=student_card)
            .exclude(student_card="")
            .first()
        )

    def get_by_personnel_number(
        self, personnel_number: str
    ) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию по табельному номеру."""
        return (
            PreRegisteredStudent.objects.select_related("group", "department", "role")
            .filter(personnel_number=personnel_number)
            .first()
        )

    def get_by_snils(self, snils: str) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию по нормализованному СНИЛС."""
        if not snils:
            return None
        return (
            PreRegisteredStudent.objects.select_related("group", "department", "role")
            .filter(snils=snils)
            .first()
        )

    def get_by_id(self, pk: int) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию по первичному ключу."""
        return (
            PreRegisteredStudent.objects.select_related("group", "department", "role")
            .filter(pk=pk)
            .first()
        )

    def delete_unregistered(self) -> int:
        """Удаляет предрегистрации без привязанного пользователя."""
        deleted, _ = PreRegisteredStudent.objects.filter(user__isnull=True).delete()
        return deleted

    def upsert_from_import(
        self,
        *,
        row,
        group_id: int,
        existing: PreRegisteredStudent | None = None,
    ) -> tuple[PreRegisteredStudent, bool]:
        """Создаёт или обновляет предрегистрацию студента по табельному номеру."""
        defaults = {
            "last_name": row.last_name,
            "first_name": row.first_name,
            "middle_name": row.middle_name,
            "student_card": row.student_card,
            "snils": row.snils,
            "group_id": group_id,
            "role_id": "student",
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

    def upsert_mentor_from_import(
        self,
        *,
        row,
        department_id: int | None,
        existing: PreRegisteredStudent | None = None,
    ) -> tuple[PreRegisteredStudent, bool]:
        """Создаёт или обновляет предрегистрацию наставника по табельному номеру."""
        defaults = {
            "last_name": row.last_name,
            "first_name": row.first_name,
            "middle_name": row.middle_name,
            "department_id": department_id,
            "role_id": "mentor",
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

    def link_user(
        self, pre_registered: PreRegisteredStudent, user_id: int
    ) -> PreRegisteredStudent:
        """Привязывает предрегистрацию к пользователю."""
        pre_registered.user_id = user_id
        pre_registered.save(update_fields=["user"])
        return pre_registered

    def list_unregistered(self) -> QuerySet[PreRegisteredStudent]:
        """Возвращает queryset предрегистраций без пользователя."""
        return PreRegisteredStudent.objects.filter(user__isnull=True)
