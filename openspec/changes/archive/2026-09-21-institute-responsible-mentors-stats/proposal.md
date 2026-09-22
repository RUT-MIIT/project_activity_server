# Proposal

## Why

Фронтенд сверстал дашборд «Наставники» (аналитика проектной деятельности для ответственного института), но бэкенд не отдаёт список наставников с нагрузкой и детальную карточку с контингентом и командами по группам. Нужны два GET-эндпоинта под уже согласованный контракт, без N+1.

## What Changes

- Добавить `GET /api/teams/institute-responsible/mentors/` — лёгкий список наставников по всем доступным институтам пользователя в указанном семестре (группы со `studentsCount`, суммарный `teamsCount`).
- Добавить `GET /api/teams/institute-responsible/mentors/{id}/` — детальная карточка с полным деревом групп → студенты (`IStatsStudent`) и команды (`IStatsTeam` с `members`).
- Источник списка: пользователи с `role.code == "mentor"` и `department` в дереве доступных институтов (включая наставников без назначенных групп).
- В JSON `institute.id` — строковый код института (`Institute.code`); фронт меняет тип с `number` на `string`.
- Поле проекта в stats-контракте — `{ id, name }` (значение из `ProjectApplication.title`).
- Идентификаторы команд — `TeamSemester.id`.
- Статус нагрузки (`loadStatus`) на бэке не отдаём — считает фронт.

## Capabilities

### New Capabilities

- `institute-responsible-mentors-stats`: API статистики наставников для ответственного института (list + detail) с правилами доступа, семестром и контрактом ответа без N+1.

### Modified Capabilities

- (нет)

## Impact

- `teams/entities/InstituteResponsible.py` — новые actions.
- `teams/services/institute_responsible_service.py` — оркестрация list/detail.
- Новые/расширенные repository-выборки и DTO под stats-контракт (не ломая существующие `employees`, `group-mentors`, `students`, `teams`).
- Тесты: `tests/teams/test_institute_responsible_viewset.py` (или отдельный модуль).
- Зависимостей от внешних сервисов нет.
