"""Сервис создания пользователя из admin с отправкой учётных данных на email."""

from __future__ import annotations

from dataclasses import dataclass
import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.template.loader import render_to_string

User = get_user_model()


def generate_numeric_password(length: int = 6) -> str:
    """Генерирует случайный цифровой пароль фиксированной длины."""
    if length <= 0:
        raise ValueError("Длина пароля должна быть положительной")
    upper_bound = 10**length
    return f"{secrets.randbelow(upper_bound):0{length}d}"


@dataclass(frozen=True)
class AdminUserProvisionResult:
    """Результат создания пользователя с отправкой письма."""

    user: User
    password: str
    email_sent: bool
    email_error: str | None = None


class AdminUserProvisionService:
    """Создаёт пользователя и отправляет ему учётные данные на email."""

    def create_user_with_credentials_email(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        role,
        middle_name: str = "",
        department=None,
        study_group=None,
        phone: str | None = None,
        is_staff: bool = False,
        is_active: bool = True,
    ) -> AdminUserProvisionResult:
        """
        Создаёт пользователя с автогенерированным паролем и отправляет письмо.

        Raises:
            ValueError: если пользователь с таким email уже существует.
        """
        normalized_email = User.objects.normalize_email(email)
        if User.objects.filter(email=normalized_email).exists():
            raise ValueError("Пользователь с таким email уже существует.")

        password = generate_numeric_password()
        user = User.objects.create_user(
            email=normalized_email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            role=role,
            department=department,
            study_group=study_group,
            phone=phone,
            is_staff=is_staff,
            is_active=is_active,
        )

        email_sent, email_error = self._send_credentials_email(
            user=user,
            password=password,
        )
        return AdminUserProvisionResult(
            user=user,
            password=password,
            email_sent=email_sent,
            email_error=email_error,
        )

    @staticmethod
    def _send_credentials_email(
        *, user: User, password: str
    ) -> tuple[bool, str | None]:
        """Отправляет письмо с учётными данными. Возвращает (успех, текст ошибки)."""
        subject = render_to_string(
            "registration/admin_user_created_subject.txt"
        ).strip()
        message = render_to_string(
            "registration/admin_user_created_body.txt",
            {
                "last_name": user.last_name,
                "first_name": user.first_name,
                "email": user.email,
                "password": password,
                "front_end": settings.FRONT_END.rstrip("/"),
            },
        )
        try:
            mail.send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as exc:
            return False, str(exc)
        return True, None
