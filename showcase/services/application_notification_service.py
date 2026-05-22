"""Уведомления автору проектной заявки по email."""

from __future__ import annotations

import logging

from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string

from showcase.models import ApplicationStatus, ProjectApplication

logger = logging.getLogger(__name__)


class ApplicationNotificationService:
    """Отправка писем автору при отклонении и отправке на доработку."""

    REVISION_SUBJECT = "project_application/revision_requested_subject.txt"
    REVISION_BODY = "project_application/revision_requested_body.txt"
    REJECTED_SUBJECT = "project_application/rejected_subject.txt"
    REJECTED_BODY = "project_application/rejected_body.txt"

    @staticmethod
    def resolve_author_recipient(application: ProjectApplication) -> str | None:
        """Email получателя: author_email заявки или email связанного пользователя-автора."""
        email = (application.author_email or "").strip()
        if email and "@" in email:
            return email
        author = application.author
        if author and author.email:
            author_email = author.email.strip()
            if author_email and "@" in author_email:
                return author_email
        return None

    def notify_author_revision_requested(
        self,
        application: ProjectApplication,
        actor,
        new_status: ApplicationStatus,
    ) -> None:
        """Письмо автору: заявка отправлена на доработку."""
        self._notify(
            application=application,
            actor=actor,
            status=new_status,
            subject_template=self.REVISION_SUBJECT,
            body_template=self.REVISION_BODY,
            reason="",
        )

    def notify_author_rejected(
        self,
        application: ProjectApplication,
        actor,
        reason: str = "",
    ) -> None:
        """Письмо автору: заявка отклонена."""
        self._notify(
            application=application,
            actor=actor,
            status=application.status,
            subject_template=self.REJECTED_SUBJECT,
            body_template=self.REJECTED_BODY,
            reason=reason or "",
        )

    def _notify(
        self,
        application: ProjectApplication,
        actor,
        status: ApplicationStatus,
        subject_template: str,
        body_template: str,
        reason: str,
    ) -> None:
        recipient = self.resolve_author_recipient(application)
        if not recipient:
            logger.warning(
                "Пропуск email по заявке id=%s: не задан author_email и нет email у автора",
                application.pk,
            )
            return
        context = self._build_context(application, actor, status, reason)
        self._send(recipient, subject_template, body_template, context)

    @staticmethod
    def _build_context(
        application: ProjectApplication,
        actor,
        status: ApplicationStatus,
        reason: str,
    ) -> dict:
        middlename = application.author_middlename or ""
        full_name = " ".join(
            part
            for part in (
                application.author_lastname,
                application.author_firstname,
                middlename,
            )
            if part
        ).strip()
        actor_name = ""
        actor_role = ""
        if actor is not None:
            actor_parts = [
                actor.last_name,
                actor.first_name,
                getattr(actor, "middle_name", "") or "",
            ]
            actor_name = " ".join(p for p in actor_parts if p).strip()
            if getattr(actor, "role", None):
                actor_role = getattr(actor.role, "name", None) or getattr(
                    actor.role, "code", ""
                )
        application_number = application.print_number or str(application.pk)
        title = application.title or application.company or ""
        path_template = getattr(
            settings,
            "FRONT_END_APPLICATION_PATH",
            "/my-applications/app/{id}",
        )
        application_url = (
            f"{settings.FRONT_END.rstrip('/')}{path_template.format(id=application.pk)}"
        )
        return {
            "full_name": full_name,
            "application_number": application_number,
            "title": title,
            "status_name": status.name if status else "",
            "actor_name": actor_name,
            "actor_role": actor_role,
            "reason": reason,
            "application_url": application_url,
        }

    @staticmethod
    def _send(
        recipient: str,
        subject_template: str,
        body_template: str,
        context: dict,
    ) -> None:
        subject = render_to_string(subject_template, context).strip()
        message = render_to_string(body_template, context)
        try:
            mail.send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception as exc:
            logger.warning(
                "Не удалось отправить письмо на %s: %s",
                recipient,
                exc,
                exc_info=True,
            )
