"""Создание псевдо-аккаунтов для незарегистрированных студентов контингента."""

from __future__ import annotations

import secrets

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import PreRegisteredStudent, Role
from accounts.repositories.preregistered_student import PreRegisteredStudentRepository

User = get_user_model()


class PlaceholderUserService:
    """Создаёт и возвращает псевдо-user для предрегистрации."""

    def __init__(self) -> None:
        self._repository = PreRegisteredStudentRepository()

    @transaction.atomic
    def get_or_create_placeholder(self, pre_registered: PreRegisteredStudent) -> User:
        """
        Возвращает существующего или создаёт псевдо-user для предрегистрации.

        Raises:
            ValueError: если роль student не найдена.
        """
        if pre_registered.student_id is not None:
            return pre_registered.student

        try:
            role = Role.objects.get(code="student")
        except Role.DoesNotExist as exc:
            raise ValueError("Роль student не найдена") from exc

        email = self._placeholder_email(pre_registered.personnel_number)
        user = User.objects.create_user(
            email=email,
            password=secrets.token_urlsafe(32),
            first_name=pre_registered.first_name,
            last_name=pre_registered.last_name,
            middle_name=pre_registered.middle_name,
            role=role,
            study_group=pre_registered.group,
            is_active=False,
            is_placeholder=True,
        )
        pre_registered.has_placeholder_user = True
        self._repository.link_student(pre_registered, user.pk)
        pre_registered.save(update_fields=["has_placeholder_user"])
        return user

    @staticmethod
    def _placeholder_email(personnel_number: str) -> str:
        """Уникальный внутренний email для псевдо-аккаунта."""
        return f"placeholder.{personnel_number}@preregistered.internal"
