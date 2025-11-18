import pytest

from accounts.models import Department
from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
)
from showcase.models import (
    ApplicationInvolvedDepartment,
    ApplicationInvolvedUser,
    ApplicationStatus,
    ProjectApplication,
    ProjectApplicationStatusLog,
)
from showcase.services.application_service import ProjectApplicationService


@pytest.mark.django_db
class TestSubmitApplicationService:
    def test_submit_success_user_flow(self, statuses, make_user):
        """Успешная подача заявки: создаётся со статусом created, затем переводится в начальный по роли.

        Проверяем: финальный статус, наличие логов (создание + перевод), добавление причастных.
        """
        user = make_user(role_code="user", with_department=True)
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Проект X",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        service = ProjectApplicationService()

        app = service.submit_application(dto, user)

        assert isinstance(app, ProjectApplication)
        assert app.status.code == "await_department"
        # Должны создаться логи: 1) создание, 2) перевод
        assert (
            ProjectApplicationStatusLog.objects.filter(
                application=app, action_type="status_change"
            ).count()
            == 2
        )
        # Причастные: пользователь и его отделы
        assert ApplicationInvolvedUser.objects.filter(
            application=app, user=user
        ).exists()
        assert ApplicationInvolvedDepartment.objects.filter(
            application=app, department=user.department
        ).exists()

    def test_submit_validation_error(self, make_user):
        """При ошибках доменной валидации выбрасывается ValueError."""
        user = make_user(role_code="user", with_department=False)
        dto = ProjectApplicationCreateDTO(
            company="A",  # слишком коротко
            title="bad",  # слишком коротко
            author_lastname="I",
            author_firstname="I",
            author_email="x@",
            author_phone="123",
            goal="short",
            problem_holder="xx",
            barrier="short",
        )
        service = ProjectApplicationService()
        with pytest.raises(ValueError):
            service.submit_application(dto, user)


@pytest.mark.django_db
class TestApproveRejectRequestService:
    def _create_app(self, author, status_code: str) -> ProjectApplication:
        return ProjectApplication.objects.create(
            title="t",
            company="Acme",
            author=author,
            status=ApplicationStatus.objects.get(code=status_code),
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )

    def test_approve_department_validator_two_step(self, statuses, make_user):
        """department_validator: await_department -> approved_department -> await_institute, два лога переводов."""
        validator = make_user(role_code="department_validator", with_department=True)
        app = self._create_app(author=validator, status_code="await_department")
        # причастность подразделения нужна матрицей
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=validator.department
        )

        service = ProjectApplicationService()
        app2 = service.approve_application(app.id, validator)

        assert app2.status.code == "await_institute"
        # Логи: промежуточный и следующий статус
        logs = ProjectApplicationStatusLog.objects.filter(
            application=app, action_type="status_change"
        )
        assert logs.count() == 2

    def test_approve_institute_adds_cpds_department(self, statuses, make_user):
        """institute_validator: await_institute -> approved_institute -> await_cpds добавляет причастное ЦПДС."""
        validator = make_user(role_code="institute_validator", with_department=True)
        app = self._create_app(author=validator, status_code="await_institute")
        cpds_department = Department.objects.create(
            name="Центр проектного развития", short_name="ЦПДС"
        )
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=validator.department
        )

        service = ProjectApplicationService()
        app2 = service.approve_application(app.id, validator)

        app2.refresh_from_db()
        assert app2.status.code == "await_cpds"
        assert ApplicationInvolvedDepartment.objects.filter(
            application=app2, department=cpds_department
        ).exists()

    def test_approve_cpds_final_forbidden_by_domain(self, statuses, make_user):
        """cpds: попытка финального approved запрещена доменом (ожидаем ValueError)."""
        cpds = make_user(role_code="cpds", with_department=True)
        app = self._create_app(author=cpds, status_code="await_cpds")
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=cpds.department
        )

        service = ProjectApplicationService()
        with pytest.raises(ValueError):
            service.approve_application(app.id, cpds)

    def test_request_changes_department_validator(self, statuses, make_user):
        """Запрос изменений: await_department -> returned_department, один лог."""
        validator = make_user(role_code="department_validator", with_department=True)
        app = self._create_app(author=validator, status_code="await_department")
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=validator.department
        )

        service = ProjectApplicationService()
        app2 = service.request_changes(app.id, validator)
        assert app2.status.code == "returned_department"
        assert (
            ProjectApplicationStatusLog.objects.filter(
                application=app, action_type="status_change"
            ).count()
            == 1
        )

    def test_reject_department_validator_to_final(self, statuses, make_user):
        """Отклонение: await_department -> rejected_department -> rejected, два лога."""
        validator = make_user(role_code="department_validator", with_department=True)
        app = self._create_app(author=validator, status_code="await_department")
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=validator.department
        )

        service = ProjectApplicationService()
        app2 = service.reject_application(app.id, validator, reason="not good")
        assert app2.status.code == "rejected"
        assert (
            ProjectApplicationStatusLog.objects.filter(
                application=app, action_type="status_change"
            ).count()
            == 2
        )

    def test_approve_permission_denied(self, statuses, make_user):
        """Нет причастности подразделения — матрица запрещает действие, ожидаем PermissionError."""
        validator = make_user(role_code="department_validator", with_department=True)
        app = self._create_app(author=validator, status_code="await_department")
        service = ProjectApplicationService()
        with pytest.raises(PermissionError):
            service.approve_application(app.id, validator)


