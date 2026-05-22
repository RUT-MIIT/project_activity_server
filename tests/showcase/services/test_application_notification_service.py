from unittest.mock import patch

import pytest

from showcase.models import ApplicationStatus, ProjectApplication
from showcase.services.application_notification_service import (
    ApplicationNotificationService,
)


@pytest.mark.django_db
class TestApplicationNotificationService:
    def _make_application(self, author_email="", author=None):
        status = ApplicationStatus.objects.get(code="await_department")
        return ProjectApplication.objects.create(
            title="Проект",
            company="Acme",
            status=status,
            author=author,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email=author_email,
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )

    def test_resolve_author_recipient_from_author_email(self, statuses):
        app = self._make_application(author_email="author@example.com")
        assert (
            ApplicationNotificationService.resolve_author_recipient(app)
            == "author@example.com"
        )

    def test_resolve_author_recipient_fallback_to_author_user(
        self, statuses, make_user
    ):
        user = make_user(role_code="user", with_department=False)
        user.email = "user@example.com"
        user.save(update_fields=["email"])
        app = self._make_application(author_email="", author=user)
        assert ApplicationNotificationService.resolve_author_recipient(app) == (
            "user@example.com"
        )

    def test_resolve_author_recipient_empty(self, statuses):
        app = self._make_application(author_email="")
        assert ApplicationNotificationService.resolve_author_recipient(app) is None

    @patch(
        "showcase.services.application_notification_service.mail.send_mail",
    )
    def test_notify_author_revision_requested_sends_mail(
        self, mock_send_mail, statuses, make_user
    ):
        actor = make_user(role_code="department_validator", with_department=True)
        app = self._make_application(author_email="notify@example.com")
        new_status = ApplicationStatus.objects.get(code="returned_department")
        service = ApplicationNotificationService()

        service.notify_author_revision_requested(app, actor, new_status)

        mock_send_mail.assert_called_once()
        assert mock_send_mail.call_args.kwargs["recipient_list"] == [
            "notify@example.com"
        ]

    @patch(
        "showcase.services.application_notification_service.mail.send_mail",
    )
    def test_notify_author_rejected_includes_reason(
        self, mock_send_mail, statuses, make_user
    ):
        actor = make_user(role_code="institute_validator", with_department=True)
        app = self._make_application(author_email="reject@example.com")
        app.status = ApplicationStatus.objects.get(code="rejected")
        app.save(update_fields=["status"])
        service = ApplicationNotificationService()

        service.notify_author_rejected(app, actor, reason="Неполные данные")

        mock_send_mail.assert_called_once()
        message = mock_send_mail.call_args.kwargs["message"]
        assert "Неполные данные" in message

    @patch(
        "showcase.services.application_notification_service.mail.send_mail",
    )
    def test_send_logs_warning_on_failure(self, mock_send_mail, statuses):
        mock_send_mail.side_effect = ConnectionError("SMTP down")
        app = self._make_application(author_email="fail@example.com")
        service = ApplicationNotificationService()

        service.notify_author_rejected(app, None, reason="")

        mock_send_mail.assert_called_once()
