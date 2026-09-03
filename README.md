# project_activity_server

## Импорт контингента 1С

Источник по умолчанию: `data/контингент_29_08.xls` (актуальный файл кладите в `data/`).

**Контракт идентичности:** учебная группа в PD = **ID группы из 1С** (`StudyGroup.external_group_id`).
Имя берётся из колонки «Группа», код постоянной группы (`code`) — справочно, не ключ upsert.
Студенты привязываются **только** по remapped `ID группы` (без fallback по name/code).

Сначала учебные группы, затем предрегистрация студентов:

```bash
python manage.py import_study_groups_from_contingent --file data/контингент_03_09.xls
python manage.py import_preregistered_students --file data/контингент_03_09.xls
```

Поведение импорта групп:

- upsert / claim по `external_group_id`; при split одной постоянной на два ID старый `pk` забирает ID с совпадающим `name`, второй ID создаётся новой записью;
- группы, чей ID нет в файле (или пустой `external_group_id`) → `is_end=True` (без `delete`);
- слияния ID задаются в `EXTERNAL_GROUP_ID_REMAP` (например ТСТ-442→441: `193902`→`193901`);
- оверрайды имени/института по ID — `STUDY_GROUP_OVERRIDES_BY_EXTERNAL_ID` (ЭПО и т.п.).

Опции:

```bash
# группы: --year/--semester устарели (не влияют на identity); --clear удаляет все группы
python manage.py import_study_groups_from_contingent --file data/контингент_03_09.xls --clear

# студенты: удалить только предрегистрации без привязанного User
python manage.py import_preregistered_students --file data/контингент_03_09.xls --clear
```

Если `--file` не указан, обе команды берут файл по умолчанию из кода команды.
`--clear` у студентов не трогает уже зарегистрированных пользователей.

## Преподаватели проектной деятельности (`project_teachers_marked.xlsx`)

Файл `data/project_teachers_marked.xlsx` — сводка по дисциплине «Проектная деятельность» из расписания РУТ (МИИТ) с пометкой, есть ли преподаватель в PD.

### 1. Обновить Excel (локально)

Из корня проекта, в активированном venv:

```bash
python data/sync_project_teachers.py
```

Скрипт по порядку:

1. Обновляет `data/prod_users.json` с prod API PD (для колонок «В системе PD», «ID в PD», «Email в PD»)
2. Парсит расписание всех групп через API `rut-miit.ru`
3. Сохраняет результат в `data/project_teachers_marked.xlsx`

Переменные в `.env` (корень проекта):

```env
PROD_PD_API_URL=https://pd.rut-miit.ru
PROD_PD_API_TOKEN=...          # приоритет: если задан, login не нужен
PROD_PD_EMAIL=...
PROD_PD_PASSWORD=...
```

Полезные опции:

```bash
# другой выходной файл
python data/sync_project_teachers.py --output data/project_teachers_marked.xlsx

# не тянуть пользователей с prod (использовать уже скачанный prod_users.json)
python data/sync_project_teachers.py --skip-refresh-users

# параллелизм запросов к RUT API
python data/sync_project_teachers.py --concurrency 8
```

Подробности парсинга расписания — в [data/timetable/README.md](data/timetable/README.md).

Устаревший вариант (только сверка готового `project_teachers.xlsx`): `data/mark_teachers_in_system.py` — не использовать, см. `sync_project_teachers.py`.

### 2. Загрузить в БД на проде

**Порядок:** сначала в PD должны быть актуальные учебные группы (`import_study_groups_from_contingent`), потому что импорт преподавателей ищет группу по колонке **«Группа»** = `StudyGroup.name`.

На сервере (в каталоге проекта, venv активен):

```bash
# 1. Положить свежий файл (с локальной машины), например:
# scp data/project_teachers_marked.xlsx user@host:/path/to/project/data/

# 2. Импорт в БД (идемпотентный upsert по семестр + группа + ID преподавателя)
python manage.py import_project_teachers_from_excel --file data/project_teachers_marked.xlsx
```

Команда создаёт/обновляет записи `StudyGroupProjectTeacher` и добавляет преподавателя в наставники группы на семестр (`StudyGroupSemester`), если пользователь найден в PD (по «ID в PD» или по ФИО).

Строки без преподавателя или без «ID преподавателя» пропускаются. В логе смотрите счётчики: `создано`, `обновлено`, `пропущено`, `групп не найдено`, `семестров не найдено`.

**Типичный полный цикл на проде после обновления контингента:**

```bash
# желательно: dumpdata teams.StudyGroup перед прогоном
python manage.py import_study_groups_from_contingent --file data/контингент_03_09.xls
python manage.py import_preregistered_students --file data/контингент_03_09.xls
python manage.py import_project_teachers_from_excel --file data/project_teachers_marked.xlsx
```

Если имена групп в PD переименованы (например ЭБП → ЭПТ в `teams/domain/study_group_import.py`), а в расписании РУТ ещё старые аббревиатуры — строки с несовпадающим «Группа» попадут в `групп не найдено`; при необходимости поправьте имена в Excel или дождитесь обновления каталога групп на стороне RUT.

