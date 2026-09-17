# Proposal

## Why

Ответственные по институтам выгружают контингент в Excel вместе с выбранным проектом команды, но без заказчика и автора заявки. Для операционной работы и связи с авторами/заказчиками этих данных не хватает — их уже есть в `ProjectApplication`, но в xlsx они не попадают.

## What Changes

- В Excel-выгрузку `GET /api/teams/institute-responsible/students/export/` добавить три колонки после «Проект»:
  - **Заказчик** — `ProjectApplication.company`
  - **Контакты заказчика** — `ProjectApplication.company_contacts`
  - **Автор заявки** — ФИО из `author_lastname` / `author_firstname` / `author_middlename`
- Если у студента нет выбранного проекта (нет `project_application`), новые колонки пустые.
- JSON API `GET .../students/` **не меняется** — только файл Excel.

## Capabilities

### New Capabilities

- `institute-students-excel`: поведение Excel-выгрузки контингента института (колонки, источники данных из выбранной заявки команды).

### Modified Capabilities

- (нет — проектных specs ещё нет)

## Impact

- Код: `teams/domain/institute_students_excel.py`, возможно `teams/services/institute_responsible_service.py` (payload только для export)
- Тесты: `tests/teams/test_institute_responsible_viewset.py` (ожидания заголовков и ячеек xlsx)
- Документация: `docs/frontend/institute_responsible.md` (таблица колонок §9.1)
- API JSON: без изменений контракта
