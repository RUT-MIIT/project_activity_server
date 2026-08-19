"""Сервис предрегистрации и регистрации студентов из контингента."""

from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import mail
from django.db import transaction
from django.db.models import Prefetch
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.domain.preregistered_student_import import normalize_snils
from accounts.models import PreRegisteredStudent, Role
from accounts.repositories.preregistered_student import PreRegisteredStudentRepository
from accounts.serializers import UserSerializer
from showcase.models import Institute


@dataclass(frozen=True)
class PreRegisteredStudentLookupResult:
    """Результат поиска предрегистрации."""

    id: int
    last_name: str
    first_name: str
    middle_name: str
    group_name: str
    student_card: str
    is_registered: bool

    def to_dict(self) -> dict[str, object]:
        """Сериализует результат для API."""
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "group_name": self.group_name,
            "student_card": self.student_card,
            "is_registered": self.is_registered,
        }


class PreRegisteredStudentService:
    """Оркестрация поиска, регистрации и уведомлений по предрегистрации."""

    def __init__(self) -> None:
        self._repository = PreRegisteredStudentRepository()

    def lookup(
        self,
        *,
        student_card: str | None = None,
        personnel_number: str | None = None,
        snils: str | None = None,
    ) -> PreRegisteredStudentLookupResult | None:
        """
        Ищет предрегистрацию по одному из идентификаторов.

        Returns:
            DTO результата или None, если запись не найдена.
        """
        pre_registered = self._find_by_identifiers(
            student_card=student_card,
            personnel_number=personnel_number,
            snils=snils,
        )
        if pre_registered is None:
            return None
        return self._to_lookup_result(pre_registered)

    @transaction.atomic
    def register(
        self,
        *,
        pre_registered_id: int,
        email: str,
        password: str,
    ) -> dict[str, object]:
        """
        Создаёт пользователя по предрегистрации и возвращает JWT + профиль.

        Raises:
            ValueError: при бизнес-ошибках регистрации.
            ValidationError: при невалидном пароле.
        """
        pre_registered = self._repository.get_by_id(pre_registered_id)
        if pre_registered is None:
            raise ValueError("Предрегистрация не найдена")
        if pre_registered.is_registered:
            raise ValueError("Студент уже зарегистрирован")

        user_model = get_user_model()
        if user_model.objects.filter(email=email).exists():
            raise ValueError("Пользователь с таким email уже существует")

        try:
            role = Role.objects.get(code="student")
        except Role.DoesNotExist as exc:
            raise ValueError("Роль student не найдена") from exc

        validate_password(password)

        user = user_model.objects.create_user(
            email=email,
            password=password,
            first_name=pre_registered.first_name,
            last_name=pre_registered.last_name,
            middle_name=pre_registered.middle_name,
            role=role,
            study_group=pre_registered.group,
        )
        self._send_registration_email(
            pre_registered=pre_registered,
            email=email,
            password=password,
        )
        self._repository.link_student(pre_registered, user.pk)

        refresh = RefreshToken.for_user(user)
        user_data = self._serialize_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data,
        }

    def report_mismatch(
        self,
        *,
        pre_registered_id: int,
        comment: str,
    ) -> None:
        """
        Отправляет администратору письмо о расхождении данных.

        Raises:
            ValueError: если предрегистрация не найдена или не настроен ADMIN_EMAIL.
        """
        admin_email = (getattr(settings, "ADMIN_EMAIL", "") or "").strip()
        if not admin_email:
            raise ValueError("ADMIN_EMAIL не настроен")

        pre_registered = self._repository.get_by_id(pre_registered_id)
        if pre_registered is None:
            raise ValueError("Предрегистрация не найдена")

        subject = render_to_string("registration/student_mismatch_subject.txt").strip()
        message = render_to_string(
            "registration/student_mismatch_body.txt",
            {
                "last_name": pre_registered.last_name,
                "first_name": pre_registered.first_name,
                "middle_name": pre_registered.middle_name,
                "group_name": pre_registered.group.name,
                "student_card": pre_registered.student_card,
                "personnel_number": pre_registered.personnel_number,
                "snils": pre_registered.snils,
                "comment": comment,
            },
        )
        mail.send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[admin_email],
            fail_silently=False,
        )

    @staticmethod
    def _send_registration_email(
        *,
        pre_registered: PreRegisteredStudent,
        email: str,
        password: str,
    ) -> None:
        """Отправляет студенту письмо после успешной регистрации."""
        subject = render_to_string("registration/student_registered_subject.txt").strip()
        message = render_to_string(
            "registration/student_registered_body.txt",
            {
                "last_name": pre_registered.last_name,
                "first_name": pre_registered.first_name,
                "email": email,
                "password": password,
                "front_end": settings.FRONT_END.rstrip("/"),
            },
        )
        try:
            mail.send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as exc:
            raise RuntimeError(
                "Не удалось отправить письмо студенту. Регистрация отменена."
            ) from exc

    def _find_by_identifiers(
        self,
        *,
        student_card: str | None,
        personnel_number: str | None,
        snils: str | None,
    ) -> PreRegisteredStudent | None:
        if student_card:
            return self._repository.get_by_student_card(student_card.strip())
        if personnel_number:
            return self._repository.get_by_personnel_number(personnel_number.strip())
        if snils:
            return self._repository.get_by_snils(normalize_snils(snils))
        return None

    @staticmethod
    def _to_lookup_result(
        pre_registered: PreRegisteredStudent,
    ) -> PreRegisteredStudentLookupResult:
        return PreRegisteredStudentLookupResult(
            id=pre_registered.pk,
            last_name=pre_registered.last_name,
            first_name=pre_registered.first_name,
            middle_name=pre_registered.middle_name,
            group_name=pre_registered.group.name,
            student_card=pre_registered.student_card,
            is_registered=pre_registered.is_registered,
        )

    @staticmethod
    def _serialize_user(user) -> dict[str, object]:
        user_with_relations = (
            get_user_model()
            .objects.select_related("department", "role", "study_group")
            .prefetch_related(
                Prefetch(
                    "department__institutes",
                    queryset=Institute.objects.filter(is_active=True),
                )
            )
            .get(pk=user.pk)
        )
        return UserSerializer(user_with_relations).data
