"""Unit-тесты для DTO классов в showcase.dto.application.

Проверяем создание, преобразование в словари, работу со связанными объектами.
"""

from unittest.mock import Mock

import pytest

from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationListDTO,
    ProjectApplicationReadDTO,
    ProjectApplicationUpdateDTO,
    serialize_comment_author,
)


class TestSerializeCommentAuthor:
    """Тесты для функции serialize_comment_author."""

    def test_serialize_comment_author_none(self):
        """Если author равен None, возвращаются None значения."""
        result = serialize_comment_author(None)
        assert result == {
            "id": None,
            "name": None,
            "role_name": None,
            "department_name": None,
        }

    def test_serialize_comment_author_full_data(self):
        """Сериализация автора с полными данными: имя, фамилия, отчество, роль, подразделение."""
        # Создаём мок объекта пользователя
        role = Mock()
        role.name = "Валидатор"

        department = Mock()
        department.name = "Отдел разработки"

        author = Mock()
        author.id = 1
        author.first_name = "Иван"
        author.last_name = "Иванов"
        author.middle_name = "Петрович"
        author.role = role
        author.department = department

        result = serialize_comment_author(author)

        assert result["id"] == 1
        assert result["name"] == "Иван Иванов"
        assert result["short_name"] == "Иванов И. П."
        assert result["role_name"] == "Валидатор"
        assert result["department_name"] == "Отдел разработки"

    def test_serialize_comment_author_without_middle_name(self):
        """Сериализация автора без отчества."""
        author = Mock()
        author.id = 1
        author.first_name = "Иван"
        author.last_name = "Иванов"
        author.middle_name = None
        author.role = None
        author.department = None

        result = serialize_comment_author(author)

        assert result["short_name"] == "Иванов И."
        assert result["role_name"] is None
        assert result["department_name"] is None

    def test_serialize_comment_author_without_role_and_department(self):
        """Сериализация автора без роли и подразделения."""
        author = Mock()
        author.id = 1
        author.first_name = "Иван"
        author.last_name = "Иванов"
        author.middle_name = "Петрович"
        author.role = None
        author.department = None

        # Проверяем, что функция корректно обрабатывает отсутствие role и department
        result = serialize_comment_author(author)

        assert result["role_name"] is None
        assert result["department_name"] is None

    def test_serialize_comment_author_minimal_data(self):
        """Сериализация автора с минимальными данными (только last_name)."""
        author = Mock()
        author.id = 1
        author.first_name = None
        author.last_name = "Иванов"
        author.middle_name = None
        author.role = None
        author.department = None

        result = serialize_comment_author(author)

        assert result["short_name"] == "Иванов"
        assert result["name"] is None


class TestProjectApplicationCreateDTO:
    """Тесты для ProjectApplicationCreateDTO."""

    def test_create_dto_from_dict(self):
        """Создание DTO из словаря через from_dict."""
        data = {
            "company": "Acme Corp",
            "title": "Test Project",
            "author_lastname": "Иванов",
            "author_firstname": "Иван",
            "goal": "Длинная цель",
            "target_institutes": ["INST1"],
        }
        dto = ProjectApplicationCreateDTO.from_dict(data)

        assert dto.company == "Acme Corp"
        assert dto.title == "Test Project"
        assert dto.author_lastname == "Иванов"
        assert dto.target_institutes == ["INST1"]

    def test_create_dto_to_dict(self):
        """Преобразование DTO в словарь через to_dict."""
        dto = ProjectApplicationCreateDTO(
            company="Acme Corp",
            title="Test Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель",
            problem_holder="Носитель",
            barrier="Барьер",
            target_institutes=["INST1", "INST2"],
            needs_consultation=True,
        )

        result = dto.to_dict()

        assert result["company"] == "Acme Corp"
        assert result["title"] == "Test Project"
        assert result["author_lastname"] == "Иванов"
        assert result["target_institutes"] == ["INST1", "INST2"]
        assert result["needs_consultation"] is True
        assert "goal" in result
        assert "problem_holder" in result

    def test_create_dto_default_values(self):
        """Проверяем значения по умолчанию: пустые строки для title, company_contacts, пустой список для target_institutes."""
        dto = ProjectApplicationCreateDTO(company="Acme")

        assert dto.title == ""
        assert dto.company_contacts == ""
        assert dto.target_institutes == []
        assert dto.needs_consultation is False


