# Tasks

## 1. Domain: классификация и Excel

- [x] 1.1 Создать `showcase/domain/track_composer_comment_excel.py` с константой placeholder’ов и `is_empty_track_composer_comment`; проверить unit-тестами сценарии из спеки (пустая/пробелы/`-`/`нет` → empty; `ML` → filled)
- [x] 1.2 Добавить сборку строки (автор из `author_*`, институт через `get_root_department(author.department).name`, title, comment) и `build_track_composer_comment_xlsx` с листами «Заполненные» / «Пустые»; проверить через openpyxl `load_workbook`, что строки попадают на нужные листы и заголовки колонок совпадают со спекой

## 2. Admin action

- [x] 2.1 В `ProjectApplicationAdmin` добавить action «Выгрузить комментарии составителю трека (Excel)»: валидация непустого queryset и единого `semester_id`, `select_related` для author/department/parent, ответ xlsx или `messages.error` + redirect; проверить через `AdminSite`/`Client` staff-пользователем сценарии успешной выгрузки, пустой выборки и смешанных семестров

## 3. Тесты и graphify

- [x] 3.1 Покрыть корневой институт: child department с parent → в колонке имя parent; author/department отсутствует → пустой институт; `pytest` зелёный
- [x] 3.2 Выполнить `graphify update .` после правок кода и убедиться, что команда завершилась без ошибки
