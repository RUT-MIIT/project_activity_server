from django.apps import AppConfig


class ShowcaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "showcase"

    def ready(self):
        # Сигналы Django удалены в пользу сервисной архитектуры
        # Логика работы со статусами теперь выполняется через StatusManager
        # в сервисах showcase.services.status
        pass
