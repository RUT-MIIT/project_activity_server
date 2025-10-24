# Архитектура работы со статусами заявок

Новая архитектура работы со статусами заявок, построенная на принципах SOLID и лучших практиках ООП.

## Обзор

Система разделена на несколько компонентов, каждый из которых отвечает за свою область ответственности:

- **StatusManager** - главный менеджер, координирует работу всех сервисов
- **StatusLogService** - сервис логирования изменений статусов
- **StatusTransitionService** - сервис выполнения переходов между статусами
- **StatusTransitionRegistry** - реестр переходов
- **StatusServiceFactory** - фабрика для создания сервисов

## Принципы архитектуры

### 1. Single Responsibility Principle (SRP)
Каждый сервис отвечает за одну конкретную задачу:
- `StatusLogService` - только логирование
- `StatusTransitionService` - только выполнение переходов
- `StatusManager` - только координация

### 2. Open/Closed Principle (OCP)
Новые переходы добавляются без изменения существующего кода через регистрацию в `StatusTransitionRegistry`.

### 3. Dependency Inversion Principle (DIP)
Все зависимости работают через абстракции (Protocols), а не конкретные реализации.

## Использование

### Базовое использование

```python
from showcase.services.status import StatusServiceFactory

# Создаем менеджер статусов
status_manager = StatusServiceFactory.create_status_manager()

# Изменяем статус заявки
application, status_log = status_manager.change_status(
    application=application,
    new_status=new_status,
    actor=request.user,
    comments=[{'field': 'general', 'text': 'Комментарий'}]
)

# Или по коду статуса
application, status_log = status_manager.change_status_with_log(
    application=application,
    new_status='approved',
    actor=request.user,
    comments=[{'field': 'general', 'text': 'Одобрено'}]
)
```

### Работа с логами

```python
# Получить все логи заявки
logs = status_manager.get_application_logs(application)

# Получить последний лог
last_log = status_manager.get_last_log(application)

# Добавить комментарий к последнему логу
comment = status_manager.add_comment_to_log(
    application=application,
    field='general',
    text='Новый комментарий',
    author=request.user
)
```

## Создание новых переходов

### 1. Создайте класс перехода

```python
from showcase.services.status.transitions.base import BaseStatusTransitionImpl
from showcase.models import ProjectApplication, ApplicationStatus

class MyCustomTransition(BaseStatusTransitionImpl):
    def can_apply(self, from_status: Optional[str], to_status: str) -> bool:
        # Логика проверки возможности применения перехода
        return to_status in ['approved', 'rejected']
    
    def apply(self, application, from_status, to_status, actor):
        # Логика выполнения перехода
        # Например, отправка уведомлений, обновление связанных объектов и т.д.
        pass
```

### 2. Зарегистрируйте переход в фабрике

```python
# В showcase/services/status/factory.py
def _register_transitions(registry: StatusTransitionRegistry) -> None:
    # Существующие переходы...
    
    # Новый переход
    custom_transition = MyCustomTransition()
    registry.register('created', 'approved', custom_transition)
    registry.register('await_department', 'approved', custom_transition)
```

## Миграция со старого API

### Старый код (deprecated)

```python
# DEPRECATED - не используйте
from showcase.services.status_log import StatusLogManager
from showcase.services.status_actions import StatusTransitionHandler

# Создание лога
log = StatusLogManager.create_status_log(application, new_status, actor)

# Изменение статуса с логом
application, log = StatusLogManager.change_status_with_log(
    application, new_status, actor
)

# Выполнение переходов
StatusTransitionHandler.handle(application, from_status, to_status, actor)
```

### Новый код (рекомендуется)

```python
# РЕКОМЕНДУЕТСЯ - используйте новый API
from showcase.services.status import StatusServiceFactory

status_manager = StatusServiceFactory.create_status_manager()

# Создание лога
log = status_manager.log_service.create_log(application, new_status, actor)

# Изменение статуса с логом
application, log = status_manager.change_status_with_log(
    application, new_status, actor
)

# Выполнение переходов (автоматически при change_status)
# Или вручную:
status_manager.transition_service.execute_transitions(
    application, from_status, to_status, actor
)
```

## Структура файлов

```
showcase/services/status/
├── __init__.py              # Публичный API
├── base.py                  # Протоколы и абстракции
├── manager.py               # StatusManager
├── log_service.py           # StatusLogService
├── transition_service.py    # StatusTransitionService
├── factory.py               # StatusServiceFactory
├── transitions/
│   ├── __init__.py
│   ├── base.py              # BaseStatusTransitionImpl
│   └── author_involvement.py # AuthorInvolvementTransition
└── README.md                # Эта документация
```

## Тестирование

### Тестирование сервисов

```python
from django.test import TestCase
from showcase.services.status import StatusServiceFactory
from showcase.models import ProjectApplication, ApplicationStatus

class StatusManagerTest(TestCase):
    def setUp(self):
        self.status_manager = StatusServiceFactory.create_status_manager()
        self.application = ProjectApplication.objects.create(...)
        self.status = ApplicationStatus.objects.create(code='test', name='Test')
    
    def test_change_status(self):
        application, log = self.status_manager.change_status(
            self.application, self.status, self.user
        )
        self.assertEqual(application.status, self.status)
        self.assertIsNotNone(log)
```

### Тестирование переходов

```python
class AuthorInvolvementTransitionTest(TestCase):
    def test_can_apply(self):
        transition = AuthorInvolvementTransition()
        self.assertTrue(transition.can_apply(None, 'created'))
        self.assertTrue(transition.can_apply('created', 'approved'))
        self.assertFalse(transition.can_apply('created', 'draft'))
    
    def test_apply(self):
        transition = AuthorInvolvementTransition()
        # Тестируем логику добавления автора в причастные
        pass
```

## Преимущества новой архитектуры

1. **Тестируемость** - каждый компонент можно тестировать изолированно
2. **Расширяемость** - новые переходы добавляются без изменения существующего кода
3. **Читаемость** - четкое разделение ответственностей
4. **Соблюдение SOLID** - все принципы соблюдены
5. **Обратная совместимость** - старый API продолжает работать через фасады

## Планы развития

1. **Валидация переходов** - добавление проверки прав пользователей на переходы
2. **Уведомления** - автоматические уведомления при изменении статусов
3. **Метрики** - отслеживание времени обработки заявок
4. **Аудит** - детальное логирование всех действий пользователей

