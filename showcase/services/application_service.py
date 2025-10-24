"""
Сервис для оркестрации операций с проектными заявками.

Координирует Domain, Repository и существующие сервисы.
"""

from django.db import transaction
from django.contrib.auth import get_user_model

from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
    ProjectApplicationReadDTO,
    ProjectApplicationListDTO,
)
from showcase.domain.application import ProjectApplicationDomain
from showcase.domain.capabilities import ApplicationCapabilities
from showcase.repositories.application import ProjectApplicationRepository
from showcase.services.status import StatusServiceFactory

User = get_user_model()


class ProjectApplicationService:
    """
    Сервис - оркестрация всех операций.
    
    Координирует Domain, Repository и StatusService.
    Использует существующие сервисы без изменений.
    """
    
    def __init__(self):
        self.repository = ProjectApplicationRepository()
        self.status_service = StatusServiceFactory.create_status_manager()
    
    @transaction.atomic
    def submit_application(self, dto: ProjectApplicationCreateDTO, user: User):
        """
        Бизнес-операция: подача заявки.
        
        Координирует Domain, Repository и StatusService.
        """
        # 1. Валидация (Domain)
        validation = ApplicationCapabilities.submit_application(dto, user.role.code if user.role else 'user')
        if not validation.is_valid:
            raise ValueError(validation.errors)
        
        # 2. Определяем начальный статус (Domain)
        initial_status = ProjectApplicationDomain.calculate_initial_status(
            user.role.code if user.role else 'user'
        )
        
        # 3. Определяем необходимость консультации (Domain)
        needs_consultation = ProjectApplicationDomain.should_require_consultation(dto)
        dto.needs_consultation = needs_consultation
        
        # 4. Создаем заявку (Repository)
        application = self.repository.create(dto, user, initial_status)
        
        # 5. Логируем создание и выполняем переходы (StatusService)
        application, status_log = self.status_service.create_application_with_log(
            application=application,
            actor=user
        )
        
        return application, status_log
    
    @transaction.atomic
    def approve_application(self, application_id: int, approver: User):
        """
        Бизнес-операция: одобрение заявки.
        """
        # 1. Проверка прав (Domain)
        can_approve, error = ApplicationCapabilities.approve_application(
            'approved',  # new_status
            approver.role.code if approver.role else 'user',
            application_id
        )
        if not can_approve:
            raise PermissionError(error)
        
        # 2. Получаем заявку (Repository)
        application = self.repository.get_by_id_simple(application_id)
        
        # 3. Проверяем возможность перехода (Domain)
        can_change, error = ProjectApplicationDomain.can_change_status(
            application.status.code,
            'approved',
            approver.role.code if approver.role else 'user'
        )
        if not can_change:
            raise ValueError(error)
        
        # 4. Меняем статус (StatusService)
        application, status_log = self.status_service.change_status_with_log(
            application=application,
            new_status='approved',
            actor=approver,
            comments=[]
        )
        
        return application, status_log
    
    @transaction.atomic
    def reject_application(self, application_id: int, rejector: User, reason: str = ""):
        """
        Бизнес-операция: отклонение заявки.
        """
        # 1. Проверка прав (Domain)
        can_reject, error = ApplicationCapabilities.reject_application(
            'rejected',  # new_status
            rejector.role.code if rejector.role else 'user',
            application_id
        )
        if not can_reject:
            raise PermissionError(error)
        
        # 2. Получаем заявку (Repository)
        application = self.repository.get_by_id_simple(application_id)
        
        # 3. Проверяем возможность перехода (Domain)
        can_change, error = ProjectApplicationDomain.can_change_status(
            application.status.code,
            'rejected',
            rejector.role.code if rejector.role else 'user'
        )
        if not can_change:
            raise ValueError(error)
        
        # 4. Меняем статус (StatusService)
        comments = [{'field': 'rejection_reason', 'text': reason}] if reason else []
        application, status_log = self.status_service.change_status_with_log(
            application=application,
            new_status='rejected',
            actor=rejector,
            comments=comments
        )
        
        return application, status_log
    
    @transaction.atomic
    def request_changes(self, application_id: int, requester: User, comments: list):
        """
        Бизнес-операция: запрос изменений.
        """
        # 1. Проверка прав (Domain)
        can_request, error = ApplicationCapabilities.request_changes(
            'created',  # предполагаем текущий статус
            requester.role.code if requester.role else 'user',
            application_id
        )
        if not can_request:
            raise PermissionError(error)
        
        # 2. Получаем заявку (Repository)
        application = self.repository.get_by_id_simple(application_id)
        
        # 3. Проверяем возможность перехода (Domain)
        can_change, error = ProjectApplicationDomain.can_change_status(
            application.status.code,
            'created',  # возвращаем в статус "создана" для изменений
            requester.role.code if requester.role else 'user'
        )
        if not can_change:
            raise ValueError(error)
        
        # 4. Меняем статус (StatusService)
        application, status_log = self.status_service.change_status_with_log(
            application=application,
            new_status='created',
            actor=requester,
            comments=comments
        )
        
        return application, status_log
    
    @transaction.atomic
    def update_application(self, application_id: int, dto: ProjectApplicationUpdateDTO, updater: User):
        """
        Бизнес-операция: обновление заявки.
        """
        # 1. Получаем заявку (Repository)
        application = self.repository.get_by_id_simple(application_id)
        
        # 2. Проверка прав и валидация (Domain)
        validation, can_update, error = ApplicationCapabilities.update_application(
            dto,
            application.status.code,
            updater.role.code if updater.role else 'user',
            application.author.id if application.author else 0,
            updater.id
        )
        if not can_update:
            raise PermissionError(error)
        if not validation.is_valid:
            raise ValueError(validation.errors)
        
        # 3. Обновляем заявку (Repository)
        application = self.repository.update(application, dto)
        
        return application
    
    def get_application(self, application_id: int, viewer: User):
        """
        Бизнес-операция: получение заявки.
        """
        # 1. Получаем заявку (Repository)
        application = self.repository.get_by_id(application_id)
        
        # 2. Проверка доступа (Domain)
        can_view, error = ApplicationCapabilities.view_application(
            application.status.code,
            viewer.role.code if viewer.role else 'user',
            application.author.id if application.author else 0,
            viewer.id
        )
        if not can_view:
            raise PermissionError(error)
        
        return application
    
    def get_user_applications(self, user: User):
        """
        Бизнес-операция: получение заявок пользователя.
        """
        # 1. Проверка прав (Domain)
        can_list, error = ApplicationCapabilities.list_applications(
            user.role.code if user.role else 'user'
        )
        if not can_list:
            raise PermissionError(error)
        
        # 2. Получаем заявки (Repository)
        applications = self.repository.filter_by_user(user)
        
        return applications
    
    def get_application_dto(self, application) -> ProjectApplicationReadDTO:
        """
        Преобразование модели в DTO для чтения.
        """
        return ProjectApplicationReadDTO(application)
    
    def get_application_list_dto(self, application) -> ProjectApplicationListDTO:
        """
        Преобразование модели в DTO для списка.
        """
        return ProjectApplicationListDTO(application)
    
    def get_applications_by_status(self, status_code: str, user: User):
        """
        Бизнес-операция: получение заявок по статусу.
        """
        # 1. Проверка прав (Domain)
        if user.role and user.role.code not in ['admin', 'moderator']:
            raise PermissionError("Недостаточно прав для просмотра заявок по статусу")
        
        # 2. Получаем заявки (Repository)
        applications = self.repository.filter_by_status(status_code)
        
        return applications
    
    def get_recent_applications(self, limit: int = 10, user: User = None):
        """
        Бизнес-операция: получение последних заявок.
        """
        # 1. Проверка прав (Domain)
        if user and user.role and user.role.code not in ['admin', 'moderator']:
            raise PermissionError("Недостаточно прав для просмотра последних заявок")
        
        # 2. Получаем заявки (Repository)
        applications = self.repository.get_recent_applications(limit)
        
        return applications
