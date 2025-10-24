"""
Фабрика для создания сервисов работы со статусами.

Создает и настраивает все зависимости для работы со статусами.
Реализует принцип DIP - создает объекты через абстракции.
"""

from .manager import StatusManager
from .log_service import StatusLogService
from .transition_service import StatusTransitionRegistry, StatusTransitionService
from .transitions import AuthorInvolvementTransition
from .role_status_service import RoleStatusService
from .auto_transition_service import AutoTransitionService


class StatusServiceFactory:
    """
    Фабрика для создания сервисов работы со статусами.
    
    Создает и настраивает все зависимости, регистрирует переходы.
    """
    
    @staticmethod
    def create_status_manager() -> StatusManager:
        """
        Создает полностью настроенный менеджер статусов.
        
        Returns:
            StatusManager: Настроенный менеджер со всеми зависимостями
        """
        # Создаем сервисы
        log_service = StatusLogService()
        registry = StatusTransitionRegistry()
        transition_service = StatusTransitionService(registry)
        
        # Регистрируем переходы
        StatusServiceFactory._register_transitions(registry)
        
        # Создаем менеджер
        manager = StatusManager(log_service, transition_service)

        # Подключаем сервис автопереходов
        # Передаем ссылку на менеджер, чтобы он мог инициировать второй шаг
        manager.auto_transition_service = AutoTransitionService(manager)
        return manager
    
    @staticmethod
    def _register_transitions(registry: StatusTransitionRegistry) -> None:
        """
        Регистрирует все переходы в реестре.
        
        Args:
            registry: Реестр переходов
        """
        # Создаем экземпляр перехода
        author_involvement = AuthorInvolvementTransition()
        
        # Регистрируем переходы для создания заявки
        registry.register('__none__', 'created', author_involvement)
        registry.register('__none__', 'await_department', author_involvement)
        registry.register('__none__', 'approved', author_involvement)
        registry.register('__none__', 'rejected', author_involvement)
        
        # Регистрируем переходы для обновления статуса
        registry.register('created', 'created', author_involvement)
        registry.register('created', 'await_department', author_involvement)
        registry.register('created', 'approved', author_involvement)
        registry.register('created', 'rejected', author_involvement)
        
        # Можно добавить другие переходы по мере необходимости
        # registry.register('await_department', 'approved', notification_transition)
        # registry.register('await_department', 'rejected', notification_transition)
    
    @staticmethod
    def create_log_service() -> StatusLogService:
        """Создает сервис логирования"""
        return StatusLogService()
    
    @staticmethod
    def create_transition_service() -> StatusTransitionService:
        """Создает сервис переходов с зарегистрированными переходами"""
        registry = StatusTransitionRegistry()
        StatusServiceFactory._register_transitions(registry)
        return StatusTransitionService(registry)
    
    @staticmethod
    def create_transition_registry() -> StatusTransitionRegistry:
        """Создает реестр переходов с зарегистрированными переходами"""
        registry = StatusTransitionRegistry()
        StatusServiceFactory._register_transitions(registry)
        return registry
    
    @staticmethod
    def create_role_status_service() -> RoleStatusService:
        """Создает сервис для перевода статусов по ролям"""
        status_manager = StatusServiceFactory.create_status_manager()
        return RoleStatusService(status_manager)
