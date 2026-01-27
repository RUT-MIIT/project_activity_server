"""Unit-тесты для доменной логики TagDomain.

Проверяем все чистые функции бизнес-логики: фильтрацию по ролям, проверку прав доступа.
"""

import pytest

from accounts.models import Department, User
from showcase.domain.tag import TagDomain
from showcase.models import Tag


@pytest.mark.django_db
class TestGetFilteredQueryset:
    """Тесты для фильтрации queryset тегов по ролям."""

    def test_cpds_sees_only_general_tags(self, roles, make_user):
        """cpds видит только общие теги (без departments)."""
        user = make_user(role_code="cpds")
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept = Department.objects.create(name="Dept", short_name="D")
        department_tag = Tag.objects.create(
            name="Тег подразделения", category="Категория 1"
        )
        department_tag.departments.set([dept])

        queryset = Tag.objects.all()
        filtered = TagDomain.get_filtered_queryset(user, queryset)

        assert general_tag in filtered
        assert department_tag not in filtered

    def test_institute_validator_sees_general_and_own_department_tags(
        self, roles, make_user, departments
    ):
        """institute_validator видит общие теги + теги своего подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        own_dept_tag = Tag.objects.create(
            name="Тег моего подразделения",
            category="Категория 1",
        )
        own_dept_tag.departments.set([user.department])
        other_dept = Department.objects.create(name="Other Dept", short_name="OD")
        other_dept_tag = Tag.objects.create(
            name="Тег другого подразделения",
            category="Категория 1",
        )
        other_dept_tag.departments.set([other_dept])

        queryset = Tag.objects.all()
        filtered = TagDomain.get_filtered_queryset(user, queryset)

        assert general_tag in filtered
        assert own_dept_tag in filtered
        assert other_dept_tag not in filtered

    def test_institute_validator_without_department_sees_only_general(
        self, roles, make_user
    ):
        """institute_validator без подразделения видит только общие теги."""
        user = make_user(role_code="institute_validator", with_department=False)
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept = Department.objects.create(name="Dept", short_name="D")
        department_tag = Tag.objects.create(
            name="Тег подразделения", category="Категория 1"
        )
        department_tag.departments.set([dept])

        queryset = Tag.objects.all()
        filtered = TagDomain.get_filtered_queryset(user, queryset)

        assert general_tag in filtered
        assert department_tag not in filtered

    def test_admin_sees_all_tags(self, roles, make_user, departments):
        """admin видит все теги."""
        user = make_user(role_code="admin")
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept = Department.objects.create(name="Dept", short_name="D")
        department_tag = Tag.objects.create(
            name="Тег подразделения", category="Категория 1"
        )
        department_tag.departments.set([dept])

        queryset = Tag.objects.all()
        filtered = TagDomain.get_filtered_queryset(user, queryset)

        assert general_tag in filtered
        assert department_tag in filtered
        assert filtered.count() == 2

    def test_other_role_sees_general_and_root_department_tags(
        self, roles, make_user, departments
    ):
        """Остальные роли видят общие теги + теги с корневым подразделением."""
        user = make_user(role_code="user", with_department=True)
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        root_dept_tag = Tag.objects.create(
            name="Тег корневого подразделения",
            category="Категория 1",
        )
        root_dept_tag.departments.set([departments["parent"]])  # Корневое подразделение
        child_dept_tag = Tag.objects.create(
            name="Тег дочернего подразделения",
            category="Категория 1",
        )
        child_dept_tag.departments.set([user.department])  # Дочернее подразделение

        queryset = Tag.objects.all()
        filtered = TagDomain.get_filtered_queryset(user, queryset)

        assert general_tag in filtered
        assert root_dept_tag in filtered
        assert child_dept_tag not in filtered

    def test_other_role_without_department_sees_only_general(self, roles, make_user):
        """Остальные роли без подразделения видят только общие теги."""
        user = make_user(role_code="user", with_department=False)
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept = Department.objects.create(name="Dept", short_name="D")
        department_tag = Tag.objects.create(
            name="Тег подразделения", category="Категория 1"
        )
        department_tag.departments.set([dept])

        queryset = Tag.objects.all()
        filtered = TagDomain.get_filtered_queryset(user, queryset)

        assert general_tag in filtered
        assert department_tag not in filtered

    def test_unauthenticated_user_sees_only_general(self):
        """Неавторизованный пользователь видит только общие теги."""
        user = None
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept = Department.objects.create(name="Dept", short_name="D")
        department_tag = Tag.objects.create(
            name="Тег подразделения", category="Категория 1"
        )
        department_tag.departments.set([dept])

        queryset = Tag.objects.all()
        filtered = TagDomain.get_filtered_queryset(user, queryset)

        assert general_tag in filtered
        assert department_tag not in filtered


@pytest.mark.django_db
class TestCanCreateTag:
    """Тесты для проверки прав на создание тегов."""

    def test_cpds_can_create_general_tag(self, roles, make_user):
        """cpds может создавать только общие теги."""
        user = make_user(role_code="cpds")
        can_create, message = TagDomain.can_create_tag(user, department_ids=None)
        assert can_create is True

    def test_cpds_cannot_create_department_tag(self, roles, make_user, departments):
        """cpds не может создавать теги с подразделением."""
        user = make_user(role_code="cpds")
        can_create, message = TagDomain.can_create_tag(
            user, department_ids=[departments["parent"].id]
        )
        assert can_create is False
        assert "общие теги" in message.lower()

    def test_institute_validator_can_create_general_tag(self, roles, make_user):
        """institute_validator может создавать общие теги."""
        user = make_user(role_code="institute_validator", with_department=True)
        can_create, message = TagDomain.can_create_tag(user, department_ids=None)
        assert can_create is True

    def test_institute_validator_can_create_own_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator может создавать теги для своего подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        can_create, message = TagDomain.can_create_tag(
            user, department_ids=[user.department.id]
        )
        assert can_create is True

    def test_institute_validator_cannot_create_other_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator не может создавать теги для чужого подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        other_dept = Department.objects.create(name="Other", short_name="O")
        can_create, message = TagDomain.can_create_tag(
            user, department_ids=[other_dept.id]
        )
        assert can_create is False
        assert "своего подразделения" in message.lower()

    def test_admin_can_create_any_tag(self, roles, make_user, departments):
        """admin может создавать любые теги."""
        user = make_user(role_code="admin")
        can_create_general, _ = TagDomain.can_create_tag(user, department_ids=None)
        can_create_dept, _ = TagDomain.can_create_tag(
            user, department_ids=[departments["parent"].id]
        )
        assert can_create_general is True
        assert can_create_dept is True

    def test_other_role_cannot_create_tag(self, roles, make_user):
        """Остальные роли не могут создавать теги."""
        user = make_user(role_code="user")
        can_create, message = TagDomain.can_create_tag(user, department_ids=None)
        assert can_create is False
        assert "недостаточно прав" in message.lower()

    def test_unauthenticated_cannot_create_tag(self):
        """Неавторизованный пользователь не может создавать теги."""
        user = None
        can_create, message = TagDomain.can_create_tag(user, department_ids=None)
        assert can_create is False
        assert "авторизация" in message.lower()


@pytest.mark.django_db
class TestCanUpdateTag:
    """Тесты для проверки прав на обновление тегов."""

    def test_cpds_can_update_general_tag(self, roles, make_user):
        """cpds может обновлять общие теги."""
        user = make_user(role_code="cpds")
        tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        can_update, message = TagDomain.can_update_tag(user, tag)
        assert can_update is True

    def test_cpds_cannot_update_department_tag(self, roles, make_user, departments):
        """cpds не может обновлять теги с подразделением."""
        user = make_user(role_code="cpds")
        tag = Tag.objects.create(name="Тег подразделения", category="Категория 1")
        tag.departments.set([departments["parent"]])
        can_update, message = TagDomain.can_update_tag(user, tag)
        assert can_update is False
        assert "общие теги" in message.lower()

    def test_institute_validator_can_update_general_tag(self, roles, make_user):
        """institute_validator может обновлять общие теги."""
        user = make_user(role_code="institute_validator", with_department=True)
        tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        can_update, message = TagDomain.can_update_tag(user, tag)
        assert can_update is True

    def test_institute_validator_can_update_own_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator может обновлять теги своего подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        tag = Tag.objects.create(
            name="Тег моего подразделения",
            category="Категория 1",
        )
        tag.departments.set([user.department])
        can_update, message = TagDomain.can_update_tag(user, tag)
        assert can_update is True

    def test_institute_validator_cannot_update_other_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator не может обновлять теги чужого подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        other_dept = Department.objects.create(name="Other", short_name="O")
        tag = Tag.objects.create(
            name="Тег чужого подразделения",
            category="Категория 1",
        )
        tag.departments.set([other_dept])
        can_update, message = TagDomain.can_update_tag(user, tag)
        assert can_update is False
        assert "своего подразделения" in message.lower()

    def test_admin_can_update_any_tag(self, roles, make_user, departments):
        """admin может обновлять любые теги."""
        user = make_user(role_code="admin")
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept_tag = Tag.objects.create(name="Тег подразделения", category="Категория 1")
        dept_tag.departments.set([departments["parent"]])
        can_update_general, _ = TagDomain.can_update_tag(user, general_tag)
        can_update_dept, _ = TagDomain.can_update_tag(user, dept_tag)
        assert can_update_general is True
        assert can_update_dept is True

    def test_other_role_cannot_update_tag(self, roles, make_user):
        """Остальные роли не могут обновлять теги."""
        user = make_user(role_code="user")
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        can_update, message = TagDomain.can_update_tag(user, tag)
        assert can_update is False
        assert "недостаточно прав" in message.lower()


@pytest.mark.django_db
class TestCanDeleteTag:
    """Тесты для проверки прав на удаление тегов."""

    def test_cpds_can_delete_general_tag(self, roles, make_user):
        """cpds может удалять общие теги."""
        user = make_user(role_code="cpds")
        tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        can_delete, message = TagDomain.can_delete_tag(user, tag)
        assert can_delete is True

    def test_cpds_cannot_delete_department_tag(self, roles, make_user, departments):
        """cpds не может удалять теги с подразделением."""
        user = make_user(role_code="cpds")
        tag = Tag.objects.create(name="Тег подразделения", category="Категория 1")
        tag.departments.set([departments["parent"]])
        can_delete, message = TagDomain.can_delete_tag(user, tag)
        assert can_delete is False
        assert "общие теги" in message.lower()

    def test_institute_validator_can_delete_general_tag(self, roles, make_user):
        """institute_validator может удалять общие теги."""
        user = make_user(role_code="institute_validator", with_department=True)
        tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        can_delete, message = TagDomain.can_delete_tag(user, tag)
        assert can_delete is True

    def test_institute_validator_can_delete_own_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator может удалять теги своего подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        tag = Tag.objects.create(
            name="Тег моего подразделения",
            category="Категория 1",
        )
        tag.departments.set([user.department])
        can_delete, message = TagDomain.can_delete_tag(user, tag)
        assert can_delete is True

    def test_institute_validator_cannot_delete_other_department_tag(
        self, roles, make_user, departments
    ):
        """institute_validator не может удалять теги чужого подразделения."""
        user = make_user(role_code="institute_validator", with_department=True)
        other_dept = Department.objects.create(name="Other", short_name="O")
        tag = Tag.objects.create(
            name="Тег чужого подразделения",
            category="Категория 1",
        )
        tag.departments.set([other_dept])
        can_delete, message = TagDomain.can_delete_tag(user, tag)
        assert can_delete is False
        assert "своего подразделения" in message.lower()

    def test_admin_can_delete_any_tag(self, roles, make_user, departments):
        """admin может удалять любые теги."""
        user = make_user(role_code="admin")
        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept_tag = Tag.objects.create(name="Тег подразделения", category="Категория 1")
        dept_tag.departments.set([departments["parent"]])
        can_delete_general, _ = TagDomain.can_delete_tag(user, general_tag)
        can_delete_dept, _ = TagDomain.can_delete_tag(user, dept_tag)
        assert can_delete_general is True
        assert can_delete_dept is True

    def test_other_role_cannot_delete_tag(self, roles, make_user):
        """Остальные роли не могут удалять теги."""
        user = make_user(role_code="user")
        tag = Tag.objects.create(name="Тег", category="Категория 1")
        can_delete, message = TagDomain.can_delete_tag(user, tag)
        assert can_delete is False
        assert "недостаточно прав" in message.lower()
