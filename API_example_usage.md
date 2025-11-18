# API для работы с проектными заявками

## Endpoints

### 1. Проектные заявки (ProjectApplicationViewSet)
- **POST** `/showcase/project-applications/` - создание новой заявки (требует аутентификации)
- **GET** `/showcase/project-applications/` - список заявок пользователя
- **GET** `/showcase/project-applications/{id}/` - получение конкретной заявки
- **PUT/PATCH** `/showcase/project-applications/{id}/` - обновление заявки
- **DELETE** `/showcase/project-applications/{id}/` - удаление заявки
- **GET** `/showcase/project-applications/my_applications/` - альтернативный способ получения заявок
- **POST** `/showcase/project-applications/simple/` - простое создание заявки без авторизации (AllowAny)

#### Система статусов и логов:
- **GET** `/showcase/project-applications/{id}/status_logs/` - получение логов изменений статуса

### 2. Справочники
- **GET** `/showcase/institutes/` - список институтов
- **GET** `/showcase/application-statuses/` - список статусов заявок

## Пример полного запроса на создание заявки

```json
{
  "_comment": "=== ОСНОВНЫЕ ПОЛЯ ===",
  "title": "Название проекта (необязательно)",
  "needs_consultation": true,

  "_comment_contact": "=== КОНТАКТНЫЕ ДАННЫЕ (обязательные поля) ===",
  "author_surname": "Фамилия автора заявки",
  "author_firstname": "Имя автора заявки",
  "author_middlename": "Отчество автора (необязательно)",
  "author_email": "email@example.com",
  "author_phone": "+7 (495) 123-45-67",
  "author_role": "Роль автора в организации (необязательно)",
  "author_division": "Подразделение автора (необязательно)",

  "_comment_project": "=== О ПРОЕКТЕ (обязательные поля) ===",
  "company": "Наименование организации-заказчика",
  "company_contacts": "Контактные данные представителя заказчика (длинный текст)",
  "target_institute_codes": ["INST_001", "INST_002"],
  "project_level": "Уровень проекта (например: Федеральный, Региональный, Муниципальный)",

  "_comment_problem": "=== ПРОБЛЕМА (обязательные поля) ===",
  "problem_holder": "Кто является носителем проблемы",
  "goal": "Цель проекта (длинный текст)",
  "barrier": "Какие барьеры препятствуют достижению цели (длинный текст)",
  "existing_solutions": "Описание существующих решений (длинный текст)",

  "_comment_context": "=== КОНТЕКСТ (необязательные поля) ===",
  "context": "Контекст проекта (длинный текст, необязательно)",
  "stakeholders": "Другие заинтересованные стороны (длинный текст, необязательно)",
  "recommended_tools": "Рекомендуемые инструменты и технологии (длинный текст, необязательно)",
  "experts": "Эксперты, которые могут помочь (длинный текст, необязательно)",
  "additional_materials": "Дополнительные материалы (длинный текст, необязательно)"
}
```

## Минимальный пример запроса

```json
{
  "author_surname": "Иванов",
  "author_firstname": "Алексей",
  "author_email": "ivanov@example.com",
  "author_phone": "+7 (495) 123-45-67",
  "company": "ООО 'Пример'",
  "company_contacts": "Директор: Петров П.П., тел: +7 (495) 987-65-43",
  "project_level": "Региональный",
  "problem_holder": "Промышленные предприятия",
  "goal": "Создание системы мониторинга",
  "barrier": "Отсутствие единой системы",
  "existing_solutions": "Существующие системы работают изолированно"
}
```

## Объяснение полей

### Обязательные поля:
- **author_surname** - Фамилия автора заявки
- **author_firstname** - Имя автора заявки
- **author_email** - Электронная почта автора
- **author_phone** - Телефон автора
- **company** - Наименование организации-заказчика
- **company_contacts** - Контактные данные представителя заказчика
- **project_level** - Уровень проекта
- **problem_holder** - Носитель проблемы
- **goal** - Цель проекта
- **barrier** - Барьеры для достижения цели
- **existing_solutions** - Существующие решения

### Необязательные поля:
- **title** - Название проекта
- **author_middlename** - Отчество автора
- **author_role** - Роль автора
- **author_division** - Подразделение автора
- **target_institute_codes** - Массив кодов институтов
- **needs_consultation** - Нужна ли консультация (boolean)
- **context** - Контекст проекта
- **stakeholders** - Заинтересованные стороны
- **recommended_tools** - Рекомендуемые инструменты
- **experts** - Эксперты
- **additional_materials** - Дополнительные материалы
- **status_code** - Код статуса (по умолчанию "created")

## Автоматическая установка статуса

