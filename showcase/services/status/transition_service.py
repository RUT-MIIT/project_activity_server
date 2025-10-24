"""
Сервис для управления переходами между статусами.

Содержит реестр переходов и сервис для их выполнения.
Реализует принципы OCP и DIP.
"""

from typing import Dict, List, Tuple, Optional
from django.contrib.auth import get_user_model

from showcase.models import ProjectApplication, ApplicationStatus
from .base import StatusTransition

User = get_user_model()


class StatusTransitionRegistry:
    """
    Реестр переходов между статусами.
    
    Позволяет регистрировать переходы для конкретных пар статусов.
    Реализует принцип OCP - новые переходы добавляются без изменения кода.
    """
    
    def __init__(self):
        self._transitions: Dict[Tuple[str, str], List[StatusTransition]] = {}
    
    def register(
        self, 
        from_code: str, 
        to_code: str, 
        transition: StatusTransition
    ) -> None:
        """
        Регистрирует переход для пары статусов.
        
        Args:
            from_code: Код исходного статуса ('__none__' для создания)
            to_code: Код целевого статуса
            transition: Объект перехода
        """
        key = (from_code, to_code)
        if key not in self._transitions:
            self._transitions[key] = []
        self._transitions[key].append(transition)
    
    def get_transitions(
        self, 
        from_code: str, 
        to_code: str
    ) -> List[StatusTransition]:
        """
        Получает все переходы для пары статусов.
        
        Args:
            from_code: Код исходного статуса
            to_code: Код целевого статуса
            
        Returns:
            Список переходов для данной пары статусов
        """
        return self._transitions.get((from_code, to_code), [])
    
    def get_all_transitions(self) -> Dict[Tuple[str, str], List[StatusTransition]]:
        """Возвращает все зарегистрированные переходы"""
        return self._transitions.copy()
    
    def clear(self) -> None:
        """Очищает реестр переходов"""
        self._transitions.clear()


class StatusTransitionService:
    """
    Сервис для выполнения переходов между статусами.
    
    Использует реестр для получения подходящих переходов
    и выполняет их в правильном порядке.
    """
    
    def __init__(self, registry: StatusTransitionRegistry):
        self.registry = registry
    
    def execute_transitions(
        self,
        application: ProjectApplication,
        from_status: Optional[ApplicationStatus],
        to_status: ApplicationStatus,
        actor: Optional[User] = None
    ) -> None:
        """
        Выполняет все переходы для пары статусов.
        
        Args:
            application: Заявка
            from_status: Исходный статус (None для создания)
            to_status: Целевой статус
            actor: Пользователь, выполняющий переход
        """
        from_code = from_status.code if from_status else '__none__'
        to_code = to_status.code
        
        transitions = self.registry.get_transitions(from_code, to_code)
        
        for transition in transitions:
            if transition.can_apply(from_code, to_code):
                try:
                    transition.apply(application, from_status, to_status, actor)
                except Exception as e:
                    # Логируем ошибку, но не прерываем выполнение других переходов
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(
                        f"Error executing transition {transition.__class__.__name__}: {e}",
                        exc_info=True
                    )
    
    def can_execute_transitions(
        self,
        from_status: Optional[ApplicationStatus],
        to_status: ApplicationStatus
    ) -> bool:
        """
        Проверяет, можно ли выполнить переходы для пары статусов.
        
        Args:
            from_status: Исходный статус
            to_status: Целевой статус
            
        Returns:
            True если есть хотя бы один применимый переход
        """
        from_code = from_status.code if from_status else '__none__'
        to_code = to_status.code
        
        transitions = self.registry.get_transitions(from_code, to_code)
        return any(transition.can_apply(from_code, to_code) for transition in transitions)
