from django.contrib.auth import get_user_model
from showcase.models import (
    ProjectApplication,
    ApplicationStatus,
)
from .status import StatusServiceFactory

User = get_user_model()


class StatusLogManager:
    """
    DEPRECATED: Используйте StatusManager из showcase.services.status
    
    Этот класс оставлен для обратной совместимости.
    Все методы делегируют вызовы новому StatusManager.
    """

    @staticmethod
    def create_status_log(application, new_status, actor=None, comments=None, from_status=None):
        """
        DEPRECATED: Используйте StatusManager.create_log()
        
        Создает лог изменения статуса заявки

        Args:
            application: Объект ProjectApplication
            new_status: Новый статус (ApplicationStatus или код статуса)
            actor: Пользователь, который изменил статус
            comments: Список комментариев [{'field': str, 'text': str}, ...]

        Returns:
            ProjectApplicationStatusLog: Созданный лог
        """
        import warnings
        warnings.warn(
            "StatusLogManager.create_status_log is deprecated. Use StatusManager from showcase.services.status",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Делегируем вызов новому сервису
        status_manager = StatusServiceFactory.create_status_manager()
        
        # Если new_status - строка, ищем статус по коду
        if isinstance(new_status, str):
            try:
                new_status = ApplicationStatus.objects.get(code=new_status)
            except ApplicationStatus.DoesNotExist:
                raise ValueError(f"Status with code '{new_status}' not found")
        
        return status_manager.log_service.create_log(
            application=application,
            new_status=new_status,
            actor=actor,
            comments=comments,
            from_status=from_status
        )

    @staticmethod
    def change_status_with_log(application, new_status, actor=None, comments=None):
        """
        DEPRECATED: Используйте StatusManager.change_status_with_log()
        
        Изменяет статус заявки и создает лог

        Returns:
            tuple: (application, status_log)
        """
        import warnings
        warnings.warn(
            "StatusLogManager.change_status_with_log is deprecated. Use StatusManager from showcase.services.status",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Делегируем вызов новому сервису
        status_manager = StatusServiceFactory.create_status_manager()
        return status_manager.change_status_with_log(application, new_status, actor, comments)


    @staticmethod
    def get_application_logs(application: ProjectApplication):
        """DEPRECATED: Используйте StatusManager.get_application_logs()"""
        import warnings
        warnings.warn(
            "StatusLogManager.get_application_logs is deprecated. Use StatusManager from showcase.services.status",
            DeprecationWarning,
            stacklevel=2
        )
        status_manager = StatusServiceFactory.create_status_manager()
        return status_manager.get_application_logs(application)

    @staticmethod
    def get_last_log(application: ProjectApplication):
        """DEPRECATED: Используйте StatusManager.get_last_log()"""
        import warnings
        warnings.warn(
            "StatusLogManager.get_last_log is deprecated. Use StatusManager from showcase.services.status",
            DeprecationWarning,
            stacklevel=2
        )
        status_manager = StatusServiceFactory.create_status_manager()
        return status_manager.get_last_log(application)

    @staticmethod
    def add_comment_to_last_log(application: ProjectApplication, field: str, text: str, author: User | None = None):
        """DEPRECATED: Используйте StatusManager.add_comment_to_log()"""
        import warnings
        warnings.warn(
            "StatusLogManager.add_comment_to_last_log is deprecated. Use StatusManager from showcase.services.status",
            DeprecationWarning,
            stacklevel=2
        )
        status_manager = StatusServiceFactory.create_status_manager()
        return status_manager.add_comment_to_log(application, field, text, author)



