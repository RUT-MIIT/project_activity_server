"""
Репозиторий для работы с проектными заявками в БД.

Изолирует всю работу с базой данных от бизнес-логики.
"""

from typing import List, Optional
from django.db.models import Q
from django.contrib.auth import get_user_model

from showcase.models import ProjectApplication, ApplicationStatus, Institute
from showcase.dto.application import ProjectApplicationCreateDTO, ProjectApplicationUpdateDTO

User = get_user_model()


class ProjectApplicationRepository:
    """Репозиторий - вся работа с БД здесь"""
    
    def create(self, dto: ProjectApplicationCreateDTO, author: User, status_code: str) -> ProjectApplication:
        """
        Создание заявки в БД.
        
        Принимает DTO и пользователя, возвращает созданную модель.
        """
        # Получаем статус
        status = ApplicationStatus.objects.get(code=status_code)
        
        # Создаем заявку
        application = ProjectApplication.objects.create(
            title=dto.title,
            company=dto.company,
            author=author,
            author_lastname=dto.author_lastname or "",
            author_firstname=dto.author_firstname or "",
            author_middlename=dto.author_middlename or "",
            author_email=dto.author_email or "",
            author_phone=dto.author_phone or "",
            author_role=dto.author_role or "",
            author_division=dto.author_division or "",
            company_contacts=dto.company_contacts,
            project_level=dto.project_level,
            problem_holder=dto.problem_holder or "",
            goal=dto.goal or "",
            barrier=dto.barrier or "",
            existing_solutions=dto.existing_solutions,
            context=dto.context,
            stakeholders=dto.stakeholders,
            recommended_tools=dto.recommended_tools,
            experts=dto.experts,
            additional_materials=dto.additional_materials,
            needs_consultation=dto.needs_consultation,
            status=status,
        )
        
        # Устанавливаем M2M поля
        if dto.target_institutes:
            institutes = Institute.objects.filter(code__in=dto.target_institutes)
            application.target_institutes.set(institutes)
        
        return application
    
    def get_by_id(self, application_id: int) -> ProjectApplication:
        """
        Получение заявки по ID с оптимизацией запросов.
        
        Включает все связанные объекты для детального просмотра.
        """
        return (
            ProjectApplication.objects
            .select_related('status', 'author')
            .prefetch_related(
                'target_institutes',
                'involved_users__user',
                'involved_departments__department',
                'status_logs__from_status',
                'status_logs__to_status',
                'status_logs__actor',
                'status_logs__comments__author',
            )
            .get(pk=application_id)
        )
    
    def get_by_id_simple(self, application_id: int) -> ProjectApplication:
        """
        Получение заявки по ID без дополнительных связанных объектов.
        
        Для простых операций, где не нужны все связи.
        """
        return ProjectApplication.objects.select_related('status', 'author').get(pk=application_id)
    
    def filter_by_user(self, user: User) -> List[ProjectApplication]:
        """
        Получение заявок пользователя (автор или причастный).
        
        Оптимизированный запрос для списка заявок.
        """
        return list(
            ProjectApplication.objects
            .filter(Q(author=user) | Q(involved_users__user=user))
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .distinct()
            .order_by('-creation_date')
        )
    
    def filter_by_user_queryset(self, user: User):
        """
        Получение QuerySet заявок пользователя для пагинации.
        
        Возвращает QuerySet вместо списка для поддержки пагинации.
        """
        return (
            ProjectApplication.objects
            .filter(Q(author=user) | Q(involved_users__user=user))
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .distinct()
            .order_by('-creation_date')
        )
    
    def filter_in_work_by_user(self, user: User) -> List[ProjectApplication]:
        """
        Получение заявок в работе пользователя.
        Заявки, где пользователь причастен и статус не approved/rejected.
        """
        return list(
            ProjectApplication.objects
            .filter(involved_users__user=user)
            .exclude(status__code__in=['approved', 'rejected'])
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .distinct()
            .order_by('-creation_date')
        )
    
    def filter_in_work_by_user_queryset(self, user: User):
        """
        Получение QuerySet заявок в работе пользователя для пагинации.
        """
        return (
            ProjectApplication.objects
            .filter(involved_users__user=user)
            .exclude(status__code__in=['approved', 'rejected'])
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .distinct()
            .order_by('-creation_date')
        )
    
    def filter_by_status(self, status_code: str) -> List[ProjectApplication]:
        """
        Получение заявок по статусу.
        
        Для административных операций.
        """
        return list(
            ProjectApplication.objects
            .filter(status__code=status_code)
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .order_by('-creation_date')
        )
    
    def filter_by_status_queryset(self, status_code: str):
        """
        Получение QuerySet заявок по статусу для пагинации.
        """
        return (
            ProjectApplication.objects
            .filter(status__code=status_code)
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .order_by('-creation_date')
        )
    
    def filter_by_company(self, company_name: str) -> List[ProjectApplication]:
        """
        Получение заявок по компании.
        
        Для поиска и аналитики.
        """
        return list(
            ProjectApplication.objects
            .filter(company__icontains=company_name)
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .order_by('-creation_date')
        )
    
    def update(self, application: ProjectApplication, dto: ProjectApplicationUpdateDTO) -> ProjectApplication:
        """
        Обновление заявки.
        
        Обновляет только переданные поля.
        """
        # Обновляем только переданные поля
        if dto.title is not None:
            application.title = dto.title
        if dto.company is not None:
            application.company = dto.company
        if dto.author_lastname is not None:
            application.author_lastname = dto.author_lastname
        if dto.author_firstname is not None:
            application.author_firstname = dto.author_firstname
        if dto.author_middlename is not None:
            application.author_middlename = dto.author_middlename
        if dto.author_email is not None:
            application.author_email = dto.author_email
        if dto.author_phone is not None:
            application.author_phone = dto.author_phone
        if dto.author_role is not None:
            application.author_role = dto.author_role
        if dto.author_division is not None:
            application.author_division = dto.author_division
        if dto.company_contacts is not None:
            application.company_contacts = dto.company_contacts
        if dto.project_level is not None:
            application.project_level = dto.project_level
        if dto.problem_holder is not None:
            application.problem_holder = dto.problem_holder
        if dto.goal is not None:
            application.goal = dto.goal
        if dto.barrier is not None:
            application.barrier = dto.barrier
        if dto.existing_solutions is not None:
            application.existing_solutions = dto.existing_solutions
        if dto.context is not None:
            application.context = dto.context
        if dto.stakeholders is not None:
            application.stakeholders = dto.stakeholders
        if dto.recommended_tools is not None:
            application.recommended_tools = dto.recommended_tools
        if dto.experts is not None:
            application.experts = dto.experts
        if dto.additional_materials is not None:
            application.additional_materials = dto.additional_materials
        if dto.needs_consultation is not None:
            application.needs_consultation = dto.needs_consultation
        
        # Обновляем M2M поля
        if dto.target_institutes is not None:
            institutes = Institute.objects.filter(code__in=dto.target_institutes)
            application.target_institutes.set(institutes)
        
        application.save()
        return application
    
    def update_status(self, application: ProjectApplication, status_code: str) -> ProjectApplication:
        """
        Обновление статуса заявки.
        
        Простая операция для изменения статуса.
        """
        status = ApplicationStatus.objects.get(code=status_code)
        application.status = status
        application.save()
        return application
    
    def delete(self, application: ProjectApplication) -> bool:
        """
        Удаление заявки.
        
        Возвращает True если заявка была удалена.
        """
        application_id = application.id
        application.delete()
        return not ProjectApplication.objects.filter(pk=application_id).exists()
    
    def exists(self, application_id: int) -> bool:
        """
        Проверка существования заявки.
        
        Быстрая проверка без загрузки объекта.
        """
        return ProjectApplication.objects.filter(pk=application_id).exists()
    
    def count_by_user(self, user: User) -> int:
        """
        Подсчет заявок пользователя.
        
        Для статистики и ограничений.
        """
        return ProjectApplication.objects.filter(author=user).count()
    
    def count_by_status(self, status_code: str) -> int:
        """
        Подсчет заявок по статусу.
        
        Для аналитики и отчетов.
        """
        return ProjectApplication.objects.filter(status__code=status_code).count()
    
    def get_recent_applications(self, limit: int = 10) -> List[ProjectApplication]:
        """
        Получение последних заявок.
        
        Для дашборда и новостей.
        """
        return list(
            ProjectApplication.objects
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .order_by('-creation_date')[:limit]
        )
    
    def get_all_applications_queryset(self):
        """
        Получение QuerySet всех заявок для пагинации.
        
        Для административных операций и общего списка.
        """
        return (
            ProjectApplication.objects
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .order_by('-creation_date')
        )
