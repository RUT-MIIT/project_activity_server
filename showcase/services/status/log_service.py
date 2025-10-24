"""
Сервис для работы с логами изменения статусов.

Отвечает только за создание, получение и управление логами статусов.
Не содержит бизнес-логику изменения статусов.
"""

from typing import List, Dict, Optional
from django.db import transaction
from django.contrib.auth import get_user_model

from showcase.models import (
    ProjectApplication,
    ApplicationStatus,
    ProjectApplicationStatusLog,
    ProjectApplicationComment,
)
# from .base import IStatusLogService

User = get_user_model()


class StatusLogService:
    """
    Сервис для работы с логами изменения статусов.
    
    Реализует принцип SRP - отвечает только за логирование.
    """
    
    def create_log(
        self,
        application: ProjectApplication,
        new_status: ApplicationStatus,
        actor: Optional[User] = None,
        comments: Optional[List[Dict[str, str]]] = None,
        from_status: Optional[ApplicationStatus] = None,
        is_creation: bool = False
    ) -> ProjectApplicationStatusLog:
        """
        Создает лог изменения статуса заявки.

        Args:
            application: Объект ProjectApplication
            new_status: Новый статус (ApplicationStatus)
            actor: Пользователь, который изменил статус
            comments: Список комментариев [{'field': str, 'text': str}, ...]
            from_status: Предыдущий статус (если None, берется из application.status)
            is_creation: True если это создание заявки (from_status будет None)

        Returns:
            ProjectApplicationStatusLog: Созданный лог
        """
        with transaction.atomic():
            # Получаем предыдущий статус
            if is_creation:
                old_status = None  # При создании заявки предыдущий статус = None
            elif from_status is not None:
                old_status = from_status  # Явно передан предыдущий статус
            else:
                old_status = application.status  # Берем текущий статус заявки

            # Получаем предыдущий лог
            previous_log = application.status_logs.first()

            # Создаем лог
            status_log = ProjectApplicationStatusLog.objects.create(
                application=application,
                from_status=old_status,
                to_status=new_status,
                actor=actor,
                previous_status_log=previous_log,
            )

            # Добавляем комментарии если есть
            if comments:
                for comment_data in comments:
                    ProjectApplicationComment.objects.create(
                        status_log=status_log,
                        author=actor,
                        **comment_data,
                    )

            return status_log

    def get_application_logs(self, application: ProjectApplication) -> List[ProjectApplicationStatusLog]:
        """Получает все логи заявки"""
        return list(application.status_logs.all())

    def get_last_log(self, application: ProjectApplication) -> Optional[ProjectApplicationStatusLog]:
        """Возвращает последний по времени лог заявки"""
        return application.status_logs.order_by('-changed_at').first()

    def add_comment_to_log(
        self, 
        application: ProjectApplication, 
        field: str, 
        text: str, 
        author: Optional[User] = None
    ) -> ProjectApplicationComment:
        """Добавляет комментарий к последнему логу заявки"""
        last_log = self.get_last_log(application)
        if not last_log:
            raise ValueError("No status logs found for this application")
        
        return ProjectApplicationComment.objects.create(
            status_log=last_log,
            field=field,
            text=text,
            author=author,
        )
