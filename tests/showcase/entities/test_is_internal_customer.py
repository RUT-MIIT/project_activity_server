"""Тесты для проверки поля is_internal_customer при создании заявки."""

import pytest
from rest_framework.test import APIClient

from showcase.models import ProjectApplication


@pytest.mark.django_db
class TestProjectApplicationViewSetIsInternalCustomer:
    """Тесты для проверки поля is_internal_customer при создании заявки."""

    def test_create_with_is_internal_customer_true(self, statuses, make_user):
        """POST /api/showcase/project-applications/ создает заявку с is_internal_customer=True."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            "company": "Внутренняя Компания",
            "title": "Внутренний проект",
            "author_lastname": "Петров",
            "author_firstname": "Петр",
            "author_email": "petrov@example.com",
            "author_phone": "+79991111111",
            "goal": "Длинная цель проекта, больше 50 символов для консультации",
            "problem_holder": "Носитель проблемы",
            "barrier": "Длинное описание барьера",
            "project_level": "L1",
            "is_internal_customer": True,
        }

        response = client.post(
            "/api/showcase/project-applications/", data, format="json"
        )

        assert response.status_code == 201
        assert response.data["is_internal_customer"] is True

        # Проверяем в БД
        app_id = response.data["id"]
        app = ProjectApplication.objects.get(pk=app_id)
        assert app.is_internal_customer is True

    def test_create_with_is_internal_customer_false(self, statuses, make_user):
        """POST /api/showcase/project-applications/ создает заявку с is_internal_customer=False."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            "company": "Внешняя Компания",
            "title": "Внешний проект",
            "author_lastname": "Сидоров",
            "author_firstname": "Сидор",
            "author_email": "sidorov@example.com",
            "author_phone": "+79992222222",
            "goal": "Длинная цель проекта, больше 50 символов для консультации",
            "problem_holder": "Носитель проблемы",
            "barrier": "Длинное описание барьера",
            "project_level": "L1",
            "is_internal_customer": False,
        }

        response = client.post(
            "/api/showcase/project-applications/", data, format="json"
        )

        assert response.status_code == 201
        assert response.data["is_internal_customer"] is False

        # Проверяем в БД
        app_id = response.data["id"]
        app = ProjectApplication.objects.get(pk=app_id)
        assert app.is_internal_customer is False

    def test_create_without_is_internal_customer_defaults_to_false(
        self, statuses, make_user
    ):
        """POST /api/showcase/project-applications/ по умолчанию устанавливает is_internal_customer=False."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            "company": "Компания без указания типа",
            "title": "Проект без типа заказчика",
            "author_lastname": "Иванов",
            "author_firstname": "Иван",
            "author_email": "ivanov@example.com",
            "author_phone": "+79993333333",
            "goal": "Длинная цель проекта, больше 50 символов для консультации",
            "problem_holder": "Носитель проблемы",
            "barrier": "Длинное описание барьера",
            "project_level": "L1",
        }

        response = client.post(
            "/api/showcase/project-applications/", data, format="json"
        )

        assert response.status_code == 201
        assert response.data["is_internal_customer"] is False

        # Проверяем в БД
        app_id = response.data["id"]
        app = ProjectApplication.objects.get(pk=app_id)
        assert app.is_internal_customer is False

    def test_update_is_internal_customer(self, statuses, make_user):
        """PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer."""
        # Используем пользователя с ролью cpds, который может редактировать заявки
        # в любом статусе (кроме rejected)
        cpds_user = make_user(role_code="cpds", with_department=True)
        client = APIClient()
        client.force_authenticate(user=cpds_user)

        # Создаем заявку с is_internal_customer=False
        # Используем отдельного пользователя как автора заявки
        author_user = make_user(role_code="user", with_department=True)
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()
        dto = ProjectApplicationCreateDTO(
            company="Тестовая Компания",
            title="Тестовый проект",
            author_lastname="Тестов",
            author_firstname="Тест",
            author_email="test@example.com",
            author_phone="+79994444444",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель проблемы",
            barrier="Длинное описание барьера",
            is_internal_customer=False,
        )
        application = service.submit_application(dto, author_user)

        # Обновляем на True через пользователя cpds
        update_data = {"is_internal_customer": True}
        response = client.patch(
            f"/api/showcase/project-applications/{application.id}/",
            update_data,
            format="json",
        )

        assert response.status_code == 200
        assert response.data["is_internal_customer"] is True

        # Проверяем в БД
        app = ProjectApplication.objects.get(pk=application.id)
        assert app.is_internal_customer is True

    def test_update_is_internal_customer_by_author_on_returned_status(
        self, statuses, make_user
    ):
        """PATCH /api/showcase/project-applications/{id}/ автор может обновить is_internal_customer в статусе returned_department."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        # Создаем заявку с is_internal_customer=False
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()
        dto = ProjectApplicationCreateDTO(
            company="Тестовая Компания",
            title="Тестовый проект",
            author_lastname="Тестов",
            author_firstname="Тест",
            author_email="test@example.com",
            author_phone="+79994444444",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель проблемы",
            barrier="Длинное описание барьера",
            is_internal_customer=False,
        )
        application = service.submit_application(dto, user)

        # Устанавливаем статус returned_department, где автор может редактировать свою заявку
        returned_status = statuses["returned_department"]
        application.status = returned_status
        application.save()

        # Теперь автор может редактировать заявку в статусе returned_department
        update_data = {"is_internal_customer": True}
        response = client.patch(
            f"/api/showcase/project-applications/{application.id}/",
            update_data,
            format="json",
        )

        assert response.status_code == 200
        assert response.data["is_internal_customer"] is True

        # Проверяем в БД
        app = ProjectApplication.objects.get(pk=application.id)
        assert app.is_internal_customer is True
        assert app.status.code == "returned_department"

    def test_update_without_is_internal_customer_preserves_old_value(
        self, statuses, make_user
    ):
        """PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer сохраняет старое значение."""
        cpds_user = make_user(role_code="cpds", with_department=True)
        client = APIClient()
        client.force_authenticate(user=cpds_user)

        # Создаем заявку с is_internal_customer=True
        author_user = make_user(role_code="user", with_department=True)
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()
        dto = ProjectApplicationCreateDTO(
            company="Тестовая Компания",
            title="Тестовый проект",
            author_lastname="Тестов",
            author_firstname="Тест",
            author_email="test@example.com",
            author_phone="+79994444444",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель проблемы",
            barrier="Длинное описание барьера",
            is_internal_customer=True,  # Устанавливаем True
        )
        application = service.submit_application(dto, author_user)

        # Проверяем, что значение установлено
        assert application.is_internal_customer is True

        # Обновляем другие поля БЕЗ передачи is_internal_customer
        update_data = {
            "title": "Обновленное название",
            "company": "Обновленная компания",
            # is_internal_customer НЕ передаем
        }
        response = client.patch(
            f"/api/showcase/project-applications/{application.id}/",
            update_data,
            format="json",
        )

        assert response.status_code == 200
        # Старое значение is_internal_customer должно сохраниться
        assert response.data["is_internal_customer"] is True
        assert response.data["title"] == "Обновленное название"
        assert response.data["company"] == "Обновленная компания"

        # Проверяем в БД
        app = ProjectApplication.objects.get(pk=application.id)
        assert app.is_internal_customer is True  # Старое значение сохранилось
        assert app.title == "Обновленное название"
        assert app.company == "Обновленная компания"

    def test_update_without_is_internal_customer_preserves_false_value(
        self, statuses, make_user
    ):
        """PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer сохраняет False."""
        cpds_user = make_user(role_code="cpds", with_department=True)
        client = APIClient()
        client.force_authenticate(user=cpds_user)

        # Создаем заявку с is_internal_customer=False
        author_user = make_user(role_code="user", with_department=True)
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()
        dto = ProjectApplicationCreateDTO(
            company="Тестовая Компания",
            title="Тестовый проект",
            author_lastname="Тестов",
            author_firstname="Тест",
            author_email="test@example.com",
            author_phone="+79994444444",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель проблемы",
            barrier="Длинное описание барьера",
            is_internal_customer=False,  # Устанавливаем False
        )
        application = service.submit_application(dto, author_user)

        # Проверяем, что значение установлено
        assert application.is_internal_customer is False

        # Обновляем другие поля БЕЗ передачи is_internal_customer
        update_data = {
            "title": "Обновленное название",
            # is_internal_customer НЕ передаем
        }
        response = client.patch(
            f"/api/showcase/project-applications/{application.id}/",
            update_data,
            format="json",
        )

        assert response.status_code == 200
        # Старое значение is_internal_customer=False должно сохраниться
        assert response.data["is_internal_customer"] is False
        assert response.data["title"] == "Обновленное название"

        # Проверяем в БД
        app = ProjectApplication.objects.get(pk=application.id)
        assert app.is_internal_customer is False  # Старое значение сохранилось
        assert app.title == "Обновленное название"
