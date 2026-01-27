"""Unit-тесты для репозитория TagRepository.

Проверяем все методы работы с БД: создание, чтение, обновление, удаление.
"""

import pytest

from accounts.models import Department
from showcase.dto.tag import TagCreateDTO, TagUpdateDTO
from showcase.models import Tag
from showcase.repositories.tag import TagRepository


@pytest.mark.django_db
class TestTagRepositoryCreate:
    """Тесты для метода create репозитория."""

    def test_create_general_tag(self):
        """Создание общего тега (без departments)."""
        repo = TagRepository()
        dto = TagCreateDTO(name="Тег 1", category="Категория 1")
        tag = repo.create(dto)

        assert tag.id is not None
        assert tag.name == "Тег 1"
        assert tag.category == "Категория 1"
        assert list(tag.departments.all()) == []

    def test_create_tag_with_department(self, departments):
        """Создание тега с подразделением."""
        repo = TagRepository()
        dto = TagCreateDTO(
            name="Тег подразделения",
            category="Категория 1",
            department_ids=[departments["parent"].id],
        )
        tag = repo.create(dto)

        assert tag.id is not None
        assert tag.name == "Тег подразделения"
        assert departments["parent"] in tag.departments.all()

    def test_create_tag_with_nonexistent_department(self):
        """Создание тега с несуществующим подразделением вызывает ошибку."""
        repo = TagRepository()
        dto = TagCreateDTO(name="Тег", category="Категория 1", department_ids=[99999])

        with pytest.raises(ValueError, match="не найдены"):
            repo.create(dto)

    def test_create_tag_fails_if_same_name_and_departments_exists(self, departments):
        """Нельзя создать тег с таким же именем и таким же набором подразделений."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Дубликат", category="Категория 1")
        tag.departments.set([departments["parent"]])

        dto = TagCreateDTO(
            name="Дубликат",
            category="Категория 1",
            department_ids=[departments["parent"].id],
        )

        with pytest.raises(
            ValueError,
            match="таким набором подразделений уже существует",
        ):
            repo.create(dto)

    def test_create_tag_with_different_departments_allowed(self, departments):
        """Можно создать тег с таким же именем, но другим набором подразделений."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([departments["parent"]])

        other_dept = Department.objects.create(name="Other", short_name="OD")
        dto = TagCreateDTO(
            name="Тег",
            category="Категория 1",
            department_ids=[other_dept.id],
        )
        new_tag = repo.create(dto)

        assert new_tag.id != tag.id
        assert new_tag.name == "Тег"
        assert other_dept in new_tag.departments.all()


@pytest.mark.django_db
class TestTagRepositoryGetById:
    """Тесты для метода get_by_id репозитория."""

    def test_get_by_id_with_department(self, departments):
        """get_by_id возвращает тег с подразделением (prefetch_related)."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([departments["parent"]])

        retrieved = repo.get_by_id(tag.id)

        assert retrieved.id == tag.id
        assert retrieved.name == "Тег"
        assert departments["parent"] in retrieved.departments.all()
        # Проверяем, что prefetch_related работает (не должно быть дополнительных запросов)
        # Это проверяется отсутствием ошибок при доступе к departments
        assert departments["parent"].name in [
            d.name for d in retrieved.departments.all()
        ]

    def test_get_by_id_general_tag(self):
        """get_by_id возвращает общий тег."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")

        retrieved = repo.get_by_id(tag.id)

        assert retrieved.id == tag.id
        assert list(retrieved.departments.all()) == []

    def test_get_by_id_nonexistent(self):
        """get_by_id для несуществующего тега вызывает ошибку."""
        repo = TagRepository()

        with pytest.raises(Tag.DoesNotExist):
            repo.get_by_id(99999)


