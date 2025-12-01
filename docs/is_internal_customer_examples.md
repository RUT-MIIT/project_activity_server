# Примеры использования поля is_internal_customer

## Описание

Поле `is_internal_customer` указывает, является ли заказчик внутренним. По умолчанию `false` (внешний заказчик).

## Примеры создания заявки через API

### 1. Создание заявки с внутренним заказчиком

```bash
curl -X POST http://localhost:8000/api/showcase/project-applications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "company": "Внутренняя Компания ООО",
    "title": "Проект по разработке внутренней системы",
    "author_lastname": "Петров",
    "author_firstname": "Петр",
    "author_email": "petrov@internal-company.ru",
    "author_phone": "+79991111111",
    "goal": "Разработать внутреннюю систему управления проектами",
    "problem_holder": "Внутренний отдел компании",
    "barrier": "Отсутствие единой системы управления проектами",
    "project_level": "L1",
    "is_internal_customer": true
  }'
```

### 2. Создание заявки с внешним заказчиком

```bash
curl -X POST http://localhost:8000/api/showcase/project-applications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "company": "Внешняя Компания ООО",
    "title": "Проект по разработке внешней системы",
    "author_lastname": "Сидоров",
    "author_firstname": "Сидор",
    "author_email": "sidorov@external-company.ru",
    "author_phone": "+79992222222",
    "goal": "Разработать систему для управления заказами клиентов",
    "problem_holder": "Внешняя компания-заказчик",
    "barrier": "Текущая система не справляется с растущим объемом заказов",
    "project_level": "L2",
    "is_internal_customer": false
  }'
```

### 3. Создание заявки без указания типа заказчика (по умолчанию false)

```bash
curl -X POST http://localhost:8000/api/showcase/project-applications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "company": "Компания ООО",
    "title": "Проект разработки",
    "author_lastname": "Иванов",
    "author_firstname": "Иван",
    "author_email": "ivanov@company.ru",
    "author_phone": "+79993333333",
    "goal": "Длинная цель проекта, больше 50 символов для консультации",
    "problem_holder": "Носитель проблемы",
    "barrier": "Длинное описание барьера",
    "project_level": "L1"
  }'
```

## Пример обновления поля

### Обновление только поля is_internal_customer

```bash
curl -X PATCH http://localhost:8000/api/showcase/project-applications/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "is_internal_customer": true
  }'
```

## Пример ответа API

```json
{
  "id": 1,
  "title": "Проект по разработке внутренней системы",
  "company": "Внутренняя Компания ООО",
  "is_internal_customer": true,
  "is_external": false,
  "needs_consultation": true,
  "status": {
    "code": "await_department",
    "name": "Ожидает рассмотрения отделом"
  },
  "creation_date": "2024-01-15T10:30:00Z",
  ...
}
```

## Использование в Python коде

### Создание через DTO

```python
from showcase.dto.application import ProjectApplicationCreateDTO
from showcase.services.application_service import ProjectApplicationService

# Создание DTO с внутренним заказчиком
dto = ProjectApplicationCreateDTO(
    company="Внутренняя Компания ООО",
    title="Проект по разработке внутренней системы",
    author_lastname="Петров",
    author_firstname="Петр",
    author_email="petrov@internal-company.ru",
    author_phone="+79991111111",
    goal="Разработать внутреннюю систему управления проектами",
    problem_holder="Внутренний отдел компании",
    barrier="Отсутствие единой системы управления проектами",
    project_level="L1",
    is_internal_customer=True  # Указываем внутреннего заказчика
)

# Создание заявки через сервис
service = ProjectApplicationService()
application = service.submit_application(dto, user)

# Проверка значения
assert application.is_internal_customer is True
```

### Обновление через DTO

```python
from showcase.dto.application import ProjectApplicationUpdateDTO
from showcase.services.application_service import ProjectApplicationService

# Обновление только поля is_internal_customer
update_dto = ProjectApplicationUpdateDTO(
    is_internal_customer=True
)

service = ProjectApplicationService()
application = service.update_application(application_id, update_dto, user)
```

## Тесты

Все тесты находятся в файле `tests/showcase/entities/test_is_internal_customer.py`.

Запуск тестов:

```bash
pytest tests/showcase/entities/test_is_internal_customer.py -v
```

