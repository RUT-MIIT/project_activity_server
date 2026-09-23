# Design

## Context

См. proposal.md — Why. Уже есть:

- multi-institute stats для mentors/projects (`_resolve_mentors_stats_context`);
- `MentorGroupsRepository.list_for_institutes` + `_with_counts` (`students_count`, `students_in_teams_count`, `teams_count`);
- `InstituteResponsibleRepository.list_students_for_groups`, `list_team_semesters_for_groups`, `list_groups_with_counts`;
- stats-студент mentors (`MentorsStatsStudentDTO`) и detail-команда projects (`ProjectsStatsTeamDetailDTO` / mentors с иным naming).

Операционные `GET groups/` и `groups-overview` остаются на single-institute `_resolve_context` и другом JSON.

## Goals / Non-Goals

**Goals:**

- Два GET под фронтовый дашборд «Группы» с camelCase JSON.
- Константное (малое) число SQL относительно размера ответа.
- Переиспользовать access/semester resolve mentors/projects и существующие batch-выборки контингента/команд.

**Non-Goals:**

- KPI/агрегаты отдельным эндпоинтом и Excel-экспорт групп.
- Статус заполненности на бэке.
- Изменение контрактов `groups`, `groups-overview`, `group-mentors`, students/teams lists.
- Пагинация list (фильтры институт/курс на клиенте).

## Decisions

### 1. Path `groups-stats` (не `groups`)

Новые actions на `InstituteResponsibleViewSet`:

- `GET groups-stats/` → `url_path="groups-stats"`
- `GET groups-stats/<id>/` → `url_path=r"groups-stats/(?P<group_id>\d+)"`

**Альтернатива:** переиспользовать `GET groups/` под новый контракт — отклонено: ломает операционку (`courseNumber` / `directionCode`) и тесты; семантика доступа другая (один институт vs все доступные).

**Альтернатива:** эволюционировать `groups-overview` — отклонено: single-institute, другой shape, нет detail.

### 2. Resolve институтов

Тот же multi-institute путь, что mentors/projects (`_resolve_mentors_stats_context` / `_resolve_accessible_institute_codes`): semester + accessible institute codes + карта институтов.

Группы: `MentorGroupsRepository.list_for_institutes(codes, semester_id)` (активные, с counts).  
`institute` в ответе — по `group.institute_id` из карты `institute_by_code`.

### 3. List без N+1

```
groups = list_for_institutes(codes, semester)   # students_count, students_in_teams_count
  -> team_semesters = list_team_semesters_for_groups(group_ids, semester)
       (уже annotate members_count)
  -> group_id -> teams[{ id: TS.id, name, studentsCount: members_count }]
  -> DTO: studentsInTeamCount <- students_in_teams_count
```

Отдельный qs на members для list не нужен — достаточно `members_count`.

### 4. Detail без N+1

1. Загрузить группу (`id`, `name`, `course_number`, `institute_id`, `is_end`); проверить институт в accessible → иначе 404.
2. `list_students_for_groups({group_id}, semester)` + `MentorsStatsStudentDTO` (или общий helper stats-студента).
3. Команды: расширить `list_team_semesters_for_groups` (или локальный prefetch) — `Prefetch` mentors + fallback `mentor` FK, как в projects stats.
4. Members DTO: projects-member shape + поле `role` из `TeamSemesterMember.role`.
5. Mentors DTO: `{ id: int, fullName }` (не string/`fullname` из projects — выравнивание под фронт Groups и docs треков).

### 5. Отдельные groups-stats DTO

Файл вроде `teams/dto/institute_responsible_groups_stats.py`.  
Переиспользовать сборку stats-студента из mentors DTO (import/classmethod), не тащить тяжёлую `MentorsStatsTeamDTO`.

### 6. Ошибки

- Нет `semester_id` → 400.
- Нет группы / чужой институт / `is_end` → 404 на detail.
- Нет прав ViewSet → 403.

## Risks / Trade-offs

- **[Risk] Тяжёлый list** при многих группах и вложенных `teams[]` → Mitigation: list без members/students; только counts; клиент фильтрует.
- **[Risk] Путаница path `groups` vs `groups-stats`** → Mitigation: явно в OpenAPI summary и фронтовой интеграции.
- **[Trade-off] `studentsInTeamCount` vs overview `studentsInTeamsCount`** → сознательно имя дашборда; значение то же.
- **[Trade-off] Mentors naming в projects остаётся прежним** → Groups не копирует `fullname`/string id.

## Migration Plan

Только код + тесты, миграций БД нет. Откат — удаление actions. Фронт переключает вкладку с моков на `groups-stats`.

## Open Questions

Нет блокирующих. При желании фронт позже может попросить alias на `groups` после миграции операционных клиентов — вне этого change.
