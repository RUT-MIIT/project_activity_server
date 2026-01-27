"""Репозиторий для работы с тегами в БД.

Изолирует всю работу с базой данных от бизнес-логики.
"""

from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from accounts.models import Department
from showcase.dto.tag import TagCreateDTO, TagUpdateDTO
from showcase.models import Tag

if TYPE_CHECKING:
    from django.db.models import QuerySet


class TagRepository:
    """Репозиторий - вся работа с БД здесь."""

    def create(self, dto: TagCreateDTO) -> Tag:
        """Создание тега в БД.

        Args:
            dto: DTO с данными для создания тега

        Returns:
            Созданный тег

        Raises:
            ValueError: Если department не найден или тег с таким name+departments уже существует
        """
        # Получаем подразделения
        departments = []
        if dto.department_ids:
            try:
                departments = list(Department.objects.filter(pk__in=dto.department_ids))
                if len(departments) != len(dto.department_ids):
                    found_ids = {dept.id for dept in departments}
                    missing_ids = set(dto.department_ids) - found_ids
                    raise ValueError(f"Подразделения с id {missing_ids} не найдены")
            except ObjectDoesNotExist as err:
                raise ValueError("Подразделения не найдены") from err

        # Проверка на дубликат по (name, departments)
        # Проверяем, что нет тега с таким же name и таким же набором departments
        new_dept_ids = set(dto.department_ids) if dto.department_ids else set()
        existing_tags = Tag.objects.filter(name=dto.name).prefetch_related(
            "departments"
        )
        for existing_tag in existing_tags:
            existing_dept_ids = set(
                existing_tag.departments.values_list("id", flat=True)
            )
            if existing_dept_ids == new_dept_ids:
                raise ValueError(
                    "Тег с таким названием и таким набором подразделений уже существует"
                )

        try:
            create_kwargs = {
                "name": dto.name,
                "category": dto.category,
            }
            # Устанавливаем is_base, если оно указано в DTO
            if dto.is_base is not None:
                create_kwargs["is_base"] = dto.is_base

            tag = Tag.objects.create(**create_kwargs)
            if departments:
                tag.departments.set(departments)
        except IntegrityError as err:
            raise ValueError("Ошибка при создании тега") from err

        return tag

    def get_by_id(self, tag_id: int) -> Tag:
        """Получение тега по ID с оптимизацией запросов.

        Args:
            tag_id: ID тега

        Returns:
            Тег

        Raises:
            Tag.DoesNotExist: Если тег не найден
        """
        return Tag.objects.prefetch_related("departments").get(pk=tag_id)

    def update(self, tag: Tag, dto: TagUpdateDTO) -> Tag:
        """Обновление тега.

        Обновляет только переданные поля.

        Args:
            tag: Тег для обновления
            dto: DTO с данными для обновления

        Returns:
            Обновленный тег

        Raises:
            ValueError: Если department не найден или тег с таким name+departments уже существует
        """
        # Определяем будущие значения name и departments
        new_name = dto.name if dto.name is not None else tag.name
        new_department_ids = dto.department_ids

        # Если department_ids не указаны, оставляем текущие departments
        if new_department_ids is None:
            # Загружаем текущие departments для проверки уникальности
            tag.departments.all()
            new_dept_ids = set(tag.departments.values_list("id", flat=True))
        else:
            # Получаем новые подразделения
            try:
                departments = list(Department.objects.filter(pk__in=new_department_ids))
                if len(departments) != len(new_department_ids):
                    found_ids = {dept.id for dept in departments}
                    missing_ids = set(new_department_ids) - found_ids
                    raise ValueError(f"Подразделения с id {missing_ids} не найдены")
                new_dept_ids = set(new_department_ids)
            except ObjectDoesNotExist as err:
                raise ValueError("Подразделения не найдены") from err

        # Проверка на дубликат по (name, departments), исключая текущий тег
        existing_tags = (
            Tag.objects.filter(name=new_name)
            .exclude(pk=tag.pk)
            .prefetch_related("departments")
        )
        for existing_tag in existing_tags:
            existing_dept_ids = set(
                existing_tag.departments.values_list("id", flat=True)
            )
            if existing_dept_ids == new_dept_ids:
                raise ValueError(
                    "Тег с таким названием и таким набором подразделений уже существует"
                )

        # Применяем изменения к объекту
        update_fields = []

        if dto.name is not None:
            tag.name = dto.name
            update_fields.append("name")

        if dto.category is not None:
            tag.category = dto.category
            update_fields.append("category")

        try:
            if update_fields:
                tag.save(update_fields=update_fields)
            else:
                tag.save()

            # Обновляем ManyToMany связь departments
            if new_department_ids is not None:
                tag.departments.set(departments)
        except IntegrityError as err:
            raise ValueError("Ошибка при обновлении тега") from err

        return tag

    def delete(self, tag: Tag) -> bool:
        """Удаление тега.

        Args:
            tag: Тег для удаления

        Returns:
            True если тег был удален
        """
        tag_id = tag.id
        tag.delete()
        return not Tag.objects.filter(pk=tag_id).exists()

    def get_all(self) -> "QuerySet[Tag]":
        """Получение всех тегов с оптимизацией запросов.

        Returns:
            QuerySet всех тегов с prefetch_related для departments
        """
        return Tag.objects.prefetch_related("departments").all()

    def exists(self, tag_id: int) -> bool:
        """Проверка существования тега.

        Быстрая проверка без загрузки объекта.

        Args:
            tag_id: ID тега

        Returns:
            True если тег существует
        """
        return Tag.objects.filter(pk=tag_id).exists()
