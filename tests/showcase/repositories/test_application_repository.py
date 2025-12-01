"""Unit-тесты для репозитория ProjectApplicationRepository.

Проверяем все методы работы с БД: создание, чтение, обновление, удаление, фильтрация.
"""

from django.contrib.auth import get_user_model
import pytest

from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
)
from showcase.models import (
    ApplicationInvolvedUser,
    ApplicationStatus,
    Institute,
    ProjectApplication,
    Tag,
)
from showcase.repositories.application import ProjectApplicationRepository

User = get_user_model()


@pytest.mark.django_db
class TestRepositoryCreate:
    """Тесты для метода create репозитория."""

    def test_create_with_target_institutes(self, statuses, make_user):
        """Создание заявки с целевыми институтами: проверяем установку M2M связи.

        Проверяем, что target_institutes устанавливается корректно при создании заявки.
        """
        # Создаём институты для теста
        inst1 = Institute.objects.create(code="INST1", name="Institute 1", position=1)
        inst2 = Institute.objects.create(code="INST2", name="Institute 2", position=2)

        user = make_user(role_code="user")
        dto = ProjectApplicationCreateDTO(
            company="Acme Corp",
            title="Test Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
            target_institutes=["INST1", "INST2"],  # Проверяем установку M2M
        )

        repo = ProjectApplicationRepository()
        app = repo.create(dto, user, "await_department")

        assert app.id is not None
        assert app.target_institutes.count() == 2
        assert inst1 in app.target_institutes.all()
        assert inst2 in app.target_institutes.all()

    def test_create_without_target_institutes(self, statuses, make_user):
        """Создание заявки без целевых институтов: проверяем, что пустой список не вызывает ошибок."""
        user = make_user(role_code="user")
        dto = ProjectApplicationCreateDTO(
            company="Acme Corp",
            title="Test Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
            target_institutes=[],  # Пустой список
        )

        repo = ProjectApplicationRepository()
        app = repo.create(dto, user, "await_department")

        assert app.id is not None
        assert app.target_institutes.count() == 0

    def test_create_with_tags(self, statuses, make_user):
        """Создание заявки с тегами: проверяем установку M2M связи.

        Проверяем, что tags устанавливается корректно при создании заявки.
        """
        # Создаём теги для теста
        tag1 = Tag.objects.create(name="Тег 1", category="Категория 1")
        tag2 = Tag.objects.create(name="Тег 2", category="Категория 1")

        user = make_user(role_code="user")
        dto = ProjectApplicationCreateDTO(
            company="Acme Corp",
            title="Test Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
            tags=[tag1.id, tag2.id],  # Проверяем установку M2M
        )

        repo = ProjectApplicationRepository()
        app = repo.create(dto, user, "await_department")

        assert app.id is not None
        assert app.tags.count() == 2
        assert tag1 in app.tags.all()
        assert tag2 in app.tags.all()

    def test_create_without_tags(self, statuses, make_user):
        """Создание заявки без тегов: проверяем, что пустой список не вызывает ошибок."""
        user = make_user(role_code="user")
        dto = ProjectApplicationCreateDTO(
            company="Acme Corp",
            title="Test Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
            tags=[],  # Пустой список
        )

        repo = ProjectApplicationRepository()
        app = repo.create(dto, user, "await_department")

        assert app.id is not None
        assert app.tags.count() == 0

    def test_create_with_is_external_true(self, statuses, make_user):
        """Создание заявки с is_external=True: проверяем установку флага."""
        user = make_user(role_code="user")
        dto = ProjectApplicationCreateDTO(
            company="Acme Corp",
            title="External Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
        )

        repo = ProjectApplicationRepository()
        app = repo.create(dto, user, "await_department", is_external=True)

        assert app.id is not None
        assert app.is_external is True

    def test_create_with_is_external_false(self, statuses, make_user):
        """Создание заявки с is_external=False: проверяем установку флага по умолчанию."""
        user = make_user(role_code="user")
        dto = ProjectApplicationCreateDTO(
            company="Acme Corp",
            title="Internal Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
        )

        repo = ProjectApplicationRepository()
        app = repo.create(dto, user, "await_department", is_external=False)

        assert app.id is not None
        assert app.is_external is False

    def test_create_with_is_external_default(self, statuses, make_user):
        """Создание заявки без указания is_external: проверяем значение по умолчанию (False)."""
        user = make_user(role_code="user")
        dto = ProjectApplicationCreateDTO(
            company="Acme Corp",
            title="Default Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
        )

        repo = ProjectApplicationRepository()
        app = repo.create(dto, user, "await_department")

        assert app.id is not None
        assert app.is_external is False


