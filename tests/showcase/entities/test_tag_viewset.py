"""Unit-тесты для TagViewSet API эндпоинта.

Проверяем получение списка тегов и конкретного тега по ID.
"""

import pytest
from rest_framework.test import APIClient

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
        """GET /api/tags/{id}/ для несуществующего тега возвращает 404."""
        client = APIClient()
        response = client.get("/api/showcase/tags/99999/")

        assert response.status_code == 404

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
