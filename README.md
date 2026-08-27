# project_activity_server

## Импорт контингента 1С

Источник по умолчанию: `data/контингент_14_08.xls`.

Сначала учебные группы, затем предрегистрация студентов:

```bash
python manage.py import_study_groups_from_contingent --file data/контингент_25_08.xls
python manage.py import_preregistered_students --file data/контингент_25_08.xls
```

Опции:

```bash
# группы: семестр расчёта курса (autumn/spring), год, очистка всех групп
python manage.py import_study_groups_from_contingent --file data/контингент_14_08.xls --semester autumn --year 2026
python manage.py import_study_groups_from_contingent --file data/контингент_14_08.xls --clear

# студенты: удалить только предрегистрации без привязанного User
python manage.py import_preregistered_students --file data/контингент_14_08.xls --clear
```

Если `--file` не указан, обе команды берут `data/контингент_14_08.xls`.
`--clear` у студентов не трогает уже зарегистрированных пользователей.

