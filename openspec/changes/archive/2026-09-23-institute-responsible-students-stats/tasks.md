# Tasks

## 1. Prefetch наставников для батча контингента

- [x] 1.1 Убедиться, что путь `list_students_for_groups` / enrollment prefetch отдаёт mentors группы в семестре без N+1; при необходимости расширить Prefetch (как в операционном `_semester_enrollment_qs`); проверить через `CaptureQueriesContext` / `assertNumQueries` на фикстуре с несколькими группами и наставниками

## 2. DTO и service

- [x] 2.1 Создать `teams/dto/institute_responsible_students_stats.py`: обёртка над `MentorsStatsStudentDTO.from_contingent` + `mentors[{id, fullName}]`; проверить `to_dict()` shape на объектах-фикстурах
- [x] 2.2 Реализовать `list_students_stats` в `InstituteResponsibleService` через `_resolve_mentors_stats_context` + `list_for_institutes` + `list_students_for_groups`; проверить multi-institute и пустой контингент через сервисные/API тесты

## 3. ViewSet

- [x] 3.1 Добавить action `students-stats` в `InstituteResponsibleViewSet` с обязательным `semester_id` и OpenAPI-параметрами; проверить маршруты через APIClient (200/400); убедиться, что `GET students/` и `students/export` не изменились

## 4. Тесты

- [x] 4.1 API-тесты list: права (403 student), обязательный `semester_id` (400), студент без команды (`team`/`project` null), mentors группы, cpds видит несколько институтов, validator — только свои, shape `IStatsStudent`; `pytest` зелёный
- [x] 4.2 Регрессия: `pytest tests/teams/test_institute_responsible_viewset.py` (students + export) и соседние stats-модули + новый `test_institute_responsible_students_stats.py` зелёный

## 5. Graphify

- [x] 5.1 После правок кода выполнить `graphify update .` и убедиться, что команда завершилась без ошибки
