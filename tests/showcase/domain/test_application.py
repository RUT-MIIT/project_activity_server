"""Unit-тесты для доменной логики ProjectApplicationDomain.

Проверяем все чистые функции бизнес-логики: валидацию, определение статусов, проверку прав доступа.
"""

import pytest

from showcase.domain.application import ProjectApplicationDomain
from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
)


class TestValidateCreate:
    """Тесты для валидации при создании заявки."""

    def test_validate_create_valid_dto(self):
        """Валидный DTO проходит проверку без ошибок."""
        dto = ProjectApplicationCreateDTO(
            company="Acme Corporation",
            title="Valid Project Title",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта для валидации",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert (
            result.is_valid
        ), f"Ожидалась валидность, но получены ошибки: {result.errors}"

    def test_validate_create_title_too_short(self):
        """Название короче 5 символов вызывает ошибку валидации."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Bad",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        assert "title" in result.errors
        assert "минимум 5 символов" in result.errors["title"]

    def test_validate_create_company_too_short(self):
        """Название компании короче 2 символов вызывает ошибку."""
        dto = ProjectApplicationCreateDTO(
            company="A",
            title="Valid Title",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        assert "company" in result.errors

    def test_validate_create_email_too_short(self):
        """Email короче 5 символов вызывает ошибку."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Valid Title",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="x@y",
            author_phone="+79990000000",
            goal="Длинная цель",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        assert "author_email" in result.errors

    def test_validate_create_goal_too_short(self):
        """Цель проекта короче 10 символов вызывает ошибку."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Valid Title",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Short",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        assert "goal" in result.errors

    def test_validate_create_problem_holder_too_short(self):
        """Носитель проблемы короче 5 символов вызывает ошибку."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Valid Title",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель",
            problem_holder="X",
            barrier="Длинный барьер",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        assert "problem_holder" in result.errors

    def test_validate_create_barrier_too_short(self):
        """Барьер короче 10 символов вызывает ошибку."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Valid Title",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель",
            problem_holder="Носитель",
            barrier="Short",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        assert "barrier" in result.errors

    def test_validate_create_author_names_too_short(self):
        """Имя и фамилия автора короче 2 символов вызывают ошибки."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Valid Title",
            author_lastname="И",
            author_firstname="И",
            author_email="user@example.com",
            author_phone="+79990000000",
            goal="Длинная цель",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        assert "author_lastname" in result.errors
        assert "author_firstname" in result.errors

    def test_validate_create_phone_too_short(self):
        """Телефон короче 10 символов вызывает ошибку."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Valid Title",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="user@example.com",
            author_phone="12345",
            goal="Длинная цель",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        assert "author_phone" in result.errors

    def test_validate_create_all_errors_collected(self):
        """Все ошибки валидации собираются в одном результате."""
        dto = ProjectApplicationCreateDTO(
            company="A",
            title="Bad",
            author_lastname="И",
            author_firstname="И",
            author_email="x@",
            author_phone="123",
            goal="short",
            problem_holder="xx",
            barrier="short",
        )
        result = ProjectApplicationDomain.validate_create(dto)
        assert not result.is_valid
        # Проверяем, что все ошибки собраны
        assert len(result.errors) >= 8


class TestValidateUpdate:
    """Тесты для валидации при обновлении заявки."""

    def test_validate_update_valid_fields(self):
        """Валидные поля при обновлении проходят проверку."""
        dto = ProjectApplicationUpdateDTO(
            title="Valid Updated Title",
            goal="Длинная обновлённая цель",
            company="Updated Company Name",
        )
        result = ProjectApplicationDomain.validate_update(dto)
        assert result.is_valid

    def test_validate_update_title_too_short(self):
        """Название короче 5 символов вызывает ошибку."""
        dto = ProjectApplicationUpdateDTO(title="Bad")
        result = ProjectApplicationDomain.validate_update(dto)
        assert not result.is_valid
        assert "title" in result.errors

    def test_validate_update_email_invalid(self):
        """Email без символа @ вызывает ошибку."""
        dto = ProjectApplicationUpdateDTO(author_email="invalid-email")
        result = ProjectApplicationDomain.validate_update(dto)
        assert not result.is_valid
        assert "author_email" in result.errors

    def test_validate_update_only_provided_fields(self):
        """Валидация проверяет только переданные поля (None игнорируются)."""
        dto = ProjectApplicationUpdateDTO(title="Valid Title")
        # Другие поля None - не должны валидироваться
        result = ProjectApplicationDomain.validate_update(dto)
        assert result.is_valid

    def test_validate_update_empty_strings_trigger_errors(self):
        """Пустые строки вызывают ошибки валидации."""
        dto = ProjectApplicationUpdateDTO(
            title="",
            company="",
            goal="",
            author_email="",
        )
        result = ProjectApplicationDomain.validate_update(dto)
        assert not result.is_valid
        # Проверяем наличие ошибок для пустых полей
        assert len(result.errors) >= 4


class TestCalculateInitialStatus:
    """Тесты для определения начального статуса по роли."""

    def test_calculate_initial_status_admin(self):
        """Админ создаёт заявки со статусом approved."""
        status = ProjectApplicationDomain.calculate_initial_status("admin")
        assert status == "approved"

    def test_calculate_initial_status_cpds(self):
        """CPDS создаёт заявки со статусом approved."""
        status = ProjectApplicationDomain.calculate_initial_status("cpds")
        assert status == "approved"

    def test_calculate_initial_status_department_validator(self):
        """Валидатор подразделения создаёт заявки в статусе await_institute."""
        status = ProjectApplicationDomain.calculate_initial_status(
            "department_validator"
        )
        assert status == "await_institute"

    def test_calculate_initial_status_institute_validator(self):
        """Валидатор института создаёт заявки в статусе await_cpds."""
        status = ProjectApplicationDomain.calculate_initial_status(
            "institute_validator"
        )
        assert status == "await_cpds"

    def test_calculate_initial_status_default_user(self):
        """Обычный пользователь создаёт заявки в статусе await_department."""
        status = ProjectApplicationDomain.calculate_initial_status("user")
        assert status == "await_department"

    def test_calculate_initial_status_unknown_role(self):
        """Неизвестная роль возвращает статус await_department по умолчанию."""
        status = ProjectApplicationDomain.calculate_initial_status("unknown_role")
        assert status == "await_department"


class TestCanChangeStatus:
    """Тесты для проверки возможности изменения статуса."""

    def test_can_change_status_allowed_transition(self):
        """Разрешённый переход возвращает True."""
        can_change, error = ProjectApplicationDomain.can_change_status(
            "await_department", "approved_department", "department_validator"
        )
        assert can_change is True
        assert error == ""

    def test_can_change_status_forbidden_transition(self):
        """Запрещённый переход возвращает False с сообщением об ошибке."""
        can_change, error = ProjectApplicationDomain.can_change_status(
            "await_department", "approved", "department_validator"
        )
        assert can_change is False
        assert "запрещен" in error

    def test_can_change_status_approved_requires_admin_or_moderator(self):
        """Переход в approved разрешён только admin или moderator."""
        can_change_admin, _ = ProjectApplicationDomain.can_change_status(
            "await_cpds", "approved", "admin"
        )
        assert can_change_admin is True

        can_change_moderator, _ = ProjectApplicationDomain.can_change_status(
            "await_cpds", "approved", "moderator"
        )
        assert can_change_moderator is True

        can_change_user, error = ProjectApplicationDomain.can_change_status(
            "await_cpds", "approved", "user"
        )
        assert can_change_user is False
        assert "Недостаточно прав" in error

    def test_can_change_status_reject_approved_requires_admin(self):
        """Отклонение одобренной заявки разрешено только админу."""
        can_change_admin, _ = ProjectApplicationDomain.can_change_status(
            "approved", "rejected", "admin"
        )
        assert can_change_admin is True

        can_change_moderator, error = ProjectApplicationDomain.can_change_status(
            "approved", "rejected", "moderator"
        )
        assert can_change_moderator is False
        assert "Только администратор" in error

        can_change_user, error = ProjectApplicationDomain.can_change_status(
            "approved", "rejected", "user"
        )
        assert can_change_user is False

    @pytest.mark.parametrize(
        "current,new,role,expected",
        [
            ("created", "await_department", "user", True),
            ("created", "rejected", "user", True),
            ("await_department", "returned_department", "department_validator", True),
            ("await_institute", "returned_institute", "institute_validator", True),
            ("returned_department", "await_department", "mentor", True),
            ("approved_department", "await_institute", "admin", True),
        ],
    )
    def test_can_change_status_multiple_allowed_transitions(
        self, current, new, role, expected
    ):
        """Проверяем различные разрешённые переходы статусов."""
        can_change, _ = ProjectApplicationDomain.can_change_status(current, new, role)
        assert can_change is expected

    @pytest.mark.parametrize(
        "current,new,role,expected",
        [
            ("await_department", "approved", "user", False),
            ("await_institute", "approved_department", "user", False),
            ("approved", "await_department", "admin", False),
        ],
    )
    def test_can_change_status_multiple_forbidden_transitions(
        self, current, new, role, expected
    ):
        """Проверяем различные запрещённые переходы статусов."""
        can_change, _ = ProjectApplicationDomain.can_change_status(current, new, role)
        assert can_change is expected


class TestCanUserAccessApplication:
    """Тесты для проверки доступа пользователя к заявке."""

    def test_can_user_access_application_author_always_allowed(self):
        """Автор всегда имеет доступ к своей заявке."""
        has_access = ProjectApplicationDomain.can_user_access_application(
            user_role="user", application_author_id=1, user_id=1
        )
        assert has_access is True

    def test_can_user_access_application_admin_allowed(self):
        """Админ имеет доступ ко всем заявкам."""
        has_access = ProjectApplicationDomain.can_user_access_application(
            user_role="admin", application_author_id=1, user_id=2
        )
        assert has_access is True

    def test_can_user_access_application_moderator_allowed(self):
        """Модератор имеет доступ ко всем заявкам."""
        has_access = ProjectApplicationDomain.can_user_access_application(
            user_role="moderator", application_author_id=1, user_id=2
        )
        assert has_access is True

    def test_can_user_access_application_cpds_allowed(self):
        """CPDS имеет доступ ко всем заявкам."""
        has_access = ProjectApplicationDomain.can_user_access_application(
            user_role="cpds", application_author_id=1, user_id=2
        )
        assert has_access is True

    def test_can_user_access_application_department_validator_allowed(self):
        """Валидатор подразделения имеет доступ ко всем заявкам."""
        has_access = ProjectApplicationDomain.can_user_access_application(
            user_role="department_validator", application_author_id=1, user_id=2
        )
        assert has_access is True

    def test_can_user_access_application_institute_validator_allowed(self):
        """Валидатор института имеет доступ ко всем заявкам."""
        has_access = ProjectApplicationDomain.can_user_access_application(
            user_role="institute_validator", application_author_id=1, user_id=2
        )
        assert has_access is True

    def test_can_user_access_application_user_denied_foreign(self):
        """Обычный пользователь не имеет доступа к чужой заявке."""
        has_access = ProjectApplicationDomain.can_user_access_application(
            user_role="user", application_author_id=1, user_id=2
        )
        assert has_access is False

    def test_can_user_access_application_unknown_role_denied(self):
        """Неизвестная роль не имеет доступа к чужой заявке."""
        has_access = ProjectApplicationDomain.can_user_access_application(
            user_role="unknown", application_author_id=1, user_id=2
        )
        assert has_access is False


class TestShouldRequireConsultation:
    """Тесты для определения необходимости консультации."""

    def test_should_require_consultation_empty_project_level(self):
        """Если уровень проекта не указан, нужна консультация."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            project_level="",  # Пустой уровень
            target_institutes=["INST1"],
            goal="Достаточно длинная цель проекта для консультации проверки",
        )
        requires = ProjectApplicationDomain.should_require_consultation(dto)
        assert requires is True

    def test_should_require_consultation_no_target_institutes(self):
        """Если целевые институты не указаны, нужна консультация."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            project_level="L1",
            target_institutes=[],  # Пустой список
            goal="Достаточно длинная цель проекта для консультации проверки",
        )
        requires = ProjectApplicationDomain.should_require_consultation(dto)
        assert requires is True

    def test_should_require_consultation_short_goal(self):
        """Если цель проекта короче 50 символов, нужна консультация."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            project_level="L1",
            target_institutes=["INST1"],
            goal="Короткая цель",  # Меньше 50 символов
        )
        requires = ProjectApplicationDomain.should_require_consultation(dto)
        assert requires is True

    def test_should_require_consultation_all_conditions_met(self):
        """Если все условия выполнены, консультация не требуется."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            project_level="L1",  # Уровень указан
            target_institutes=["INST1", "INST2"],  # Институты указаны
            goal="Достаточно длинная цель проекта для консультации проверки длиннее 50 символов",  # > 50 символов
        )
        requires = ProjectApplicationDomain.should_require_consultation(dto)
        assert requires is False

    def test_should_require_consultation_none_project_level(self):
        """Если project_level равен None, нужна консультация."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            project_level=None,
            target_institutes=["INST1"],
            goal="Достаточно длинная цель проекта для консультации проверки",
        )
        requires = ProjectApplicationDomain.should_require_consultation(dto)
        assert requires is True

    def test_should_require_consultation_none_target_institutes(self):
        """Если target_institutes равен None, нужна консультация."""
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            project_level="L1",
            target_institutes=None,
            goal="Достаточно длинная цель проекта для консультации проверки",
        )
        requires = ProjectApplicationDomain.should_require_consultation(dto)
        assert requires is True
