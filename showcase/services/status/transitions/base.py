"""
Базовый класс для переходов между статусами.

Предоставляет общую функциональность и упрощает создание новых переходов.
"""

from abc import ABC, abstractmethod
from typing import Optional
from django.contrib.auth import get_user_model

from showcase.models import ProjectApplication, ApplicationStatus
from ..base import BaseStatusTransition

User = get_user_model()


class BaseStatusTransitionImpl(BaseStatusTransition):
    """
    Базовая реализация перехода между статусами.
    
    Предоставляет общие методы и упрощает создание новых переходов.
    """
    
    def __init__(self, name: Optional[str] = None):
        self._name = name or self.__class__.__name__
    
    @abstractmethod
    def can_apply(self, from_status: Optional[str], to_status: str) -> bool:
        """Проверяет, можно ли применить переход"""
        pass
    
    @abstractmethod
    def apply(
        self, 
        application: ProjectApplication, 
        from_status: Optional[ApplicationStatus], 
        to_status: ApplicationStatus, 
        actor: Optional[User]
    ) -> None:
        """Выполняет переход"""
        pass
    
    def get_name(self) -> str:
        """Возвращает имя перехода для логирования"""
        return self._name
    
    def _log_transition(
        self, 
        application: ProjectApplication, 
        message: str, 
        actor: Optional[User] = None
    ) -> None:
        """
        Логирует выполнение перехода.
        
        Args:
            application: Заявка
            message: Сообщение для лога
            actor: Пользователь, выполняющий переход
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Transition {self.get_name()} executed for application {application.id}: {message}")
