"""Сервис для оркестрации операций с проектными заявками.

Координирует Domain, Repository и существующие сервисы.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from showcase.domain.application import ProjectApplicationDomain
from showcase.domain.capabilities import ApplicationCapabilities
from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationListDTO,
    ProjectApplicationReadDTO,
    ProjectApplicationUpdateDTO,
)
from showcase.dto.available_actions import AvailableActionsDTO
from showcase.models import ApplicationStatus
from showcase.repositories.application import ProjectApplicationRepository
from showcase.services.involved_service import InvolvedManagementService
from showcase.services.logging_service import ApplicationLoggingService

User = get_user_model()


class ProjectApplicationService:
    """Сервис - оркестрация всех операций.

    Координирует Domain, Repository и StatusService.
    Использует существующие сервисы без изменений.
    """

    def __init__(self):
        self.repository = ProjectApplicationRepository()
        self.logging_service = ApplicationLoggingService()
        self.involved_service = InvolvedManagementService()

    @transaction.atomic
    def submit_application(self, dto: ProjectApplicationCreateDTO, user: User):
        """Бизнес-операция: подача заявки.

        Новая логика:
        1. Валидация через Domain
        2. Создание заявки со статусом "created"
        3. Логирование создания заявки
        4. Добавление причастных (пользователь + подразделения)
        5. Определение финального статуса
        6. Изменение статуса и логирование (если нужно)
        """
        # 1. Валидация (Domain)
        user_role = user.role.code if user and user.role else "user"
        validation = ApplicationCapabilities.submit_application(dto, user_role)
        if not validation.is_valid:
            raise ValueError(validation.errors)

        # 2. Определяем необходимость консультации (Domain)
        needs_consultation = ProjectApplicationDomain.should_require_consultation(dto)
        dto.needs_consultation = needs_consultation

        # 3. Создаем заявку со статусом "created" (всегда)
        application = self.repository.create(dto, user, "created")

        # 4. Логируем создание заявки
        self.logging_service.log_status_change(
            application=application,
            from_status=None,  # Заявка только что создана
            to_status=application.status,
            actor=user,
        )

        # 5. Добавляем причастных (пользователь + его подразделение + родительское)
        if user:
            self.involved_service.add_user_and_departments(
                application=application, user=user, actor=user
            )

        # 6. Определяем финальный статус на основе роли
        final_status_code = ProjectApplicationDomain.calculate_initial_status(user_role)

        # 7. Если статус изменился - обновляем и логируем
        if final_status_code != "created":
            old_status = application.status
            new_status = ApplicationStatus.objects.get(code=final_status_code)
            application.status = new_status
            application.save()

            # Логируем изменение статуса
            self.logging_service.log_status_change(
                application=application,
                from_status=old_status,
                to_status=new_status,
                actor=user,
            )

        return application

    @transaction.atomic
    def request_changes(self, application_id: int, requester: User):
        """Бизнес-операция: отправка заявки на доработку."""
        # 1. Получаем заявку (Repository)
        application = self.repository.get_by_id_simple(application_id)

        # 2. Проверка прав (Domain)
        user_role = requester.role.code if requester.role else "user"
        current_status = application.status.code

        # Проверяем права на запрос изменений
        is_user_department_involved = self._is_user_department_involved(
            application, requester
        )
        is_user_author = (
            application.author == requester if application.author else False
        )

        # Проверяем право на действие согласно матрице
        if not ApplicationCapabilities.is_action_allowed(
            action="request_changes",
            current_status=current_status,
            user_role=user_role,
            is_user_department_involved=is_user_department_involved,
            is_user_author=is_user_author,
        ):
            raise PermissionError("Недостаточно прав для запроса изменений")

        # 3. Определяем статус для доработки в зависимости от роли
        revision_status_code = self._get_revision_status_code(user_role)

        # 4. Проверяем возможность перехода (Domain)
        can_change, error = ProjectApplicationDomain.can_change_status(
            current_status, revision_status_code, user_role
        )
        if not can_change:
            raise ValueError(error)

        # 5. Сохраняем старый статус для логирования
        old_status = application.status

        # 6. Меняем статус на соответствующий статус доработки
        new_status = ApplicationStatus.objects.get(code=revision_status_code)
        application.status = new_status
        application.save()

        # 7. Логируем изменение статуса
        self.logging_service.log_status_change(
            application=application,
            from_status=old_status,
            to_status=new_status,
            actor=requester,
        )

        return application

    @transaction.atomic
    def approve_application(self, application_id: int, approver: User):
        """Бизнес-операция: одобрение заявки."""
        # 1. Получаем заявку (Repository) - нужно для проверки прав
        application = self.repository.get_by_id_simple(application_id)

        # 2. Проверка прав (Domain)
        user_role = approver.role.code if approver.role else "user"
        is_user_department_involved = self._is_user_department_involved(
            application, approver
        )
        is_user_author = application.author == approver if application.author else False

        # Проверяем право на действие согласно матрице
        if not ApplicationCapabilities.is_action_allowed(
            action="approve",
            current_status=application.status.code,
            user_role=user_role,
            is_user_department_involved=is_user_department_involved,
            is_user_author=is_user_author,
        ):
            raise PermissionError("Недостаточно прав для одобрения заявки")

        # 3. Определяем промежуточный статус для одобрения в зависимости от роли
        approved_status_code = self._get_approved_status_code(user_role)

        # 4. Проверяем возможность перехода (Domain)
        can_change, error = ProjectApplicationDomain.can_change_status(
            application.status.code, approved_status_code, user_role
        )
        if not can_change:
            raise ValueError(error)

        # 5. Сохраняем старый статус для логирования
        old_status = application.status

        # 6. Меняем статус на промежуточный
        intermediate_status = ApplicationStatus.objects.get(code=approved_status_code)
        application.status = intermediate_status
        application.save()

        # 7. Логируем изменение статуса
        self.logging_service.log_status_change(
            application=application,
            from_status=old_status,
            to_status=intermediate_status,
            actor=approver,
        )

        # 8. Определяем следующий статус после одобрения
        next_status_code = self._get_next_status_after_approved(approved_status_code)

        if next_status_code:
            # Если есть следующий статус, переводим туда
            final_status = ApplicationStatus.objects.get(code=next_status_code)
            application.status = final_status
            application.save()

            # Логируем перевод в следующий статус
            self.logging_service.log_status_change(
                application=application,
                from_status=intermediate_status,
                to_status=final_status,
                actor=approver,
            )

        if application.status.code == "await_cpds":
            self.involved_service.add_department_by_short_name(
                application=application,
                short_name="ЦПДС",
                actor=approver,
            )

        return application

    @transaction.atomic
    def reject_application(self, application_id: int, rejector: User, reason: str = ""):
        """Бизнес-операция: отклонение заявки."""
        # 1. Получаем заявку (Repository) - нужно для проверки прав
        application = self.repository.get_by_id_simple(application_id)

        # 2. Проверка прав (Domain)
        user_role = rejector.role.code if rejector.role else "user"
        is_user_department_involved = self._is_user_department_involved(
            application, rejector
        )
        is_user_author = application.author == rejector if application.author else False

        # Проверяем право на действие согласно матрице
        if not ApplicationCapabilities.is_action_allowed(
            action="reject",
            current_status=application.status.code,
            user_role=user_role,
            is_user_department_involved=is_user_department_involved,
            is_user_author=is_user_author,
        ):
            raise PermissionError("Недостаточно прав для отклонения заявки")

        # 3. Определяем статус для отклонения в зависимости от роли
        rejected_status_code = self._get_rejected_status_code(user_role)

        # 4. Проверяем возможность перехода (Domain)
        can_change, error = ProjectApplicationDomain.can_change_status(
            application.status.code, rejected_status_code, user_role
        )
        if not can_change:
            raise ValueError(error)

        # 5. Сохраняем старый статус для логирования
        old_status = application.status

        # 6. Меняем статус
        new_status = ApplicationStatus.objects.get(code=rejected_status_code)
        application.status = new_status
        application.save()

        # 7. Логируем изменение статуса
        self.logging_service.log_status_change(
            application=application,
            from_status=old_status,
            to_status=new_status,
            actor=rejector,
        )

        # 8. Если статус rejected_* (не финальный rejected), переводим в финальный rejected
        if rejected_status_code in [
            "rejected_department",
            "rejected_institute",
            "rejected_cpds",
        ]:
            intermediate_status = new_status
            final_status = ApplicationStatus.objects.get(code="rejected")
            application.status = final_status
            application.save()

            # Логируем перевод в финальный статус rejected
            self.logging_service.log_status_change(
                application=application,
                from_status=intermediate_status,
                to_status=final_status,
                actor=rejector,
            )

        return application

    @transaction.atomic
    def update_application(
        self, application_id: int, dto: ProjectApplicationUpdateDTO, updater: User
    ):
        """Бизнес-операция: обновление заявки."""
        # 1. Получаем заявку (Repository)
        try:
            application = self.repository.get_by_id_simple(application_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Заявка с ID {application_id} не найдена") from err

        # 2. Проверка прав на редактирование (Domain)
        user_role = updater.role.code if updater.role else "user"
        is_user_department_involved = self._is_user_department_involved(
            application, updater
        )
        is_user_author = application.author == updater if application.author else False

        can_edit = ApplicationCapabilities.can_edit_application(
            current_status=application.status.code,
            user_role=user_role,
            is_user_department_involved=is_user_department_involved,
            is_user_author=is_user_author,
        )
        if not can_edit:
            raise PermissionError("Нет прав для редактирования этой заявки")

        # 3. Проверка валидации (Domain)
        author_id = application.author.id if application.author else 0
        validation, can_update, error = ApplicationCapabilities.update_application(
            dto, application.status.code, user_role, author_id, updater.id
        )
        if not validation.is_valid:
            raise ValueError(validation.errors)

        # 4. Обновляем заявку (Repository)
        application = self.repository.update(application, dto)

        # 5. Логируем обновление заявки
        self.logging_service.log_application_update(
            application=application, actor=updater
        )

        return application

    def get_application(self, application_id: int, viewer: User):
        """Бизнес-операция: получение заявки."""
        # 1. Получаем заявку (Repository)
        application = self.repository.get_by_id(application_id)

        # 2. Проверка доступа (Domain)
        can_view, error = ApplicationCapabilities.view_application(
            application.status.code,
            viewer.role.code if viewer.role else "user",
            application.author.id if application.author else 0,
            viewer.id,
        )
        if not can_view:
            raise PermissionError(error)

        return application

    def get_user_applications(self, user: User):
        """Бизнес-операция: получение заявок пользователя."""
        # 1. Проверка прав (Domain)
        can_list, error = ApplicationCapabilities.list_applications(
            user.role.code if user.role else "user"
        )
        if not can_list:
            raise PermissionError(error)

        # 2. Получаем заявки (Repository)
        applications = self.repository.filter_by_user(user)

        return applications

    def get_user_applications_queryset(self, user: User):
        """Бизнес-операция: получение QuerySet заявок пользователя для пагинации."""
        # 1. Проверка прав (Domain)
        can_list, error = ApplicationCapabilities.list_applications(
            user.role.code if user.role else "user"
        )
        if not can_list:
            raise PermissionError(error)

        # 2. Получаем QuerySet (Repository)
        return self.repository.filter_by_user_queryset(user)

    def get_user_coordination_applications(self, user: User):
        """Бизнес-операция: получение заявок для координации пользователя.

        Для обычных пользователей:
        - Заявки, где пользователь причастен и статус не approved/rejected.

        Для валидаторов (department_validator, institute_validator):
        - Заявки, где пользователь причастен
        - ПЛЮС заявки, где причастно подразделение пользователя
        - Статус не approved/rejected.
        """
        # 1. Проверка прав (Domain)
        can_list, error = ApplicationCapabilities.list_applications(
            user.role.code if user.role else "user"
        )
        if not can_list:
            raise PermissionError(error)

        # 2. Получаем заявки в работе (Repository)
        applications = self.repository.filter_coordination_by_user(user)

        # 3. Если пользователь - валидатор (department_validator или institute_validator),
        #    добавляем заявки, где причастно его подразделение
        user_role = user.role.code if user.role else "user"
        if user_role in ["department_validator", "institute_validator"]:
            if hasattr(user, "department") and user.department:
                department_applications = (
                    self.repository.filter_coordination_by_department(user.department)
                )
                # Объединяем и убираем дубликаты
                application_ids = {app.id for app in applications}
                for app in department_applications:
                    if app.id not in application_ids:
                        applications.append(app)
                        application_ids.add(app.id)

        return applications

    def get_application_dto(self, application) -> ProjectApplicationReadDTO:
        """Преобразование модели в DTO для чтения."""
        return ProjectApplicationReadDTO(application)

    def get_application_list_dto(self, application) -> ProjectApplicationListDTO:
        """Преобразование модели в DTO для списка."""
        return ProjectApplicationListDTO(application)

    def get_applications_by_status(self, status_code: str, user: User):
        """Бизнес-операция: получение заявок по статусу."""
        # 1. Проверка прав (Domain)
        if user.role and user.role.code not in ["admin", "moderator"]:
            raise PermissionError("Недостаточно прав для просмотра заявок по статусу")

        # 2. Получаем заявки (Repository)
        applications = self.repository.filter_by_status(status_code)

        return applications

    def get_recent_applications(self, limit: int = 10, user: User = None):
        """Бизнес-операция: получение последних заявок."""
        # 1. Проверка прав (Domain)
        if user and user.role and user.role.code not in ["admin", "moderator"]:
            raise PermissionError("Недостаточно прав для просмотра последних заявок")

        # 2. Получаем заявки (Repository)
        applications = self.repository.get_recent_applications(limit)

        return applications

    def get_all_applications_queryset(self, user: User):
        """Бизнес-операция: получение QuerySet всех заявок для пагинации."""
        # 1. Проверка прав (Domain)
        if not user.role or user.role.code not in ["admin", "moderator"]:
            raise PermissionError("Недостаточно прав для просмотра всех заявок")

        # 2. Получаем QuerySet (Repository)
        return self.repository.get_all_applications_queryset()

    def get_available_actions(
        self, application_id: int, user: User
    ) -> AvailableActionsDTO:
        """Бизнес-операция: получение доступных действий для заявки.

        Args:
            application_id: ID заявки
            user: Пользователь, запрашивающий действия

        Returns:
            AvailableActionsDTO: DTO с доступными действиями

        """
        # 1. Получаем заявку (Repository)
        try:
            application = self.repository.get_by_id_simple(application_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Заявка с ID {application_id} не найдена") from err

        # 2. Получаем роль пользователя
        user_role = user.role.code if user.role else "user"
        current_status = application.status.code

        # 3. Определяем доступные действия
        available_actions = []

        # Проверяем права на управление заявкой
        is_user_department_involved = self._is_user_department_involved(
            application, user
        )
        is_user_author = application.author == user if application.author else False

        # Получаем список доступных действий из новой матрицы
        available_actions = ApplicationCapabilities.get_available_actions(
            current_status=current_status,
            user_role=user_role,
            is_user_department_involved=is_user_department_involved,
            is_user_author=is_user_author,
        )
        return AvailableActionsDTO.from_actions_list(available_actions)

    def _is_user_department_involved(self, application, user) -> bool:
        """Проверяет, есть ли подразделение пользователя в причастных подразделениях заявки."""
        if not hasattr(user, "department") or not user.department:
            return False

        # Получаем причастные подразделения заявки
        involved_departments = application.involved_departments.all()

        # Проверяем, есть ли подразделение пользователя в списке причастных
        return involved_departments.filter(department__id=user.department.id).exists()

    def _get_revision_status_code(self, user_role: str) -> str:
        """Определяет статус для доработки в зависимости от роли пользователя.

        Args:
            user_role: Роль пользователя

        Returns:
            str: Код статуса для доработки

        """
        if user_role == "department_validator":
            return "returned_department"
        elif user_role == "institute_validator":
            return "returned_institute"
        elif user_role == "cpds":
            return "returned_cpds"
        elif user_role == "admin":
            # Админ может направить на доработку в любой статус
            # По умолчанию - returned_department
            return "returned_department"
        else:
            # Для других ролей - returned_department по умолчанию
            return "returned_department"

    def _get_rejected_status_code(self, user_role: str) -> str:
        """Определяет статус для отклонения в зависимости от роли пользователя.

        Args:
            user_role: Роль пользователя

        Returns:
            str: Код статуса для отклонения

        """
        if user_role == "department_validator":
            return "rejected_department"
        elif user_role == "institute_validator":
            return "rejected_institute"
        elif user_role == "cpds":
            return "rejected_cpds"
        elif user_role == "admin":
            # Админ отклоняет в статус rejected
            return "rejected"
        else:
            # Для других ролей - rejected по умолчанию
            return "rejected"

    def _get_approved_status_code(self, user_role: str) -> str:
        """Определяет промежуточный статус для одобрения в зависимости от роли пользователя.

        Args:
            user_role: Роль пользователя

        Returns:
            str: Код промежуточного статуса для одобрения

        """
        if user_role == "department_validator":
            return "approved_department"
        elif user_role == "institute_validator":
            return "approved_institute"
        elif user_role == "cpds":
            return "approved"
        elif user_role == "admin":
            # Админ одобряет сразу в финальный статус
            return "approved"
        else:
            # Для других ролей - await_department по умолчанию
            return "await_department"

    def _get_next_status_after_approved(self, approved_status_code: str) -> str:
        """Определяет следующий статус после промежуточного одобрения.

        Args:
            approved_status_code: Код промежуточного статуса одобрения

        Returns:
            str: Код следующего статуса или None если это финальное одобрение

        """
        if approved_status_code == "approved_department":
            return "await_institute"
        elif approved_status_code == "approved_institute":
            return "await_cpds"
        elif approved_status_code == "approved":
            return None  # Финальный статус, не требуется переход
        else:
            return None
