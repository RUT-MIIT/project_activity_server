"""
Новая архитектура работы со статусами заявок.

Основные компоненты:
- StatusManager - главный менеджер статусов
- StatusLogService - сервис логирования
- StatusTransitionService - сервис переходов
- StatusTransitionRegistry - реестр переходов
- StatusServiceFactory - фабрика для создания сервисов

Использование:
    from showcase.services.status import StatusServiceFactory
    
    status_manager = StatusServiceFactory.create_status_manager()
    status_manager.change_status(application, new_status, actor, comments)
"""

from .factory import StatusServiceFactory
from .manager import StatusManager
from .log_service import StatusLogService
from .transition_service import StatusTransitionService, StatusTransitionRegistry
from .role_status_service import RoleStatusService

__all__ = [
    'StatusServiceFactory',
    'StatusManager', 
    'StatusLogService',
    'StatusTransitionService',
    'StatusTransitionRegistry',
    'RoleStatusService',
]
