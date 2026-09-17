# Design

## Context

См. proposal.md — Why.

Текущий пайплайн:

```
list_institute_students
  -> InstituteResponsibleStudentDTO.to_dict()
       project = _project_snapshot(app)  # только id, title
  -> build_students_xlsx(payload)        # читает project.title
```

JSON `/students/` и Excel `/students/export/` сейчас делят один DTO. Нужно обогатить только Excel, не расширяя публичный JSON.

## Goals / Non-Goals

**Goals:**

- Три новые колонки в xlsx из полей заявки
- Минимальный diff, без смены контракта JSON
- Обновить тест выгрузки и фронтенд-доки колонок

**Non-Goals:**

- Не менять `_project_snapshot` для JSON API
- Не добавлять email/телефон/роль автора и `is_internal_customer`
- Не делать отдельный endpoint и не менять права доступа

## Decisions

### 1. Enrichment только в export-пайплайне

**Выбор:** собирать расширенный словарь проекта внутри export (сервис или excel-domain), не трогая `_project_snapshot` и `InstituteResponsibleStudentDTO.to_dict()`.

Практичный вариант:

- В `export_students` после (или вместо) DTO-словаря передать в `build_students_xlsx` данные, где для каждой строки доступны `company`, `companyContacts`, `authorFullName` на уровне строки или вложенного `project` **только для export**.
- Проще всего: расширить вход builder'а — читать поля из объекта заявки через отдельный helper в `institute_students_excel.py` / тонкий adapter в service, который клонирует student-dict и дополняет `project` полями только перед `build_students_xlsx`.

Чтобы не гонять N+1: заявка уже на `membership.team_semester.project_application` (select_related в репозитории memberships). Значит enrichment можно сделать либо:

- **A)** в excel-слое, если передать туда ORM/сырые поля (нежелательно — domain excel сейчас работает только с dict);
- **B)** в `InstituteResponsibleService.export_students`: при сборке payload для export вызвать helper, который из `ContingentStudent` / membership достаёт заявку и кладёт поля в dict **только для xlsx**.

Рекомендация: **B** — service строит export-специфичный dict (или дополняет project), builder остаётся чистым преобразованием dict → строки.

**Альтернатива (отклонена):** расширить `_project_snapshot` и скрывать поля в JSON — риск утечки полей в API и путаница контрактов.

### 2. Формат ФИО автора

Собрать из `author_lastname`, `author_firstname`, `author_middlename` через пробел, пропуская пустые части — по аналогии с `format_student_full_name`. Не использовать FK `author.get_full_name()`, чтобы совпадать с данными заявки (снимок на форме), даже если User изменился.

### 3. Заголовки колонок

Порядок после «Проект»:

1. Заказчик
2. Контакты заказчика
3. Автор заявки

### 4. Документация

Обновить таблицу колонок в `docs/frontend/institute_responsible.md` §9.1.

## Risks / Trade-offs

- **Дублирование логики student→row для JSON vs Excel** → держать enrichment тонким и рядом с `export_students`; общие format-helpers в `institute_students_excel.py`.
- **Пустые author_* при заполненном User.author** → осознанно берём поля заявки; при необходимости позже можно fallback (вне scope).
- **Регрессия теста заголовков** → обновить `test_export_students_returns_xlsx` с заполненными company/contacts/author_*.

## Migration Plan

- Деплой без миграций БД.
- Rollback: откат кода; клиенты Excel просто снова получат старые колонки.
