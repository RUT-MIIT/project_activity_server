# Spec Delta

## MODIFIED Requirements

### Requirement: Детальная карточка наставника

Система SHALL предоставлять `GET /api/teams/institute-responsible/mentors/{id}/` с обязательным `semester_id`.

Система MUST вернуть HTTP 404, если пользователь с таким id не найден, не имеет роли `mentor`, либо его институт не входит в доступные вызывающему.

При успехе ответ MUST содержать те же поля верхнего уровня, что и элемент списка (`id`, `fullName`, `institute`, `teamsCount`), а `groups` MUST быть массивом детальных групп:

- `id`, `name`;
- `students` — полный контингент группы в формате stats-студента;
- `teams` — команды группы в семестре в формате stats-команды.

Stats-студент MUST содержать: `id`, `fullName`, `institute` (`{ id: string, name }`), `studyGroup` (`{ id, name }`), `course` (номер курса группы), `isRegistered`, `team` (`{ id, name } | null`), `project` (`{ id, name, applicationKind, caseDescription } | null`).
`team.id` и id команды в `teams` MUST быть id записи `TeamSemester`.
`project.name` MUST заполняться из названия заявки (`ProjectApplication.title`).

Stats-команда MUST содержать: `id`, `name`, `status`, `project` (`{ id, name, applicationKind, caseDescription } | null`), `studyGroup` (`{ id, name }`), `members` (массив stats-студентов — участников команды), `membersCount`.

Система MUST выполнять сборку detail без N+1 по группам, студентам и участникам команд.

#### Scenario: Успешная деталь с группами

- **WHEN** ответственный запрашивает detail наставника, у которого в семестре есть группы со студентами и командами
- **THEN** система возвращает HTTP 200, в каждой группе заполнены `students` и `teams`, у команд заполнены `members` и `membersCount`

#### Scenario: Нет доступа к институту наставника

- **WHEN** `institute_validator` запрашивает detail наставника другого института
- **THEN** система возвращает HTTP 404

#### Scenario: Наставник без групп в detail

- **WHEN** запрашивается detail наставника без назначений в семестре
- **THEN** система возвращает HTTP 200 с `groups: []` и `teamsCount: 0`
