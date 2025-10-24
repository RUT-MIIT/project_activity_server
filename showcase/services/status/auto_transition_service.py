"""
Сервис автопереходов статусов.

Проверяет, требуется ли выполнить дополнительный автоматический переход
после ручного изменения статуса, и выполняет его синхронно.
"""

from typing import Optional

from django.contrib.auth import get_user_model

from showcase.models import ProjectApplication, ApplicationStatus
from .auto_rules import AUTO_TRANSITION_RULES, AUTO_TRANSITION_COMMENTS

User = get_user_model()


class AutoTransitionService:
    """Применяет автопереходы согласно правилам."""

    def __init__(self, status_manager: "StatusManager") -> None:
        # Циклическая зависимость разрешается на уровне фабрики
        self.status_manager = status_manager

    def maybe_apply(
        self,
        application: ProjectApplication,
        from_status: Optional[ApplicationStatus],
        to_status: ApplicationStatus,
        *,
        depth: int = 0,
    ) -> Optional[ApplicationStatus]:
        """
        Если для статуса `to_status` есть правило автоперехода — применяет его.

        Возвращает целевой статус автоперехода или None, если правила нет.
        """
        if depth > 1:
            # Защита от теоретических циклов
            return None

        current_code = getattr(to_status, 'code', None)
        if not current_code:
            return None

        next_code = AUTO_TRANSITION_RULES.get(current_code)
        if not next_code:
            return None

        try:
            next_status = ApplicationStatus.objects.get(code=next_code)
        except ApplicationStatus.DoesNotExist:
            return None

        # Готовим комментарий
        template = AUTO_TRANSITION_COMMENTS.get(current_code, 'Автопереход: статус "{from_name}" → "{to_name}"')
        comment_text = template.format(from_name=to_status.name, to_name=next_status.name)

        # Выполняем автопереход с actor=None и пометкой поля
        self.status_manager.change_status(
            application=application,
            new_status=next_status,
            actor=None,  # системный
            comments=[{
                'field': 'auto_transition',
                'text': comment_text,
            }],
        )

        return next_status


