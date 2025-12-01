"""Тесты для ProjectApplicationViewSet - проверка API endpoints."""

from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

from showcase.models import ProjectApplication

User = get_user_model()


@pytest.mark.django_db
class TestProjectApplicationViewSetSimple:
    """Тесты для упрощенного создания заявок (simple endpoint)."""

    def test_simple_create_sets_is_external_true(self, statuses):
        """POST /api/showcase/project-applications/simple/ устанавливает is_external=True и статус await_cpds."""
        client = APIClient()
        data = {
            "company": "Test Company",
            "title": "Test Project",
            "author_lastname": "Иванов",
            "author_firstname": "Иван",
            "author_email": "test@example.com",
            "author_phone": "+79990000000",
            "goal": "Длинная цель проекта, больше 50 символов для консультации",
            "problem_holder": "Носитель проблемы",
            "barrier": "Длинное описание барьера",
            "project_level": "L1",
        }

        response = client.post(
            "/api/showcase/project-applications/simple/", data, format="json"
        )

        assert response.status_code == 201
        assert response.data["is_external"] is True
        assert response.data["status"]["code"] == "await_cpds"

        # Проверяем в БД
        app_id = response.data["id"]
        app = ProjectApplication.objects.get(pk=app_id)
        assert app.is_external is True
        assert app.status.code == "await_cpds"

    def test_simple_create_returns_is_external_in_response(self, statuses):
        """POST /api/showcase/project-applications/simple/ возвращает is_external в ответе."""
        client = APIClient()
        data = {
            "company": "Test Company",
            "title": "Test Project",
            "author_lastname": "Иванов",
            "author_firstname": "Иван",
            "author_email": "test@example.com",
            "author_phone": "+79990000000",
            "goal": "Длинная цель проекта, больше 50 символов для консультации",
            "problem_holder": "Носитель проблемы",
            "barrier": "Длинное описание барьера",
            "project_level": "L1",
        }

        response = client.post(
            "/api/showcase/project-applications/simple/", data, format="json"
        )

        assert response.status_code == 201
        assert "is_external" in response.data
        assert response.data["is_external"] is True
        assert response.data["status"]["code"] == "await_cpds"

    def test_simple_create_adds_cpds_department(self, statuses):
        """POST /api/showcase/project-applications/simple/ добавляет причастное подразделение ЦПДС."""
        from accounts.models import Department

        # Создаем подразделение ЦПДС если его нет
        cpds_department, _ = Department.objects.get_or_create(
            short_name="ЦПДС", defaults={"name": "Центр проектного развития"}
        )

        client = APIClient()
        data = {
            "company": "Test Company",
            "title": "Test Project",
            "author_lastname": "Иванов",
            "author_firstname": "Иван",
            "author_email": "test@example.com",
            "author_phone": "+79990000000",
            "goal": "Длинная цель проекта, больше 50 символов для консультации",
            "problem_holder": "Носитель проблемы",
            "barrier": "Длинное описание барьера",
            "project_level": "L1",
        }

        response = client.post(
            "/api/showcase/project-applications/simple/", data, format="json"
        )

        assert response.status_code == 201

        # Проверяем в БД, что подразделение ЦПДС добавлено как причастное
        app_id = response.data["id"]
        app = ProjectApplication.objects.get(pk=app_id)

        from showcase.models import ApplicationInvolvedDepartment

        assert ApplicationInvolvedDepartment.objects.filter(
            application=app, department=cpds_department
        ).exists()


