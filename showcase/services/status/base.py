"""
Базовые абстракции и протоколы для работы со статусами.

Определяет интерфейсы для всех компонентов системы статусов,
обеспечивая соблюдение принципов SOLID.
"""

from abc import ABC, abstractmethod
from typing import Protocol, Optional, List, Dict, Any
from django.contrib.auth import get_user_model

from showcase.models import ProjectApplication, ApplicationStatus

User = get_user_model()


class StatusTransition(Protocol):
    """
    Протокол для переходов между статусами.
    
    Каждый переход должен реализовывать методы can_apply и apply.
    """
    
    def can_apply(self, from_status: Optional[str], to_status: str) -> bool:
        """
        Проверяет, можно ли применить данный переход.
        
        Args:
            from_status: Код исходного статуса (None для создания)
            to_status: Код целевого статуса
            
        Returns:
            True если переход можно применить
        """
        ...
    
    def apply(
        self, 
        application: ProjectApplication, 
        from_status: Optional[ApplicationStatus], 
        to_status: ApplicationStatus, 
        actor: Optional[User]
    ) -> None:
        """
        Выполняет переход.
        
        Args:
            application: Заявка
            from_status: Исходный статус
            to_status: Целевой статус
            actor: Пользователь, выполняющий переход
        """
        ...


class IStatusLogService(Protocol):
    """
    Протокол для сервиса логирования статусов.
    """
    
    def create_log(
        self,
        application: ProjectApplication,
        new_status: ApplicationStatus,
        actor: Optional[User] = None,
        comments: Optional[List[Dict[str, str]]] = None,
        from_status: Optional[ApplicationStatus] = None
    ) -> Any:
        """Создает лог изменения статуса"""
        ...
    
    def get_application_logs(self, application: ProjectApplication) -> Any:
        """Получает все логи заявки"""
        ...
    
    def get_last_log(self, application: ProjectApplication) -> Any:
        """Возвращает последний лог заявки"""
        ...
    
    def add_comment_to_log(
        self, 
        application: ProjectApplication, 
        field: str, 
        text: str, 
        author: Optional[User] = None
    ) -> Any:
        """Добавляет комментарий к последнему логу"""
        ...


class IStatusManager(Protocol):
    """
    Протокол для главного менеджера статусов.
    """
    
    def change_status(
        self,
        application: ProjectApplication,
        new_status: ApplicationStatus,
        actor: Optional[User] = None,
        comments: Optional[List[Dict[str, str]]] = None
    ) -> tuple[ProjectApplication, Any]:
        """Изменяет статус заявки с логированием и выполнением переходов"""
        ...
    
    def change_status_with_log(
        self,
        application: ProjectApplication,
        new_status: str,
        actor: Optional[User] = None,
        comments: Optional[List[Dict[str, str]]] = None
    ) -> tuple[ProjectApplication, Any]:
        """Изменяет статус по коду с логированием и выполнением переходов"""
        ...


class BaseStatusTransition(ABC):
    """
    Базовый абстрактный класс для переходов статусов.
    
    Предоставляет общую функциональность и упрощает создание новых переходов.
    """
    
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
        return self.__class__.__name__
