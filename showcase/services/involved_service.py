"""Сервис для управления причастными пользователями и подразделениями.

Обеспечивает добавление пользователей, их подразделений и родительских
подразделений как причастных к проектным заявкам.
"""

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Department
from showcase.models import (
    ApplicationInvolvedDepartment,
    ApplicationInvolvedUser,
    ProjectApplication,
)

User = get_user_model()


class InvolvedManagementService:
    """Сервис для управления причастными пользователями и подразделениями.

    Обеспечивает автоматическое добавление пользователя, его подразделения
    и родительского подразделения как причастных к заявке.
    """

    @transaction.atomic
    def add_user_and_departments(
        self, application: ProjectApplication, user: User, actor: User
    ) -> dict[str, list]:
        """Добавляет пользователя, его подразделение и родительское подразделение
        как причастных к заявке.

        Args:
            application: Заявка, к которой добавляются причастные
            user: Пользователь для добавления
            actor: Пользователь, выполняющий добавление

        Returns:
            Dict[str, List]: Информация о добавленных причастных:
            {
                'users_added': [User],           # Добавленные пользователи
                'departments_added': [Department], # Добавленные подразделения
                'users_existed': [User],         # Уже существующие пользователи
                'departments_existed': [Department] # Уже существующие подразделения
            }

        Raises:
            ValueError: При некорректных входных данных

        """
        if not application:
            raise ValueError("Заявка не может быть None")
        if not user:
            raise ValueError("Пользователь не может быть None")
        if not actor:
            raise ValueError("Актор не может быть None")

        result = {
            "users_added": [],
            "departments_added": [],
            "users_existed": [],
            "departments_existed": [],
        }

        # 1. Добавляем пользователя как причастного
        user_added = self._add_involved_user(application, user, actor)
        if user_added:
            result["users_added"].append(user)
        else:
            result["users_existed"].append(user)

        # 2. Добавляем подразделение пользователя (если есть)
        if user.department:
            department_added = self._add_involved_department(
                application, user.department, actor
            )
            if department_added:
                result["departments_added"].append(user.department)
            else:
                result["departments_existed"].append(user.department)

            # 3. Добавляем родительское подразделение (если есть)
            if user.department.parent:
                parent_department_added = self._add_involved_department(
                    application, user.department.parent, actor
                )
                if parent_department_added:
                    result["departments_added"].append(user.department.parent)
                else:
                    result["departments_existed"].append(user.department.parent)

        return result

    @transaction.atomic
    def add_department_by_short_name(
        self,
        application: ProjectApplication,
        short_name: str,
        actor: User | None = None,
    ) -> bool:
        """Добавляет причастное подразделение по его краткому названию.

        Args:
            application: Заявка, к которой добавляется подразделение
            short_name: Краткое название подразделения
            actor: Пользователь, выполняющий добавление

        Returns:
            bool: True если подразделение найдено и добавлено/присутствует, False если не найдено

        Raises:
            ValueError: Если не указано краткое название
        """
        if not short_name:
            raise ValueError("Краткое название подразделения обязательно")

        department = Department.objects.filter(short_name=short_name).first()
        if not department:
            return False

        self._add_involved_department(application, department, actor)
        return True

    @transaction.atomic
    def add_department_by_id(
        self,
        application: ProjectApplication,
        department_id: int,
        actor: User | None = None,
    ) -> bool:
        """Добавляет причастное подразделение по его ID.

        Args:
            application: Заявка, к которой добавляется подразделение
            department_id: ID подразделения
            actor: Пользователь, выполняющий добавление

        Returns:
            bool: True если подразделение найдено и добавлено/присутствует, False если не найдено

        Raises:
            ValueError: Если не указан ID подразделения
        """
        if not department_id:
            raise ValueError("ID подразделения обязательно")

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return False

        self._add_involved_department(application, department, actor)
        return True

    def _add_involved_user(
        self, application: ProjectApplication, user: User, actor: User
    ) -> bool:
        """Добавляет пользователя как причастного к заявке.

        Args:
            application: Заявка
            user: Пользователь для добавления
            actor: Пользователь, выполняющий добавление

        Returns:
            bool: True если пользователь был добавлен, False если уже существовал

        """
        # Проверяем, не добавлен ли уже пользователь
        if application.involved_users.filter(user=user).exists():
            return False

        # Добавляем пользователя
        ApplicationInvolvedUser.objects.create(
            application=application, user=user, added_by=actor
        )
        return True

    def _add_involved_department(
        self,
        application: ProjectApplication,
        department: "Department",
        actor: User | None = None,
    ) -> bool:
        """Добавляет подразделение как причастное к заявке.

        Args:
            application: Заявка
            department: Подразделение для добавления
            actor: Пользователь, выполняющий добавление

        Returns:
            bool: True если подразделение было добавлено, False если уже существовало

        """
        # Проверяем, не добавлено ли уже подразделение
        if application.involved_departments.filter(department=department).exists():
            return False

        # Добавляем подразделение
        ApplicationInvolvedDepartment.objects.create(
            application=application, department=department, added_by=actor
        )
        return True

    def get_involved_users(self, application: ProjectApplication) -> list[User]:
        """Получает всех причастных пользователей заявки.

        Args:
            application: Заявка

        Returns:
            List[User]: Список причастных пользователей

        """
        return [
            involved.user
            for involved in application.involved_users.select_related("user").all()
        ]

    def get_involved_departments(
        self, application: ProjectApplication
    ) -> list["Department"]:
        """Получает все причастные подразделения заявки.

        Args:
            application: Заявка

        Returns:
            List[Department]: Список причастных подразделений

        """
        return [
            involved.department
            for involved in application.involved_departments.select_related(
                "department"
            ).all()
        ]

    def remove_involved_user(
        self, application: ProjectApplication, user: User, actor: User
    ) -> bool:
        """Удаляет пользователя из причастных к заявке.

        Args:
            application: Заявка
            user: Пользователь для удаления
            actor: Пользователь, выполняющий удаление

        Returns:
            bool: True если пользователь был удален, False если не был причастным

        """
        involved_user = application.involved_users.filter(user=user).first()
        if involved_user:
            involved_user.delete()
            return True
        return False

    def remove_involved_department(
        self, application: ProjectApplication, department: "Department", actor: User
    ) -> bool:
        """Удаляет подразделение из причастных к заявке.

        Args:
            application: Заявка
            department: Подразделение для удаления
            actor: Пользователь, выполняющий удаление

        Returns:
            bool: True если подразделение было удалено, False если не было причастным

        """
        involved_department = application.involved_departments.filter(
            department=department
        ).first()
        if involved_department:
            involved_department.delete()
            return True
        return False