@pytest.mark.django_db
class TestProjectApplicationViewSetExternal:
    """Тесты для получения списка внешних заявок (external endpoint)."""

    def test_external_list_requires_authentication(self, statuses):
        """GET /api/showcase/project-applications/external/ требует авторизации."""
        client = APIClient()

        response = client.get("/api/showcase/project-applications/external/")

        assert response.status_code == 401  # Unauthorized

    def test_external_list_returns_only_external_applications(
        self, statuses, make_user
    ):
        """GET /api/showcase/project-applications/external/ возвращает только внешние заявки."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        # Создаём внешнюю заявку через репозиторий
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()

        dto_external = ProjectApplicationCreateDTO(
            company="External Corp",
            title="External Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="external@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app_external = service.submit_application(dto_external, user, is_external=True)

        # Создаём обычную заявку
        dto_internal = ProjectApplicationCreateDTO(
            company="Internal Corp",
            title="Internal Project",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="internal@example.com",
            author_phone="+79990000001",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app_internal = service.submit_application(dto_internal, user, is_external=False)

        # Получаем список внешних заявок
        response = client.get("/api/showcase/project-applications/external/")

        assert response.status_code == 200
        assert isinstance(
            response.data, (list, dict)
        )  # Может быть список или пагинированный ответ

        # Если пагинация включена, данные в response.data["results"]
        if isinstance(response.data, dict) and "results" in response.data:
            results = response.data["results"]
        else:
            results = response.data

        external_ids = {item["id"] for item in results}
        assert app_external.id in external_ids
        assert app_internal.id not in external_ids

        # Проверяем, что все заявки имеют is_external=True
        for item in results:
            assert item["is_external"] is True

    def test_external_list_includes_is_external_field(self, statuses, make_user):
        """GET /api/showcase/project-applications/external/ включает поле is_external в ответе."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        # Создаём внешнюю заявку
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()

        dto = ProjectApplicationCreateDTO(
            company="External Corp",
            title="External Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="external@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        service.submit_application(dto, user, is_external=True)

        # Получаем список внешних заявок
        response = client.get("/api/showcase/project-applications/external/")

        assert response.status_code == 200

        # Если пагинация включена, данные в response.data["results"]
        if isinstance(response.data, dict) and "results" in response.data:
            results = response.data["results"]
        else:
            results = response.data

        assert len(results) > 0
        assert "is_external" in results[0]
        assert results[0]["is_external"] is True


@pytest.mark.django_db
class TestProjectApplicationViewSetIsExternalInResponses:
    """Тесты для проверки наличия поля is_external в ответах API."""

    def test_create_returns_is_external(self, statuses, make_user):
        """POST /api/showcase/project-applications/ возвращает is_external в ответе."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            "company": "Test Company",
            "title": "Test Project",
            "author_lastname": "Иванов",
            "author_firstname": "Иван",
            "author_email": "test@example.com",
            "author_phone": "+79990000000",
            "goal": "Длинная цель проекта, больше 50 символов для консультации",
            "problem_holder": "Носитель проблемы",
            "barrier": "Длинное описание барьера",
            "project_level": "L1",
        }

        response = client.post(
            "/api/showcase/project-applications/", data, format="json"
        )

        assert response.status_code == 201
        assert "is_external" in response.data
        assert response.data["is_external"] is False  # Обычная заявка

    def test_retrieve_returns_is_external(self, statuses, make_user):
        """GET /api/showcase/project-applications/{id}/ возвращает is_external в ответе."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        # Создаём заявку
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()

        dto = ProjectApplicationCreateDTO(
            company="Test Company",
            title="Test Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app = service.submit_application(dto, user, is_external=False)

        # Получаем заявку
        response = client.get(f"/api/showcase/project-applications/{app.id}/")

        assert response.status_code == 200
        assert "is_external" in response.data
        assert response.data["is_external"] is False

    def test_list_returns_is_external(self, statuses, make_user):
        """GET /api/showcase/project-applications/ возвращает is_external в списке."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        # Создаём заявку
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()

        dto = ProjectApplicationCreateDTO(
            company="Test Company",
            title="Test Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        service.submit_application(dto, user, is_external=False)

        # Получаем список заявок
        response = client.get("/api/showcase/project-applications/")

        assert response.status_code == 200

        # Если пагинация включена, данные в response.data["results"]
        if isinstance(response.data, dict) and "results" in response.data:
            results = response.data["results"]
        else:
            results = response.data

        assert len(results) > 0
        assert "is_external" in results[0]
