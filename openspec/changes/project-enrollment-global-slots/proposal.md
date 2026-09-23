# Proposal

## Why

Лимит команд на проектную заявку (`recommended_teams_count`) задуман как квота **на заявку**, и фронтовая документация витрины уже так описывает слоты. Фактически счётчик записи фильтрует по `project_track_id`, поэтому одна заявка в нескольких треках допускает `rec × N` команд (на проде до 10 при `rec=3`). Нужно выровнять поведение с контрактом и закрыть обход через запись капитаном и наставником.

## What Changes

- Считать занятые слоты **глобально по заявке** (все `TeamSemester` с данным `project_application`), без фильтра по треку.
- В API студенческой и наставнической витрины отдавать `enrolled_teams_count` / `enrolledTeamsCount` и `can_enroll` по этому глобальному счётчику (имена полей без изменений).
- При `POST .../enroll` капитана и при записи/смене проекта наставником проверять `enrolled < recommended_teams_count` по заявке целиком (с блокировкой строк всех команд заявки).
- Уже перелимиченные заявки на проде **не мигрируем и не откатываем** — только блокируем новые записи сверх квоты.
- Admin mixed-team и пересчёт `ProjectTrack.recommendedTeamsCount` (сумма rec заявок трека для лобби) **вне скоупа**.

## Capabilities

### New Capabilities

- `project-enrollment-slots`: правила квоты команд на проектную заявку при отображении витрины и при записи капитаном/наставником.

### Modified Capabilities

- (нет — существующих OpenSpec-capability по витрине/enroll нет)

## Impact

- `showcase/repositories/student_showcase.py` — `map_enrolled_teams_counts`, `count_enrolled_teams`, `count_enrolled_teams_for_update`.
- `showcase/services/student_showcase_service.py` — list/detail/enroll капитана.
- `teams/services/mentor_team_service.py` — enroll-project наставника.
- DTO витрины без смены имён полей; семантика `enrolled_*` становится глобальной.
- Тесты: `test_student_showcase_viewset.py`, `test_mentor_team_viewset.py` / mentor showcase, domain-тесты слотов.
- Документация `docs/frontend/student_showcase.md` уже описывает глобальный слот — при необходимости уточнить явно «по всем трекам».
