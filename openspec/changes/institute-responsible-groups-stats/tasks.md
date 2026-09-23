# Tasks

## 1. Repository: batch команд с наставниками

- [x] 1.1 Расширить `list_team_semesters_for_groups` (или добавить параметр/`Prefetch`) так, чтобы подгружались `mentors` и при необходимости FK `mentor` без N+1; проверить через `CaptureQueriesContext` / `assertNumQueries` на фикстуре с несколькими командами
- [x] 1.2 Убедиться, что `list_for_institutes` отдаёт `students_count`, `students_in_teams_count` и что `members_count` на `TeamSemester` доступен для list; проверить счётчики на фикстуре с известными числами

## 2. DTO и service

- [x] 2.1 Создать `teams/dto/institute_responsible_groups_stats.py`: list-item (`IStatsGroup`), detail (`IStatsGroupDetail`), team list/detail, member с `role`, mentor `{id:number, fullName}`; переиспользовать stats-студента mentors; проверить `to_dict()` на объектах-фикстурах
- [x] 2.2 Реализовать `list_groups_stats` / `get_group_stats_detail` в `InstituteResponsibleService` с multi-institute resolve и 404 для чужой/неактивной группы; проверить сценарии из spec через сервисные/API тесты

## 3. ViewSet

- [x] 3.1 Добавить actions `groups-stats` и `groups-stats/{id}` в `InstituteResponsibleViewSet` с обязательным `semester_id` и OpenAPI-параметрами; проверить маршруты через APIClient (200/400); убедиться, что `GET groups/` и `groups-overview` не изменились

## 4. Тесты

- [x] 4.1 API-тесты list: права (403 student), обязательный `semester_id` (400), группа без команд, cpds видит несколько институтов, validator — только свои, shape `teams[].studentsCount` / `studentsInTeamCount`; `pytest` зелёный
- [x] 4.2 API-тесты detail: полный shape students/teams/members(+role)/mentors, 404 чужой институт и неактивная группа, пустые teams; `pytest` зелёный
- [x] 4.3 Регрессия: `pytest tests/teams/test_institute_responsible_viewset.py tests/teams/test_institute_responsible_mentors_stats.py tests/teams/test_institute_responsible_projects_stats.py` (и новый модуль) зелёный

## 5. Graphify

- [x] 5.1 После правок кода выполнить `graphify update .` и убедиться, что команда завершилась без ошибки
