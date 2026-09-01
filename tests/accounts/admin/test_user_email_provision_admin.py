"""Тесты admin-интерфейса создания пользователя с письмом."""

import re
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core import mail
from django.test import Client, override_settings
import pytest

from accounts.models import Role

User = get_user_model()
ADD_URL = "/admin/accounts/userwithemailprovision/add/"


@pytest.fixture
def admin_client(db, roles):
    """Авторизованный клиент Django admin (superuser)."""
    User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass",
        first_name="Admin",
        last_name="Adminov",
        role=roles["admin"],
    )
    client = Client()
    client.login(email="admin@example.com", password="adminpass")
    return client


def _provision_form_data(role: Role, **overrides) -> dict[str, str]:
    data = {
        "email": "new.user@example.com",
        "first_name": "Новый",
        "last_name": "Пользователь",
        "middle_name": "",
        "role": str(role.pk),
        "phone": "",
        "is_active": "on",
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
class TestUserEmailProvisionAdmin:
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_create_user_sends_credentials_email(self, admin_client, roles):
        response = admin_client.post(
            ADD_URL,
            data=_provision_form_data(roles["user"]),
            follow=True,
        )

        assert response.status_code == 200
        user = User.objects.get(email="new.user@example.com")
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["new.user@example.com"]

        password_match = re.search(r"Пароль: (\d{6})", mail.outbox[0].body)
        assert password_match is not None
        password = password_match.group(1)
        assert user.check_password(password)

        messages = [str(message) for message in get_messages(response.wsgi_request)]
        assert any(
            "Письмо с учётными данными отправлено" in message for message in messages
        )

    def test_duplicate_email_shows_form_error(self, admin_client, roles, make_user):
        make_user(email="existing@example.com", role_code="user")

        response = admin_client.post(
            ADD_URL,
            data=_provision_form_data(roles["user"], email="existing@example.com"),
        )

        assert response.status_code == 200
        assert User.objects.filter(email="existing@example.com").count() == 1
        assert "Пользователь с таким email уже существует" in response.content.decode()
        assert len(mail.outbox) == 0

    def test_smtp_failure_keeps_user_and_shows_warning(self, admin_client, roles):
        with patch(
            "accounts.services.admin_user_provision_service.mail.send_mail",
            side_effect=ConnectionError("SMTP down"),
        ):
            response = admin_client.post(
                ADD_URL,
                data=_provision_form_data(roles["user"], email="smtp.fail@example.com"),
                follow=True,
            )

        assert response.status_code == 200
        assert User.objects.filter(email="smtp.fail@example.com").exists()
        assert len(mail.outbox) == 0

        messages = [str(message) for message in get_messages(response.wsgi_request)]
        assert any(
            "не удалось отправить письмо" in message.lower() for message in messages
        )

    def test_changelist_redirects_to_add(self, admin_client):
        response = admin_client.get("/admin/accounts/userwithemailprovision/")

        assert response.status_code == 302
        assert response.url == ADD_URL
