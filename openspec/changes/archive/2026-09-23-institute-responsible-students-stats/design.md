# Design

## Context

См. proposal.md — Why. Уже есть:

- multi-institute resolve для mentors/projects/groups-stats (`_resolve_mentors_stats_context` / `_resolve_accessible_institute_codes`);
- `MentorGroupsRepository.list_for_institutes` — активные группы по кодам институтов;
- `InstituteResponsibleRepository.list_students_for_groups` — батч контингента с членством в команде/проектом;
- `MentorsStatsStudentDTO` — почти полный `IStatsStudent` (без `mentors`);
- операционный `InstituteResponsibleStudentDTO` + `list_institute_students` (single-institute, другой JSON) — не трогаем.

## Goals / Non-Goals

**Goals:**

- Один GET `students-stats/` под фронтовый дашборд «Студенты» с camelCase JSON.
- Константное (малое) число SQL относительно размера ответа.
- Переиспользовать access/semester resolve и batch контингента groups/mentors stats.

**Non-Goals:**

- Detail `students-stats/{id}`.
- KPI/агрегаты отдельным эндпоинтом.
- Изменение `GET students/` и Excel `students/export`.
- Пагинация list (фильтры институт/курс/статус на клиенте).
- Серверная фильтрация по `institute_code` / `course` (клиент фильтрует).

## Decisions

### 1. Path `students-stats` (не `students`)

Новый action на `InstituteResponsibleViewSet`:

- `GET students-stats/` → `url_path="students-stats"`

**Альтернатива:** заменить контракт `GET students/` — отклонено: ломает операционку и Excel; спека `institute-students-excel` явно держит JSON-контракт списка стабильным.

### 2. Resolve институтов

Тот же multi-institute путь, что mentors/projects/groups-stats (`_resolve_mentors_stats_context`): semester + accessible institute codes + карта институтов.

Группы: `list_for_institutes(codes, semester_id)` (только активные).  
Студенты: `list_students_for_groups(group_ids, semester_id)`.

`institute` в ответе — по `group.institute_id` из карты `institute_by_code`.

### 3. List без N+1

```
codes, semester, institute_by_code = _resolve_mentors_stats_context(...)
groups = list_for_institutes(codes, semester)
students = list_students_for_groups({g.id}, semester)
  # контингент уже с membership/project prefetch
  # наставники группы: через semester enrollment Prefetch на группах
  -> DTO: MentorsStatsStudentDTO + mentors[{id, fullName}]
```

Если текущий `list_students_for_groups` / enrollment prefetch не отдаёт mentors группы — расширить prefetch один раз (как в операционном `_semester_enrollment_qs` / `_mentors_from_group`), без пер-студентных запросов.

### 4. DTO: stats-студент + mentors

Вариант A (предпочтительный): в `teams/dto/institute_responsible_students_stats.py` тонкая обёртка/`StudentsStatsStudentDTO`, которая берёт `MentorsStatsStudentDTO.from_contingent(...).to_dict()` и добавляет `mentors` из enrollment группы (`{id, fullName}` через тот же naming, что `InstituteResponsibleEmployeeDTO`).

Вариант B: добавить `mentors` прямо в `MentorsStatsStudentDTO` (default `[]`) — допустимо как additive поле во вложенных students mentors/groups detail, но меняет чужой модуль без нужды; для этого change достаточно обёртки.

Имя поля наставника: **`fullName`**, не `fullname` из черновика фронта.

### 5. Ошибки

- Нет `semester_id` → 400.
- Нет прав ViewSet → 403.
- Пустой контингент → `[]` (200).

## Risks / Trade-offs

- **[Risk] Тяжёлый list** при большом контингенте всех институтов → Mitigation: один batch без per-student queries; пагинация вне scope (как у остальных stats-вкладок).
- **[Risk] Путаница path `students` vs `students-stats`** → Mitigation: OpenAPI summary явно «для дашборда»; фронт переключает моки на `students-stats`.
- **[Trade-off] Дублирование контингента** с операционным `/students/` → сознательно: разные контракты и семантика доступа (один институт vs все доступные).

## Migration Plan

Только код + тесты, миграций БД нет. Откат — удаление action. Фронт переключает вкладку «Студенты» с моков на `students-stats`.

## Open Questions

Нет блокирующих.
