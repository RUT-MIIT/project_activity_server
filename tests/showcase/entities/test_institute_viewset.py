"""Тесты для InstituteViewSet."""

import pytest
from rest_framework.test import APIClient

from showcase.models import Institute


@pytest.mark.django_db
class TestInstituteViewSet:
    """Проверяем выдачу списка институтов с полем department_id."""

    def test_list_institutes_contains_department_id(self, departments):
        """Эндпоинт возвращает department_id, если институт связан с подразделением."""
        client = APIClient()
        Institute.objects.create(
            code="INST-1",
            name="Институт тестовый",
            position=1,
            department=departments["parent"],
        )

        response = client.get("/api/showcase/institutes/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["department_id"] == departments["parent"].id

    def test_list_institutes_department_id_is_none_when_not_set(self):
        """Если подразделение не задано, department_id равно None."""
        client = APIClient()
        Institute.objects.create(
            code="INST-2",
            name="Институт без департамента",
            position=2,
        )

        response = client.get("/api/showcase/institutes/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["department_id"] is None
