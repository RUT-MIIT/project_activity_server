import pytest

from showcase.domain.capabilities import ApplicationCapabilities
from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
)


class TestSubmitApplication:
    def test_submit_valid(self):
        """Проверяем, что валидный DTO проходит валидацию без ошибок."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Valid title",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_phone="+79990000000",
            author_email="user@example.com",
            goal="Цель проекта достаточно длинная строка 12345",
            problem_holder="Носитель",
            barrier="Длинное описание барьера",
        )
        result = ApplicationCapabilities.submit_application(dto, user_role="user")
        assert result.is_valid, result.errors

    def test_submit_invalid_collects_errors(self):
        """Невалидные поля аккумулируют ошибки в ValidationResult."""
        dto = ProjectApplicationCreateDTO(
            company="A",
            title="bad",
            author_lastname="I",
            author_firstname="I",
            author_phone="123",
            author_email="x@",
            goal="short",
            problem_holder="xx",
            barrier="short",
        )
        result = ApplicationCapabilities.submit_application(dto, user_role="user")
        assert not result.is_valid
        # Проверяем наличие ключевых ошибок
        for field in [
            "title",
            "company",
            "author_email",
            "goal",
            "problem_holder",
            "barrier",
            "author_lastname",
            "author_firstname",
            "author_phone",
        ]:
            assert field in result.errors


class TestApproveRejectRequest:
    @pytest.mark.parametrize(
        "status,role,expected",
        [
            ("await_department", "department_validator", True),
            ("await_institute", "department_validator", False),
            ("await_institute", "institute_validator", True),
            ("await_cpds", "cpds", True),
        ],
    )
    def test_approve_allowed_matrix(self, status, role, expected):
        """Матрица прав определяет доступность approve для ролей и статусов."""
        ok, _ = ApplicationCapabilities.approve_application(
            application_status=status,
            approver_role=role,
            is_user_department_involved=True,
            is_user_author=False,
        )
        assert ok is expected

    @pytest.mark.parametrize(
        "status,role,expected",
        [
            ("await_department", "department_validator", True),
            ("await_institute", "institute_validator", True),
            ("await_cpds", "cpds", True),
        ],
    )
    def test_reject_allowed_matrix(self, status, role, expected):
        """Матрица прав определяет доступность reject."""
        ok, _ = ApplicationCapabilities.reject_application(
            application_status=status,
            rejector_role=role,
            is_user_department_involved=True,
            is_user_author=False,
        )
        assert ok is expected

    @pytest.mark.parametrize(
        "status,role,dept_involved,own,expected",
        [
            ("returned_department", "mentor", False, True, False),
            ("returned_department", "mentor", False, False, False),
            ("returned_institute", "department_validator", True, False, False),
            ("returned_institute", "department_validator", False, False, False),
        ],
    )
    def test_request_changes_matrix(self, status, role, dept_involved, own, expected):
        """Для returned_* действует агрегирующее правило returned_(all)."""
        ok, _ = ApplicationCapabilities.request_changes(
            application_status=status,
            requester_role=role,
            is_user_department_involved=dept_involved,
            is_user_author=own,
        )
        assert ok is expected


class TestUpdateApplication:
    def test_update_ok(self, monkeypatch):
        """При валидных данных и доступе возвращается валидный результат без ошибок."""
        dto = ProjectApplicationUpdateDTO(
            title="Valid title", goal="Длинная цель 12345"
        )

        # Гарантируем, что доменная валидация вернёт ok для данного DTO
        result, can_update, _ = ApplicationCapabilities.update_application(
            dto=dto,
            application_status="await_department",
            updater_role="admin",
            application_author_id=1,
            updater_id=1,
        )
        assert result.is_valid
        assert can_update is True

    def test_update_errors_on_access_and_status(self):
        """Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult."""
        dto = ProjectApplicationUpdateDTO(title="Valid title")
        # Статус rejected всегда запрещён для обновления
        result, can_update, _ = ApplicationCapabilities.update_application(
            dto=dto,
            application_status="rejected",
            updater_role="user",
            application_author_id=2,
            updater_id=1,
        )
        assert not result.is_valid
        assert "status" in result.errors or "access" in result.errors

        # approved запрещён для не-админов
        result2, can_update2, _ = ApplicationCapabilities.update_application(
            dto=dto,
            application_status="approved",
            updater_role="user",
            application_author_id=2,
            updater_id=1,
        )
        assert not result2.is_valid
        assert "status" in result2.errors


class TestViewAndList:
    def test_view_allowed_for_author(self):
        """Автор всегда имеет доступ к просмотру своей заявки."""
        ok, _ = ApplicationCapabilities.view_application(
            application_status="await_department",
            viewer_role="user",
            application_author_id=1,
            viewer_id=1,
        )
        assert ok is True

    def test_view_denied_for_foreign_user(self):
        """Обычному пользователю чужая заявка недоступна."""
        ok, _ = ApplicationCapabilities.view_application(
            application_status="await_department",
            viewer_role="user",
            application_author_id=1,
            viewer_id=2,
        )
        assert ok is False

    def test_list_applications_always_true(self):
        """Список заявок разрешён всем (возвращает True)."""
        ok, _ = ApplicationCapabilities.list_applications("any")
        assert ok is True


class TestHelpers:
    def test_is_action_allowed_policies(self):
        """Проверяем интерпретацию политик '+', '-', 'только своего подразделения', 'только свои'."""
        # Разрешено (+)
        assert ApplicationCapabilities.is_action_allowed(
            action="approve",
            current_status="await_cpds",
            user_role="cpds",
            is_user_department_involved=False,
            is_user_author=False,
        )

        # Запрещено (-)
        assert not ApplicationCapabilities.is_action_allowed(
            action="approve",
            current_status="await_department",
            user_role="mentor",
            is_user_department_involved=False,
            is_user_author=False,
        )

        # Требует участия подразделения
        assert ApplicationCapabilities.is_action_allowed(
            action="approve",
            current_status="await_department",
            user_role="department_validator",
            is_user_department_involved=True,
            is_user_author=False,
        )
        assert not ApplicationCapabilities.is_action_allowed(
            action="approve",
            current_status="await_department",
            user_role="department_validator",
            is_user_department_involved=False,
            is_user_author=False,
        )

        # Только свои
        assert ApplicationCapabilities.is_action_allowed(
            action="approve",
            current_status="returned_(all)",
            user_role="mentor",
            is_user_department_involved=False,
            is_user_author=True,
        )
