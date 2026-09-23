# Proposal

## Why

Фронтенд сверстал вкладку дашборда «Группы» (аналитика для ответственного института), но бэкенд не отдаёт multi-institute список учебных групп со счётчиками/командами и детальную карточку с контингентом и составом команд. Операционные `GET groups/` и `groups-overview` не закрывают этот контракт и другую семантику доступа.

## What Changes

- Добавить `GET /api/teams/institute-responsible/groups-stats/` — список активных учебных групп по всем доступным институтам в семестре (`IStatsGroup`: институт, курс, `studentsCount`, `studentsInTeamCount`, вложенные `teams[{id,name,studentsCount}]`).
- Добавить `GET /api/teams/institute-responsible/groups-stats/{id}/` — детальная карточка (`IStatsGroupDetail`: студенты в формате stats-студента как у mentors; команды с `status`, `members` (+ `role`), `mentors` с `id:number` / `fullName`).
- Обязательный `semester_id`; фильтрация по институту/курсу на клиенте (как у mentors/projects).
- Статусы заполненности группы на бэке не отдаём — считает фронт.
- Существующие `GET groups/`, `groups-overview`, `group-mentors`, `groups/{id}/mentor` **не меняем** (path `groups-stats` выбран, чтобы не ломать операционку).
- Excel-экспорт вкладки — вне scope.

## Capabilities

### New Capabilities

- `institute-responsible-groups-stats`: API статистики учебных групп для дашборда ответственного (list + detail), доступ, семестр, контракт ответа без N+1.

### Modified Capabilities

- (нет)

## Impact

- `teams/entities/InstituteResponsible.py` — новые actions.
- `teams/services/institute_responsible_service.py` — оркестрация list/detail (переиспользовать multi-institute resolve mentors/projects).
- Новые DTO (например `institute_responsible_groups_stats.py`); выборки — через уже существующие `MentorGroupsRepository.list_for_institutes`, `list_students_for_groups`, `list_team_semesters_for_groups` / аналоги с доработкой prefetch наставников команды при необходимости.
- Тесты: отдельный модуль по образцу `test_institute_responsible_mentors_stats.py` / `..._projects_stats.py`.
- Зависимостей от внешних сервисов нет.
