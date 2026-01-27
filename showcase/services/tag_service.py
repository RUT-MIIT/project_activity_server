"""Сервис для оркестрации операций с тегами.

Координирует Domain, Repository и DTO.
"""

from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from accounts.models import Department
from showcase.domain.tag import TagDomain
from showcase.dto.tag import TagCreateDTO, TagUpdateDTO
from showcase.models import Tag
from showcase.repositories.tag import TagRepository

if TYPE_CHECKING:
    from django.db.models import QuerySet

User = get_user_model()


class TagService:
    """Сервис - оркестрация всех операций с тегами.

    Координирует Domain, Repository и DTO.
    """

    def __init__(self):
        self.repository = TagRepository()
        self.domain = TagDomain()

    @transaction.atomic
    def create_tag(self, dto: TagCreateDTO, user: User) -> Tag:
        """Бизнес-операция: создание тега.

        Args:
            dto: DTO с данными для создания тега
            user: Пользователь, создающий тег

        Returns:
            Созданный тег

        Raises:
            ValueError: Если нет прав или данные некорректны
        """
        # Проверка прав на создание
        can_create, error_message = self.domain.can_create_tag(user, dto.department_ids)
        if not can_create:
            raise ValueError(error_message)

        role_code = user.role.code if user.role else None

        # Устанавливаем is_base и departments в зависимости от роли
        if role_code in {"cpds", "admin"} or user.is_staff:
            # cpds и admin создают базовые теги без подразделений
            dto.is_base = True
            dto.department_ids = []
        elif role_code == "institute_validator":
            # institute_validator создает небазовые теги со своим подразделением
            dto.is_base = False
            if user.department:
                dto.department_ids = [user.department.id]
            else:
                raise ValueError("У пользователя нет подразделения для создания тега")

        # Создание через репозиторий
        return self.repository.create(dto)

    @transaction.atomic
    def update_tag(self, tag_id: int, dto: TagUpdateDTO, user: User) -> Tag:
        """Бизнес-операция: обновление тега.

        Args:
            tag_id: ID тега для обновления
            dto: DTO с данными для обновления
            user: Пользователь, обновляющий тег

        Returns:
            Обновленный тег

        Raises:
            ValueError: Если нет прав, тег не найден или данные некорректны
            Tag.DoesNotExist: Если тег не найден
        """
        # Получаем тег
        try:
            tag = self.repository.get_by_id(tag_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Тег с ID {tag_id} не найден") from err

        # Проверка прав на обновление
        can_update, error_message = self.domain.can_update_tag(user, tag)
        if not can_update:
            raise ValueError(error_message)

        # Автоматическая установка department для institute_validator при обновлении
        role_code = user.role.code if user.role else None
        if role_code == "institute_validator" and dto.department_ids is None:
            # Если institute_validator обновляет тег и не указывает departments,
            # оставляем текущие departments (или устанавливаем свой, если тег общий)
            tag_departments = list(tag.departments.values_list("id", flat=True))
            if not tag_departments and user.department:
                dto.department_ids = [user.department.id]

        # Обновление через репозиторий
        return self.repository.update(tag, dto)

    @transaction.atomic
    def delete_tag(self, tag_id: int, user: User) -> bool:
        """Бизнес-операция: удаление тега.

        Args:
            tag_id: ID тега для удаления
            user: Пользователь, удаляющий тег

        Returns:
            True если тег был удален

        Raises:
            ValueError: Если нет прав или тег не найден
            Tag.DoesNotExist: Если тег не найден
        """
        # Получаем тег
        try:
            tag = self.repository.get_by_id(tag_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Тег с ID {tag_id} не найден") from err

        # Проверка прав на удаление
        can_delete, error_message = self.domain.can_delete_tag(user, tag)
        if not can_delete:
            raise ValueError(error_message)

        # Удаление через репозиторий
        return self.repository.delete(tag)

    def list_tags(self, user: User) -> "QuerySet[Tag]":
        """Бизнес-операция: получение списка тегов с фильтрацией по ролям.

        Для institute_validator: если у подразделения и родительского нет тегов,
        автоматически сопоставляем все базовые теги с подразделением.

        Args:
            user: Пользователь для фильтрации

        Returns:
            QuerySet отфильтрованных тегов
        """
        # Оптимизация: для всех пользователей с подразделением загружаем его с parent одним запросом
        department = None
        if user.is_authenticated and user.department:
            try:
                department = Department.objects.select_related("parent").get(
                    pk=user.department.id
                )
                # Обновляем user.department для использования в domain
                user.department = department
            except Department.DoesNotExist:
                pass

        # Для institute_validator: если у подразделения и родительского нет тегов,
        # автоматически сопоставляем все базовые теги с подразделением
        if department:
            # Проверяем, есть ли у подразделения или родительского связанные теги
            department_ids = [department.id]
            if department.parent:
                department_ids.append(department.parent.id)

            # Используем exists() для более эффективной проверки
            department_tags_exist = Tag.objects.filter(
                departments__in=department_ids
            ).exists()

            # Автоматическое сопоставление только для institute_validator
            if (
                not department_tags_exist
                and hasattr(user, "role")
                and user.role
                and user.role.code == "institute_validator"
            ):
                with transaction.atomic():
                    # Сопоставляем все базовые теги с подразделением пользователя
                    # Используем prefetch_related для оптимизации
                    base_tags = Tag.objects.filter(is_base=True).prefetch_related(
                        "departments"
                    )
                    for tag in base_tags:
                        tag.departments.add(department)

        # Получаем базовый queryset через репозиторий
        queryset = self.repository.get_all()

        # Фильтруем через domain
        return self.domain.get_filtered_queryset(user, queryset)

    def get_tag(self, tag_id: int, user: User) -> Tag:
        """Бизнес-операция: получение тега по ID с проверкой доступа.

        Args:
            tag_id: ID тега
            user: Пользователь для проверки доступа

        Returns:
            Тег

        Raises:
            ValueError: Если нет доступа или тег не найден
            Tag.DoesNotExist: Если тег не найден
        """
        # Получаем тег
        try:
            tag = self.repository.get_by_id(tag_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Тег с ID {tag_id} не найден") from err

        # Проверяем доступ через фильтрацию
        queryset = self.repository.get_all()
        filtered_queryset = self.domain.get_filtered_queryset(user, queryset)

        if not filtered_queryset.filter(pk=tag_id).exists():
            raise ValueError("Нет доступа к этому тегу")

        return tag

    @transaction.atomic
    def attach_department(self, tag_id: int, department_id: int, user: User) -> Tag:
        """Бизнес-операция: присоединение подразделения к тегу.

        Args:
            tag_id: ID тега
            department_id: ID подразделения для присоединения
            user: Пользователь, выполняющий операцию

        Returns:
            Обновленный тег

        Raises:
            ValueError: Если нет прав, тег/подразделение не найдены или данные некорректны
        """
        # Получаем тег
        try:
            tag = self.repository.get_by_id(tag_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Тег с ID {tag_id} не найден") from err

        # Проверяем существование подразделения
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist as err:
            raise ValueError(f"Подразделение с ID {department_id} не найдено") from err

        # Проверка прав на присоединение
        can_attach, error_message = self.domain.can_attach_department(
            user, tag, department_id
        )
        if not can_attach:
            raise ValueError(error_message)

        # Проверяем, что подразделение еще не присоединено
        if tag.departments.filter(pk=department_id).exists():
            raise ValueError("Подразделение уже присоединено к этому тегу")

        # Присоединяем подразделение
        tag.departments.add(department)

        # Обновляем тег из БД для возврата актуальных данных
        return self.repository.get_by_id(tag_id)

    @transaction.atomic
    def detach_department(
        self, tag_id: int, department_id: int, user: User
    ) -> Optional[Tag]:
        """Бизнес-операция: отцепление подразделения от тега.

        Если тег не базовый (is_base=False) и после отцепления не осталось подразделений,
        тег будет удален.

        Args:
            tag_id: ID тега
            department_id: ID подразделения для отцепления
            user: Пользователь, выполняющий операцию

        Returns:
            Обновленный тег или None, if тег был удален

        Raises:
            ValueError: Если нет прав, тег/подразделение не найдены или данные некорректны
        """
        # Получаем тег
        try:
            tag = self.repository.get_by_id(tag_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Тег с ID {tag_id} не найден") from err

        # Проверяем существование подразделения
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist as err:
            raise ValueError(f"Подразделение с ID {department_id} не найдено") from err

        # Проверка прав на отцепление
        can_detach, error_message = self.domain.can_detach_department(
            user, tag, department_id
        )
        if not can_detach:
            raise ValueError(error_message)

        # Проверяем, что подразделение действительно присоединено
        if not tag.departments.filter(pk=department_id).exists():
            raise ValueError("Подразделение не присоединено к этому тегу")

        # Отцепляем подразделение
        tag.departments.remove(department)

        # Проверяем, остались ли подразделения у тега
        remaining_departments_count = tag.departments.count()

        # If тег не базовый и подразделений не осталось - удаляем тег
        if not tag.is_base and remaining_departments_count == 0:
            self.repository.delete(tag)
            return None

        # Обновляем тег из БД для возврата актуальных данных
        return self.repository.get_by_id(tag_id)
