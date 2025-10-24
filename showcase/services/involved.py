from django.db import transaction
from django.contrib.auth import get_user_model
from showcase.models import (
    ProjectApplication,
    ProjectApplicationStatusLog,
    ProjectApplicationComment,
    ApplicationInvolvedUser,
    ApplicationInvolvedDepartment,
)


User = get_user_model()


class InvolvedManager:
    """Менеджер для управления причастными пользователями и подразделениями."""

    @staticmethod
    @transaction.atomic
    def add_involved_user(
        application: ProjectApplication,
        user: User,
        actor: User | None = None,
        log_action: bool = True,
    ) -> ApplicationInvolvedUser:
        involved, created = ApplicationInvolvedUser.objects.get_or_create(
            application=application,
            user=user,
            defaults={
                'added_by': actor,
            }
        )
        if created and log_action:
            log = ProjectApplicationStatusLog.objects.create(
                application=application,
                from_status=application.status,
                to_status=application.status,
                actor=actor,
                action_type='involved_user_added',
                involved_user=user,
            )
            ProjectApplicationComment.objects.create(
                status_log=log,
                author=actor,
                field='involved_user',
                text=f'Добавлен причастный пользователь: {getattr(user, "email", user.pk)}'
            )
        return involved

    @staticmethod
    @transaction.atomic
    def remove_involved_user(application: ProjectApplication, user: User, actor: User | None = None) -> int:
        deleted, _ = ApplicationInvolvedUser.objects.filter(
            application=application,
            user=user
        ).delete()
        if deleted:
            log = ProjectApplicationStatusLog.objects.create(
                application=application,
                from_status=application.status,
                to_status=application.status,
                actor=actor,
                action_type='involved_user_removed',
                involved_user=user,
            )
            ProjectApplicationComment.objects.create(
                status_log=log,
                author=actor,
                field='involved_user',
                text=f'Удалён причастный пользователь: {getattr(user, "email", user)}'
            )
        return deleted

    @staticmethod
    @transaction.atomic
    def add_involved_department(application: ProjectApplication, department, actor: User | None = None) -> ApplicationInvolvedDepartment:
        involved, created = ApplicationInvolvedDepartment.objects.get_or_create(
            application=application,
            department=department,
            defaults={
                'added_by': actor,
            }
        )
        if created:
            log = ProjectApplicationStatusLog.objects.create(
                application=application,
                from_status=application.status,
                to_status=application.status,
                actor=actor,
                action_type='involved_department_added',
                involved_department=department,
            )
            ProjectApplicationComment.objects.create(
                status_log=log,
                author=actor,
                field='involved_department',
                text=f'Добавлено причастное подразделение: {getattr(department, "name", department.pk)}'
            )
        return involved

    @staticmethod
    @transaction.atomic
    def remove_involved_department(application: ProjectApplication, department, actor: User | None = None) -> int:
        deleted, _ = ApplicationInvolvedDepartment.objects.filter(
            application=application,
            department=department
        ).delete()
        if deleted:
            log = ProjectApplicationStatusLog.objects.create(
                application=application,
                from_status=application.status,
                to_status=application.status,
                actor=actor,
                action_type='involved_department_removed',
                involved_department=department,
            )
            ProjectApplicationComment.objects.create(
                status_log=log,
                author=actor,
                field='involved_department',
                text=f'Удалено причастное подразделение: {getattr(department, "name", department)}'
            )
        return deleted


