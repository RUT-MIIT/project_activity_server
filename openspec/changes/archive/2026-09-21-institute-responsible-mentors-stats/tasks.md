# Tasks

## 1. Repository: выборки без N+1

- [x] 1.1 Добавить выборку наставников `role=mentor` по `department_id__in` и построение карты `department_id → {code, name}` института; проверить unit/ручным запросом, что наставник без групп попадает в qs, а student — нет
- [x] 1.2 Добавить batch-выборку связей mentor↔group в семестре (через `StudyGroupSemester.mentors`) и агрегацию group ids на mentor_id; проверить, что M2M (два наставника на одну группу) даёт группу обоим
- [x] 1.3 Переиспользовать `_with_counts` для `studentsCount` / per-group `teams_count` и суммировать `teamsCount` на наставника; проверить счётчики на фикстуре с известными числами
- [x] 1.4 Добавить `list_for_groups(group_ids, semester_id, with_project=True)` в `ContingentStudentRepository` (или аналог) без цикла по группам; проверить отсутствие N+1 через `assertNumQueries` / django debug
- [x] 1.5 Добавить batch `TeamSemester` по `home_study_group_id__in` с `members_count` и Prefetch `members__user` + project; проверить, что members доступны без доп. запросов

## 2. DTO и service

- [x] 2.1 Создать stats-DTO list/detail (`fullName`, `institute.id` string, `project.name` из title, `TeamSemester.id`); проверить `to_dict()` на объектах-фикстурах
- [x] 2.2 Реализовать `list_mentors_stats` / `get_mentor_stats_detail` в `InstituteResponsibleService` с multi-institute resolve и 404 для чужого/не-mentor; проверить сценарии из spec через сервисные/API тесты

## 3. ViewSet

- [x] 3.1 Добавить actions `mentors` и `mentors/{id}` в `InstituteResponsibleViewSet` с обязательным `semester_id` и OpenAPI-параметрами; проверить маршруты через APIClient (200/400)

## 4. Тесты

- [x] 4.1 API-тесты list: права (403 student), обязательный semester_id (400), mentor без групп, cpds видит несколько институтов, validator — только свои; `pytest` зелёный
- [x] 4.2 API-тесты detail: полный shape students/teams/members, 404 чужой институт, пустые groups; `pytest` зелёный
- [x] 4.3 Регрессия: существующие тесты `institute-responsible` не падают; `pytest tests/teams/test_institute_responsible_viewset.py` (и новый модуль, если вынесен)

## 5. Graphify

- [x] 5.1 После правок кода выполнить `graphify update .` и убедиться, что команда завершилась без ошибки
