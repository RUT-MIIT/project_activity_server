"""Сервис для логирования изменений в проектных заявках.

Обеспечивает отслеживание всех изменений статусов, причастных пользователей
и подразделений в проектных заявках.
"""

from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Department
from showcase.models import (
    ApplicationStatus,
    ProjectApplication,
    ProjectApplicationStatusLog,
)

User = get_user_model()


class ApplicationLoggingService:
    """Сервис для логирования изменений в проектных заявках.

    Обеспечивает полное отслеживание всех изменений:
    - Изменения статусов заявок
    - Добавление/удаление причастных пользователей
    - Добавление/удаление причастных подразделений
    """

    @transaction.atomic
    def log_status_change(
        self,
        application: ProjectApplication,
        from_status: ApplicationStatus,
        to_status: ApplicationStatus,
        actor: User,
        previous_log: Optional[ProjectApplicationStatusLog] = None,
    ) -> ProjectApplicationStatusLog:
        """Логирование изменения статуса заявки.

        Args:
            application: Заявка, статус которой изменяется
            from_status: Предыдущий статус
            to_status: Новый статус
            actor: Пользователь, выполнивший изменение
            previous_log: Предыдущий лог для создания цепочки

        Returns:
            ProjectApplicationStatusLog: Созданная запись лога

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not to_status:
            raise ValueError("Новый статус не может быть None")
        if not actor:
            raise ValueError("Актор не может быть None")

        # Создаем лог изменения статуса
        status_log = ProjectApplicationStatusLog.objects.create(
            application=application,
            action_type="status_change",
            actor=actor,
            from_status=from_status,
            to_status=to_status,
            previous_status_log=previous_log,
        )

        return status_log

    @transaction.atomic
    def log_involved_user_added(
        self, application: ProjectApplication, user: User, actor: User
    ) -> ProjectApplicationStatusLog:
        """Логирование добавления причастного пользователя.

        Args:
            application: Заявка
            user: Добавляемый пользователь
            actor: Пользователь, выполнивший добавление

        Returns:
            ProjectApplicationStatusLog: Созданная запись лога

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not user:
            raise ValueError("Пользователь не может быть None")
        if not actor:
            raise ValueError("Актор не может быть None")

        # Получаем текущий статус заявки
        current_status = application.status

        # Создаем лог добавления пользователя
        status_log = ProjectApplicationStatusLog.objects.create(
            application=application,
            action_type="involved_user_added",
            involved_user=user,
            actor=actor,
            from_status=current_status,
            to_status=current_status,  # Статус заявки не меняется
        )

        return status_log

    @transaction.atomic
    def log_involved_user_removed(
        self, application: ProjectApplication, user: User, actor: User
    ) -> ProjectApplicationStatusLog:
        """Логирование удаления причастного пользователя.

        Args:
            application: Заявка
            user: Удаляемый пользователь
            actor: Пользователь, выполнивший удаление

        Returns:
            ProjectApplicationStatusLog: Созданная запись лога

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not user:
            raise ValueError("Пользователь не может быть None")
        if not actor:
            raise ValueError("Актор не может быть None")

        # Получаем текущий статус заявки
        current_status = application.status

        # Создаем лог удаления пользователя
        status_log = ProjectApplicationStatusLog.objects.create(
            application=application,
            action_type="involved_user_removed",
            involved_user=user,
            actor=actor,
            from_status=current_status,
            to_status=current_status,  # Статус заявки не меняется
        )

        return status_log

    @transaction.atomic
    def log_involved_department_added(
        self, application: ProjectApplication, department: Department, actor: User
    ) -> ProjectApplicationStatusLog:
        """Логирование добавления причастного подразделения.

        Args:
            application: Заявка
            department: Добавляемое подразделение
            actor: Пользователь, выполнивший добавление

        Returns:
            ProjectApplicationStatusLog: Созданная запись лога

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not department:
            raise ValueError("Подразделение не может быть None")
        if not actor:
            raise ValueError("Актор не может быть None")

        # Получаем текущий статус заявки
        current_status = application.status

        # Создаем лог добавления подразделения
        status_log = ProjectApplicationStatusLog.objects.create(
            application=application,
            action_type="involved_department_added",
            involved_department=department,
            actor=actor,
            from_status=current_status,
            to_status=current_status,  # Статус заявки не меняется
        )

        return status_log

    @transaction.atomic
    def log_involved_department_removed(
        self, application: ProjectApplication, department: Department, actor: User
    ) -> ProjectApplicationStatusLog:
        """Логирование удаления причастного подразделения.

        Args:
            application: Заявка
            department: Удаляемое подразделение
            actor: Пользователь, выполнивший удаление

        Returns:
            ProjectApplicationStatusLog: Созданная запись лога

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not department:
            raise ValueError("Подразделение не может быть None")
        if not actor:
            raise ValueError("Актор не может быть None")

        # Получаем текущий статус заявки
        current_status = application.status

        # Создаем лог удаления подразделения
        status_log = ProjectApplicationStatusLog.objects.create(
            application=application,
            action_type="involved_department_removed",
            involved_department=department,
            actor=actor,
            from_status=current_status,
            to_status=current_status,  # Статус заявки не меняется
        )

        return status_log

    def get_application_logs(
        self, application: ProjectApplication
    ) -> list[ProjectApplicationStatusLog]:
        """Получение всех логов по заявке.

        Args:
            application: Заявка

        Returns:
            List[ProjectApplicationStatusLog]: Список логов, отсортированный по времени

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")

        return list(
            ProjectApplicationStatusLog.objects.filter(application=application)
            .select_related(
                "actor",
                "from_status",
                "to_status",
                "involved_user",
                "involved_department",
            )
            .order_by("-changed_at")
        )

    def get_latest_log(
        self, application: ProjectApplication
    ) -> Optional[ProjectApplicationStatusLog]:
        """Получение последнего лога заявки.

        Args:
            application: Заявка

        Returns:
            Optional[ProjectApplicationStatusLog]: Последний лог или None

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")

        try:
            return (
                ProjectApplicationStatusLog.objects.filter(application=application)
                .select_related(
                    "actor",
                    "from_status",
                    "to_status",
                    "involved_user",
                    "involved_department",
                )
                .order_by("-changed_at")
                .first()
            )
        except ProjectApplicationStatusLog.DoesNotExist:
            return None

    def get_logs_by_action_type(
        self, application: ProjectApplication, action_type: str
    ) -> list[ProjectApplicationStatusLog]:
        """Получение логов по типу действия.

        Args:
            application: Заявка
            action_type: Тип действия (status_change, involved_user_added, и т.д.)

        Returns:
            List[ProjectApplicationStatusLog]: Список логов указанного типа

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not action_type:
            raise ValueError("Тип действия не может быть пустым")

        return list(
            ProjectApplicationStatusLog.objects.filter(
                application=application, action_type=action_type
            )
            .select_related(
                "actor",
                "from_status",
                "to_status",
                "involved_user",
                "involved_department",
            )
            .order_by("-changed_at")
        )

    def get_logs_by_actor(
        self, application: ProjectApplication, actor: User
    ) -> list[ProjectApplicationStatusLog]:
        """Получение логов по актору (пользователю, выполнившему действие).

        Args:
            application: Заявка
            actor: Пользователь-актор

        Returns:
            List[ProjectApplicationStatusLog]: Список логов указанного актора

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not actor:
            raise ValueError("Актор не может быть None")

        return list(
            ProjectApplicationStatusLog.objects.filter(
                application=application, actor=actor
            )
            .select_related(
                "actor",
                "from_status",
                "to_status",
                "involved_user",
                "involved_department",
            )
            .order_by("-changed_at")
        )

    @transaction.atomic
    def log_application_update(
        self, application: ProjectApplication, actor: User
    ) -> ProjectApplicationStatusLog:
        """Логирование обновления заявки.

        Args:
            application: Обновленная заявка
            actor: Пользователь, выполнивший обновление

        Returns:
            ProjectApplicationStatusLog: Созданная запись лога

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not actor:
            raise ValueError("Актор не может быть None")

        # Получаем текущий статус заявки
        current_status = application.status

        # Создаем лог обновления заявки
        status_log = ProjectApplicationStatusLog.objects.create(
            application=application,
            action_type="application_updated",
            actor=actor,
            from_status=current_status,
            to_status=current_status,  # Статус заявки не меняется при обновлении
        )

        return status_log
