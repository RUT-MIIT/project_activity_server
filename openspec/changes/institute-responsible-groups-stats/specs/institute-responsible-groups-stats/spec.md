# Spec Delta

## Purpose

Описывает API статистики учебных групп для дашборда ответственного института: список групп со счётчиками и командами по доступным институтам в семестре и детальная карточка с контингентом и составом команд.

## ADDED Requirements

### Requirement: Список групп по доступным институтам

Система SHALL предоставлять аутентифицированным пользователям с ролью `institute_validator`, `cpds`, `admin` либо `is_staff` эндпоинт `GET /api/teams/institute-responsible/groups-stats/`, который возвращает массив учебных групп для аналитики.

Система MUST требовать query-параметр `semester_id` (числовой id либо `actual` / `next`). При отсутствии параметра система MUST отвечать HTTP 400.

Система SHALL включать активные (`is_end=False`) учебные группы, у которых `institute_id` входит в множество **всех доступных** институтов вызывающего (для `cpds` / `admin` / `staff` — все активные институты; для `institute_validator` — институты его подразделения). Параметр `institute_code` для этого эндпоинта не обязателен и не сужает выборку по умолчанию: фильтрация по институту и курсу выполняется на клиенте по полям `institute` и `course`.

Система MUST NOT изменять контракт существующих эндпоинтов `GET .../groups/`, `GET .../groups-overview/` и назначения наставников `.../groups/{id}/mentor/`.

Каждый элемент списка MUST содержать:

- `id` (number) — id учебной группы;
- `name` (string);
- `institute` — объект `{ id: string, name: string }`, где `id` равен `Institute.code`;
- `studentsCount` (number) — размер контингента группы (предрегистрация + прямые студенты без двойного учёта), как в обзоре групп наставника / `groups-overview`;
- `studentsInTeamCount` (number) — число студентов контингента, состоящих в команде семестра (как `studentsInTeamsCount` в overview, имя поля — по контракту дашборда);
- `course` (number) — `StudyGroup.course_number`;
- `teams` — массив `{ id, name, studentsCount }`, где `id` — id записи `TeamSemester` домашней группы в запрошенном семестре, `studentsCount` — число участников команды (`TeamSemesterMember`).

Система MUST включать группы без команд (`teams: []`, `studentsInTeamCount = 0`).

Система MUST NOT включать в ответ вычисляемый статус заполненности («Нет команд» / «Есть студенты без команды» / «Все студенты в командах»): его считает клиент.

Система MUST выполнять выборку без N+1 (число SQL-запросов не растёт пропорционально числу групп или команд).

#### Scenario: Успешный список для ответственного института

- **WHEN** пользователь с ролью `institute_validator` запрашивает `GET .../groups-stats/?semester_id=actual`
- **THEN** система возвращает HTTP 200 и массив групп только по институтам, доступным этому пользователю, включая записи с пустым `teams`

#### Scenario: cpds видит группы всех институтов

- **WHEN** пользователь с ролью `cpds` запрашивает `GET .../groups-stats/?semester_id=<id>`
- **THEN** система возвращает группы по всем активным институтам

#### Scenario: semester_id обязателен

- **WHEN** клиент вызывает `GET .../groups-stats/` без `semester_id`
- **THEN** система возвращает HTTP 400 с описанием ошибки

#### Scenario: Группа без команд в списке

- **WHEN** в доступном институте есть активная учебная группа без `TeamSemester` в семестре
- **THEN** она присутствует в ответе с `teams: []` и `studentsInTeamCount = 0`

### Requirement: Детальная карточка группы

Система SHALL предоставлять `GET /api/teams/institute-responsible/groups-stats/{id}/` с обязательным `semester_id`.

Система MUST вернуть HTTP 404, если группа с таким id не найдена, неактивна (`is_end=True`), либо её институт не входит в доступные вызывающему.

При успехе ответ MUST содержать:

- `id`, `name`, `institute` (`{ id: string, name }`), `course` — как в элементе списка;
- `students` — полный контингент группы в формате stats-студента;
- `teams` — команды группы в семестре в формате stats-команды группы.

Stats-студент MUST содержать: `id`, `fullName`, `institute` (`{ id: string, name }`), `studyGroup` (`{ id, name }`), `course` (номер курса группы), `isRegistered`, `team` (`{ id, name } | null`), `project` (`{ id, name } | null`).  
`team.id` и id команды в `teams` MUST быть id записи `TeamSemester`.  
`project.name` MUST заполняться из названия заявки (`ProjectApplication.title`).

Stats-команда группы MUST содержать:

- `id`, `name`, `status`;
- `members` — массив участников: `id`, `fullName`, `institute`, `studyGroup`, `course`, `role` (роль в `TeamSemesterMember`);
- `mentors` — массив `{ id: number, fullName }` наставников команды (`TeamSemester.mentors`, с fallback на `TeamSemester.mentor` при пустом M2M).

Система MUST выполнять сборку detail без N+1 по студентам, командам, участникам и наставникам.

#### Scenario: Успешная деталь со студентами и командами

- **WHEN** ответственный запрашивает detail группы, у которой в семестре есть студенты и команды с участниками и наставниками
- **THEN** система возвращает HTTP 200, заполнены `students` и `teams`, у команд заполнены `members` (с `role`) и `mentors`

#### Scenario: Нет доступа к институту группы

- **WHEN** `institute_validator` запрашивает detail группы другого института
- **THEN** система возвращает HTTP 404

#### Scenario: Группа без команд в detail

- **WHEN** запрашивается detail активной доступной группы без команд в семестре
- **THEN** система возвращает HTTP 200 с `teams: []` и контингентом в `students`

### Requirement: Права доступа к API статистики групп

Система MUST применять те же правила доступа, что и к остальному API `institute-responsible`: только `institute_validator`, `cpds`, `admin` или `is_staff`. Неавторизованный либо недопущенный пользователь MUST получать отказ в доступе.

#### Scenario: Студент не имеет доступа

- **WHEN** пользователь с ролью `student` вызывает `GET .../groups-stats/?semester_id=actual`
- **THEN** система отказывает в доступе (HTTP 403)