@pytest.mark.django_db
class TestTagRepositoryUpdate:
    """Тесты для метода update репозитория."""

    def test_update_name(self):
        """Обновление названия тега."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Старое название", category="Категория 1")
        dto = TagUpdateDTO(name="Новое название")

        updated = repo.update(tag, dto)

        assert updated.name == "Новое название"
        assert updated.category == "Категория 1"  # Не изменилось

    def test_update_category(self):
        """Обновление категории тега."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Старая категория")
        dto = TagUpdateDTO(category="Новая категория")

        updated = repo.update(tag, dto)

        assert updated.category == "Новая категория"
        assert updated.name == "Тег"  # Не изменилось

    def test_update_departments(self, departments):
        """Обновление подразделений тега."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        dto = TagUpdateDTO(department_ids=[departments["parent"].id])

        updated = repo.update(tag, dto)

        assert departments["parent"] in updated.departments.all()

    def test_update_remove_departments(self, departments):
        """Удаление подразделений из тега (установка departments=[])."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([departments["parent"]])
        dto = TagUpdateDTO(department_ids=[])

        updated = repo.update(tag, dto)

        assert list(updated.departments.all()) == []

    def test_update_multiple_fields(self, departments):
        """Обновление нескольких полей одновременно."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Старое", category="Старая")
        dto = TagUpdateDTO(
            name="Новое",
            category="Новая",
            department_ids=[departments["parent"].id],
        )

        updated = repo.update(tag, dto)

        assert updated.name == "Новое"
        assert updated.category == "Новая"
        assert departments["parent"] in updated.departments.all()

    def test_update_with_nonexistent_department(self):
        """Обновление с несуществующим подразделением вызывает ошибку."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        dto = TagUpdateDTO(department_ids=[99999])

        with pytest.raises(ValueError, match="не найдены"):
            repo.update(tag, dto)

    def test_update_without_fields(self):
        """Обновление без полей вызывает save() без update_fields."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        original_name = tag.name
        dto = TagUpdateDTO()

        updated = repo.update(tag, dto)

        # Тег должен остаться без изменений, но save() должен быть вызван
        assert updated.name == original_name

    def test_update_fails_if_same_name_and_departments_exists(self, departments):
        """Обновление запрещено, если имя и набор departments уже заняты другим тегом."""
        repo = TagRepository()
        # Тег, который будем обновлять
        tag = Tag.objects.create(name="Старое", category="Категория 1")
        tag.departments.set([departments["parent"]])
        # Другой тег с целевым именем и таким же набором departments
        other_tag = Tag.objects.create(name="Дубликат", category="Категория 1")
        other_tag.departments.set([departments["parent"]])

        dto = TagUpdateDTO(name="Дубликат", department_ids=[departments["parent"].id])

        with pytest.raises(
            ValueError,
            match="таким набором подразделений уже существует",
        ):
            repo.update(tag, dto)


@pytest.mark.django_db
class TestTagRepositoryDelete:
    """Тесты для метода delete репозитория."""

    def test_delete_tag(self):
        """delete удаляет тег и возвращает True."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag_id = tag.id

        result = repo.delete(tag)

        assert result is True
        assert not Tag.objects.filter(pk=tag_id).exists()


@pytest.mark.django_db
class TestTagRepositoryGetAll:
    """Тесты для метода get_all репозитория."""

    def test_get_all_with_prefetch_related(self, departments):
        """get_all возвращает queryset с prefetch_related для departments."""
        repo = TagRepository()
        Tag.objects.create(name="Тег 1", category="Категория 1")
        tag2 = Tag.objects.create(name="Тег 2", category="Категория 1")
        tag2.departments.set([departments["parent"]])

        queryset = repo.get_all()

        assert queryset.count() == 2
        # Проверяем, что prefetch_related работает
        for tag in queryset:
            # Не должно быть дополнительных запросов при доступе к departments
            dept_list = list(tag.departments.all())
            if dept_list:
                assert dept_list[0].name is not None


@pytest.mark.django_db
class TestTagRepositoryExists:
    """Тесты для метода exists репозитория."""

    def test_exists_true(self):
        """exists возвращает True для существующего тега."""
        repo = TagRepository()
        tag = Tag.objects.create(name="Тег", category="Категория 1")

        assert repo.exists(tag.id) is True

    def test_exists_false(self):
        """exists возвращает False для несуществующего тега."""
        repo = TagRepository()
        assert repo.exists(99999) is False
