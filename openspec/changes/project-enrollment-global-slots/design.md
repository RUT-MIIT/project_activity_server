# Design

## Context

See proposal.md — Why. Сейчас `StudentShowcaseRepository.count_enrolled_teams` / `map_enrolled_teams_counts` / `count_enrolled_teams_for_update` фильтруют по `(semester_id, project_track_id, project_application_id)`. Тот же репозиторий используют:

- `StudentShowcaseService` (list / detail / enroll капитана);
- `MentorTeamService.enroll_project` (запись/смена проекта наставником).

Доменный метод `StudentShowcaseDomain.ensure_enrollment_slot_available(enrolled_count, max_teams)` уже корректен: менять нужно только источник `enrolled_count`. Фронт-док `docs/frontend/student_showcase.md` уже описывает глобальный слот.

## Goals / Non-Goals

**Goals:**

- Один источник правды: занятость слотов = count `TeamSemester` по `project_application_id` (и семестру при необходимости), без `project_track_id`.
- Согласованные list/detail/`can_enroll`/enroll капитана и наставника.
- Сохранить имена полей API; конкурентный enroll не превышает глобальную квоту.

**Non-Goals:**

- Миграция/откат уже перелимиченных заявок на проде.
- Лимит при admin mixed-team.
- Изменение смысла `ProjectTrack.recommendedTeamsCount` (сумма rec заявок трека для лобби).
- Переименование API-полей или новый эндпоинт.

## Decisions

### 1. Глобальный count в репозитории витрины

Изменить три метода в `showcase/repositories/student_showcase.py`:

| Метод | Было | Станет |
|-------|------|--------|
| `map_enrolled_teams_counts` | `dict[(track_id, app_id), int]` | `dict[app_id, int]` (или оставить ключ-пару, но считать без группировки по треку — предпочтительно упростить до `app_id`) |
| `count_enrolled_teams` | + `track_id` | без `track_id` (параметр убрать или игнорировать с deprecate в сигнатуре за один проход — лучше убрать и поправить call sites) |
| `count_enrolled_teams_for_update` | + `track_id` + `select_for_update` | без `track_id`; lock всех `TeamSemester` заявки (и семестра) |

**Альтернатива:** считать глобально только в service, оставив per-track map — отвергнуто: легко рассинхронизировать mentor/student и list vs enroll.

**Семестр:** оставить фильтр `semester_id` наряду с `project_application_id` (заявка уже привязана к семестру; фильтр дешёвый и защищает от аномалий).

### 2. Call sites

- `StudentShowcaseService.list_tracks_for_group` — lookup `enrolled_map[application.id]`.
- `get_project` / `enroll` — вызовы без `track_id`.
- `MentorTeamService.enroll_project` — тот же `count_enrolled_teams_for_update` без трека; `exclude_team_semester_id` при rewrite уже есть — сохранить.

### 3. Тесты

Добавить/расширить сценарий «одна заявка — два трека — rec=1»: занятость в треке A блокирует enroll в треке B для капитана и наставника. Существующие quota-тесты в одном треке должны остаться зелёными.

### 4. Документация

В `docs/frontend/student_showcase.md` одной фразой уточнить: enrolled считается по всем трекам заявки. Контракт полей без изменений.

## Risks / Trade-offs

- [Перелимиченные заявки на проде] → После деплоя новые записи закрыты; 10/3 остаётся до ручного разбора. Согласовано с заказчиком.
- [Жёсткая конкуренция за популярный проект между треками] → Ожидаемое поведение квоты; UX: фронт видит общий enrolled и disabled enroll.
- [Lock всех команд заявки при enroll] → Чуть шире, чем lock «в треке»; на практике число команд на заявку мало (единицы–десятки), приемлемо.

## Migration Plan

1. Задеплоить код с глобальным счётчиком.
2. Data-fix / un-enroll не делаем.
3. Rollback: откат коммита возвращает per-track подсчёт (старое поведение).

## Open Questions

(нет — scope зафиксирован в explore)
