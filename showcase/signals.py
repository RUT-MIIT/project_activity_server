# Сигналы Django удалены в пользу сервисной архитектуры
#
# Логика отслеживания и логирования изменений статусов
# теперь выполняется через StatusManager в сервисах.
#
# Это обеспечивает:
# - Лучшую тестируемость
# - Более явное управление зависимостями
# - Соблюдение принципов SOLID
#
# Для изменения статусов используйте:
# from showcase.services.status import StatusServiceFactory
# status_manager = StatusServiceFactory.create_status_manager()
# status_manager.change_status(application, new_status, actor, comments)
