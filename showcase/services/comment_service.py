"""Сервис для управления комментариями к проектным заявкам.

Обеспечивает добавление и получение комментариев напрямую к заявкам.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from showcase.models import ProjectApplication, ProjectApplicationComment

User = get_user_model()


class CommentService:
    """Сервис для управления комментариями к заявкам.

    Обеспечивает добавление и получение комментариев напрямую к заявкам.
    """

    @transaction.atomic
    def add_comment(
        self, application_id: int, field: str, text: str, author: User
    ) -> ProjectApplicationComment:
        """Добавляет комментарий к заявке.

        Args:
            application_id: ID заявки
            field: Поле, к которому относится комментарий
            text: Текст комментария
            author: Автор комментария

        Returns:
            ProjectApplicationComment: Созданный комментарий

        Raises:
            ValueError: Если заявка не найдена или данные некорректны

        """
        if not field or not field.strip():
            raise ValueError("Поле обязательно для заполнения")
        if not text or not text.strip():
            raise ValueError("Текст комментария обязателен")

        try:
            application = ProjectApplication.objects.get(id=application_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Заявка с ID {application_id} не найдена") from err

        comment = ProjectApplicationComment.objects.create(
            application=application,
            author=author,
            field=field.strip(),
            text=text.strip(),
        )

        return comment

    def get_application_comments(
        self, application_id: int
    ) -> list[ProjectApplicationComment]:
        """Получает все комментарии к заявке.

        Args:
            application_id: ID заявки

        Returns:
            List[ProjectApplicationComment]: Список комментариев, отсортированный по дате создания

        Raises:
            ValueError: Если заявка не найдена

        """
        try:
            application = ProjectApplication.objects.get(id=application_id)
        except ObjectDoesNotExist as err:
            raise ValueError(f"Заявка с ID {application_id} не найдена") from err

        return list(
            ProjectApplicationComment.objects.filter(application=application)
            .select_related("author", "author__role", "author__department")
            .order_by("-created_at")
        )