@pytest.mark.django_db
class TestRepositoryGetById:
    """Тесты для методов получения заявок по ID."""

    def test_get_by_id_with_prefetch(self, statuses, make_user):
        """get_by_id возвращает заявку с оптимизированными запросами (prefetch_related)."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app = repo.create(dto, user, "await_department")

        # Проверяем, что метод возвращает заявку
        retrieved = repo.get_by_id(app.id)
        assert retrieved.id == app.id
        assert retrieved.status.code == "await_department"

    def test_get_by_id_simple(self, statuses, make_user):
        """get_by_id_simple возвращает заявку без дополнительных prefetch."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app = repo.create(dto, user, "await_department")

        retrieved = repo.get_by_id_simple(app.id)
        assert retrieved.id == app.id


@pytest.mark.django_db
class TestRepositoryFilter:
    """Тесты для методов фильтрации заявок."""

    def test_filter_coordination_by_user_queryset(self, statuses, make_user):
        """filter_coordination_by_user_queryset возвращает QuerySet заявок для координации (в работе) для пагинации."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        # Создаём заявки: одну в работе, одну одобренную
        dto1 = ProjectApplicationCreateDTO(
            company="Acme",
            title="In Work",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app1 = repo.create(dto1, user, "await_department")
        ApplicationInvolvedUser.objects.create(application=app1, user=user)

        dto2 = ProjectApplicationCreateDTO(
            company="Acme2",
            title="Approved",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="test2@example.com",
            author_phone="+79990000001",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app2 = repo.create(dto2, user, "approved")
        ApplicationInvolvedUser.objects.create(application=app2, user=user)

        qs = repo.filter_coordination_by_user_queryset(user)
        assert hasattr(qs, "filter")  # QuerySet
        results = list(qs)
        assert len(results) == 1
        assert results[0].id == app1.id

    def test_filter_by_status_queryset(self, statuses, make_user):
        """filter_by_status_queryset возвращает QuerySet заявок по статусу."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app = repo.create(dto, user, "await_department")

        qs = repo.filter_by_status_queryset("await_department")
        assert hasattr(qs, "filter")  # QuerySet
        results = list(qs)
        assert app.id in [a.id for a in results]

    def test_filter_by_company(self, statuses, make_user):
        """filter_by_company ищет заявки по названию компании (case-insensitive)."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        dto1 = ProjectApplicationCreateDTO(
            company="Acme Corporation",
            title="Test1",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app1 = repo.create(dto1, user, "await_department")

        dto2 = ProjectApplicationCreateDTO(
            company="Other Corp",
            title="Test2",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="test2@example.com",
            author_phone="+79990000001",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        repo.create(dto2, user, "await_department")

        results = repo.filter_by_company("Acme")
        assert len(results) == 1
        assert results[0].id == app1.id

        # Проверяем case-insensitive поиск
        results_lower = repo.filter_by_company("acme")
        assert len(results_lower) == 1


@pytest.mark.django_db
class TestRepositoryUpdate:
    """Тесты для методов обновления заявок."""

    def test_update_with_target_institutes(self, statuses, make_user):
        """Обновление заявки с изменением целевых институтов: проверяем установку M2M связи."""
        inst1 = Institute.objects.create(code="INST1", name="Institute 1", position=1)
        inst2 = Institute.objects.create(code="INST2", name="Institute 2", position=2)
        inst3 = Institute.objects.create(code="INST3", name="Institute 3", position=3)

        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
            target_institutes=["INST1"],
        )
        app = repo.create(dto, user, "await_department")
        assert app.target_institutes.count() == 1

        # Обновляем с новым списком институтов
        update_dto = ProjectApplicationUpdateDTO(
            title="Updated Title",
            target_institutes=["INST2", "INST3"],  # Изменяем список
        )
        updated_app = repo.update(app, update_dto)

        assert updated_app.title == "Updated Title"
        assert updated_app.target_institutes.count() == 2
        assert inst2 in updated_app.target_institutes.all()
        assert inst3 in updated_app.target_institutes.all()

    def test_update_with_tags(self, statuses, make_user):
        """Обновление заявки с изменением тегов: проверяем установку M2M связи."""
        tag1 = Tag.objects.create(name="Тег 1", category="Категория 1")
        tag2 = Tag.objects.create(name="Тег 2", category="Категория 1")
        tag3 = Tag.objects.create(name="Тег 3", category="Категория 2")

        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
            tags=[tag1.id],
        )
        app = repo.create(dto, user, "await_department")
        assert app.tags.count() == 1

        # Обновляем с новым списком тегов
        update_dto = ProjectApplicationUpdateDTO(
            title="Updated Title",
            tags=[tag2.id, tag3.id],  # Изменяем список
        )
        updated_app = repo.update(app, update_dto)

        assert updated_app.title == "Updated Title"
        assert updated_app.tags.count() == 2
        assert tag2 in updated_app.tags.all()
        assert tag3 in updated_app.tags.all()

    def test_update_without_fields(self, statuses, make_user):
        """Обновление заявки без полей: проверяем вызов save() без update_fields."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app = repo.create(dto, user, "await_department")
        original_title = app.title

        # Обновляем с пустым DTO (все поля None)
        update_dto = ProjectApplicationUpdateDTO()
        updated_app = repo.update(app, update_dto)

        # Заявка должна остаться без изменений, но save() должен быть вызван
        assert updated_app.title == original_title

    def test_update_status(self, statuses, make_user):
        """update_status изменяет статус заявки."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app = repo.create(dto, user, "await_department")
        assert app.status.code == "await_department"

        updated_app = repo.update_status(app, "await_institute")
        assert updated_app.status.code == "await_institute"

        # Проверяем, что изменения сохранились в БД
        app.refresh_from_db()
        assert app.status.code == "await_institute"


@pytest.mark.django_db
class TestRepositoryDeleteAndExists:
    """Тесты для методов удаления и проверки существования."""

    def test_delete(self, statuses, make_user):
        """delete удаляет заявку и возвращает True."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app = repo.create(dto, user, "await_department")
        app_id = app.id

        result = repo.delete(app)
        assert result is True
        assert not ProjectApplication.objects.filter(pk=app_id).exists()

    def test_exists_true(self, statuses, make_user):
        """exists возвращает True для существующей заявки."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app = repo.create(dto, user, "await_department")

        assert repo.exists(app.id) is True

    def test_exists_false(self):
        """exists возвращает False для несуществующей заявки."""
        repo = ProjectApplicationRepository()
        assert repo.exists(99999) is False


@pytest.mark.django_db
class TestRepositoryCount:
    """Тесты для методов подсчёта заявок."""

    def test_count_by_user(self, statuses, make_user):
        """count_by_user возвращает количество заявок автора."""
        user1 = make_user(role_code="user")
        user2 = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        # Создаём 2 заявки для user1
        for i in range(2):
            dto = ProjectApplicationCreateDTO(
                company=f"Acme{i}",
                title=f"Test{i}",
                author_lastname="Иванов",
                author_firstname="Иван",
                author_email=f"test{i}@example.com",
                author_phone=f"+7999000000{i}",
                goal="Длинная цель 1234567890",
                problem_holder="Носитель",
                barrier="Длинный барьер",
            )
            repo.create(dto, user1, "await_department")

        # Создаём 1 заявку для user2
        dto = ProjectApplicationCreateDTO(
            company="Other",
            title="Test",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="other@example.com",
            author_phone="+79990000010",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        repo.create(dto, user2, "await_department")

        assert repo.count_by_user(user1) == 2
        assert repo.count_by_user(user2) == 1

    def test_count_by_status(self, statuses, make_user):
        """count_by_status возвращает количество заявок с указанным статусом."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        # Создаём заявки с разными статусами
        for status_code in ["await_department", "await_institute", "await_department"]:
            dto = ProjectApplicationCreateDTO(
                company="Acme",
                title="Test",
                author_lastname="Иванов",
                author_firstname="Иван",
                author_email="test@example.com",
                author_phone="+79990000000",
                goal="Длинная цель 1234567890",
                problem_holder="Носитель",
                barrier="Длинный барьер",
            )
            repo.create(dto, user, status_code)

        assert repo.count_by_status("await_department") == 2
        assert repo.count_by_status("await_institute") == 1
        assert repo.count_by_status("approved") == 0


