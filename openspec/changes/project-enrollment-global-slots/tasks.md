# Tasks

## 1. Репозиторий: глобальный счётчик

- [x] 1.1 Изменить `map_enrolled_teams_counts` в `showcase/repositories/student_showcase.py`: группировка только по `project_application_id` (без `project_track_id`), возвращать `dict[int, int]`; обновить вызов в `list_tracks_for_group` и проверить существующий list-тест enrolled
- [x] 1.2 Убрать `track_id` из `count_enrolled_teams` и `count_enrolled_teams_for_update` (оставить `semester_id` + `application_id`, плюс `exclude_team_semester_id` / `select_for_update`); поправить все call sites в student/mentor services
- [x] 1.3 Прогнать точечно `pytest tests/showcase/entities/test_student_showcase_viewset.py tests/teams/test_mentor_team_viewset.py -q` и убедиться, что старые same-track quota-тесты зелёные

## 2. Тесты на кросс-трековую квоту

- [x] 2.1 Добавить тест капитана: заявка в двух треках, `rec=1`, команда уже записана через трек A → enroll через трек B → 400 «максимальное число команд»; list/detail показывают `enrolled=1` и `can_enroll=false`
- [x] 2.2 Добавить тест наставника: та же фикстура (или аналог) → `enroll-project` на полную заявку из другого трека → 400; идемпотентный повтор enroll на тот же проект своей команды не падает по квоте
- [x] 2.3 При необходимости поправить mentor showcase list/detail enrolled, если там отдельный путь счёта (не через обновлённый `map_enrolled_teams_counts`); проверить `tests/teams/test_mentor_showcase_viewset.py`

## 3. Документация

- [x] 3.1 В `docs/frontend/student_showcase.md` явно указать, что `enrolled_teams_count` считается по всем трекам заявки, и проверить, что описание `can_enroll` / enroll согласовано
