# Design

## Context

См. proposal.md — Why. Сейчас `InstituteResponsibleViewSet` умеет `employees`, `group-mentors`, `groups-overview`, `students`, `teams`, но не «наставник как сущность аналитики». Назначения живут в M2M `StudyGroupSemester.mentors`; контингент и счётчики уже собраны без N+1 в `MentorGroupsRepository._with_counts` и `ContingentStudentRepository`.

Ограничение: у существующих эндпоинтов `institute_code` при отсутствии резолвится в **один** институт. Для mentors list нужна другая семантика — **множество** доступных институтов.

## Goals / Non-Goals

**Goals:**

- Два GET под фронтовый дашборд с согласованным JSON (camelCase).
- Выборки с константным (или малым) числом запросов относительно размера ответа.
- Переиспользовать правила доступа `InstituteResponsiblePermission` / `get_accessible_institute_codes`.

**Non-Goals:**

- KPI/агрегаты отдельным эндпоинтом и Excel-экспорт наставников.
- Поле `loadStatus` на бэке.
- Изменение контрактов `employees`, `students`, `group-mentors`.
- Пагинация list (объём — наставники институтов; фильтры на клиенте).

## Decisions

### 1. Размещение API

Новые actions на `InstituteResponsibleViewSet`:

- `GET mentors/` → `url_path="mentors"`
- `GET mentors/<id>/` → `url_path=r"mentors/(?P<mentor_id>\d+)"`

**Альтернатива:** отдельный ViewSet / dashboard app — отклонено: та же роль и контекст семестра.

### 2. Resolve институтов для list

Новый путь в service (не `_resolve_context` с одним кодом):

1. Проверить `can_access` / department.
2. `semester_id = Semester.resolve_list_semester_id(...)`.
3. `codes = get_accessible_institute_codes(user)` → если `None`, взять все активные `Institute.code`.
4. `department_ids = get_department_ids_for_institute_codes(codes)`.
5. Mentors: `User.objects.filter(role__code="mentor", department_id__in=department_ids)` (+ select_related по необходимости).

Карта `department_id → Institute {code, name}` строится один раз из `Institute` + деревьев подразделений (как в `get_department_ids_by_institute_code`, обратный индекс).

**Альтернатива:** только назначенные в семестре наставники — отклонено (нужны «без групп»).

### 3. List без N+1

```
mentors (1 qs)
  -> enrollments: StudyGroupSemester.filter(semester, mentors__in=ids)
       .select_related(study_group)
       .prefetch mentors only id  OR values(mentor_id, group_id)
  -> group_ids unique
  -> MentorGroupsRepository._with_counts(groups, semester)  # studentsCount, teams_count per group
  -> aggregate in Python: mentor_id -> groups[], sum(teams_count)
```

Учитывать M2M: одна группа может попасть к нескольким наставникам.  
`teamsCount` наставника = сумма `teams_count` его групп (не distinct по team id между наставниками — на уровне одного наставника группы не пересекаются по смыслу home_study_group; если теоретически дубль группы — использовать set group ids).

### 4. Detail без N+1

1. Загрузить наставника; проверить role + institute в accessible codes → иначе 404.
2. Группы наставника в семестре (как `list_for_mentor`).
3. Батч студентов: расширить/добавить метод репозитория `list_for_groups(group_ids, semester_id, with_project=True)` на базе `ContingentStudentRepository` (не цикл `list_for_group`).
4. Батч команд: `TeamSemester` по `home_study_group_id__in` + `annotate(members_count)` + `prefetch members__user` (+ project_application).
5. Собрать stats-DTO: студент и `team.members[]` из одних загруженных данных.

`id` команды / `student.team.id` = `TeamSemester.id`.  
`project.name` ← `ProjectApplication.title`.  
`course` ← `StudyGroup.course_number`.  
`fullName` ← сборка ФИО (как `get_full_name` / `TeamLobbyDomain.user_display_name`).

### 5. Отдельные stats-DTO

Не переиспользовать `InstituteResponsibleStudentDTO` / `MentorGroupStudentDTO` (другой shape: `fullName`, `project.name`, вложенный `institute`). Новые классы в `teams/dto/` (например `institute_responsible_mentors_stats.py`) или рядом с institute_responsible.

### 6. Ошибки

- Нет `semester_id` → 400 (как сейчас).
- Нет mentor / чужой институт / не mentor → 404 на detail (не светить существование).
- Нет прав на ViewSet → 403.

## Risks / Trade-offs

- **[Risk] Тяжёлый JSON detail** при многих группах/студентах → Mitigation: один mentor за запрос; list остаётся лёгким; при необходимости позже — lazy подгрузка группы.
- **[Risk] Полный `IStatsStudent` внутри `members` дублирует данные** → Mitigation: осознанный контракт фронта; в Python объекты переиспользовать.
- **[Risk] Наставник с role=mentor, но department вне институтов** не попадёт в list, даже если висит в M2M → Mitigation: соответствует правилу источника; данные чинятся назначением department.
- **[Trade-off] Без `institute_code` на list** отличается от других actions → явно задокументировать в OpenAPI summary.

## Migration Plan

Только код + тесты, миграций БД нет. Откат — удаление actions. Фронт параллельно меняет `institute.id` на `string`.

## Open Questions

Нет блокирующих. При реализации уточнить точное имя action/url только в коде (контракт путей зафиксирован в specs).
