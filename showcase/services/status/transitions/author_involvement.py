"""
Переход: добавление автора заявки в причастные пользователи.

Выполняется при создании заявки или переходе в определенные статусы.
"""

from typing import Optional
from django.db import transaction
from django.contrib.auth import get_user_model

from showcase.models import ProjectApplication, ApplicationStatus
from showcase.services.involved import InvolvedManager
from .base import BaseStatusTransitionImpl

User = get_user_model()


class AuthorInvolvementTransition(BaseStatusTransitionImpl):
    """
    Переход для добавления автора заявки в причастные пользователи.
    
    Добавляет автора и его подразделение (включая родительское) 
    в причастные пользователи/подразделения.
    """
    
    def __init__(self):
        super().__init__("AuthorInvolvementTransition")
    
    def can_apply(self, from_status: Optional[str], to_status: str) -> bool:
        """
        Переход применяется при создании заявки или переходе в определенные статусы.
        """
        # Применяется при создании заявки с любым статусом
        if from_status is None:
            return True
        
        # Применяется при переходе в определенные статусы
        target_statuses = ['created', 'await_department', 'approved', 'rejected']
        return to_status in target_statuses
    
    def apply(
        self, 
        application: ProjectApplication, 
        from_status: Optional[ApplicationStatus], 
        to_status: ApplicationStatus, 
        actor: Optional[User]
    ) -> None:
        """
        Добавляет автора заявки в причастные пользователи и его подразделение
        (включая родительское) в причастные подразделения.
        """
        if not application.author:
            self._log_transition(application, "No author to add to involved users")
            return

        with transaction.atomic():
            # Добавляем автора в причастные пользователи
            InvolvedManager.add_involved_user(
                application=application,
                user=application.author,
                actor=actor,
                log_action=True
            )

            # Добавляем подразделение автора в причастные подразделения
            if (hasattr(application.author, 'department') and
                application.author.department):
                
                # Добавляем само подразделение автора
                InvolvedManager.add_involved_department(
                    application=application,
                    department=application.author.department,
                    actor=actor
                )

                # Добавляем родительское подразделение, если оно есть
                if application.author.department.parent:
                    InvolvedManager.add_involved_department(
                        application=application,
                        department=application.author.department.parent,
                        actor=actor
                    )
                
                self._log_transition(
                    application, 
                    f"Added author {application.author.email} and departments to involved"
                )
            else:
                self._log_transition(
                    application, 
                    f"Added author {application.author.email} to involved (no department)"
                )
