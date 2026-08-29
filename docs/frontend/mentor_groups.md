# Мои группы (наставник) — API для фронта

Базовый префикс: `/api/teams/study-groups/`

**Доступ:** любой аутентифицированный пользователь; в ответ попадают только группы, где он назначен наставником в указанном семестре.

**Авторизация:** `Authorization: Bearer <token>`
**Формат полей:** camelCase.

---

## Список групп наставника

```http
GET /api/teams/study-groups/my-groups/?semester_id=actual
```

### Query-параметры

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `semester_id` | `number` \| `"actual"` \| `"next"` | да | Семестр |

### Ответ `200`

```json
[
  {
    "id": 1,
    "name": "ИВТ-101",
    "studentsCount": 25,
    "teamsCount": 3
  }
]
```

| Поле | Описание |
|------|----------|
| `id` | ID учебной группы |
| `name` | Название группы |
| `studentsCount` | Число студентов в контингенте группы |
| `teamsCount` | Число команд с `home_study_group` этой группы в выбранном семестре |

Пустой массив — наставник не назначен ни на одну группу в этом семестре.

### Ошибки

| Код | Когда |
|-----|--------|
| `401` | Не авторизован |
| `400` | Не передан или некорректный `semester_id` |

---

## Детали группы наставника

```http
GET /api/teams/study-groups/{groupId}/mentor-detail/?semester_id=actual
```

Экран деталей группы из списка «Мои группы»: контингент студентов и команды в семестре.

### Query-параметры

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `semester_id` | `number` \| `"actual"` \| `"next"` | да | Семестр |

### Ответ `200`

```json
{
  "id": 1,
  "name": "ИВТ-101",
  "students": [
    {
      "id": 10,
      "lastName": "Иванов",
      "firstName": "Иван",
      "middleName": "Иванович",
      "isRegistered": true,
      "userId": 42,
      "team": { "id": 5, "name": "Alpha", "role": "leader" }
    },
    {
      "id": 11,
      "lastName": "Петров",
      "firstName": "Пётр",
      "middleName": "",
      "isRegistered": false,
      "userId": null,
      "team": null
    }
  ],
  "teams": [
    {
      "id": 5,
      "name": "Alpha",
      "status": "forming",
      "membersCount": 4
    }
  ]
}
```

| Поле | Описание |
|------|----------|
| `students` | Контингент группы, сортировка по ФИО |
| `isRegistered` | Студент прошёл полную регистрацию (`false` для псевдо-аккаунта контингента) |
| `userId` | ID пользователя-студента (в т.ч. псевдо-аккаунта) или `null` |
| `team` | Команда студента в семестре (`id` = `TeamSemester.id`) или `null` |
| `teams[].id` | `TeamSemester.id` |
| `teams[].status` | `forming` или `assembled` |
| `teams[].membersCount` | Число участников команды в семестре |

### Ошибки

| Код | Когда |
|-----|--------|
| `401` | Не авторизован |
| `400` | Не передан или некорректный `semester_id` |
| `403` | Пользователь не назначен наставником этой группы в семестре |
| `404` | Группа не найдена |

---

## Витрина проектов

```http
GET /api/teams/study-groups/{groupId}/project-showcase/?semester_id=actual
```

Список проектных треков группы с одобренными проектами. Формат ответа **идентичен** студенческой витрине (`GET /api/showcase/student-showcase/`).

### Query-параметры

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `semester_id` | `number` \| `"actual"` \| `"next"` | да | Семестр |

### Ответ `200`

```json
[
  {
    "id": 1,
    "name": "Трек 1",
    "description": "Описание трека",
    "projects": [
      {
        "id": 10,
        "title": "Название проекта",
        "company": "ООО Заказчик",
        "maxTeams": 3,
        "enrolledTeamsCount": 1,
        "minTeamMembers": 4,
        "maxTeamMembers": 7,
        "tags": [{ "id": 1, "name": "AI", "category": "Tech" }]
      }
    ]
  }
]
```