class TestProjectApplicationUpdateDTO:
    """Тесты для ProjectApplicationUpdateDTO."""

    def test_update_dto_from_dict(self):
        """Создание DTO для обновления из словаря."""
        data = {
            "title": "Updated Title",
            "goal": "Updated Goal",
            "company": "Updated Company",
        }
        dto = ProjectApplicationUpdateDTO.from_dict(data)

        assert dto.title == "Updated Title"
        assert dto.goal == "Updated Goal"
        assert dto.company == "Updated Company"

    def test_update_dto_to_dict_excludes_none(self):
        """to_dict исключает поля со значением None, оставляя только заполненные."""
        dto = ProjectApplicationUpdateDTO(
            title="Updated Title",
            goal=None,  # None значение не должно попасть в словарь
            company="Updated Company",
            author_email=None,
        )

        result = dto.to_dict()

        assert "title" in result
        assert "company" in result
        assert "goal" not in result  # None значения исключены
        assert "author_email" not in result

    def test_update_dto_to_dict_includes_all_provided_fields(self):
        """to_dict включает все поля, которые не None."""
        dto = ProjectApplicationUpdateDTO(
            title="Title",
            company="Company",
            goal="Goal",
            problem_holder="Holder",
            barrier="Barrier",
        )

        result = dto.to_dict()

        # Все переданные поля должны быть в словаре
        assert len(result) >= 5
        assert "title" in result
        assert "company" in result
        assert "goal" in result


