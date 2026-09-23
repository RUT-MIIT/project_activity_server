# Proposal

## Why

Фронтенд сверстал вкладку дашборда «Студенты» (аналитика для ответственного института) под контракт `IStatsStudent`, но бэкенд отдаёт только операционный `GET .../students/` с другим JSON (раздельное ФИО, `teamName`/`teamRole`, `project.title`, без `institute`/`course`, single-institute). Ломать этот контракт нельзя: на нём завязаны операционка и Excel-выгрузка.

## What Changes

- Добавить `GET /api/teams/institute-responsible/students-stats/` — multi-institute список контингента в формате stats-студента для дашборда (`IStatsStudent`: `fullName`, `institute`, `studyGroup`, `course`, `isRegistered`, `team`/`project` как объекты или `null`, `mentors[{id, fullName}]`).
- Обязательный `semester_id`; фильтрация по институту/курсу/статусу на клиенте (как у mentors/projects/groups-stats).
- Detail `students-stats/{id}` **не** добавляем — хватает списка.
- KPI и графики дашборда бэкенд не считает.
- Существующие `GET .../students/` и `GET .../students/export/` **не меняем**.

## Capabilities

### New Capabilities

- `institute-responsible-students-stats`: API списка студентов для дашборда ответственного (stats-контракт, multi-institute, доступ, семестр, без N+1).

### Modified Capabilities

- (нет)

## Impact

- `teams/entities/InstituteResponsible.py` — новый action `students-stats`.
- `teams/services/institute_responsible_service.py` — оркестрация list (переиспользовать multi-institute resolve mentors/projects/groups-stats).
- DTO: расширить или обернуть `MentorsStatsStudentDTO` полем `mentors` (новый файл вроде `institute_responsible_students_stats.py` и/или доработка mentors-stats DTO).
- Выборки: активные группы по доступным институтам + `list_students_for_groups` / контингент с prefetch наставников группы в семестре.
- Тесты: отдельный модуль по образцу `test_institute_responsible_mentors_stats.py` / `..._groups_stats.py`.
- Зависимостей от внешних сервисов нет.