При создании заявки автоматически устанавливается статус **"created"** (Создана), если не указан другой статус через поле `status_code`.

## Неавторизованное создание заявок

### Простое создание заявки (без аутентификации)
**POST** `/showcase/project-applications/simple/`

Этот endpoint позволяет создавать заявки без регистрации и авторизации. Использует тот же сериализатор, что и авторизованное создание, но:

- **Разрешение `AllowAny`** - доступ открыт для всех
- **Не требует аутентификации**
- **Поле `author` будет `null`** (заявка не привязана к пользователю)
- **Автоматически устанавливается статус "created"**
- **Поддерживает все те же поля**, что и обычное создание

#### Пример запроса:
```json
POST /showcase/project-applications/simple/
{
  "author_surname": "Иванов",
  "author_firstname": "Алексей",
  "author_email": "ivanov@example.com",
  "author_phone": "+7 (495) 123-45-67",
  "company": "ООО 'Пример'",
  "company_contacts": "Контактные данные...",
  "project_level": "Региональный",
  "problem_holder": "Промышленные предприятия",
  "goal": "Создание системы мониторинга",
  "barrier": "Отсутствие единой системы",
  "existing_solutions": "Существующие системы работают изолированно"
}
```

#### Ответ:
```json
{
  "id": 1,
  "title": null,
  "author": null,
  "status": {
    "code": "created",
    "name": "Создана"
  },
  "creation_date": "2024-01-15T10:30:00Z",
  "needs_consultation": false,
  "author_surname": "Иванов",
  "author_firstname": "Алексей",
  "author_middlename": null,
  "author_email": "ivanov@example.com",
  "author_phone": "+7 (495) 123-45-67",
  "author_role": null,
  "author_division": null,
  "company": "ООО 'Пример'",
  "company_contacts": "Контактные данные...",
  "target_institutes": [],
  "project_level": "Региональный",
  "problem_holder": "Промышленные предприятия",
  "goal": "Создание системы мониторинга",
  "barrier": "Отсутствие единой системы",
  "existing_solutions": "Существующие системы работают изолированно",
  "context": null,
  "stakeholders": null,
  "recommended_tools": null,
  "experts": null,
  "additional_materials": null
}
```

## Система статусов и логов


### Получение логов изменения статуса
**GET** `/showcase/project-applications/{id}/status_logs/`

Ответ:
```json
[
  {
    "id": 1,
    "changed_at": "2024-01-15T10:30:00Z",
    "actor": 1,
    "actor_name": "Иванов Иван Иванович",
    "from_status": {"code": "NEW", "name": "Новая"},
    "to_status": {"code": "IN_REVIEW", "name": "На рассмотрении"},
    "comments": [
      {
        "id": 1,
        "author": 1,
        "author_name": "Иванов Иван Иванович",
        "created_at": "2024-01-15T10:30:00Z",
        "field": "status_change",
        "text": "Заявка передана на рассмотрение экспертам"
      }
    ]
  }
]
```



## Дополнительные возможности ViewSet

### Получение заявок пользователя (альтернативный способ)
**GET** `/showcase/project-applications/my_applications/`

### Полный CRUD для заявок
- **POST** - создание
- **GET** - получение списка или конкретной заявки
- **PUT/PATCH** - обновление
- **DELETE** - удаление

## Аутентификация

Все запросы требуют аутентификации. Передавайте токен в заголовке:
```
Authorization: Bearer <your_token>
```

## Ответ при успешном создании

```json
{
  "id": 1,
  "title": "Название проекта",
  "author": 1,
  "status": {
    "code": "created",
    "name": "Создана"
  },
  "creation_date": "2024-01-15T10:30:00Z",
  "needs_consultation": true,
  "author_surname": "Иванов",
  "author_firstname": "Алексей",
  "author_middlename": "Сергеевич",
  "author_email": "ivanov@example.com",
  "author_phone": "+7 (495) 123-45-67",
  "author_role": "Руководитель проекта",
  "author_division": "Отдел инноваций",
  "company": "ООО 'Пример'",
  "company_contacts": "Контактные данные...",
  "target_institutes": [
    {"code": "INST_001", "name": "Институт экологии"},
    {"code": "INST_002", "name": "Институт технологий"}
  ],
  "project_level": "Федеральный",
  "problem_holder": "Промышленные предприятия",
  "goal": "Создание системы мониторинга...",
  "barrier": "Отсутствие единой системы...",
  "existing_solutions": "Существующие системы...",
  "context": "Контекст проекта...",
  "stakeholders": "Заинтересованные стороны...",
  "recommended_tools": "Рекомендуемые инструменты...",
  "experts": "Эксперты...",
  "additional_materials": "Дополнительные материалы..."
}
```