@pytest.mark.django_db
class TestProjectApplicationReadDTO:
    """Тесты для ProjectApplicationReadDTO."""

    def test_read_dto_basic_fields(self, statuses, make_user):
        """Базовые поля DTO заполняются из модели заявки."""
        from showcase.models import ProjectApplication

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test App",
            company="Acme Corp",
            author=user,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        dto = ProjectApplicationReadDTO(app)

        assert dto.id == app.id
        assert dto.title == "Test App"
        assert dto.company == "Acme Corp"
        assert dto.status == {"code": "await_department", "name": "await_department"}

    def test_read_dto_status_none(self, make_user):
        """Если статус заявки None, DTO.status тоже None."""
        from showcase.models import ProjectApplication

        user = make_user(role_code="user")

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=None,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        dto = ProjectApplicationReadDTO(app)
        assert dto.status is None

    def test_read_dto_author_none(self, statuses):
        """Если автор заявки None, DTO.author тоже None."""
        from showcase.models import ProjectApplication

        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=None,
            status=status,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        dto = ProjectApplicationReadDTO(app)
        assert dto.author is None

    def test_read_dto_target_institutes(self, statuses, make_user):
        """target_institutes сериализуется как список словарей с code и name."""
        from showcase.models import Institute, ProjectApplication

        user = make_user(role_code="user")
        status = statuses["await_department"]

        inst1 = Institute.objects.create(code="INST1", name="Institute 1", position=1)
        inst2 = Institute.objects.create(code="INST2", name="Institute 2", position=2)

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
        app.target_institutes.add(inst1, inst2)

        dto = ProjectApplicationReadDTO(app)

        assert len(dto.target_institutes) == 2
        assert {"code": "INST1", "name": "Institute 1"} in dto.target_institutes
        assert {"code": "INST2", "name": "Institute 2"} in dto.target_institutes

    def test_read_dto_involved_users(self, statuses, make_user):
        """involved_users сериализуется с данными пользователя, added_at и added_by."""
        from showcase.models import ApplicationInvolvedUser, ProjectApplication

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

        involved = ApplicationInvolvedUser.objects.create(
            application=app, user=user2, added_by=user1
        )

        dto = ProjectApplicationReadDTO(app)

        assert len(dto.involved_users) == 1
        involved_data = dto.involved_users[0]
        assert involved_data["user"]["id"] == user2.id
        assert involved_data["user"]["email"] == "user2@example.com"
        assert involved_data["added_by"]["id"] == user1.id

    def test_read_dto_involved_departments(self, statuses, make_user):
        """involved_departments сериализуется с данными подразделения."""
        from accounts.models import Department
        from showcase.models import ApplicationInvolvedDepartment, ProjectApplication

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

        involved = ApplicationInvolvedDepartment.objects.create(
            application=app, department=department, added_by=user
        )

        dto = ProjectApplicationReadDTO(app)

        assert len(dto.involved_departments) == 1
        dept_data = dto.involved_departments[0]
        assert dept_data["department"]["id"] == department.id
        assert dept_data["department"]["name"] == "Test Dept"
        assert dept_data["added_by"]["id"] == user.id

    def test_read_dto_comments_with_exception(self, statuses, make_user):
        """Если при получении комментариев возникает исключение, comments становится пустым списком."""
        from showcase.models import ProjectApplication

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

        # Ломаем доступ к comments, чтобы вызвать исключение
        app.comments = Mock()
        app.comments.all = Mock(side_effect=Exception("Database error"))

        dto = ProjectApplicationReadDTO(app)
        assert dto.comments == []

    def test_read_dto_to_dict(self, statuses, make_user):
        """to_dict преобразует DTO в словарь для JSON, включая ISO формат даты."""
        from showcase.models import ProjectApplication

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

        dto = ProjectApplicationReadDTO(app)
        result = dto.to_dict()

        assert "id" in result
        assert "title" in result
        assert "creation_date" in result
        assert isinstance(result["creation_date"], str)  # ISO формат
        assert "status" in result
        assert "author" in result
        assert "target_institutes" in result
        assert "involved_users" in result
        assert "comments" in result


@pytest.mark.django_db
class TestProjectApplicationListDTO:
    """Тесты для ProjectApplicationListDTO."""

    def test_list_dto_basic_fields(self, statuses, make_user):
        """Базовые поля DTO для списка заполняются из модели."""
        from showcase.models import ProjectApplication

        user = make_user(role_code="user")
        status = statuses["await_department"]

        app = ProjectApplication.objects.create(
            title="Test App",
            company="Acme Corp",
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

        dto = ProjectApplicationListDTO(app)

        assert dto.id == app.id
        assert dto.title == "Test App"
        assert dto.company == "Acme Corp"
        assert dto.status == {"code": "await_department", "name": "await_department"}
        assert dto.author_name == "Иванов Иван"
        assert dto.author_email == "test@example.com"

    def test_list_dto_status_none(self, make_user):
        """Если статус None, DTO.status тоже None."""
        from showcase.models import ProjectApplication

        user = make_user(role_code="user")

        app = ProjectApplication.objects.create(
            title="Test",
            company="Acme",
            author=user,
            status=None,
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель",
            problem_holder="Носитель",
            barrier="Барьер",
        )

        dto = ProjectApplicationListDTO(app)
        assert dto.status is None

    def test_list_dto_to_dict(self, statuses, make_user):
        """to_dict преобразует DTO в словарь с ISO форматированием даты."""
        from showcase.models import ProjectApplication

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

        dto = ProjectApplicationListDTO(app)
        result = dto.to_dict()

        assert "id" in result
        assert "title" in result
        assert "creation_date" in result
        assert isinstance(result["creation_date"], str)  # ISO формат
        assert "status" in result
        assert "author_name" in result
        assert "author_email" in result
