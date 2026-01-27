"""Доменная логика для тегов - чистые функции без эффектов."""

from django.db.models import QuerySet

from accounts.models import User
from showcase.models import Tag


class TagDomain:
    """Чистая бизнес-логика для тегов - только функции, никаких эффектов."""

    @staticmethod
    def get_filtered_queryset(user: User, queryset: QuerySet[Tag]) -> QuerySet[Tag]:
        """Фильтрует queryset тегов в зависимости от роли пользователя.

        Чистая функция - принимает пользователя и queryset, возвращает отфильтрованный queryset.

        Правила фильтрации:
        - cpds: только теги с is_base=True
        - institute_validator: теги со своим department
        - admin: все теги без фильтрации
        - остальные роли: теги с корневым подразделением пользователя

        Args:
            user: Пользователь для фильтрации
            queryset: Базовый queryset тегов

        Returns:
            Отфильтрованный queryset тегов
        """
        if not user or not user.is_authenticated:
            # Неавторизованные пользователи видят только базовые теги (is_base=True)
            return queryset.filter(is_base=True).distinct()

        role_code = user.role.code if user.role else None

        if role_code == "cpds":
            # cpds видит только базовые теги (is_base=True)
            return queryset.filter(is_base=True).distinct()

        elif role_code == "admin" or user.is_staff:
            # admin видит все теги
            return queryset

        else:
            # Для всех остальных ролей (включая institute_validator):
            # только теги своего подразделения или родительского
            if user.department:
                # Получаем список ID подразделений для фильтрации
                department_ids = [user.department.id]
                # Используем parent_id для избежания дополнительного запроса
                if hasattr(user.department, "parent_id") and user.department.parent_id:
                    department_ids.append(user.department.parent_id)
                elif hasattr(user.department, "parent") and user.department.parent:
                    department_ids.append(user.department.parent.id)

                # Фильтруем теги по подразделениям
                # prefetch_related("departments") из get_all() сохранится
                return queryset.filter(departments__in=department_ids).distinct()
            else:
                # Если нет подразделения, возвращаем пустой queryset
                return queryset.none()

    @staticmethod
    def can_create_tag(
        user: User, department_ids: list[int] | None
    ) -> tuple[bool, str]:
        """Проверяет права пользователя на создание тега.

        Args:
            user: Пользователь
            department_ids: Список ID подразделений для тега (None или пустой список для общих тегов)

        Returns:
            Кортеж (разрешено, сообщение об ошибке)
        """
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        role_code = user.role.code if user.role else None

        if (
            role_code not in {"cpds", "admin", "institute_validator"}
            and not user.is_staff
        ):
            return False, "Недостаточно прав для создания тегов"

        # cpds может создавать только общие теги (department_ids должен быть None или пустым)
        if role_code == "cpds" and department_ids:
            return False, "Роль cpds может создавать только общие теги"

        # institute_validator может создавать только общие теги или теги со своим подразделением
        if role_code == "institute_validator":
            if department_ids:
                if not user.department or user.department.id not in department_ids:
                    return False, "Можно создавать теги только для своего подразделения"

        return True, ""

    @staticmethod
    def can_update_tag(user: User, tag: Tag) -> tuple[bool, str]:
        """Проверяет права пользователя на обновление тега.

        Args:
            user: Пользователь
            tag: Тег для обновления

        Returns:
            Кортеж (разрешено, сообщение об ошибке)
        """
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        role_code = user.role.code if user.role else None

        if (
            role_code not in {"cpds", "admin", "institute_validator"}
            and not user.is_staff
        ):
            return False, "Недостаточно прав для обновления тегов"

        # admin может обновлять любые теги
        if role_code == "admin" or user.is_staff:
            return True, ""

        # Загружаем departments для проверки
        tag_departments = set(tag.departments.values_list("id", flat=True))

        # cpds может обновлять только общие теги (без departments)
        if role_code == "cpds":
            if tag_departments:
                return False, "Роль cpds может обновлять только общие теги"
            return True, ""

        # institute_validator может обновлять общие теги и теги своего подразделения
        if role_code == "institute_validator":
            if not tag_departments:
                return True, ""
            if user.department and user.department.id in tag_departments:
                return True, ""
            return False, "Можно обновлять только теги своего подразделения"

        return False, "Недостаточно прав"

    @staticmethod
    def can_delete_tag(user: User, tag: Tag) -> tuple[bool, str]:
        """Проверяет права пользователя на удаление тега.

        Args:
            user: Пользователь
            tag: Тег для удаления

        Returns:
            Кортеж (разрешено, сообщение об ошибке)
        """
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        role_code = user.role.code if user.role else None

        if (
            role_code not in {"cpds", "admin", "institute_validator"}
            and not user.is_staff
        ):
            return False, "Недостаточно прав для удаления тегов"

        # admin может удалять любые теги
        if role_code == "admin" or user.is_staff:
            return True, ""

        # Загружаем departments для проверки
        tag_departments = set(tag.departments.values_list("id", flat=True))

        # cpds может удалять только общие теги (без departments)
        if role_code == "cpds":
            if tag_departments:
                return False, "Роль cpds может удалять только общие теги"
            return True, ""

        # institute_validator может удалять общие теги и теги своего подразделения
        if role_code == "institute_validator":
            if not tag_departments:
                return True, ""
            if user.department and user.department.id in tag_departments:
                return True, ""
            return False, "Можно удалять только теги своего подразделения"

        return False, "Недостаточно прав"

    @staticmethod
    def can_attach_department(
        user: User, tag: Tag, department_id: int
    ) -> tuple[bool, str]:
        """Проверяет права пользователя на присоединение подразделения к тегу.

        Args:
            user: Пользователь
            tag: Тег для присоединения подразделения
            department_id: ID подразделения для присоединения

        Returns:
            Кортеж (разрешено, сообщение об ошибке)
        """
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        role_code = user.role.code if user.role else None

        # Только admin и institute_validator могут присоединять подразделения
        if role_code not in {"admin", "institute_validator"} and not user.is_staff:
            return False, "Недостаточно прав для управления подразделениями тега"

        # admin может присоединять любые подразделения к любым тегам
        if role_code == "admin" or user.is_staff:
            return True, ""

        # institute_validator может присоединять только свое подразделение
        if role_code == "institute_validator":
            if not user.department or user.department.id != department_id:
                return False, "Можно присоединять только свое подразделение"
            return True, ""

        return False, "Недостаточно прав"

    @staticmethod
    def can_detach_department(
        user: User, tag: Tag, department_id: int
    ) -> tuple[bool, str]:
        """Проверяет права пользователя на отцепление подразделения от тега.

        Args:
            user: Пользователь
            tag: Тег для отцепления подразделения
            department_id: ID подразделения для отцепления

        Returns:
            Кортеж (разрешено, сообщение об ошибке)
        """
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        role_code = user.role.code if user.role else None

        # Только admin и institute_validator могут отцеплять подразделения
        if role_code not in {"admin", "institute_validator"} and not user.is_staff:
            return False, "Недостаточно прав для управления подразделениями тега"

        # admin может отцеплять любые подразделения от любых тегов
        if role_code == "admin" or user.is_staff:
            return True, ""

        # Загружаем departments для проверки
        tag_departments = set(tag.departments.values_list("id", flat=True))

        # Проверяем, что подразделение действительно связано с тегом
        if department_id not in tag_departments:
            return False, "Подразделение не связано с этим тегом"

        # institute_validator может отцеплять подразделения только от тегов своего подразделения
        if role_code == "institute_validator":
            if user.department and user.department.id in tag_departments:
                # Можно отцепить любое подразделение от тега, если тег связан с нашим подразделением
                return True, ""
            return (
                False,
                "Можно отцеплять подразделения только от тегов своего подразделения",
            )

        return False, "Недостаточно прав"
