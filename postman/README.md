# Postman и OpenAPI

## Вариант 1: импорт схемы с автообновлением

Сервер отдаёт живую OpenAPI 3-схему (drf-spectacular):

| Environment | URL схемы | Swagger UI |
|---|---|---|
| local | `http://localhost:8000/api/schema/` | `http://localhost:8000/api/schema/swagger-ui/` |
| prod | `https://pd.emiit.ru/api/schema/` | `https://pd.emiit.ru/api/schema/swagger-ui/` |

Также: YAML — `http://localhost:8000/api/schema/?format=openapi-yaml`

### Импорт в Postman

1. В Postman: **Import → Link**.
2. Вставьте URL схемы (`…/api/schema/`).
3. Выберите **OpenAPI 3.0 with a Postman Collection** (или аналог).
4. После импорта привяжите коллекцию к definition и включите обновление:
   - **Keep in sync with definition** / **Update collection** из OpenAPI.
5. Подключите environment:
   - [`local.postman_environment.json`](local.postman_environment.json)
   - [`prod.postman_environment.json`](prod.postman_environment.json)

После изменений API на бэкенде обновите definition в Postman (**Update from definition**) — эндпоинты подтянутся из схемы.

> **Важно:** sync из OpenAPI обновляет контракт (пути, методы, тела).
> Скрипты Login → `token_*`, папки «Use token» живут в ручной коллекции
> [`Project_Activity_API.postman_collection.json`](Project_Activity_API.postman_collection.json) — их OpenAPI не заменяет.

### Ручная коллекция с ролями

Для JWT по ролям (`token_admin`, `token_cpds`, `token_institute_validator`) используйте полную коллекцию из этого каталога — она дополняет OpenAPI-импорт.

### Обновить локальный файл схемы (опционально)

```bash
# Windows
venv\Scripts\activate
python manage.py spectacular --file postman/openapi.yml --validate
```

Файл можно импортировать в Postman офлайн (Import → File), если URL недоступен.
