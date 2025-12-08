from django.contrib.auth import get_user_model
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
    Institute,
    ProjectApplication,
    ProjectApplicationStatusLog,
)
from showcase.services.application_service import ProjectApplicationService

User = get_user_model()


@pytest.mark.django_db
class TestSubmitApplicationService:
    def test_submit_success_user_flow(self, statuses, make_user):
        """Успешная подача заявки: создаётся со статусом created, затем переводится в начальный по роли.

        Проверяем: финальный статус (await_institute, если нет валидаторов),
        наличие логов (создание + перевод), добавление причастных.
        """
        user = make_user(role_code="user", with_department=True)
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Проект X",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
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
        # Без валидаторов заявка должна перейти в await_institute
        assert app.status.code == "await_institute"
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
            company_contacts="",
            existing_solutions="",
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

    def test_submit_preserves_manual_needs_consultation(self, statuses, make_user):
        """Явно переданный needs_consultation не переопределяется доменной логикой."""
        user = make_user(role_code="user", with_department=True)
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Проект X",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
            goal="Цель менее 50 символов",
            project_level="",
            target_institutes=["INST"],
            needs_consultation=False,
        )
        service = ProjectApplicationService()

        app = service.submit_application(dto, user)

        assert app.needs_consultation is False

    def test_submit_sets_needs_consultation_when_not_provided(
        self, statuses, make_user
    ):
        """Если needs_consultation не передан, значение остается False по умолчанию."""
        user = make_user(role_code="user", with_department=True)
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Проект X",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
            goal="Цель менее 50 символов",
            project_level="",
            target_institutes=[],
        )
        service = ProjectApplicationService()

        app = service.submit_application(dto, user)

        assert app.needs_consultation is False

    def test_submit_with_is_external_true(self, statuses, make_user):
        """При создании упрощенной заявки устанавливается is_external=True и статус require_assignment."""
        user = make_user(role_code="user", with_department=True)
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="External Project",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
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

        app = service.submit_application(dto, user, is_external=True)

        assert isinstance(app, ProjectApplication)
        assert app.is_external is True
        assert app.status.code == "require_assignment"

    def test_submit_with_is_external_true_adds_cpds_department(
        self, statuses, make_user
    ):
        """При создании упрощенной заявки добавляется причастное подразделение ЦПДС."""
        from accounts.models import Department

        # Создаем подразделение ЦПДС если его нет
        cpds_department, _ = Department.objects.get_or_create(
            short_name="ЦПДС", defaults={"name": "Центр проектного развития"}
        )

        user = make_user(role_code="user", with_department=True)
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="External Project",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
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

        app = service.submit_application(dto, user, is_external=True)

        # Проверяем, что подразделение ЦПДС добавлено как причастное
        assert ApplicationInvolvedDepartment.objects.filter(
            application=app, department=cpds_department
        ).exists()

    def test_submit_with_is_external_false(self, statuses, make_user):
        """При создании обычной заявки is_external=False по умолчанию."""
        user = make_user(role_code="user", with_department=True)
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Internal Project",
            company_contacts="Контакты представителя",
            existing_solutions="Описание существующих решений",
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

        app = service.submit_application(dto, user, is_external=False)

        assert isinstance(app, ProjectApplication)
        assert app.is_external is False

    def test_submit_without_department_validator_auto_transition(
        self, statuses, make_user, roles
    ):
        """Заявка автоматически переходит в await_institute, если в подразделении нет department_validator."""
        # Создаём пользователя с подразделением, но без валидатора в этом подразделении
        user = make_user(role_code="user", with_department=True)
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Проект X",
            company_contacts="Контактные данные представителя",
            existing_solutions="Описание существующих решений",
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

        # Должен автоматически перейти в await_institute, так как нет валидатора
        assert app.status.code == "await_institute"
        # Должны создаться логи: 1) создание, 2) перевод в await_institute
        assert (
            ProjectApplicationStatusLog.objects.filter(
                application=app, action_type="status_change"
            ).count()
            == 2
        )

    def test_submit_with_department_validator_stays_await_department(
        self, statuses, make_user, roles
    ):
        """Заявка остаётся в await_department, если в подразделении есть department_validator."""
        # Создаём пользователя с подразделением
        user = make_user(role_code="user", with_department=True)
        # Создаём валидатора в том же подразделении
        validator_role = roles["department_validator"]
        User.objects.create_user(
            email="validator@example.com",
            password="pass",
            first_name="Validator",
            last_name="User",
            role=validator_role,
            department=user.department,  # То же подразделение
        )

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Проект X",
            company_contacts="Контактные данные представителя",
            existing_solutions="Описание существующих решений",
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

        # Должен остаться в await_department, так как есть валидатор
        assert app.status.code == "await_department"
        # Должны создаться логи: 1) создание, 2) перевод в await_department
        assert (
            ProjectApplicationStatusLog.objects.filter(
                application=app, action_type="status_change"
            ).count()
            == 2
        )

    def test_submit_with_validator_in_parent_department(
        self, statuses, make_user, roles, departments
    ):
        """Заявка остаётся в await_department, если валидатор есть в родительском подразделении."""
        # Создаём пользователя с дочерним подразделением
        user = make_user(role_code="user", with_department=True)
        # Создаём валидатора в родительском подразделении
        parent_dept = departments["parent"]
        validator_role = roles["department_validator"]
        User.objects.create_user(
            email="validator@example.com",
            password="pass",
            first_name="Validator",
            last_name="User",
            role=validator_role,
            department=parent_dept,
        )

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Проект X",
            company_contacts="Контактные данные представителя",
            existing_solutions="Описание существующих решений",
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

        # Должен остаться в await_department, так как есть валидатор в родительском подразделении
        # (которое также добавляется как причастное)
        assert app.status.code == "await_department"

    def test_submit_no_validator_in_multiple_involved_departments(
        self, statuses, make_user, roles, departments
    ):
        """Заявка переходит в await_institute, если ни в одном из причастных подразделений нет department_validator.

        Проверяет ситуацию, когда у заявки есть несколько причастных подразделений
        (подразделение пользователя + родительское), но ни в одном из них нет валидатора.
        """
        # Создаём пользователя с подразделением
        # Важно: убеждаемся, что в подразделении пользователя и родительском нет валидаторов
        user = make_user(role_code="user", with_department=True)

        # Убеждаемся, что в подразделении пользователя нет валидатора
        user_dept = user.department
        parent_dept = user_dept.parent if hasattr(user_dept, 'parent') else None

        # Проверяем, что в подразделении пользователя нет валидатора
        has_validator_in_user_dept = User.objects.filter(
            department=user_dept,
            role__code="department_validator",
            is_active=True,
        ).exists()
        assert (
            not has_validator_in_user_dept
        ), "В подразделении пользователя не должно быть валидатора"

        # Проверяем родительское подразделение, если оно есть
        if parent_dept:
            has_validator_in_parent = User.objects.filter(
                department=parent_dept,
                role__code="department_validator",
                is_active=True,
            ).exists()
            assert (
                not has_validator_in_parent
            ), "В родительском подразделении не должно быть валидатора"

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

        # Проверяем все причастные подразделения после создания заявки
        involved_depts = ApplicationInvolvedDepartment.objects.filter(application=app)
        assert (
            involved_depts.count() >= 1
        ), "Должно быть хотя бы одно причастное подразделение"

        # Проверяем, что ни в одном из причастных подразделений нет валидатора
        departments_without_validator = []
        for involved_dept in involved_depts:
            has_validator = User.objects.filter(
                department=involved_dept.department,
                role__code="department_validator",
                is_active=True,
            ).exists()
            if not has_validator:
                departments_without_validator.append(involved_dept.department.name)
            else:
                # Если нашли валидатора, это ошибка теста
                assert False, (
                    f"В подразделении {involved_dept.department.name} найден валидатор, "
                    "но тест предполагает отсутствие валидаторов"
                )

        # Статус должен быть await_institute, так как ни в одном причастном подразделении нет валидатора
        assert app.status.code == "await_institute", (
            f"Ожидался статус await_institute, но получен {app.status.code}. "
            f"Причастные подразделения без валидаторов: {', '.join(departments_without_validator)}. "
            "Заявка должна автоматически перейти в await_institute при отсутствии валидаторов "
            "во всех причастных подразделениях."
        )


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

    def test_approve_cpds_from_await_cpds(self, statuses, make_user):
        """cpds: может одобрять заявки в статусе await_cpds (переход в approved разрешен)."""
        cpds = make_user(role_code="cpds", with_department=True)
        app = self._create_app(author=cpds, status_code="await_cpds")
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=cpds.department
        )

        service = ProjectApplicationService()
        app2 = service.approve_application(app.id, cpds)
        # CPDS одобряет в финальный статус approved
        assert app2.status.code == "approved"

    def test_cpds_request_changes_after_full_approval_chain(
        self, statuses, make_user, roles
    ):
        """Полный цикл: заявка создается, одобряется department_validator, затем institute_validator,
        затем cpds возвращает на доработку.

        Проверяет:
        - Заявка создается со статусом await_department
        - department_validator одобряет -> await_institute
        - institute_validator одобряет -> await_cpds
        - cpds возвращает на доработку -> returned_cpds
        - Все логи статусов созданы правильно
        """
        # Создаем пользователей с разными ролями
        author = make_user(role_code="user", with_department=True)
        inst_validator = make_user(
            role_code="institute_validator", with_department=True
        )
        cpds_user = make_user(role_code="cpds", with_department=True)

        # Создаем валидатора в подразделении автора, чтобы заявка точно была в await_department
        validator_role = roles["department_validator"]
        dept_validator = User.objects.create_user(
            email="dept_validator@example.com",
            password="pass",
            first_name="Dept",
            last_name="Validator",
            role=validator_role,
            department=author.department,  # То же подразделение, что и у автора
        )

        # Создаем заявку
        service = ProjectApplicationService()
        dto = ProjectApplicationCreateDTO(
            company="Test Company",
            title="Test Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="author@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app = service.submit_application(dto, author)

        # Проверяем, что заявка в статусе await_department
        assert app.status.code == "await_department"

        # Одобряем через department_validator
        # Причастность подразделения уже добавлена автоматически при создании заявки
        app = service.approve_application(app.id, dept_validator)
        app.refresh_from_db()
        assert app.status.code == "await_institute"

        # Одобряем через institute_validator
        # Добавляем причастность подразделения валидатора института (если еще не добавлено)
        ApplicationInvolvedDepartment.objects.get_or_create(
            application=app, department=inst_validator.department
        )
        app = service.approve_application(app.id, inst_validator)
        app.refresh_from_db()
        assert app.status.code == "await_cpds"

        # CPDS возвращает на доработку
        # Добавляем причастность подразделения CPDS (если еще не добавлено)
        cpds_department, _ = Department.objects.get_or_create(
            short_name="ЦПДС", defaults={"name": "Центр проектного развития"}
        )
        ApplicationInvolvedDepartment.objects.get_or_create(
            application=app, department=cpds_department
        )
        app = service.request_changes(app.id, cpds_user)
        app.refresh_from_db()

        # Проверяем финальный статус
        assert app.status.code == "returned_cpds"

        # Проверяем логи статусов
        status_logs = ProjectApplicationStatusLog.objects.filter(
            application=app, action_type="status_change"
        ).order_by("changed_at")

        # Должно быть минимум 4 лога:
        # 1) создание заявки (created -> await_department)
        # 2) одобрение department_validator (await_department -> approved_department -> await_institute)
        # 3) одобрение institute_validator (await_institute -> approved_institute -> await_cpds)
        # 4) возврат на доработку cpds (await_cpds -> returned_cpds)
        assert status_logs.count() >= 4

        # Проверяем последний лог - возврат на доработку
        last_log = status_logs.last()
        assert last_log.from_status.code == "await_cpds"
        assert last_log.to_status.code == "returned_cpds"
        assert last_log.actor == cpds_user

        # Проверяем, что в логах есть все необходимые переходы
        log_statuses = [log.to_status.code for log in status_logs]
        assert (
            "await_institute" in log_statuses
        ), "Должен быть лог перехода в await_institute"
        assert "await_cpds" in log_statuses, "Должен быть лог перехода в await_cpds"
        assert (
            "returned_cpds" in log_statuses
        ), "Должен быть лог перехода в returned_cpds"

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

    def test_transfer_to_institute_success(self, statuses, make_user):
        """cpds может передать внешнюю заявку в институт по коду института.

        Проверяем:
        - используется связанное с институтом подразделение;
        - подразделение добавлено в причастные;
        - статус заявки становится await_institute;
        - создаётся лог изменения статуса.
        """
        cpds_user = make_user(role_code="cpds", with_department=True)

        # Создаём внешнюю заявку со статусом require_assignment
        service = ProjectApplicationService()
        dto = ProjectApplicationCreateDTO(
            company="External Corp",
            title="External Project",
            company_contacts="Контактные данные представителя",
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
        app = service.submit_application(dto, cpds_user, is_external=True)
        assert app.status.code == "require_assignment"

        # Создаём институт и связываем его с подразделением
        department = Department.objects.create(name="Институт 1", short_name="INST1")
        institute = Institute.objects.create(
            code="INST_CODE",
            name="Институт тестовый",
            position=1,
            is_active=True,
            department=department,
        )

        # Вызываем передачу в институт
        app2 = service.transfer_to_institute(
            application_id=app.id,
            institute_code=institute.code,
            transferrer=cpds_user,
        )

        app2.refresh_from_db()
        assert app2.status.code == "await_institute"
        # Подразделение института добавлено в причастные
        assert ApplicationInvolvedDepartment.objects.filter(
            application=app2, department=department
        ).exists()

        # Проверяем, что есть лог изменения статуса на await_institute
        assert ProjectApplicationStatusLog.objects.filter(
            application=app2,
            to_status__code="await_institute",
            action_type="status_change",
        ).exists()

    def test_transfer_to_institute_requires_external_and_require_assignment(
        self, statuses, make_user
    ):
        """Передача в институт доступна только для внешних заявок со статусом require_assignment."""
        cpds_user = make_user(role_code="cpds", with_department=True)
        service = ProjectApplicationService()

        # Создаём обычную (внутреннюю) заявку
        dto_internal = ProjectApplicationCreateDTO(
            company="Internal Corp",
            title="Internal Project",
            company_contacts="Контактные данные представителя",
            existing_solutions="Описание существующих решений",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="internal@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app_internal = service.submit_application(
            dto_internal, cpds_user, is_external=False
        )

        # Создаём внешний апп, но вручную меняем статус на отличный от require_assignment
        dto_external = ProjectApplicationCreateDTO(
            company="External Corp",
            title="External Project",
            company_contacts="Контактные данные представителя",
            existing_solutions="Описание существующих решений",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="external@example.com",
            author_phone="+79990000001",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app_external = service.submit_application(
            dto_external, cpds_user, is_external=True
        )
        # Меняем статус на await_institute
        app_external.status = ApplicationStatus.objects.get(code="await_institute")
        app_external.save()

        # Создаём институт с подразделением
        department = Department.objects.create(name="Институт 2", short_name="INST2")
        institute = Institute.objects.create(
            code="INST2",
            name="Институт 2",
            position=2,
            is_active=True,
            department=department,
        )

        # Для внутренней заявки ожидаем ValueError (is_external=False)
        with pytest.raises(
            ValueError, match="Действие доступно только для внешних заявок"
        ):
            service.transfer_to_institute(
                application_id=app_internal.id,
                institute_code=institute.code,
                transferrer=cpds_user,
            )

        # Для внешней заявки в неверном статусе — тоже ValueError
        with pytest.raises(
            ValueError,
            match="Действие доступно только для заявок со статусом require_assignment",
        ):
            service.transfer_to_institute(
                application_id=app_external.id,
                institute_code=institute.code,
                transferrer=cpds_user,
            )

    def test_transfer_to_institute_institute_validation_errors(
        self, statuses, make_user
    ):
        """Ошибки валидации института: несуществующий код или отсутствие связанного подразделения."""
        cpds_user = make_user(role_code="cpds", with_department=True)
        service = ProjectApplicationService()

        # Создаём внешнюю заявку в правильном статусе
        dto = ProjectApplicationCreateDTO(
            company="External Corp",
            title="External Project",
            company_contacts="Контактные данные представителя",
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
        app = service.submit_application(dto, cpds_user, is_external=True)
        assert app.status.code == "require_assignment"

        # 1. Неверный код института
        with pytest.raises(
            ValueError, match="Институт с кодом 'UNKNOWN' не найден или неактивен"
        ):
            service.transfer_to_institute(
                application_id=app.id,
                institute_code="UNKNOWN",
                transferrer=cpds_user,
            )

        # 2. Институт без связанного подразделения
        institute = Institute.objects.create(
            code="NO_DEPT",
            name="Институт без подразделения",
            position=3,
            is_active=True,
            department=None,
        )

        with pytest.raises(
            ValueError,
            match="У института 'Институт без подразделения' \\(код NO_DEPT\\) не настроено связанное подразделение",
        ):
            service.transfer_to_institute(
                application_id=app.id,
                institute_code=institute.code,
                transferrer=cpds_user,
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

    def test_update_success_by_author(self, statuses, make_user):
        """Автор может редактировать свою заявку."""
        author = make_user(role_code="user", with_department=False)
        app = self._create_app(author=author, status_code="await_department")
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="New valid title")
        app2 = service.update_application(app.id, dto, author)
        assert app2.title == "New valid title"
        assert ProjectApplicationStatusLog.objects.filter(
            application=app, action_type="application_updated"
        ).exists()

    def test_update_success_by_cpds(self, statuses, make_user):
        """Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)."""
        author = make_user(role_code="user", with_department=False)
        cpds = make_user(role_code="cpds", with_department=True)
        app = self._create_app(author=author, status_code="await_department")
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="New valid title")
        app2 = service.update_application(app.id, dto, cpds)
        assert app2.title == "New valid title"
        assert ProjectApplicationStatusLog.objects.filter(
            application=app, action_type="application_updated"
        ).exists()

    def test_update_success_by_department_validator_as_author(
        self, statuses, make_user
    ):
        """department_validator может редактировать свою заявку (как автор)."""
        validator = make_user(role_code="department_validator", with_department=True)
        app = self._create_app(author=validator, status_code="await_department")
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="New valid title")
        app2 = service.update_application(app.id, dto, validator)
        assert app2.title == "New valid title"
        assert ProjectApplicationStatusLog.objects.filter(
            application=app, action_type="application_updated"
        ).exists()

    def test_update_permission_denied(self, statuses, make_user):
        """Не-автор и не-ЦПДС не может редактировать чужую заявку — PermissionError."""
        author = make_user(role_code="user", with_department=False)
        other = make_user(role_code="user", with_department=False)
        app = self._create_app(author=author, status_code="await_department")
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="New title")
        with pytest.raises(PermissionError):
            service.update_application(app.id, dto, other)

    def test_update_permission_denied_for_validator(self, statuses, make_user):
        """Валидатор не может редактировать чужую заявку (только если он не автор)."""
        author = make_user(role_code="user", with_department=False)
        validator = make_user(role_code="department_validator", with_department=True)
        app = self._create_app(author=author, status_code="await_department")
        # Добавляем причастность подразделения валидатора
        ApplicationInvolvedDepartment.objects.create(
            application=app, department=validator.department
        )
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="New title")
        # Валидатор не является автором, поэтому не может редактировать
        with pytest.raises(PermissionError):
            service.update_application(app.id, dto, validator)

    def test_update_validation_error(self, statuses, make_user):
        """Некорректный title вызывает ValueError при роли, которой разрешено редактировать."""
        author = make_user(role_code="user", with_department=False)
        app = self._create_app(author=author, status_code="await_department")
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="bad")
        with pytest.raises(ValueError):
            service.update_application(app.id, dto, author)

    def test_update_rejected_status_denied(self, statuses, make_user):
        """Нельзя редактировать заявки со статусом rejected (даже автору и cpds)."""
        author = make_user(role_code="user", with_department=False)
        cpds = make_user(role_code="cpds", with_department=True)
        app = self._create_app(author=author, status_code="rejected")
        service = ProjectApplicationService()
        dto = ProjectApplicationUpdateDTO(title="New title")
        # Автор не может редактировать rejected
        with pytest.raises(PermissionError):
            service.update_application(app.id, dto, author)
        # CPDS тоже не может редактировать rejected
        with pytest.raises(PermissionError):
            service.update_application(app.id, dto, cpds)

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

    def test_cpds_sees_await_cpds_without_involvement(self, statuses, make_user):
        """cpds видит все заявки в статусе await_cpds даже без причастности."""
        cpds = make_user(role_code="cpds", with_department=True)
        await_app = self._create_app(author=cpds, status_code="await_cpds")
        other_app = self._create_app(author=cpds, status_code="await_department")

        service = ProjectApplicationService()
        items = service.get_user_coordination_applications(cpds)
        ids = {i.id for i in items}

        assert await_app.id in ids
        assert other_app.id not in ids

    def test_dto_builders(self, statuses, make_user):
        """Преобразователи к DTO возвращают ожидаемые экземпляры."""
        user = make_user(role_code="admin")
        app = self._create_app(author=user, status_code="await_department")
        service = ProjectApplicationService()
        read_dto = service.get_application_dto(app)
        list_dto = service.get_application_list_dto(app)
        assert read_dto.id == app.id
        assert list_dto.id == app.id

    def test_get_external_applications(self, statuses, make_user):
        """get_external_applications возвращает только заявки с is_external=True."""
        user = make_user(role_code="user", with_department=True)
        service = ProjectApplicationService()

        # Создаём внешнюю заявку
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

        # Получаем внешние заявки без фильтра по статусу
        external_apps = service.get_external_applications(user)

        # Проверяем, что только внешняя заявка в списке
        external_ids = {app.id for app in external_apps}
        assert app_external.id in external_ids
        assert app_internal.id not in external_ids

    def test_get_external_applications_with_status_filter(self, statuses, make_user):
        """get_external_applications позволяет фильтровать внешние заявки по коду статуса."""
        user = make_user(role_code="user", with_department=True)
        service = ProjectApplicationService()

        # Создаём две внешние заявки с разными статусами
        dto1 = ProjectApplicationCreateDTO(
            company="External Corp 1",
            title="External Project 1",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="external1@example.com",
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
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="external2@example.com",
            author_phone="+79990000001",
            goal="Длинная цель проекта, больше 50 символов для консультации",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
            target_institutes=[],
            project_level="L1",
        )
        app2 = service.submit_application(dto2, user, is_external=True)

        # Принудительно меняем статус второй заявки на await_institute
        app2.status = ApplicationStatus.objects.get(code="await_institute")
        app2.save()

        # Фильтруем по статусу require_assignment
        apps_require_assignment = service.get_external_applications(
            user, status_code="require_assignment"
        )
        ids_require_assignment = {app.id for app in apps_require_assignment}
        assert app1.id in ids_require_assignment
        assert app2.id not in ids_require_assignment

        # Фильтруем по статусу await_institute
        apps_await_institute = service.get_external_applications(
            user, status_code="await_institute"
        )
        ids_await_institute = {app.id for app in apps_await_institute}
        assert app2.id in ids_await_institute
        assert app1.id not in ids_await_institute

    def test_get_external_applications_with_invalid_status_raises_value_error(
        self, statuses, make_user
    ):
        """get_external_applications с несуществующим статусом выбрасывает ValueError."""
        user = make_user(role_code="user", with_department=True)
        service = ProjectApplicationService()

        with pytest.raises(
            ValueError, match="Статус с кодом 'unknown_status' не найден"
        ):
            service.get_external_applications(user, status_code="unknown_status")

    def test_get_external_applications_queryset(self, statuses, make_user):
        """get_external_applications_queryset возвращает QuerySet внешних заявок."""
        user = make_user(role_code="user", with_department=True)
        service = ProjectApplicationService()

        # Создаём внешнюю заявку
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

        # Получаем QuerySet внешних заявок
        qs = service.get_external_applications_queryset(user)

        assert hasattr(qs, "filter")  # QuerySet
        results = list(qs)
        assert len(results) == 1
        assert results[0].id == app_external.id
        assert results[0].is_external is True

    def test_get_external_applications_requires_authentication(self, statuses):
        """get_external_applications требует авторизации."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        # Создаём неавторизованного пользователя (AnonymousUser)
        anonymous_user = User()

        service = ProjectApplicationService()

        with pytest.raises(PermissionError, match="Требуется авторизация"):
            service.get_external_applications(anonymous_user)
