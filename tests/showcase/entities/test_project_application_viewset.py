"""Тесты для ProjectApplicationViewSet - проверка API endpoints."""

from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

from showcase.models import ApplicationStatus, Institute, ProjectApplication

User = get_user_model()


@pytest.mark.django_db
class TestProjectApplicationViewSetSimple:
    """Тесты для упрощенного создания заявок (simple endpoint)."""

    def test_simple_create_sets_is_external_true(self, statuses):
        """POST /api/showcase/project-applications/simple/ устанавливает is_external=True и статус require_assignment."""
        client = APIClient()
        data = {
            "company": "Test Company",
            "title": "Test Project",
            "company_contacts": "Контакты представителя",
            "existing_solutions": "Описание существующих решений",
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
        assert response.data["status"]["code"] == "require_assignment"

        # Проверяем в БД
        app_id = response.data["id"]
        app = ProjectApplication.objects.get(pk=app_id)
        assert app.is_external is True
        assert app.status.code == "require_assignment"

    def test_simple_create_returns_is_external_in_response(self, statuses):
        """POST /api/showcase/project-applications/simple/ возвращает is_external в ответе."""
        client = APIClient()
        data = {
            "company": "Test Company",
            "title": "Test Project",
            "company_contacts": "Контакты представителя",
            "existing_solutions": "Описание существующих решений",
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
        assert response.data["status"]["code"] == "require_assignment"

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
            "company_contacts": "Контакты представителя",
            "existing_solutions": "Описание существующих решений",
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
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
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
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
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
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
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
class TestProjectApplicationViewSetTransferToInstitute:
    """Тесты для действия передачи заявки в институт по коду института."""

    def _create_external_app_require_assignment(self, user):
        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()
        dto = ProjectApplicationCreateDTO(
            company="External Corp",
            title="External Project",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
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
        return service.submit_application(dto, user, is_external=True)

    def test_transfer_to_institute_success(self, statuses, make_user):
        """POST /api/showcase/project-applications/{id}/transfer_to_institute/ с корректным code."""
        user = make_user(role_code="cpds", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        # Внешняя заявка в статусе require_assignment
        app = self._create_external_app_require_assignment(user)
        assert app.status.code == "require_assignment"

        # Институт с привязанным подразделением
        department = user.department
        institute = Institute.objects.create(
            code="INST_TRANSFER",
            name="Институт передачи",
            position=1,
            is_active=True,
            department=department,
        )

        url = f"/api/showcase/project-applications/{app.id}/transfer_to_institute/"
        response = client.post(url, {"code": institute.code}, format="json")

        assert response.status_code == 200
        assert response.data["status"] == "await_institute"
        assert response.data["message"] == "Заявка передана в институт"
        assert "available_actions" in response.data

        app.refresh_from_db()
        assert app.status.code == "await_institute"

    def test_transfer_to_institute_missing_code(self, statuses, make_user):
        """Отсутствующий параметр code возвращает 400."""
        user = make_user(role_code="cpds", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        app = self._create_external_app_require_assignment(user)

        url = f"/api/showcase/project-applications/{app.id}/transfer_to_institute/"
        response = client.post(url, {}, format="json")

        assert response.status_code == 400
        assert "error" in response.data
        assert "code обязателен" in response.data["error"]

    def test_transfer_to_institute_invalid_code(self, statuses, make_user):
        """Несуществующий код института возвращает 400 от сервиса."""
        user = make_user(role_code="cpds", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        app = self._create_external_app_require_assignment(user)

        url = f"/api/showcase/project-applications/{app.id}/transfer_to_institute/"
        response = client.post(url, {"code": "UNKNOWN"}, format="json")

        assert response.status_code == 400
        assert (
            "Институт с кодом 'UNKNOWN' не найден или неактивен"
            in response.data["error"]
        )

    def test_transfer_to_institute_no_department_on_institute(
        self, statuses, make_user
    ):
        """Институт без связанного подразделения возвращает 400."""
        user = make_user(role_code="cpds", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        app = self._create_external_app_require_assignment(user)

        institute = Institute.objects.create(
            code="NO_DEPT",
            name="Институт без подразделения",
            position=1,
            is_active=True,
            department=None,
        )

        url = f"/api/showcase/project-applications/{app.id}/transfer_to_institute/"
        response = client.post(url, {"code": institute.code}, format="json")

        assert response.status_code == 400
        assert "не настроено связанное подразделение" in response.data["error"]

    def test_external_list_filters_by_status(self, statuses, make_user):
        """GET /api/showcase/project-applications/external/?status=... фильтрует внешние заявки по коду статуса."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        from showcase.dto.application import ProjectApplicationCreateDTO
        from showcase.models import ApplicationStatus
        from showcase.services.application_service import ProjectApplicationService

        service = ProjectApplicationService()

        # Создаём две внешние заявки
        dto1 = ProjectApplicationCreateDTO(
            company="External Corp 1",
            title="External Project 1",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="ext1@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app1 = service.submit_application(dto1, user, is_external=True)

        dto2 = ProjectApplicationCreateDTO(
            company="External Corp 2",
            title="External Project 2",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="ext2@example.com",
            author_phone="+79990000001",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app2 = service.submit_application(dto2, user, is_external=True)

        # Меняем статус второй заявки на await_institute
        app2.status = ApplicationStatus.objects.get(code="await_institute")
        app2.save()

        # Фильтруем по статусу require_assignment
        response = client.get(
            "/api/showcase/project-applications/external/?status=require_assignment"
        )

        assert response.status_code == 200

        if isinstance(response.data, dict) and "results" in response.data:
            results = response.data["results"]
        else:
            results = response.data

        ids = {item["id"] for item in results}
        assert app1.id in ids
        assert app2.id not in ids

    def test_external_list_invalid_status_returns_400(self, statuses, make_user):
        """GET /api/showcase/project-applications/external/?status=... с несуществующим статусом возвращает 400."""
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(
            "/api/showcase/project-applications/external/?status=unknown_status"
        )

        assert response.status_code == 400
        assert "error" in response.data


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
            "company_contacts": "Контактные данные представителя",
            "existing_solutions": "Описание существующих решений",
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
            company_contacts="Контактные данные представителя",
            existing_solutions="Описание существующих решений",
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
            company_contacts="Контактные данные представителя",
            existing_solutions="Описание существующих решений",
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
