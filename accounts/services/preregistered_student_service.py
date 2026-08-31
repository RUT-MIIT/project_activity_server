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

from accounts.domain.preregistered_student_import import (
    last_names_match,
    normalize_snils,
)
from accounts.models import PreRegisteredStudent
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
    role: str
    group_name: str
    department_name: str
    student_card: str
    is_registered: bool

    def to_dict(self) -> dict[str, object]:
        """Сериализует результат для API."""
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "role": self.role,
            "group_name": self.group_name,
            "department_name": self.department_name or None,
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
        last_name: str,
        student_card: str | None = None,
        personnel_number: str | None = None,
        snils: str | None = None,
    ) -> PreRegisteredStudentLookupResult | None:
        """
        Ищет предрегистрацию по одному из идентификаторов.

        Returns:
            DTO результата или None, если запись не найдена.

        Raises:
            ValueError: если запись найдена, но фамилия не совпадает.
        """
        pre_registered = self._find_by_identifiers(
            student_card=student_card,
            personnel_number=personnel_number,
            snils=snils,
        )
        if pre_registered is None:
            return None
        if not last_names_match(pre_registered.last_name, last_name):
            raise ValueError("Фамилия не совпадает с данными в системе")
        if pre_registered.role_id == "student":
            if pre_registered.group is None or pre_registered.group.is_end:
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
            raise ValueError("Пользователь уже зарегистрирован")
        if pre_registered.role_id == "student":
            if pre_registered.group is None or pre_registered.group.is_end:
                raise ValueError("Учебная группа завершила обучение")

        user_model = get_user_model()
        if user_model.objects.filter(email=email).exists():
            raise ValueError("Пользователь с таким email уже существует")

        validate_password(password)

        if (
            pre_registered.has_placeholder_user
            and pre_registered.user is not None
            and pre_registered.user.is_placeholder
        ):
            user = pre_registered.user
            user.email = email
            user.set_password(password)
            user.is_active = True
            user.is_placeholder = False
            if pre_registered.role_id:
                user.role = pre_registered.role
            if pre_registered.department_id is not None:
                user.department = pre_registered.department
            user.save(
                update_fields=[
                    "email",
                    "password",
                    "is_active",
                    "is_placeholder",
                    "role",
                    "department",
                ]
            )
            pre_registered.has_placeholder_user = False
            pre_registered.save(update_fields=["has_placeholder_user"])
        else:
            role = pre_registered.role
            if role is None:
                raise ValueError("Роль не указана в предрегистрации")

            create_kwargs: dict[str, object] = {
                "first_name": pre_registered.first_name,
                "last_name": pre_registered.last_name,
                "middle_name": pre_registered.middle_name,
                "role": role,
            }
            if pre_registered.role_id == "student":
                create_kwargs["study_group"] = pre_registered.group
            if pre_registered.department_id is not None:
                create_kwargs["department"] = pre_registered.department

            user = user_model.objects.create_user(
                email=email,
                password=password,
                **create_kwargs,
            )
            self._repository.link_user(pre_registered, user.pk)

        self._send_registration_email(
            pre_registered=pre_registered,
            email=email,
            password=password,
        )

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
        subject = render_to_string(
            "registration/student_registered_subject.txt"
        ).strip()
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
        group_name = ""
        if pre_registered.group_id is not None:
            group_name = pre_registered.group.name
        department_name = ""
        if pre_registered.department_id is not None:
            department_name = pre_registered.department.name
        return PreRegisteredStudentLookupResult(
            id=pre_registered.pk,
            last_name=pre_registered.last_name,
            first_name=pre_registered.first_name,
            middle_name=pre_registered.middle_name,
            role=pre_registered.role_id,
            group_name=group_name,
            department_name=department_name,
            student_card=pre_registered.student_card,
            is_registered=pre_registered.is_registered,
        )

    @staticmethod
    def _serialize_user(user) -> dict[str, object]:
        user_with_relations = (
            get_user_model()
            .objects.select_related(
                "department",
                "role",
                "study_group",
                "study_group__direction",
                "study_group__institute",
            )
            .prefetch_related(
                Prefetch(
                    "department__institutes",
                    queryset=Institute.objects.filter(is_active=True),
                ),
                "pre_registration",
            )
            .get(pk=user.pk)
        )
        return UserSerializer(user_with_relations).data
