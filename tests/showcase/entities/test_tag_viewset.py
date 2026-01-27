"""Unit-тесты для TagViewSet API эндпоинта.

Проверяем получение списка тегов, конкретного тега по ID, и CRUD операции.
"""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department
from showcase.models import Tag


@pytest.mark.django_db
class TestTagViewSet:
    """Тесты для TagViewSet."""

    def test_list_tags_returns_all_tags(self):
        """GET /api/tags/ возвращает все теги без пагинации."""
        client = APIClient()
        # Создаём теги
        tag1 = Tag.objects.create(name="Тег 1", category="Категория 1")
        tag2 = Tag.objects.create(name="Тег 2", category="Категория 1")
        tag3 = Tag.objects.create(name="Тег 3", category="Категория 2")

        # Делаем запрос без авторизации (AllowAny)
        response = client.get("/api/showcase/tags/")

        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) == 3

        # Проверяем структуру данных
        tag_data = response.data[0]
        assert "id" in tag_data
        assert "name" in tag_data
        assert "category" in tag_data

        # Проверяем, что все теги присутствуют
        tag_names = [tag["name"] for tag in response.data]
        assert "Тег 1" in tag_names
        assert "Тег 2" in tag_names
        assert "Тег 3" in tag_names

    def test_list_tags_sorted_by_category_and_name(self):
        """Теги отсортированы по категории и названию."""
        client = APIClient()
        # Создаём теги в разном порядке
        tag_b = Tag.objects.create(name="B Тег", category="Категория 2")
        tag_a = Tag.objects.create(name="A Тег", category="Категория 1")
        tag_c = Tag.objects.create(name="C Тег", category="Категория 1")

        response = client.get("/api/showcase/tags/")

        assert response.status_code == 200
        # Должны быть отсортированы: сначала Категория 1 (A, C), потом Категория 2 (B)
        assert response.data[0]["name"] == "A Тег"
        assert response.data[1]["name"] == "C Тег"
        assert response.data[2]["name"] == "B Тег"

    def test_retrieve_tag_by_id(self):
        """GET /api/tags/{id}/ возвращает конкретный тег."""
        client = APIClient()
        tag = Tag.objects.create(name="Тест Тег", category="Тест Категория")

        response = client.get(f"/api/showcase/tags/{tag.id}/")

        assert response.status_code == 200
        assert response.data["id"] == tag.id
        assert response.data["name"] == "Тест Тег"
        assert response.data["category"] == "Тест Категория"

    def test_retrieve_nonexistent_tag_returns_404(self):
        """GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level)."""
        client = APIClient()
        response = client.get("/api/showcase/tags/99999/")

        # Теперь retrieve использует сервис и обрабатывает через ValueError -> 403
        assert response.status_code == 403

    def test_list_tags_no_pagination(self):
        """Список тегов возвращается без пагинации (все теги сразу)."""
        client = APIClient()
        # Создаём несколько тегов
        for i in range(15):
            Tag.objects.create(name=f"Тег {i}", category=f"Категория {i % 3}")

        response = client.get("/api/showcase/tags/")

        assert response.status_code == 200
        # Должен быть список, а не объект с пагинацией
        assert isinstance(response.data, list)
        assert len(response.data) == 15

    def test_list_tags_accessible_without_auth(self):
        """Эндпоинт доступен без авторизации (AllowAny)."""
        client = APIClient()
        Tag.objects.create(name="Публичный тег", category="Публичная категория")

        # Делаем запрос без токена авторизации
        response = client.get("/api/showcase/tags/")

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_list_tags_filters_by_role_cpds(self, roles, make_user, departments):
        """Список тегов фильтруется для роли cpds (только общие теги)."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)

        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept_tag = Tag.objects.create(
            name="Тег подразделения",
            category="Категория 1",
            department=departments["parent"],
        )

        response = client.get("/api/showcase/tags/")

        assert response.status_code == 200
        tag_ids = [tag["id"] for tag in response.data]
        assert general_tag.id in tag_ids
        assert dept_tag.id not in tag_ids

    def test_list_tags_filters_by_role_institute_validator(
        self, roles, make_user, departments
    ):
        """Список тегов фильтруется для роли institute_validator (общие + своего подразделения)."""
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        own_dept_tag = Tag.objects.create(
            name="Тег моего подразделения",
            category="Категория 1",
            department=user.department,
        )
        other_dept = Department.objects.create(name="Other", short_name="O")
        other_dept_tag = Tag.objects.create(
            name="Тег чужого подразделения",
            category="Категория 1",
            department=other_dept,
        )

        response = client.get("/api/showcase/tags/")

        assert response.status_code == 200
        tag_ids = [tag["id"] for tag in response.data]
        assert general_tag.id in tag_ids
        assert own_dept_tag.id in tag_ids
        assert other_dept_tag.id not in tag_ids

    def test_list_tags_admin_sees_all(self, roles, make_user, departments):
        """Admin видит все теги."""
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        general_tag = Tag.objects.create(name="Общий тег", category="Категория 1")
        dept_tag = Tag.objects.create(
            name="Тег подразделения",
            category="Категория 1",
            department=departments["parent"],
        )

        response = client.get("/api/showcase/tags/")

        assert response.status_code == 200
        tag_ids = [tag["id"] for tag in response.data]
        assert general_tag.id in tag_ids
        assert dept_tag.id in tag_ids


@pytest.mark.django_db
class TestTagViewSetCreate:
    """Тесты для создания тегов через API."""

    def test_cpds_can_create_general_tag(self, roles, make_user):
        """cpds может создавать общие теги."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)

        data = {"name": "Новый тег", "category": "Категория 1"}
        response = client.post("/api/showcase/tags/", data, format="json")

        assert response.status_code == 201
        assert response.data["name"] == "Новый тег"
        assert response.data["department"] is None

    def test_cpds_cannot_create_department_tag(self, roles, make_user, departments):
        """cpds не может создавать теги с подразделением."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            "name": "Тег",
            "category": "Категория 1",
            "department_id": departments["parent"].id,
        }
        response = client.post("/api/showcase/tags/", data, format="json")

        assert response.status_code == 400
        assert "общие теги" in response.data["error"].lower()

    def test_institute_validator_auto_sets_department(self, roles, make_user):
        """institute_validator автоматически устанавливает свое подразделение."""
        user = make_user(role_code="institute_validator", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        data = {"name": "Тег", "category": "Категория 1"}
        response = client.post("/api/showcase/tags/", data, format="json")

        assert response.status_code == 201
        assert response.data["department"]["id"] == user.department.id

    def test_admin_can_create_any_tag(self, roles, make_user, departments):
        """admin может создавать любые теги."""
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            "name": "Тег подразделения",
            "category": "Категория 1",
            "department_id": departments["parent"].id,
        }
        response = client.post("/api/showcase/tags/", data, format="json")

        assert response.status_code == 201
        assert response.data["department"]["id"] == departments["parent"].id

    def test_other_role_cannot_create_tag(self, roles, make_user):
        """Остальные роли не могут создавать теги."""
        user = make_user(role_code="user")
        client = APIClient()
        client.force_authenticate(user=user)

        data = {"name": "Тег", "category": "Категория 1"}
        response = client.post("/api/showcase/tags/", data, format="json")

        assert response.status_code == 403

    def test_cannot_create_department_tag_if_general_exists(
        self, roles, make_user, departments
    ):
        """Нельзя создать тег для подразделения, если уже есть общий тег с таким именем."""
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        Tag.objects.create(
            name="Дубликат",
            category="Категория 1",
            department=None,
        )

        data = {
            "name": "Дубликат",
            "category": "Категория 1",
            "department_id": departments["parent"].id,
        }
        response = client.post("/api/showcase/tags/", data, format="json")

        assert response.status_code == 400
        assert "уже существует общий тег с таким названием" in response.data["error"]

    def test_cannot_create_general_tag_if_used_anywhere(
        self, roles, make_user, departments
    ):
        """Нельзя создать общий тег, если имя уже используется (общим или departmental тегом)."""
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)

        Tag.objects.create(
            name="Дубликат",
            category="Категория 1",
            department=departments["parent"],
        )

        data = {"name": "Дубликат", "category": "Категория 1"}
        response = client.post("/api/showcase/tags/", data, format="json")

        assert response.status_code == 400
        assert "существует (общий или для подразделения)" in response.data["error"]


@pytest.mark.django_db
class TestTagViewSetUpdate:
    """Тесты для обновления тегов через API."""

    def test_cpds_can_update_general_tag(self, roles, make_user):
        """cpds может обновлять общие теги."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(name="Старое", category="Категория 1")

        data = {"name": "Новое"}
        response = client.patch(f"/api/showcase/tags/{tag.id}/", data, format="json")

        assert response.status_code == 200
        assert response.data["name"] == "Новое"

    def test_cpds_cannot_update_department_tag(self, roles, make_user, departments):
        """cpds не может обновлять теги с подразделением."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(
            name="Тег",
            category="Категория 1",
            department=departments["parent"],
        )

        data = {"name": "Новое"}
        response = client.patch(f"/api/showcase/tags/{tag.id}/", data, format="json")

        assert response.status_code == 400
        assert "общие теги" in response.data["error"].lower()

    def test_admin_can_update_any_tag(self, roles, make_user, departments):
        """admin может обновлять любые теги."""
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(
            name="Старое",
            category="Категория 1",
            department=departments["parent"],
        )

        data = {"name": "Новое"}
        response = client.patch(f"/api/showcase/tags/{tag.id}/", data, format="json")

        assert response.status_code == 200
        assert response.data["name"] == "Новое"


@pytest.mark.django_db
class TestTagViewSetDelete:
    """Тесты для удаления тегов через API."""

    def test_cpds_can_delete_general_tag(self, roles, make_user):
        """cpds может удалять общие теги."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(name="Тег", category="Категория 1")

        response = client.delete(f"/api/showcase/tags/{tag.id}/")

        assert response.status_code == 204
        assert not Tag.objects.filter(pk=tag.id).exists()

    def test_cpds_cannot_delete_department_tag(self, roles, make_user, departments):
        """cpds не может удалять теги с подразделением."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(
            name="Тег",
            category="Категория 1",
            department=departments["parent"],
        )

        response = client.delete(f"/api/showcase/tags/{tag.id}/")

        assert response.status_code == 400
        assert "общие теги" in response.data["error"].lower()

    def test_admin_can_delete_any_tag(self, roles, make_user, departments):
        """admin может удалять любые теги."""
        user = make_user(role_code="admin")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(
            name="Тег",
            category="Категория 1",
            department=departments["parent"],
        )

        response = client.delete(f"/api/showcase/tags/{tag.id}/")

        assert response.status_code == 204
        assert not Tag.objects.filter(pk=tag.id).exists()

    def test_other_role_cannot_delete_tag(self, roles, make_user):
        """Остальные роли не могут удалять теги."""
        user = make_user(role_code="user")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(name="Тег", category="Категория 1")

        response = client.delete(f"/api/showcase/tags/{tag.id}/")

        assert response.status_code == 403


@pytest.mark.django_db
class TestTagViewSetRetrieve:
    """Тесты для получения конкретного тега через API."""

    def test_retrieve_with_access(self, roles, make_user):
        """Получение тега с доступом возвращает тег."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(name="Тег", category="Категория 1")

        response = client.get(f"/api/showcase/tags/{tag.id}/")

        assert response.status_code == 200
        assert response.data["id"] == tag.id

    def test_retrieve_without_access(self, roles, make_user, departments):
        """Получение тега без доступа возвращает 403."""
        user = make_user(role_code="cpds")
        client = APIClient()
        client.force_authenticate(user=user)
        tag = Tag.objects.create(
            name="Тег",
            category="Категория 1",
            department=departments["parent"],
        )

        response = client.get(f"/api/showcase/tags/{tag.id}/")

        assert response.status_code == 403
