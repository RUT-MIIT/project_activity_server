"""Unit-тесты для сервиса TagService.

Проверяем все методы работы с тегами: создание, обновление, удаление, получение списка.
"""

import pytest

from accounts.models import Department
from showcase.dto.tag import TagCreateDTO, TagUpdateDTO
from showcase.models import Tag
from showcase.services.tag_service import TagService


@pytest.mark.django_db
class TestTagServiceCreate:
    """Тесты для метода create_tag сервиса."""

    def test_cpds_can_create_general_tag(self, roles, make_user):
        """cpds может создавать общие теги."""
        user = make_user(role_code="cpds")
        service = TagService()
        dto = TagCreateDTO(name="Тег", category="Категория 1")

        tag = service.create_tag(dto, user)

        assert tag.id is not None
        assert tag.name == "Тег"
        assert list(tag.departments.all()) == []

    def test_cpds_cannot_create_department_tag(self, roles, make_user, departments):
        """cpds не может создавать теги с подразделением."""
        user = make_user(role_code="cpds")
        service = TagService()
        dto = TagCreateDTO(
            name="Тег",
            category="Категория 1",
            department_ids=[departments["parent"].id],
        )

        with pytest.raises(ValueError, match="общие теги"):
            service.create_tag(dto, user)

    def test_institute_validator_auto_sets_department(self, roles, make_user):
        """institute_validator всегда создает тег для своего подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        service = TagService()
        dto = TagCreateDTO(name="Тег", category="Категория 1")

        tag = service.create_tag(dto, user)

        assert user.department in tag.departments.all()

    def test_institute_validator_can_create_own_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator может создавать теги для своего подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        service = TagService()
        dto = TagCreateDTO(
            name="Тег",
            category="Категория 1",
            department_ids=[user.department.id],
        )

        tag = service.create_tag(dto, user)

        assert user.department in tag.departments.all()

    def test_institute_validator_cannot_create_other_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator не может создавать теги для чужого подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        other_dept = Department.objects.create(name="Other", short_name="O")
        service = TagService()
        dto = TagCreateDTO(
            name="Тег",
            category="Категория 1",
            department_ids=[other_dept.id],
        )

        with pytest.raises(ValueError, match="своего подразделения"):
            service.create_tag(dto, user)

    def test_admin_can_create_any_tag(self, roles, make_user, departments):
        """admin может создавать любые теги."""
        user = make_user(role_code="admin")
        service = TagService()
        dto_general = TagCreateDTO(name="Общий тег", category="Категория 1")
        dto_dept = TagCreateDTO(
            name="Тег подразделения",
            category="Категория 1",
            department_ids=[departments["parent"].id],
        )

        tag_general = service.create_tag(dto_general, user)
        tag_dept = service.create_tag(dto_dept, user)

        assert list(tag_general.departments.all()) == []
        assert departments["parent"] in tag_dept.departments.all()

    def test_cannot_create_tag_if_same_name_and_departments_exists(
        self, roles, make_user, departments
    ):
        """Нельзя создать тег с таким же именем и таким же набором подразделений."""
        user = make_user(role_code="admin")
        service = TagService()
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
            service.create_tag(dto, user)

    def test_other_role_cannot_create_tag(self, roles, make_user):
        """Остальные роли не могут создавать теги."""
        user = make_user(role_code="user")
        service = TagService()
        dto = TagCreateDTO(name="Тег", category="Категория 1")

        # Сообщение формируется доменом: "Недостаточно прав для создания тегов"
        with pytest.raises(ValueError, match="Недостаточно прав"):
            service.create_tag(dto, user)


@pytest.mark.django_db
class TestTagServiceUpdate:
    """Тесты для метода update_tag сервиса."""

    def test_cpds_can_update_general_tag(self, roles, make_user):
        """cpds может обновлять общие теги."""
        user = make_user(role_code="cpds")
        service = TagService()
        tag = Tag.objects.create(name="Старое", category="Категория 1")
        dto = TagUpdateDTO(name="Новое")

        updated = service.update_tag(tag.id, dto, user)

        assert updated.name == "Новое"

    def test_cpds_cannot_update_department_tag(self, roles, make_user, departments):
        """cpds не может обновлять теги с подразделением."""
        user = make_user(role_code="cpds")
        service = TagService()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([departments["parent"]])
        dto = TagUpdateDTO(name="Новое")

        with pytest.raises(ValueError, match="общие теги"):
            service.update_tag(tag.id, dto, user)

    def test_institute_validator_can_update_own_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator может обновлять теги своего подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        service = TagService()
        tag = Tag.objects.create(name="Старое", category="Категория 1")
        tag.departments.set([user.department])
        dto = TagUpdateDTO(name="Новое")

        updated = service.update_tag(tag.id, dto, user)

        assert updated.name == "Новое"

    def test_institute_validator_cannot_update_other_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator не может обновлять теги чужого подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        other_dept = Department.objects.create(name="Other", short_name="O")
        service = TagService()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([other_dept])
        dto = TagUpdateDTO(name="Новое")

        with pytest.raises(ValueError, match="своего подразделения"):
            service.update_tag(tag.id, dto, user)

    def test_admin_can_update_any_tag(self, roles, make_user, departments):
        """admin может обновлять любые теги."""
        user = make_user(role_code="admin")
        service = TagService()
        tag = Tag.objects.create(name="Старое", category="Категория 1")
        tag.departments.set([departments["parent"]])
        dto = TagUpdateDTO(name="Новое")

        updated = service.update_tag(tag.id, dto, user)

        assert updated.name == "Новое"

    def test_admin_cannot_update_if_same_name_and_departments_exists(
        self, roles, make_user, departments
    ):
        """Нельзя обновить тег, если имя и набор departments уже заняты другим тегом."""
        user = make_user(role_code="admin")
        service = TagService()
        tag = Tag.objects.create(name="Старое", category="Категория 1")
        tag.departments.set([departments["parent"]])
        other_tag = Tag.objects.create(name="Дубликат", category="Категория 1")
        other_tag.departments.set([departments["parent"]])

        dto = TagUpdateDTO(name="Дубликат", department_ids=[departments["parent"].id])

        with pytest.raises(
            ValueError,
            match="таким набором подразделений уже существует",
        ):
            service.update_tag(tag.id, dto, user)

    def test_update_nonexistent_tag(self, roles, make_user):
        """Обновление несуществующего тега вызывает ошибку."""
        user = make_user(role_code="admin")
        service = TagService()
        dto = TagUpdateDTO(name="Новое")

        with pytest.raises(ValueError, match="не найден"):
            service.update_tag(99999, dto, user)


@pytest.mark.django_db
class TestTagServiceDelete:
    """Тесты для метода delete_tag сервиса."""

    def test_cpds_can_delete_general_tag(self, roles, make_user):
        """cpds может удалять общие теги."""
        user = make_user(role_code="cpds")
        service = TagService()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag_id = tag.id

        result = service.delete_tag(tag_id, user)

        assert result is True
        assert not Tag.objects.filter(pk=tag_id).exists()

    def test_cpds_cannot_delete_department_tag(self, roles, make_user, departments):
        """cpds не может удалять теги с подразделением."""
        user = make_user(role_code="cpds")
        service = TagService()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([departments["parent"]])

        with pytest.raises(ValueError, match="общие теги"):
            service.delete_tag(tag.id, user)

    def test_institute_validator_can_delete_own_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator может удалять теги своего подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        service = TagService()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([user.department])
        tag_id = tag.id

        result = service.delete_tag(tag_id, user)

        assert result is True
        assert not Tag.objects.filter(pk=tag_id).exists()

    def test_admin_can_delete_any_tag(self, roles, make_user, departments):
        """admin может удалять любые теги."""
        user = make_user(role_code="admin")
        service = TagService()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([departments["parent"]])
        tag_id = tag.id

        result = service.delete_tag(tag_id, user)

        assert result is True
        assert not Tag.objects.filter(pk=tag_id).exists()

    def test_delete_nonexistent_tag(self, roles, make_user):
        """Удаление несуществующего тега вызывает ошибку."""
        user = make_user(role_code="admin")
        service = TagService()

        with pytest.raises(ValueError, match="не найден"):
            service.delete_tag(99999, user)


@pytest.mark.django_db
class TestTagServiceListTags:
    """Тесты для метода list_tags сервиса."""

    def test_list_tags_filters_by_role_cpds(self, roles, make_user, departments):
        """list_tags фильтрует теги для роли cpds."""
        user = make_user(role_code="cpds")
        service = TagService()
        general_tag = Tag.objects.create(name="Общий", category="Категория 1")
        dept_tag = Tag.objects.create(name="Подразделения", category="Категория 1")
        dept_tag.departments.set([departments["parent"]])

        queryset = service.list_tags(user)
        tag_ids = list(queryset.values_list("id", flat=True))

        assert general_tag.id in tag_ids
        assert dept_tag.id not in tag_ids

    def test_list_tags_filters_by_role_institute_validator(
        self, roles, make_user, departments
    ):
        """list_tags фильтрует теги для роли institute_validator."""
        user = make_user(role_code="institute_validator", with_department=True)
        service = TagService()
        general_tag = Tag.objects.create(name="Общий", category="Категория 1")
        own_dept_tag = Tag.objects.create(
            name="Моего подразделения", category="Категория 1"
        )
        own_dept_tag.departments.set([user.department])
        other_dept = Department.objects.create(name="Other", short_name="O")
        other_dept_tag = Tag.objects.create(
            name="Чужого подразделения", category="Категория 1"
        )
        other_dept_tag.departments.set([other_dept])

        queryset = service.list_tags(user)
        tag_ids = list(queryset.values_list("id", flat=True))

        assert general_tag.id in tag_ids
        assert own_dept_tag.id in tag_ids
        assert other_dept_tag.id not in tag_ids

    def test_list_tags_admin_sees_all(self, roles, make_user, departments):
        """list_tags для admin возвращает все теги."""
        user = make_user(role_code="admin")
        service = TagService()
        general_tag = Tag.objects.create(name="Общий", category="Категория 1")
        dept_tag = Tag.objects.create(name="Подразделения", category="Категория 1")
        dept_tag.departments.set([departments["parent"]])

        queryset = service.list_tags(user)
        tag_ids = list(queryset.values_list("id", flat=True))

        assert general_tag.id in tag_ids
        assert dept_tag.id in tag_ids


@pytest.mark.django_db
class TestTagServiceGetTag:
    """Тесты для метода get_tag сервиса."""

    def test_get_tag_with_access(self, roles, make_user):
        """get_tag возвращает тег, если есть доступ."""
        user = make_user(role_code="cpds")
        service = TagService()
        tag = Tag.objects.create(name="Тег", category="Категория 1")

        retrieved = service.get_tag(tag.id, user)

        assert retrieved.id == tag.id

    def test_get_tag_without_access(self, roles, make_user, departments):
        """get_tag вызывает ошибку, если нет доступа."""
        user = make_user(role_code="cpds")
        service = TagService()
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        tag.departments.set([departments["parent"]])

        with pytest.raises(ValueError, match="Нет доступа"):
            service.get_tag(tag.id, user)

    def test_get_nonexistent_tag(self, roles, make_user):
        """get_tag для несуществующего тега вызывает ошибку."""
        user = make_user(role_code="admin")
        service = TagService()

        with pytest.raises(ValueError, match="не найден"):
            service.get_tag(99999, user)
