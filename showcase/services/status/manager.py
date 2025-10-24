"""
Главный менеджер статусов заявок.

Координирует работу всех сервисов: логирования, переходов и валидации.
Реализует принцип SRP - отвечает за координацию, а не за конкретную логику.
"""

from typing import List, Dict, Optional, Tuple
from django.contrib.auth import get_user_model

from showcase.models import ProjectApplication, ApplicationStatus
# from .base import IStatusManager, IStatusLogService
# from .log_service import StatusLogService
from .transition_service import StatusTransitionService

User = get_user_model()

class StatusManager:
    """
    Главный менеджер статусов заявок.

    Координирует работу сервисов логирования и переходов.
    Предоставляет единый интерфейс для изменения статусов.
    """

    def __init__(
        self,
        log_service,  # StatusLogService
        transition_service: StatusTransitionService
    ):
        self.log_service = log_service
        self.transition_service = transition_service
        # Будет установлен фабрикой
        self.auto_transition_service = None

    def change_status(
        self,
        application: ProjectApplication,
        new_status: ApplicationStatus,
        actor: Optional[User] = None,
        comments: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[ProjectApplication, any]:
        """
        Изменяет статус заявки с логированием и выполнением переходов.

        Args:
            application: Заявка
            new_status: Новый статус
            actor: Пользователь, выполняющий изменение
            comments: Комментарии к изменению
            
        Returns:
            Tuple[ProjectApplication, ProjectApplicationStatusLog]
        """
        old_status = application.status

        # Создаем лог ПЕРЕД изменением статуса
        status_log = self.log_service.create_log(
            application=application,
            new_status=new_status,
            actor=actor,
            comments=comments,
            from_status=old_status
        )

        # Обновляем статус заявки
        application.status = new_status
        application.save()

        # Выполняем переходы
        self.transition_service.execute_transitions(
            application=application,
            from_status=old_status,
            to_status=new_status,
            actor=actor
        )

        # Пост-хук: автопереходы (только если инициатор не автосистема)
        has_auto = getattr(self, 'auto_transition_service', None) is not None
        is_user_initiated = actor is not None
        if has_auto and is_user_initiated:
            try:
                self.auto_transition_service.maybe_apply(
                    application=application,
                    from_status=old_status,
                    to_status=new_status,
                    depth=0,
                )
            except Exception:
                # Не роняем основной поток при сбое автоперехода
                pass

        return application, status_log
    
    def change_status_with_log(
        self,
        application: ProjectApplication,
        new_status: str,
        actor: Optional[User] = None,
        comments: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[ProjectApplication, any]:
        """
        Изменяет статус по коду с логированием и выполнением переходов.

        Args:
            application: Заявка
            new_status: Код нового статуса
            actor: Пользователь, выполняющий изменение
            comments: Комментарии к изменению
            
        Returns:
            Tuple[ProjectApplication, ProjectApplicationStatusLog]
            
        Raises:
            ApplicationStatus.DoesNotExist: Если статус с указанным кодом не найден
        """
        try:
            status_obj = ApplicationStatus.objects.get(code=new_status)
        except ApplicationStatus.DoesNotExist:
            raise ValueError(f"Status with code '{new_status}' not found")

        return self.change_status(application, status_obj, actor, comments)
    
    def create_application_with_log(
        self,
        application: ProjectApplication,
        actor: Optional[User] = None
    ) -> Tuple[ProjectApplication, any]:
        """
        Создает лог о создании заявки и выполняет переходы.

        Args:
            application: Заявка
            actor: Пользователь, создающий заявку
            
        Returns:
            Tuple[ProjectApplication, ProjectApplicationStatusLog]
        """
        # Создаем лог о создании заявки
        status_log = self.log_service.create_log(
            application=application,
            new_status=application.status,
            actor=actor,
            comments=[{
                'field': 'initial_status',
                'text': f'Заявка создана со статусом "{application.status.name}"'
            }],
            is_creation=True
        )

        # Выполняем переходы (добавление автора в причастные и т.д.)
        self.transition_service.execute_transitions(
            application=application,
            from_status=None,
            to_status=application.status,
            actor=actor
        )
        
        return application, status_log
    
    def get_application_logs(self, application: ProjectApplication) -> List[any]:
        """Получает все логи заявки"""
        return self.log_service.get_application_logs(application)
    
    def get_last_log(self, application: ProjectApplication) -> Optional[any]:
        """Возвращает последний лог заявки"""
        return self.log_service.get_last_log(application)
    
    def add_comment_to_log(
        self, 
        application: ProjectApplication, 
        field: str, 
        text: str, 
        author: Optional[User] = None
    ) -> any:
        """Добавляет комментарий к последнему логу заявки"""
        return self.log_service.add_comment_to_log(application, field, text, author)