@pytest.mark.django_db
class TestRepositoryFilterExternal:
    """Тесты для методов фильтрации внешних заявок."""

    def test_filter_external_applications(self, statuses, make_user):
        """filter_external_applications возвращает только заявки с is_external=True."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        # Создаём внешнюю заявку
        dto_external = ProjectApplicationCreateDTO(
            company="External Corp",
            title="External Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="external@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
        )
        app_external = repo.create(
            dto_external, user, "await_department", is_external=True
        )

        # Создаём обычную заявку
        dto_internal = ProjectApplicationCreateDTO(
            company="Internal Corp",
            title="Internal Project",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="internal@example.com",
            author_phone="+79990000001",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
        )
        app_internal = repo.create(
            dto_internal, user, "await_department", is_external=False
        )

        # Получаем внешние заявки
        external_apps = repo.filter_external_applications()

        # Проверяем, что только внешняя заявка в списке
        external_ids = {app.id for app in external_apps}
        assert app_external.id in external_ids
        assert app_internal.id not in external_ids

    def test_filter_external_applications_queryset(self, statuses, make_user):
        """filter_external_applications_queryset возвращает QuerySet внешних заявок."""
        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        # Создаём внешнюю заявку
        dto_external = ProjectApplicationCreateDTO(
            company="External Corp",
            title="External Project",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="external@example.com",
            author_phone="+79990000000",
            goal="Цель проекта достаточно длинная",
            problem_holder="Носитель проблемы",
            barrier="Описание барьера достаточно длинное",
        )
        app_external = repo.create(
            dto_external, user, "await_department", is_external=True
        )

        # Получаем QuerySet внешних заявок
        qs = repo.filter_external_applications_queryset()

        assert hasattr(qs, "filter")  # QuerySet
        results = list(qs)
        assert len(results) == 1
        assert results[0].id == app_external.id
        assert results[0].is_external is True


@pytest.mark.django_db
class TestRepositoryApplicationNumbering:
    """Тесты для генерации номеров заявок."""

    def test_first_application_gets_number_one(self, statuses, make_user):
        """Первая заявка в году получает номер 1."""
        from django.utils import timezone

        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()
        dto = ProjectApplicationCreateDTO(
            company="Acme",
            title="Test",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test@example.com",
            author_phone="+79990000000",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )

        app = repo.create(dto, user, "await_department")

        current_year = timezone.now().year
        assert app.application_year == current_year
        assert app.year_sequence_number == 1
        assert app.print_number == f"{str(current_year)[-2:]}-00001"

    def test_sequential_numbering_in_same_year(self, statuses, make_user):
        """Номера последовательно увеличиваются в пределах одного года."""
        from django.utils import timezone

        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()
        current_year = timezone.now().year

        # Создаём несколько заявок
        for i in range(5):
            dto = ProjectApplicationCreateDTO(
                company=f"Acme{i}",
                title=f"Test{i}",
                author_lastname="Иванов",
                author_firstname="Иван",
                author_email=f"test{i}@example.com",
                author_phone=f"+7999000000{i}",
                goal="Длинная цель 1234567890",
                problem_holder="Носитель",
                barrier="Длинный барьер",
            )
            app = repo.create(dto, user, "await_department")
            assert app.application_year == current_year
            assert app.year_sequence_number == i + 1
            assert app.print_number == f"{str(current_year)[-2:]}-{i+1:05d}"

    def test_numbering_respects_gaps(self, statuses, make_user):
        """Нумерация учитывает пропуски - использует максимальный номер, а не count()."""
        from django.utils import timezone

        from showcase.models import ProjectApplication

        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()
        current_year = timezone.now().year

        # Создаём первую заявку
        dto1 = ProjectApplicationCreateDTO(
            company="Acme1",
            title="Test1",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="test1@example.com",
            author_phone="+79990000001",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app1 = repo.create(dto1, user, "await_department")
        assert app1.year_sequence_number == 1

        # Вручную создаём заявку с номером 5 (имитируем пропуск)
        app_manual = ProjectApplication.objects.create(
            company="Manual",
            title="Manual",
            author=user,
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="manual@example.com",
            author_phone="+79990000002",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
            status=ApplicationStatus.objects.get(code="await_department"),
            application_year=current_year,
            year_sequence_number=5,
            print_number=f"{str(current_year)[-2:]}-00005",
        )

        # Создаём следующую заявку - она должна получить номер 6, а не 3
        dto2 = ProjectApplicationCreateDTO(
            company="Acme2",
            title="Test2",
            author_lastname="Сидоров",
            author_firstname="Сидор",
            author_email="test2@example.com",
            author_phone="+79990000003",
            goal="Длинная цель 1234567890",
            problem_holder="Носитель",
            barrier="Длинный барьер",
        )
        app2 = repo.create(dto2, user, "await_department")
        assert app2.year_sequence_number == 6
        assert app2.print_number == f"{str(current_year)[-2:]}-00006"

    def test_numbering_resets_for_new_year(self, statuses, make_user):
        """Нумерация сбрасывается при смене года."""
        from datetime import datetime
        from unittest.mock import patch

        from django.utils import timezone

        user = make_user(role_code="user")
        repo = ProjectApplicationRepository()

        # Создаём заявку в 2024 году
        with patch("showcase.repositories.application.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(
                datetime(2024, 12, 31, 23, 59, 59)
            )

            dto1 = ProjectApplicationCreateDTO(
                company="Acme2024",
                title="Test2024",
                author_lastname="Иванов",
                author_firstname="Иван",
                author_email="test2024@example.com",
                author_phone="+79990000001",
                goal="Длинная цель 1234567890",
                problem_holder="Носитель",
                barrier="Длинный барьер",
            )
            app1 = repo.create(dto1, user, "await_department")
            assert app1.application_year == 2024
            assert app1.year_sequence_number == 1
            assert app1.print_number == "24-00001"

            # Создаём ещё одну заявку в 2024 году
            app2 = repo.create(dto1, user, "await_department")
            assert app2.application_year == 2024
            assert app2.year_sequence_number == 2
            assert app2.print_number == "24-00002"

        # Создаём заявку в 2025 году - нумерация должна начаться с 1
        with patch("showcase.repositories.application.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(datetime(2025, 1, 1, 0, 0, 0))

            dto2 = ProjectApplicationCreateDTO(
                company="Acme2025",
                title="Test2025",
                author_lastname="Петров",
                author_firstname="Пётр",
                author_email="test2025@example.com",
                author_phone="+79990000002",
                goal="Длинная цель 1234567890",
                problem_holder="Носитель",
                barrier="Длинный барьер",
            )
            app3 = repo.create(dto2, user, "await_department")
            assert app3.application_year == 2025
            assert app3.year_sequence_number == 1
            assert app3.print_number == "25-00001"