@pytest.mark.django_db
class TestUpdateAndQueriesService:
    def _create_app(self, author, status_code: str) -> ProjectApplication:
        return ProjectApplication.objects.create(
            title="t",
            company="Acme",
            author=author,
            status=ApplicationStatus.objects.get(code=status_code),
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )

    def test_update_success_by_department_validator(self, statuses, make_user):
        """department_validator может сохранить изменения в await_department при причастном подразделении."""
        validator = make_user(role_code="department_validator", with_department=True)
        app = self._create_app(author=validator, status_code="await_department")
        # причастность подразделения нужна для save_changes
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=validator.department
        )
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="New valid title")
        app2 = service.update_application(app.id, dto, validator)
        assert app2.title == "New valid title"
        assert ProjectApplicationStatusLog.objects.filter(
            application=app, action_type="application_updated"
        ).exists()

    def test_update_permission_denied(self, statuses, make_user):
        """Обычный пользователь не может редактировать чужую заявку — PermissionError."""
        author = make_user(role_code="user", with_department=False)
        other = make_user(role_code="user", with_department=False)
        app = self._create_app(author=author, status_code="await_department")
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="New title")
        with pytest.raises(PermissionError):
            service.update_application(app.id, dto, other)

    def test_update_validation_error(self, statuses, make_user):
        """Некорректный title вызывает ValueError при роли, которой разрешено редактировать."""
        validator = make_user(role_code="department_validator", with_department=True)
        app = self._create_app(author=validator, status_code="await_department")
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=validator.department
        )
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="bad")
        with pytest.raises(ValueError):
            service.update_application(app.id, dto, validator)

    def test_get_application_permission(self, statuses, make_user):
        """Доступ к просмотру: чужому user запрещено, автору разрешено."""
        author = make_user(role_code="user")
        other = make_user(role_code="user")
        app = self._create_app(author=author, status_code="await_department")
        service = ProjectApplicationService()
        with pytest.raises(PermissionError):
            service.get_application(app.id, other)
        # автор может
        got = service.get_application(app.id, author)
        assert got.id == app.id

    def test_get_user_applications_and_queryset(self, statuses, make_user):
        """Списки по пользователю возвращаются без ошибок для user роли."""
        user = make_user(role_code="user")
        service = ProjectApplicationService()
        # просто вызовы без исключений
        lst = service.get_user_applications(user)
        qs = service.get_user_applications_queryset(user)
        assert isinstance(lst, list)
        assert hasattr(qs, "filter")  # QuerySet-like

    def test_get_applications_by_status_permissions(self, statuses, make_user):
        """По статусу доступ только admin/moderator; для иных — PermissionError."""
        admin = make_user(role_code="admin")
        user = make_user(role_code="user")
        service = ProjectApplicationService()
        # неадмин
        with pytest.raises(PermissionError):
            service.get_applications_by_status("await_department", user)
        # админ
        service.get_applications_by_status("await_department", admin)

    def test_recent_and_all_queryset_permissions(self, statuses, make_user):
        """recent/all_queryset: доступ админ/модератор; для остальных — PermissionError."""
        admin = make_user(role_code="admin")
        moderator = make_user(role_code="moderator")
        user = make_user(role_code="user")
        service = ProjectApplicationService()

        with pytest.raises(PermissionError):
            service.get_recent_applications(5, user)
        assert isinstance(service.get_recent_applications(5, admin), list)
        # all_queryset
        with pytest.raises(PermissionError):
            service.get_all_applications_queryset(user)
        qs = service.get_all_applications_queryset(moderator)
        assert hasattr(qs, "filter")


@pytest.mark.django_db
class TestCoordinationAndDtosService:
    def _create_app(self, author, status_code: str) -> ProjectApplication:
        return ProjectApplication.objects.create(
            title="t",
            company="Acme",
            author=author,
            status=ApplicationStatus.objects.get(code=status_code),
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )

    def test_get_user_coordination_applications(self, statuses, make_user):
        """Валидатор получает объединённый список: его причастность пользователя + подразделения без дублей."""
        validator = make_user(role_code="department_validator", with_department=True)
        app1 = self._create_app(author=validator, status_code="await_department")
        app2 = self._create_app(author=validator, status_code="await_department")

        # причастность пользователя — app1
        ApplicationInvolvedUser.objects.create(application=app1, user=validator)
        # причастность подразделения — app2
        ApplicationInvolvedDepartment.objects.create(
            application=app2, department=validator.department
        )

        service = ProjectApplicationService()
        items = service.get_user_coordination_applications(validator)
        ids = {i.id for i in items}
        assert app1.id in ids and app2.id in ids

    def test_dto_builders(self, statuses, make_user):
        """Преобразователи к DTO возвращают ожидаемые экземпляры."""
        user = make_user(role_code="admin")
        app = self._create_app(author=user, status_code="await_department")
        service = ProjectApplicationService()
        read_dto = service.get_application_dto(app)
        list_dto = service.get_application_list_dto(app)
        assert read_dto.id == app.id
        assert list_dto.id == app.id
