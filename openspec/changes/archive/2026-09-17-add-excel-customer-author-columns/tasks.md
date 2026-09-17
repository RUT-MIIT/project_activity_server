# Tasks

## 1. Excel builder

- [x] 1.1 Расширить `HEADERS` и `student_dict_to_row` в `teams/domain/institute_students_excel.py`: колонки «Заказчик», «Контакты заказчика», «Автор заявки»; добавить helper ФИО автора из полей dict; проверить unit-логикой / существующим тестом выгрузки
- [x] 1.2 В `InstituteResponsibleService.export_students` обогащать payload только для Excel (company / companyContacts / author ФИО из `project_application`), не меняя `list_students` / `_project_snapshot`; убедиться, что `select_related("project_application")` на memberships уже покрывает поля

## 2. Tests and docs

- [x] 2.1 Обновить `test_export_students_returns_xlsx`: заполнить у заявки company, company_contacts, author_*; проверить заголовки и значения новых колонок; для строки без проекта — пустые ячейки; прогнать тест
- [x] 2.2 Обновить таблицу колонок в `docs/frontend/institute_responsible.md` §9.1 и сверить с фактическими заголовками xlsx
