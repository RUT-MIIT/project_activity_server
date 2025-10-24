"""
Сервис для оркестрации операций с проектными заявками.

Координирует Domain, Repository и существующие сервисы.
"""

from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
    ProjectApplicationReadDTO,
    ProjectApplicationListDTO,
)
from showcase.dto.available_actions import AvailableActionsDTO
from showcase.domain.application import ProjectApplicationDomain
from showcase.domain.capabilities import ApplicationCapabilities
from showcase.repositories.application import ProjectApplicationRepository
from showcase.models import ApplicationStatus

User = get_user_model()


class ProjectApplicationService:
    """
    Сервис - оркестрация всех операций.
    
    Координирует Domain, Repository и StatusService.
    Использует существующие сервисы без изменений.
    """
    
    def __init__(self):
        self.repository = ProjectApplicationRepository()
    
    @transaction.atomic
    def submit_application(self, dto: ProjectApplicationCreateDTO, user: User):
        """
        Бизнес-операция: подача заявки.
        
        Координирует Domain, Repository и StatusService.
        """
        # 1. Валидация (Domain)
        user_role = user.role.code if user and user.role else 'user'
        validation = ApplicationCapabilities.submit_application(dto, user_role)
        if not validation.is_valid:
            raise ValueError(validation.errors)
        
        # 2. Определяем начальный статус (Domain)
        initial_status = ProjectApplicationDomain.calculate_initial_status(user_role)
        
        # 3. Определяем необходимость консультации (Domain)
        needs_consultation = ProjectApplicationDomain.should_require_consultation(dto)
        dto.needs_consultation = needs_consultation
        
        # 4. Создаем заявку (Repository)
        application = self.repository.create(dto, user, initial_status)
        
        return application
    
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
        
        # 4. Меняем статус
        application.status = ApplicationStatus.objects.get(code='approved')
        application.save()
        
        return application
    
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
        
        # 4. Меняем статус
        application.status = ApplicationStatus.objects.get(code='rejected')
        application.save()
        
        return application
    
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
        
        # 4. Меняем статус
        application.status = ApplicationStatus.objects.get(code='created')
        application.save()
        
        return application
    
    @transaction.atomic
    def update_application(
        self, 
        application_id: int, 
        dto: ProjectApplicationUpdateDTO, 
        updater: User
    ):
        """
        Бизнес-операция: обновление заявки.
        """
        # 1. Получаем заявку (Repository)
        try:
            application = self.repository.get_by_id_simple(application_id)
        except ObjectDoesNotExist:
            raise ValueError(f"Заявка с ID {application_id} не найдена")
        
        # 2. Проверка прав и валидация (Domain)
        user_role = updater.role.code if updater.role else 'user'
        author_id = application.author.id if application.author else 0
        validation, can_update, error = ApplicationCapabilities.update_application(
            dto,
            application.status.code,
            user_role,
            author_id,
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
    
    def get_user_applications_queryset(self, user: User):
        """
        Бизнес-операция: получение QuerySet заявок пользователя для пагинации.
        """
        # 1. Проверка прав (Domain)
        can_list, error = ApplicationCapabilities.list_applications(
            user.role.code if user.role else 'user'
        )
        if not can_list:
            raise PermissionError(error)
        
        # 2. Получаем QuerySet (Repository)
        return self.repository.filter_by_user_queryset(user)
    
    def get_user_in_work_applications(self, user: User):
        """
        Бизнес-операция: получение заявок в работе пользователя.
        Заявки, где пользователь причастен и статус не approved/rejected.
        """
        # 1. Проверка прав (Domain)
        can_list, error = ApplicationCapabilities.list_applications(
            user.role.code if user.role else 'user'
        )
        if not can_list:
            raise PermissionError(error)
        
        # 2. Получаем заявки в работе (Repository)
        applications = self.repository.filter_in_work_by_user(user)
        
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
    
    def get_all_applications_queryset(self, user: User):
        """
        Бизнес-операция: получение QuerySet всех заявок для пагинации.
        """
        # 1. Проверка прав (Domain)
        if not user.role or user.role.code not in ['admin', 'moderator']:
            raise PermissionError("Недостаточно прав для просмотра всех заявок")
        
        # 2. Получаем QuerySet (Repository)
        return self.repository.get_all_applications_queryset()
    
    def get_available_actions(self, application_id: int, user: User) -> AvailableActionsDTO:
        """
        Бизнес-операция: получение доступных действий для заявки.
        
        Args:
            application_id: ID заявки
            user: Пользователь, запрашивающий действия
            
        Returns:
            AvailableActionsDTO: DTO с доступными действиями
        """
        # 1. Получаем заявку (Repository)
        try:
            application = self.repository.get_by_id_simple(application_id)
        except ObjectDoesNotExist:
            raise ValueError(f"Заявка с ID {application_id} не найдена")
        
        # 2. Получаем роль пользователя
        user_role = user.role.code if user.role else 'user'
        current_status = application.status.code
        
        # 3. Определяем доступные действия
        available_actions = []
        
        # Проверяем права на approve/reject
        if self._has_approve_reject_permissions(
            application, user, current_status, user_role
        ):
            # Добавляем approve
            available_actions.append({
                'action': 'approve',
                'label': 'Одобрить',
                'config': {'status_code': 'approved'}
            })
            
            # Добавляем reject
            available_actions.append({
                'action': 'reject',
                'label': 'Отклонить',
                'config': {'status_code': 'rejected'}
            })
        
        return AvailableActionsDTO.from_actions_list(available_actions)
    
    def _has_approve_reject_permissions(
        self,
        application,
        user,
        current_status: str,
        user_role: str
    ) -> bool:
        """
        Проверяет, имеет ли пользователь права на действия approve/reject
        согласно бизнес-правилам.
        """
        # Правило 1: Если статус заявки await_department
        if current_status == 'await_department':
            # 1.1 Если роль department_validator, institute_validator
            if user_role in ['department_validator', 'institute_validator']:
                # Проверяем, есть ли подразделение пользователя в причастных
                return self._is_user_department_involved(application, user)
            
            # 1.2 Роли cpds, admin - всегда доступны
            elif user_role in ['cpds', 'admin']:
                return True
        
        # Правило 2: Если статус заявки await_institute
        elif current_status == 'await_institute':
            # 2.1 Если роль institute_validator
            if user_role == 'institute_validator':
                # Проверяем, есть ли подразделение пользователя в причастных
                return self._is_user_department_involved(application, user)
            
            # 2.2 Роли cpds, admin - всегда доступны
            elif user_role in ['cpds', 'admin']:
                return True
        
        return False
    
    def _is_user_department_involved(self, application, user) -> bool:
        """
        Проверяет, есть ли подразделение пользователя в причастных подразделениях заявки.
        """
        if not hasattr(user, 'department') or not user.department:
            return False
        
        # Получаем причастные подразделения заявки
        involved_departments = application.involved_departments.all()
        
        # Проверяем, есть ли подразделение пользователя в списке причастных
        return involved_departments.filter(id=user.department.id).exists()
    
