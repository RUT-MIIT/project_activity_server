# Парсинг «Проектная деятельность» — РУТ (МИИТ)

Скрипт обходит все группы университета через публичный JSON API `rut-miit.ru`, находит преподавателей по дисциплине «Проектная деятельность» и сохраняет результат в Excel.

## Полный пайплайн (парсинг + сверка с PD)

Из корня проекта:

```bash
python data/sync_project_teachers.py
```

Команда:
1. Обновляет `data/prod_users.json` с prod API (`https://pd.rut-miit.ru`)
2. Парсит расписание всех групп РУТ
3. Сверяет преподавателей с пользователями PD и сохраняет `data/project_teachers_marked.xlsx`

Переменные окружения для prod API (читаются из `.env` в корне проекта):

```env
PROD_PD_API_URL=https://pd.rut-miit.ru
PROD_PD_API_TOKEN=...          # приоритет: если задан, login не нужен
PROD_PD_EMAIL=...
PROD_PD_PASSWORD=...
```

Опции: `--output`, `--concurrency`, `--api-url`, `--users-json`, `--skip-refresh-users`.

## Только парсинг (без сверки)

Установка:

```bash
pip install -e .
```

Запуск:

```bash
python main.py --output project_teachers.xlsx
```

Опции:

- `--output`, `-o` — путь к выходному файлу (по умолчанию `project_teachers.xlsx`)
- `--concurrency`, `-c` — число параллельных запросов (по умолчанию `8`)

## Источник данных

- Каталог групп: `https://rut-miit.ru/data-service/data/timetable/groups-catalog`
- Расписание группы: `https://rut-miit.ru/data-service/data/timetable/v2/group/{id}`
