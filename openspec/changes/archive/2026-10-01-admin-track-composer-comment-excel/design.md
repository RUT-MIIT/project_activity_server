# Design

## Context

См. proposal.md — Why. Уже есть:

- поле `ProjectApplication.track_composer_comment` и отображение в `ProjectApplicationAdmin`;
- `list_filter` по `semester` на списке заявок;
- `get_root_department()` в `accounts/utils.py` (подъём по `parent` до корня);
- образец domain Excel: `teams/domain/institute_students_excel.py` (openpyxl → bytes);
- ФИО автора в Excel уже собирается аналогично (`format_author_full_name` в institute students excel).

Публичных admin-action выгрузок xlsx по заявкам пока нет.

## Goals / Non-Goals

**Goals:**

- Admin action на `ProjectApplicationAdmin` → скачиваемый xlsx с двумя листами.
- Чистая классификация комментария и сбор строк в domain-слое (без Django admin в бизнес-логике).
- Резолв института через существующий `get_root_department(author.department)`.

**Non-Goals:**

- Отдельный HTTP API / эндпоинт для фронта.
- Автовыгрузка всего отфильтрованного changelist без отметки строк (только selected queryset).
- Изменение поля `track_composer_comment`, API заявок, треков или Excel контингента.
- Фильтрация по статусу заявки внутри action (статусы сужаются фильтрами changelist до выбора).

## Decisions

### 1. Domain-модуль `showcase/domain/track_composer_comment_excel.py`

Вынести:

- константу placeholder’ов и `is_empty_track_composer_comment(text)`;
- построение строки `(author, institute, title, comment)` из заявки;
- `build_track_composer_comment_xlsx(rows_or_applications) -> bytes` с двумя листами.

Имена листов (рекомендация): «Заполненные», «Пустые».

**Альтернатива:** собрать xlsx прямо в `admin.py` — отклонено: сложнее тестировать, расходится с паттерном `institute_students_excel`.

### 2. Источник института и автора

- Автор: `author_lastname` / `author_firstname` / `author_middlename` с заявки (снимок на момент заполнения формы), не `User.get_full_name`.
- Институт: `get_root_department(application.author.department)` → `.name`; без author/department → `""`.
- Prefetch/select_related: `author__department__parent` (и при необходимости цепочка parent) в queryset action, чтобы не ловить N+1.

**Альтернатива:** `author_division` — отклонено пользователем; нужен корневой `Department`.

**Альтернатива:** один шаг `parent`, а не корень — отклонено; зафиксировано корневое через `get_root_department`.

### 3. Admin action UX

- Действие: «Выгрузить комментарии составителю трека (Excel)».
- Вход: `queryset` отмеченных объектов.
- Валидации до генерации файла:
  1. queryset не пуст;
  2. множество `semester_id` у выбранных имеет размер ровно 1 (все с одним и тем же семестром; заявки без семестра считаются отдельным «значением» `None` и при смеси с другими тоже дают отказ).
- Успех: `HttpResponse` с `Content-Type` xlsx и `Content-Disposition` attachment; имя файла включает id/имя семестра при возможности.
- Ошибка: `messages.error` + redirect на changelist (стандартный admin pattern).

**Альтернатива:** требовать наличие semester в GET-фильтре changelist независимо от selection — отклонено как хрупкое (action не всегда видит тот же filter state надёжно); проверка однородности семестра в queryset достаточна и совпадает с «после фильтра по семестру».

### 4. Классификация «условно пустых»

Нормализация: `text.strip().casefold()`, затем membership в frozenset placeholder’ов из спеки. Список — константа рядом с функцией, покрыта unit-тестами; расширение списка — отдельный мелкий change.

Не меняем семантику `has_track_composer_comment` в DTO API (там по-прежнему `bool(strip())`) — расхождение осознанное: API флаг остаётся «непустая строка», Excel-отчёт строже к заглушкам.

## Risks / Trade-offs

- [Глубокая иерархия Department без prefetch всей цепочки] → Mitigation: `get_root_department` идёт по `parent`; для типовых 1–2 уровней достаточно `select_related("author__department__parent")`; при более глубоких деревьях — доп. join или кэш корней, если появится N+1 в тестах/проде.
- [Action только по отмеченным строкам; «выбрать все» в Django — по странице] → Mitigation: задокументировать в описании action; при необходимости позже добавить отдельную кнопку «весь фильтр» вне scope.
- [Placeholder’ы могут ложно отсечь редкий осмысленный комментарий вроде «нет»] → Mitigation: короткий фиксированный список; «нет» намеренно на листе пустых как типичная заглушка.

## Migration Plan

- Деплой кода без миграций БД (поле уже есть).
- Откат: удалить action и domain-модуль; данных не затрагивает.

## Open Questions

- Нет блокирующих; имя файла и точные названия листов можно уточнить при implement без смены спеки (спека требует только однозначности смысла листов).
