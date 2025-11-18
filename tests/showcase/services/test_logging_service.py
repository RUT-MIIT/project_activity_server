"""Unit-тесты для ApplicationLoggingService.

Проверяем логирование всех типов действий: изменение статусов, причастные пользователи/подразделения, получение логов.
"""

from unittest.mock import Mock

import pytest

from accounts.models import Department
from showcase.models import ProjectApplication
from showcase.services.logging_service import ApplicationLoggingService


@pytest.mark.django_db
class TestLogStatusChange:
    """Тесты для log_status_change."""

    def test_log_status_change_success(self, statuses, make_user):
        """Успешное логирование изменения статуса."""

        user = make_user(role_code="user")
        status_from = statuses["await_department"]
        status_to = statuses["await_institute"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status_from,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log = service.log_status_change(
            application=app,
            from_status=status_from,
            to_status=status_to,
            actor=user,
        )

        assert log.id is not None
        assert log.application.id == app.id
        assert log.action_type == "status_change"
        assert log.from_status.id == status_from.id
        assert log.to_status.id == status_to.id
        assert log.actor.id == user.id

    def test_log_status_change_with_previous_log(self, statuses, make_user):
        """Логирование с указанием предыдущего лога для создания цепочки."""

        user = make_user(role_code="user")
        status1 = statuses["await_department"]
        status2 = statuses["await_institute"]
        status3 = statuses["await_cpds"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status1,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log1 = service.log_status_change(
            application=app, from_status=status1, to_status=status2, actor=user
        )

        log2 = service.log_status_change(
            application=app,
            from_status=status2,
            to_status=status3,
            actor=user,
            previous_log=log1,
        )

        assert log2.previous_status_log.id == log1.id

    def test_log_status_change_application_none(self, statuses, make_user):
        """Если application равен None, выбрасывается ValueError."""
        user = make_user(role_code="user")
        status = statuses["await_department"]

        service = ApplicationLoggingService()
        with pytest.raises(ValueError, match="Заявка не может быть None"):
            service.log_status_change(
                application=None,
                from_status=status,
                to_status=status,
                actor=user,
            )

    def test_log_status_change_to_status_none(self, statuses, make_user):
        """Если to_status равен None, выбрасывается ValueError."""

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        with pytest.raises(ValueError, match="Новый статус не может быть None"):
            service.log_status_change(
                application=app,
                from_status=status,
                to_status=None,
                actor=user,
            )

    def test_log_status_change_actor_none(self, statuses, make_user):
        """Если actor равен None, выбрасывается ValueError."""

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        with pytest.raises(ValueError, match="Актор не может быть None"):
            service.log_status_change(
                application=app,
                from_status=status,
                to_status=status,
                actor=None,
            )


@pytest.mark.django_db
class TestLogInvolvedUser:
    """Тесты для логирования причастных пользователей."""

    def test_log_involved_user_added(self, statuses, make_user):
        """Логирование добавления причастного пользователя."""

        user1 = make_user(role_code="user", email="user1@example.com")
        user2 = make_user(role_code="user", email="user2@example.com")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user1,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log = service.log_involved_user_added(application=app, user=user2, actor=user1)

        assert log.action_type == "involved_user_added"
        assert log.involved_user.id == user2.id
        assert log.actor.id == user1.id
        assert log.from_status.id == status.id
        assert log.to_status.id == status.id  # Статус не меняется

    def test_log_involved_user_added_validation_errors(self, statuses, make_user):
        """Проверка валидации при добавлении причастного пользователя."""

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()

        with pytest.raises(ValueError, match="Заявка не может быть None"):
            service.log_involved_user_added(application=None, user=user, actor=user)

        with pytest.raises(ValueError, match="Пользователь не может быть None"):
            service.log_involved_user_added(application=app, user=None, actor=user)

        with pytest.raises(ValueError, match="Актор не может быть None"):
            service.log_involved_user_added(application=app, user=user, actor=None)

    def test_log_involved_user_removed(self, statuses, make_user):
        """Логирование удаления причастного пользователя."""

        user1 = make_user(role_code="user", email="user1@example.com")
        user2 = make_user(role_code="user", email="user2@example.com")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user1,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log = service.log_involved_user_removed(
            application=app, user=user2, actor=user1
        )

        assert log.action_type == "involved_user_removed"
        assert log.involved_user.id == user2.id
        assert log.actor.id == user1.id


@pytest.mark.django_db
class TestLogInvolvedDepartment:
    """Тесты для логирования причастных подразделений."""

    def test_log_involved_department_added(self, statuses, make_user):
        """Логирование добавления причастного подразделения."""
        from showcase.models import ProjectApplication

        user = make_user(role_code="user")
        status = statuses["await_department"]
        department = Department.objects.create(name="Test Dept", short_name="TD")

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log = service.log_involved_department_added(
            application=app, department=department, actor=user
        )

        assert log.action_type == "involved_department_added"
        assert log.involved_department.id == department.id
        assert log.actor.id == user.id
        assert log.from_status.id == status.id
        assert log.to_status.id == status.id  # Статус не меняется

    def test_log_involved_department_added_validation_errors(self, statuses, make_user):
        """Проверка валидации при добавлении подразделения."""
        from showcase.models import ProjectApplication

        user = make_user(role_code="user")
        status = statuses["await_department"]
        department = Department.objects.create(name="Test Dept", short_name="TD")

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()

        with pytest.raises(ValueError, match="Заявка не может быть None"):
            service.log_involved_department_added(
                application=None, department=department, actor=user
            )

        with pytest.raises(ValueError, match="Подразделение не может быть None"):
            service.log_involved_department_added(
                application=app, department=None, actor=user
            )

    def test_log_involved_department_removed(self, statuses, make_user):
        """Логирование удаления причастного подразделения."""
        from showcase.models import ProjectApplication

        user = make_user(role_code="user")
        status = statuses["await_department"]
        department = Department.objects.create(name="Test Dept", short_name="TD")

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log = service.log_involved_department_removed(
            application=app, department=department, actor=user
        )

        assert log.action_type == "involved_department_removed"
        assert log.involved_department.id == department.id
        assert log.actor.id == user.id


@pytest.mark.django_db
class TestGetLogs:
    """Тесты для получения логов."""

    def test_get_application_logs(self, statuses, make_user):
        """Получение всех логов по заявке."""

        user = make_user(role_code="user")
        status1 = statuses["await_department"]
        status2 = statuses["await_institute"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status1,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log1 = service.log_status_change(
            application=app, from_status=status1, to_status=status2, actor=user
        )
        log2 = service.log_status_change(
            application=app, from_status=status2, to_status=status1, actor=user
        )

        logs = service.get_application_logs(app)

        assert len(logs) == 2
        # Проверяем сортировку по убыванию даты
        assert logs[0].id == log2.id  # Последний лог первый
        assert logs[1].id == log1.id

    def test_get_application_logs_none_application(self):
        """Если application равен None, выбрасывается ValueError."""
        service = ApplicationLoggingService()

        with pytest.raises(ValueError, match="Заявка не может быть None"):
            service.get_application_logs(None)

    def test_get_latest_log(self, statuses, make_user):
        """Получение последнего лога заявки."""

        user = make_user(role_code="user")
        status1 = statuses["await_department"]
        status2 = statuses["await_institute"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status1,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log1 = service.log_status_change(
            application=app, from_status=status1, to_status=status2, actor=user
        )
        log2 = service.log_status_change(
            application=app, from_status=status2, to_status=status1, actor=user
        )

        latest = service.get_latest_log(app)

        assert latest.id == log2.id  # Последний созданный лог

    def test_get_latest_log_none_when_no_logs(self, statuses, make_user):
        """Если логов нет, возвращается None."""

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        latest = service.get_latest_log(app)

        assert latest is None

    def test_get_logs_by_action_type(self, statuses, make_user):
        """Получение логов по типу действия."""

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log1 = service.log_status_change(
            application=app, from_status=status, to_status=status, actor=user
        )
        log2 = service.log_application_update(application=app, actor=user)
        log3 = service.log_status_change(
            application=app, from_status=status, to_status=status, actor=user
        )

        status_logs = service.get_logs_by_action_type(app, "status_change")

        assert len(status_logs) == 2
        assert all(log.action_type == "status_change" for log in status_logs)
        assert log1.id in [log.id for log in status_logs]
        assert log3.id in [log.id for log in status_logs]

    def test_get_logs_by_action_type_empty_type(self, statuses, make_user):
        """Пустой тип действия вызывает ValueError."""

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()

        with pytest.raises(ValueError, match="Тип действия не может быть пустым"):
            service.get_logs_by_action_type(app, "")

    def test_get_logs_by_actor(self, statuses, make_user):
        """Получение логов по актору."""

        user1 = make_user(role_code="user", email="user1@example.com")
        user2 = make_user(role_code="user", email="user2@example.com")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user1,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log1 = service.log_status_change(
            application=app, from_status=status, to_status=status, actor=user1
        )
        log2 = service.log_application_update(application=app, actor=user2)
        log3 = service.log_status_change(
            application=app, from_status=status, to_status=status, actor=user1
        )

        user1_logs = service.get_logs_by_actor(app, user1)

        assert len(user1_logs) == 2
        assert all(log.actor.id == user1.id for log in user1_logs)
        assert log1.id in [log.id for log in user1_logs]
        assert log3.id in [log.id for log in user1_logs]

    def test_get_logs_by_actor_none_application(self):
        """Если application равен None, выбрасывается ValueError."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        service = ApplicationLoggingService()

        # Создаём мок пользователя
        user = Mock(spec=User)
        user.id = 1

        with pytest.raises(ValueError, match="Заявка не может быть None"):
            service.get_logs_by_actor(None, user)


@pytest.mark.django_db
class TestLogApplicationUpdate:
    """Тесты для логирования обновления заявки."""

    def test_log_application_update(self, statuses, make_user):
        """Логирование обновления заявки."""

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()
        log = service.log_application_update(application=app, actor=user)

        assert log.action_type == "application_updated"
        assert log.application.id == app.id
        assert log.actor.id == user.id
        assert log.from_status.id == status.id
        assert log.to_status.id == status.id  # Статус не меняется при обновлении

    def test_log_application_update_validation_errors(self, statuses, make_user):
        """Проверка валидации при логировании обновления."""

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        service = ApplicationLoggingService()

        with pytest.raises(ValueError, match="Заявка не может быть None"):
            service.log_application_update(application=None, actor=user)

        with pytest.raises(ValueError, match="Актор не может быть None"):
            service.log_application_update(application=app, actor=None)
