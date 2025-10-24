from __future__ import annotations

from typing import Callable, Tuple, Dict, List
from django.contrib.auth import get_user_model
from django.db import transaction

from showcase.models import ProjectApplication, ApplicationStatus
from showcase.services.involved import InvolvedManager
from .status import StatusServiceFactory

User = get_user_model()


class StatusTransitionHandler:
    """
    DEPRECATED: Используйте StatusManager из showcase.services.status
    
    Этот класс оставлен для обратной совместимости.
    Метод handle делегирует вызов новому StatusTransitionService.
    """

    @staticmethod
    def _add_author_as_involved(
        application: ProjectApplication,
        from_status: ApplicationStatus | None,
        to_status: ApplicationStatus,
        actor: User | None
    ):
        """
        Добавляет автора заявки в причастные пользователи и его подразделение
        (включая родительское) в причастные подразделения.
        Выполняется только если автор существует.
        """
        if not application.author:
            return

        with transaction.atomic():
            # Добавляем автора в причастные пользователи
            InvolvedManager.add_involved_user(
                application=application,
                user=application.author,
                actor=actor,
                log_action=False  # Не создаем отдельный лог
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

    # Регистрация переходов и действий:
    # Используем коды статусов (строки), чтобы не зависеть от id
    TRANSITIONS_ACTIONS: Dict[
        Tuple[str, str],
        List[Callable[[ProjectApplication, ApplicationStatus | None,
                      ApplicationStatus, User | None], None]]
    ] = {
        # При создании заявки с любым статусом добавляем автора и его подразделение
        ('__none__', 'created'): [
            _add_author_as_involved.__func__,
        ],
        ('__none__', 'await_department'): [
            _add_author_as_involved.__func__,
        ],
        ('__none__', 'approved'): [
            _add_author_as_involved.__func__,
        ],
        ('__none__', 'rejected'): [
            _add_author_as_involved.__func__,
        ],
        # При переходе от created к created добавляем автора и его подразделение
        ('created', 'created'): [
            _add_author_as_involved.__func__,
        ],
    }

    @classmethod
    def handle(
        cls,
        application: ProjectApplication,
        from_status: ApplicationStatus | None,
        to_status: ApplicationStatus,
        actor: User | None = None
    ) -> None:
        """
        DEPRECATED: Используйте StatusManager.execute_transitions()
        
        Выполняет зарегистрированные действия для пары (from_code, to_code).
        Если from_status == None (создание), можно отдельно обрабатывать
        ('__none__', to_code).
        """
        import warnings
        warnings.warn(
            "StatusTransitionHandler.handle is deprecated. Use StatusManager from showcase.services.status",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Делегируем вызов новому сервису
        status_manager = StatusServiceFactory.create_status_manager()
        status_manager.transition_service.execute_transitions(
            application=application,
            from_status=from_status,
            to_status=to_status,
            actor=actor
        )