**Заголовок ответа:** `Cache-Control: private, max-age=30`

Детали проекта — через существующий API заявок (`GET /api/showcase/project-applications/{id}/`).

### Ошибки

| Код | Когда |
|-----|--------|
| `401` | Не авторизован |
| `400` | Не передан или некорректный `semester_id` |
| `403` | Пользователь не назначен наставником этой группы в семестре |
| `404` | Группа не найдена |

---

## Управление командой

Базовый префикс: `/api/teams/study-groups/{groupId}/teams/{teamSemesterId}/`

**Доступ:** наставник группы в указанном семестре.
**Ограничение:** если команда записана на проект (`project_application` заполнен), **все** мутации возвращают `409` — сначала нужно отписать команду от проекта.

Во всех запросах обязателен query-параметр `semester_id`.

### Карточка команды (ответ всех мутаций)

```json
{
  "id": 5,
  "name": "Alpha",
  "status": "forming",
  "membersCount": 2,
  "members": [
    {
      "userId": 42,
      "fullName": "Иванов Иван",
      "role": "leader",
      "isPlaceholder": false
    }
  ]
}
```

| Поле | Описание |
|------|----------|
| `id` | `TeamSemester.id` |
| `status` | `forming` или `assembled` |
| `members[].role` | `leader` или `member` |
| `members[].isPlaceholder` | `true` для псевдо-аккаунта незарегистрированного студента |

---

### Переименовать команду

```http
PATCH /api/teams/study-groups/{groupId}/teams/{teamSemesterId}/?semester_id=actual
Content-Type: application/json

{ "name": "Новое название" }
```

---

### Назначить капитана

```http
PATCH /api/teams/study-groups/{groupId}/teams/{teamSemesterId}/captain/?semester_id=actual
Content-Type: application/json

{ "captainId": 42 }
```

Капитаном может быть только участник текущего состава.

---

### Подтвердить состав

```http
POST /api/teams/study-groups/{groupId}/teams/{teamSemesterId}/confirm-composition/?semester_id=actual
```

Переводит `forming` → `assembled`. Число участников должно быть в пределах лимитов трека.

---

### Вернуть состав на редактирование

```http
POST /api/teams/study-groups/{groupId}/teams/{teamSemesterId}/unconfirm-composition/?semester_id=actual
```

Переводит `assembled` → `forming`.

---

### Добавить участника

```http
POST /api/teams/study-groups/{groupId}/teams/{teamSemesterId}/members/?semester_id=actual
Content-Type: application/json
```

Зарегистрированный студент:

```json
{ "userId": 42 }
```

Незарегистрированный из контингента (создаётся псевдо-user):

```json
{ "preRegisteredStudentId": 10 }
```

Указывается **ровно одно** из полей. Студент должен быть из этой учебной группы и не состоять в другой команде семестра.

---

### Удалить участника

```http
DELETE /api/teams/study-groups/{groupId}/teams/{teamSemesterId}/members/{userId}/?semester_id=actual
```

Текущего капитана удалить нельзя — сначала назначьте нового через `captain`.

---

### Удалить команду

```http
DELETE /api/teams/study-groups/{groupId}/teams/{teamSemesterId}/?semester_id=actual
```

Только при **нулевом** составе участников.

---

### Ошибки (управление командой)

| Код | Когда |
|-----|--------|
| `401` | Не авторизован |
| `400` | Невалидный `semester_id`, бизнес-правила (лимиты, пустое название, капитан не в составе и т.д.) |
| `403` | Пользователь не наставник группы в семестре |
| `404` | Группа или команда не найдена (команда не принадлежит группе) |
| `409` | Команда записана на проект |

---

## Связь с назначением наставников

Назначение выполняет ответственный по институту (`POST /api/teams/institute-responsible/groups/{id}/mentor/`).
Список «Мои группы» строится по `StudyGroupSemester.mentors` для переданного `semester_id`.
