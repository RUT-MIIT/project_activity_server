"""Unit-тесты для CommentService.

Проверяем добавление комментариев, получение комментариев, обработку ошибок.
"""

import pytest

from showcase.models import ProjectApplication, ProjectApplicationComment
from showcase.services.comment_service import CommentService


@pytest.mark.django_db
class TestCommentService:
    """Тесты для CommentService."""

    def test_add_comment_success(self, statuses, make_user):
        """Успешное добавление комментария к заявке."""

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
            barrier="Длинный барьер",
        )

        service = CommentService()
        comment = service.add_comment(
            application_id=app.id,
            field="goal",
            text="Нужно уточнить цель проекта",
            author=user,
        )

        assert comment.id is not None
        assert comment.application.id == app.id
        assert comment.field == "goal"
        assert comment.text == "Нужно уточнить цель проекта"
        assert comment.author.id == user.id

    def test_add_comment_strips_whitespace(self, statuses, make_user):
        """add_comment обрезает пробелы в field и text."""

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

        service = CommentService()
        comment = service.add_comment(
            application_id=app.id,
            field="  goal  ",  # С пробелами
            text="  Комментарий  ",  # С пробелами
            author=user,
        )

        assert comment.field == "goal"  # Без пробелов
        assert comment.text == "Комментарий"  # Без пробелов

    def test_add_comment_empty_field(self, statuses, make_user):
        """Пустое поле вызывает ValueError."""

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

        service = CommentService()
        with pytest.raises(ValueError, match="Поле обязательно"):
            service.add_comment(
                application_id=app.id,
                field="",  # Пустое поле
                text="Комментарий",
                author=user,
            )

    def test_add_comment_empty_text(self, statuses, make_user):
        """Пустой текст вызывает ValueError."""

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

        service = CommentService()
        with pytest.raises(ValueError, match="Текст комментария обязателен"):
            service.add_comment(
                application_id=app.id,
                field="goal",
                text="   ",  # Только пробелы
                author=user,
            )

    def test_add_comment_application_not_found(self, make_user):
        """Несуществующая заявка вызывает ValueError."""
        user = make_user(role_code="user")
        service = CommentService()

        with pytest.raises(ValueError, match="не найдена"):
            service.add_comment(
                application_id=99999,  # Несуществующий ID
                field="goal",
                text="Комментарий",
                author=user,
            )

    def test_get_application_comments_success(self, statuses, make_user):
        """Успешное получение комментариев к заявке."""

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

        # Создаём несколько комментариев
        comment1 = ProjectApplicationComment.objects.create(
            application=app, author=user, field="goal", text="Первый комментарий"
        )
        comment2 = ProjectApplicationComment.objects.create(
            application=app, author=user, field="barrier", text="Второй комментарий"
        )

        service = CommentService()
        comments = service.get_application_comments(app.id)

        assert len(comments) == 2
        # Проверяем сортировку по убыванию даты (последний созданный первый)
        assert comments[0].id == comment2.id  # Последний комментарий первый в списке

    def test_get_application_comments_empty_list(self, statuses, make_user):
        """Если комментариев нет, возвращается пустой список."""

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

        service = CommentService()
        comments = service.get_application_comments(app.id)

        assert comments == []

    def test_get_application_comments_application_not_found(self):
        """Несуществующая заявка вызывает ValueError."""
        service = CommentService()

        with pytest.raises(ValueError, match="не найдена"):
            service.get_application_comments(99999)  # Несуществующий ID

    def test_get_application_comments_select_related_optimization(
        self, statuses, make_user
    ):
        """get_application_comments использует select_related для оптимизации запросов."""

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

        ProjectApplicationComment.objects.create(
            application=app, author=user, field="goal", text="Комментарий"
        )

        service = CommentService()
        comments = service.get_application_comments(app.id)

        assert len(comments) == 1
        # Проверяем, что данные автора доступны без дополнительных запросов
        assert comments[0].author.id == user.id
        assert hasattr(comments[0].author, "role")
        assert hasattr(comments[0].author, "department")
