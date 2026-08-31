# Graph Report - project_activity_server  (2026-08-31)

## Corpus Check
- 345 files · ~159,288 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5159 nodes · 10357 edges · 340 communities (228 shown, 112 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1018 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c933b3a9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MentorTeamViewSet
- make_user
- Department
- Ответственный по институту — API для фронта
- ProjectTrackService
- accounts/views.py
- action
- Any
- import_applications_from_excel.py
- TagRepository
- ApplicationDashboardService
- ApplicationDashboardRepository
- test_mentor_groups_viewset.py
- import_study_groups_from_contingent.py
- ApplicationNotificationService
- test_mentor_team_viewset.py
- prepare_study_groups_xlsx.py
- StudyGroupMemberDTO
- ProjectTrack
- UserManagementService
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- PreRegisteredStudentService
- ApplicationDashboardDomain
- StudyGroup.py
- test_student_showcase_viewset.py
- normalize_cell
- Request
- test_team_lobby_viewset.py
- .list_unregistered
- TestProjectApplicationViewSetIsInternalCustomer
- AvailableActionDTO
- TagCreateDTO
- test_project_track_service.py
- ProjectTrackViewSet
- TestTagViewSetCreate
- TestTagViewSetDelete
- ProjectService
- ProjectApplicationService
- StudentShowcaseDomain
- PreRegisteredStudent
- TeamLobbyService
- .calculate_initial_status
- Tag
- CommentService
- Path
- dto/institute_responsible.py
- ._get_track_with_access
- prod_users_client.py
- .can_update_tag
- TagViewSet
- .resolve_list_semester_id
- DirectionService
- TestDepartmentPlanViewSetList
- test_import_study_groups_from_contingent.py
- TestProjectViewSet
- ValidationResult
- TestProjectApplicationReadDTO
- APIView
- test_institute_access.py
- UserType
- ProjectTrackDomain
- TagUpdateDTO
- test_project_track_viewset.py
- Примеры использования поля is_internal_customer
- TeamLobbyRepository
- TeamLobbyDomain
- .can_change_status
- TestUserManagementDomain
- Settings
- MentorTeamService
- .can_user_access_application
- .get_filtered_queryset
- showcase/urls.py
- ProjectTrackRepository
- PermissionError
- ._authorize_and_load
- TestApplicationDashboardViewSet
- Any
- Tag.py
- Витрина проектов (студент) — API для фронта
- TestLogStatusChange
- API для работы с проектными заявками
- AccountsApiTests
- .can_delete_tag
- build_user_indexes
- TestProjectApplicationListDTO
- Command
- Управление командой
- ApplicationCapabilities
- .validate_update
- TeamLobbyViewSet
- test_institute_responsible_viewset.py
- test_mentor_group_detail_viewset.py
- TestTagViewSet
- extract.py
- User
- InstituteResponsibleService
- teams/admin.py
- TestProjectApplicationViewSetTransferToInstitute
- refresh_prod_users_json
- extract_group_abbrev.py
- ProjectApplication
- API Документация - Проектные заявки
- Command
- Any
- .get_dashboard
- ProjectTrackApplicationItemDTO
- ProjectTrackPermission
- TestProjectApplicationListSemesterFilter
- .validate_create
- _generate_collection.py
- StudyGroup
- TestGetLogs
- test_project_application_new_fields.py
- get_error_message
- test_sync_departments_institutes.py
- institute_access.py
- StudentShowcaseService
- TestMyTeamViewSet
- sync_project_teachers.py
- .get_filtered_queryset
- .should_require_consultation
- Поддержка multipart/form-data
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- TestProjectApplicationViewSetSimple
- Command
- Command
- TestInstituteViewSet
- update_prod.sh
- Command
- ProjectApplicationCreateDTO
- 0014_add_intermediate_approved_statuses.py
- TestDepartmentPlanViewSetMyDepartmentPlan
- StudyGroupService
- Руководство по ручному развертыванию Project Activity Server
- 4. Список проектов
- ProjectApplicationViewSet
- deploy.sh
- action_types.py
- export_client_sources_to_docx.py
- make_source_docx.py
- .auth
- parse_miit_ief_groups.py
- Command
- test_mentor_showcase_viewset.py
- schema.py
- ShowcaseConfig
- format_validation_errors
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- student_user
- test_study_group_viewset.py
- 0011_migrate_team_data.py
- Текущий статус реализации
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- repositories/application_dashboard.py
- test_study_group_domain.py
- other_institute
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- TeamEventLogPagination
- accounts/migrations/0001_initial.py
- 0002_department_user_department.py
- 0003_department_short_name.py
- 0004_alter_user_options.py
- 0005_role_alter_user_role.py
- 0006_user_phone.py
- 0007_registrationrequest.py
- 0008_alter_registrationrequest_department.py
- 0009_registrationrequest_reason.py
- 0010_alter_role_options_role_is_active_and_more.py
- 0012_registrationrequest_role.py
- 0013_department_can_save_project_applications.py
- 0014_semester.py
- 0015_academic_year_settings_semester_fk.py
- 0017_semester_remove_is_active_code_index.py
- 0018_registrationrequest_email_partial_unique.py
- 0019_user_study_group_preregisteredstudent.py
- 0020_user_mentor_fields.py
- ._application_institute_access_q
- QuerySet
- Command
- .get_or_create_placeholder
- ProjectApplicationListSerializer
- RutMiitClient
- Command
- .test_departments_list_allow_any_detail_requires_auth
- .test_registration_request_create_anonymous_allowed
- Command
- dto/mentor_groups.py
- TagService
- ._track_detail_queryset
- teams/models.py
- ApplicationDashboard.py
- 0021_user_placeholder_preregistered_flag.py
- .test_registration_request_reject_forbidden_for_regular_user
- 1. Создание заявки (авторизованные пользователи)
- asgi.py
- wsgi.py
- showcase/migrations/0001_initial.py
- 0002_institute_userrole_alter_projectapplication_options_and_more.py
- 0003_projectapplication_email_and_more.py
- 0004_remove_projectapplication_project_title.py
- 0005_remove_projectapplication_customer_organization.py
- 0006_remove_projectapplication_customer_contacts.py
- 0007_remove_projectapplication_user_role_and_more.py
- 0008_remove_projectapplication_additional_materials_and_more.py
- 0009_remove_projectapplication_description_and_more.py
- 0010_rename_author_surname_projectapplication_author_lastname.py
- 0011_delete_userrole.py
- 0012_projectapplicationstatuslog_action_type_and_more.py
- 0015_alter_projectapplicationcomment_options_and_more.py
- 0016_projectapplication_application_year_and_more.py
- 0017_tag_projectapplication_tags.py
- 0018_institute_department.py
- 0019_projectapplication_main_department.py
- 0020_projectapplication_is_external.py
- 0021_projectapplication_is_internal_customer.py
- 0022_projectapplication_semester.py
- 0023_departmentplan.py
- 0024_add_department_to_tag.py
- 0025_alter_tag_unique_name_department.py
- 0026_alter_tag_departments_m2m.py
- 0027_alter_tag_category_blank.py
- 0028_projectapplication_has_unseen_changes.py
- 0029_projectapplication_img.py
- 0030_projecttrack.py
- 0032_projectapplication_track_fields.py
- 0034_remove_projecttrack_max_teams.py
- 0035_projectapplication_team_member_limits.py
- TestSemesterAssignViewSet
- .test_semester_list_is_active_from_settings
- ._resolve_institute_semester
- .test_user_me_institute_code_from_department_institute
- .test_user_roles_list_requires_auth_and_returns
- TestProjectApplicationNewFieldsCreateUpdate
- status/__init__.py
- 3. To-be: изменения и новые сущности
- teams/migrations/0001_initial.py
- 0002_direction.py
- 0003_studygroup.py
- 0004_studygroup_course_is_end.py
- 0007_studygroup_enrollment_year.py
- 0008_studygroup_profile_form.py
- 0009_studygroup_mentor.py
- 0010_team_semester_models.py
- 0012_remove_legacy_team_fields.py
- 0013_team_lobby_workflow.py
- 0014_lobby_query_indexes.py
- tests/accounts/management/__init__.py
- ProjectTrackAddApplicationItemSerializer
- ProjectApplicationRepository
- Схема БД: студенческий портал
- Справочные эндпоинты
- Парсинг «Проектная деятельность» — РУТ (МИИТ)
- Semester
- StudyGroupSemesterRepository
- ProjectRepository
- 0017_copy_studygroup_mentors_to_semester.py
- ProjectTrackUpdateSerializer
- ._format_external_share_chart
- .recalculate_recommended_teams_count
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- Вариант 1: импорт схемы с автообновлением
- .add_groups
- .get_existing_group_ids
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- 0016_studygroupsemester.py
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- MentorTeamAddMemberSerializer
- InstituteSerializer
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- TeamSemester
- .test_password_change_success
- TeamLobby.py
- .test_password_change_wrong_current_password
- .test_password_reset_sends_email
- .test_registration_request_approve_allowed_for_cpds_user
- .test_registration_request_approve_creates_user_and_sends_email
- .test_registration_request_approve_forbidden_for_regular_user
- .test_registration_request_approve_mail_failure_returns_400_and_no_user_created
- .test_registration_request_list_requires_privileged_user
- .test_registration_request_race_condition_integrity_error
- 0018_studygroupsemester_mentors_m2m.py
- .test_semester_create_allowed_for_admin_and_cpds
- .test_semester_list_requires_auth
- .test_user_me_institute_code_none_if_no_institute
- .get_statistics_overall
- .update
- data/conftest.py
- timetable

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 529 edges
2. `User` - 255 edges
3. `ProjectApplication` - 148 edges
4. `Department` - 142 edges
5. `ProjectApplicationService` - 136 edges
6. `Semester` - 135 edges
7. `StudyGroup` - 121 edges
8. `ProjectApplicationCreateDTO` - 111 edges
9. `PreRegisteredStudent` - 78 edges
10. `Institute` - 76 edges

## Surprising Connections (you probably didn't know these)
- `TestUserManagementDomain` --uses--> `UserManagementDomain`  [INFERRED]
  tests/accounts/domain/test_user_management.py → accounts/domain/user_management.py
- `create_test_applications()` --uses--> `User`  [INFERRED]
  create_test_applications.py → accounts/models.py
- `create_test_user()` --uses--> `User`  [INFERRED]
  create_test_user.py → accounts/models.py
- `ApplicationDashboardDomain` --uses--> `User`  [INFERRED]
  showcase/domain/application_dashboard.py → accounts/models.py
- `ProjectDomain` --uses--> `User`  [INFERRED]
  showcase/domain/project.py → accounts/models.py

## Import Cycles
- None detected.

## Communities (340 total, 112 thin omitted)

### Community 0 - "MentorTeamViewSet"
Cohesion: 0.14
Nodes (17): MentorTeamSetCaptainSerializer, MentorTeamUpdateNameSerializer, MentorTeamViewSet, Request, Response, DELETE /study-groups/{groupId}/teams/{teamSemesterId}/ — удалить команду., PATCH /study-groups/{groupId}/teams/{teamSemesterId}/captain/., Тело PATCH переименования команды. (+9 more)

### Community 1 - "make_user"
Cohesion: 0.03
Nodes (27): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+19 more)

### Community 2 - "Department"
Cohesion: 0.03
Nodes (80): Правила доступа и валидации для управления пользователями., UserManagementDomain, DTO для списка пользователей., extend_schema_view, ViewSet для управления пользователями., API управления пользователями: список, деталь, частичное обновление., PATCH /api/accounts/users/{id}/ — частичное обновление., UserManagementViewSet (+72 more)

### Community 3 - "Ответственный по институту — API для фронта"
Cohesion: 0.08
Nodes (24): 1. Список активных групп института, 2. Сотрудники института, 3. Группы с назначенными наставниками, 4. Назначить наставника группе, 5. Снять наставника с группы, Значения `semester_id`, Общие query-параметры, Ответ `200` (+16 more)

### Community 4 - "ProjectTrackService"
Cohesion: 0.11
Nodes (9): Создаёт DTO из словаря., PATCH /api/showcase/project-tracks/{id}/., ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), _create_track_with_links(), django_db, TestProjectTrackService (+1 more)

### Community 5 - "accounts/views.py"
Cohesion: 0.03
Nodes (80): PreRegisteredStudentViewSet, extend_schema_view, API предрегистрации студентов из контингента., Публичные операции предрегистрации студентов., AcademicYear, Meta, RegistrationRequest, Status (+72 more)

### Community 6 - "action"
Cohesion: 0.10
Nodes (11): action, extend_schema, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, POST /api/semesters/{id}/assign-empty-applications Присваивает переданный…, POST /api/project-applications/{id}/approve/ Одобрение заявки, POST /api/project-applications/{id}/reject/ Отклонение заявки, POST /api/project-applications/{id}/request_changes/ Запрос изменений (отправка… (+3 more)

### Community 7 - "Any"
Cohesion: 0.07
Nodes (19): ProjectTrackAggregatedStatisticsDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackStatisticsDTO, Any, Преобразует DTO в словарь для API., Создаёт DTO из словаря., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API. (+11 more)

### Community 8 - "import_applications_from_excel.py"
Cohesion: 0.09
Nodes (27): ApplicationImportRow, build_import_row(), is_data_row(), iter_application_import_rows(), normalize_cell(), parse_author_name(), parse_customer_type(), parse_institute_codes() (+19 more)

### Community 9 - "TagRepository"
Cohesion: 0.05
Nodes (30): Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., TagRepository, django_db, get_by_id возвращает общий тег., get_by_id для несуществующего тега вызывает ошибку., Тесты для метода update репозитория. (+22 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.06
Nodes (28): ApplicationDashboardService, Оркестрация получения данных дашборда заявок., django_db, Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external., Фильтр по группам статусов., Карточка in_work = total - approved - rejected., Среднее и медиана времени до решения. (+20 more)

### Community 11 - "ApplicationDashboardRepository"
Cohesion: 0.08
Nodes (24): ApplicationDashboardRepository, QuerySet, Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению., Строит карту institute_code -> множество id заявок., ORM-запросы и агрегации для дашборда заявок., Строит карту department_id -> множество id заявок (как в DepartmentPlan). (+16 more)

### Community 12 - "test_mentor_groups_viewset.py"
Cohesion: 0.19
Nodes (11): api_client(), direction(), _enrollment_with_mentors(), APIClient, django_db, fixture, Тесты GET /api/teams/study-groups/my-groups/., semester() (+3 more)

### Community 13 - "import_study_groups_from_contingent.py"
Cohesion: 0.16
Nodes (12): GroupImportRow, Строка отчёта, подготовленная к импорту одной учебной группы., Command, BaseCommand, DataFrame, date, Path, Идемпотентный импорт учебных групп из отчёта контингента 1С (.xls/.xlsx). (+4 more)

### Community 14 - "ApplicationNotificationService"
Cohesion: 0.19
Nodes (8): ApplicationNotificationService, Отправка писем автору при отклонении и отправке на доработку., Email получателя: author_email заявки или email связанного пользователя-автора., Письмо автору: заявка отправлена на доработку., Письмо автору: заявка отклонена., django_db, patch, TestApplicationNotificationService

### Community 15 - "test_mentor_team_viewset.py"
Cohesion: 0.06
Nodes (38): MentorTeamRepository, Удаляет участника любой роли., Меняет статус состава., Удаляет семестровый контекст и постоянную команду при необходимости., Запросы и записи для API команд наставника., Пишет запись в лог команды., True, если пользователь уже в команде в семестре., Пользователь по id или None. (+30 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroupMemberDTO"
Cohesion: 0.22
Nodes (5): Any, Карточка наставника учебной группы., Строка списка группы из контингента., StudyGroupMemberDTO, StudyGroupMentorDTO

### Community 18 - "ProjectTrack"
Cohesion: 0.10
Nodes (12): display, Количество групп в треке., Количество заявок в треке., Общие константы приложения showcase., ProjectTrack, Проектный трек — контейнер для назначения групп и заявок в рамках семестра., Репозиторий для проектных треков., Сериализует список треков с группами и заявками. (+4 more)

### Community 19 - "UserManagementService"
Cohesion: 0.06
Nodes (24): Any, DTO для элемента списка пользователей., UserListDTO, Request, Response, Проверяет query-параметр include_authored_projects., GET /api/accounts/users/ — список пользователей., GET /api/accounts/users/{id}/ — деталь пользователя. (+16 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.08
Nodes (14): ProjectApplicationCreateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы…, Проверяет, что min_team_members не больше max_team_members., Преобразование в DTO - никакой бизнес-логики, Тесты для ProjectApplicationCreateDTO., Создание DTO из словаря через from_dict., Преобразование DTO в словарь через to_dict., Проверяем значения по умолчанию: пустые строки для title, company_contacts,… (+6 more)

### Community 22 - "PreRegisteredStudentService"
Cohesion: 0.10
Nodes (16): action, Request, Response, Отправляет администратору письмо о расхождении данных., Ищет предрегистрацию по студбилету, табельному номеру или СНИЛС., Создаёт пользователя и возвращает JWT по данным предрегистрации., PreRegisteredStudentLookupResult, PreRegisteredStudentService (+8 more)

### Community 23 - "ApplicationDashboardDomain"
Cohesion: 0.10
Nodes (11): ApplicationDashboardDomain, Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп., Парсит query-параметр application_type., Парсит query-параметр days., Возвращает id подразделения и всех его потомков., Проверяет право пользователя на просмотр дашборда., Коды институтов пользователя; None — без ограничения. (+3 more)

### Community 24 - "StudyGroup.py"
Cohesion: 0.10
Nodes (20): Any, DTO для учебных групп., DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, action (+12 more)

### Community 25 - "test_student_showcase_viewset.py"
Cohesion: 0.08
Nodes (19): api_client(), _approved_app(), _create_assembled_team(), direction(), other_group(), django_db, fixture, Тесты API студенческой витрины проектов. (+11 more)

### Community 26 - "normalize_cell"
Cohesion: 0.13
Nodes (16): build_preregistered_student_import_row(), last_names_match(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки. (+8 more)

### Community 27 - "Request"
Cohesion: 0.12
Nodes (17): ApproveJoinRequestSerializer, CreateInvitationSerializer, extend_schema, Request, Response, GET /api/teams/my-team/., GET /api/teams/my-team/event-log/ — пагинированный лог (page_size=50)., DELETE /api/teams/my-team/ — удалить свою команду. (+9 more)

### Community 28 - "test_team_lobby_viewset.py"
Cohesion: 0.11
Nodes (16): api_client(), _approved_app(), _create_captained_team(), direction(), lobby_setup(), django_db, fixture, Тесты API лобби формирования команд. (+8 more)

### Community 30 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "TagCreateDTO"
Cohesion: 0.08
Nodes (19): DTO для создания тега., TagCreateDTO, Тесты для метода create репозитория., Создание общего тега (без departments)., Создание тега с подразделением., Создание тега с несуществующим подразделением вызывает ошибку., Нельзя создать тег с таким же именем и таким же набором подразделений., Можно создать тег с таким же именем, но другим набором подразделений. (+11 more)

### Community 33 - "test_project_track_service.py"
Cohesion: 0.06
Nodes (32): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackCreateDTO, ProjectTrackGroupDetailDTO, ProjectTrackGroupProjectDTO, ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO (+24 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.09
Nodes (30): ProjectTrackAddApplicationsSerializer, ProjectTrackAddGroupsSerializer, ProjectTrackCreateSerializer, ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request (+22 more)

### Community 35 - "TestTagViewSetCreate"
Cohesion: 0.12
Nodes (9): Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем., Нельзя создать общий тег, если имя уже используется (общим или departmental… (+1 more)

### Community 36 - "TestTagViewSetDelete"
Cohesion: 0.08
Nodes (16): django_db, Тесты для обновления тегов через API., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., admin может обновлять любые теги., Тесты для удаления тегов через API., cpds может удалять общие теги., cpds не может удалять теги с подразделением. (+8 more)

### Community 37 - "ProjectService"
Cohesion: 0.21
Nodes (5): ProjectService, Оркестрация Domain + Repository для списка проектов., TestProjectApplicationNewFieldsLists, django_db, TestProjectService

### Community 38 - "ProjectApplicationService"
Cohesion: 0.02
Nodes (82): ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationService, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Сервис - оркестрация всех операций. Координирует Domain, Repository и… (+74 more)

### Community 39 - "StudentShowcaseDomain"
Cohesion: 0.10
Nodes (21): Правила доступа и записи команды на проект витрины., Проверяет роль student и наличие учебной группы; возвращает group_id., Проверяет, что пользователь — капитан команды., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект. (+13 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.11
Nodes (18): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если студент прошёл полную регистрацию (не псевдо-user)., Привязывает предрегистрацию к созданному пользователю., MonkeyPatch, Контингент группы с командой студента в семестре (без N+1)., api_client(), pre_registered_student() (+10 more)

### Community 41 - "TeamLobbyService"
Cohesion: 0.13
Nodes (12): QuerySet, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент принимает приглашение., Оркестрация Domain + Repository для студенческого лобби., Queryset лога «Моей команды» (новые сверху); 404 если нет команды., Резолвит semester_id; по умолчанию actual., Лимиты команды: свой трек → effective по трекам группы → дефолты. (+4 more)

### Community 42 - ".calculate_initial_status"
Cohesion: 0.10
Nodes (14): Определение начального статуса на основе роли пользователя. Чистая функция -…, Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, Бизнес-операция: подача заявки. Новая логика: 1. Валидация через Domain 2.…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds. (+6 more)

### Community 43 - "Tag"
Cohesion: 0.09
Nodes (14): Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, Теги для проектных заявок, Tag, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Создание тега в БД. Args: dto: DTO с данными для создания тега Returns:…, Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, Обновление тега. Обновляет только переданные поля. Args: tag: Тег для…, atomic (+6 more)

### Community 44 - "CommentService"
Cohesion: 0.10
Nodes (17): CommentService, atomic, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db, Пустой текст вызывает ValueError., Тесты для CommentService. (+9 more)

### Community 45 - "Path"
Cohesion: 0.15
Nodes (13): aga_institute(), direction(), Any, django_db, fixture, Path, Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта. (+5 more)

### Community 46 - "dto/institute_responsible.py"
Cohesion: 0.10
Nodes (12): InstituteResponsibleAssignMentorDTO, InstituteResponsibleEmployeeDTO, InstituteResponsibleGroupDTO, InstituteResponsibleGroupWithMentorDTO, InstituteResponsibleMentorDTO, Any, DTO для API ответственного по институтам., Компактное представление учебной группы. (+4 more)

### Community 47 - "._get_track_with_access"
Cohesion: 0.08
Nodes (20): ProjectTrackReadDTO, DTO для чтения проектного трека., atomic, QuerySet, UserType, Возвращает трек с проверкой доступа., Список треков по фильтрам., Возвращает детали трека. (+12 more)

### Community 48 - "prod_users_client.py"
Cohesion: 0.11
Nodes (23): Client, _http_client(), obtain_token(), Клиент prod API для обновления снимка пользователей., Возвращает базовый URL prod API., HTTP-клиент с поддержкой редиректов prod., Получает JWT access token по email и паролю., Возвращает Bearer token из CLI, env или login. (+15 more)

### Community 49 - ".can_update_tag"
Cohesion: 0.12
Nodes (8): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги., Остальные роли не могут обновлять теги.

### Community 50 - "TagViewSet"
Cohesion: 0.11
Nodes (20): Инициализация из модели Tag., TagReadDTO, DepartmentAttachDetachSerializer, action, Request, Response, GET /api/showcase/tags/{id}/ - получение тега с проверкой доступа., POST /api/showcase/tags/ - создание тега. (+12 more)

### Community 51 - ".resolve_list_semester_id"
Cohesion: 0.11
Nodes (14): Разбор query-параметра semester_id для GET-списков: id, next, actual., Any, Список треков с проектами для группы наставника в семестре., action, Request, Response, POST /api/teams/team-semesters/{id}/members/ — добавить участника., DELETE /api/teams/team-semesters/{id}/members/{member_id}/. (+6 more)

### Community 52 - "DirectionService"
Cohesion: 0.05
Nodes (30): DirectionDomain, QuerySet, Фильтрация направлений по роли пользователя., Фильтрует направления: institute_validator — только из групп своего института., DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений. (+22 more)

### Community 53 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 54 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.10
Nodes (22): build_group_import_row(), build_group_name(), calculate_course_number(), group_ended_by_planned_dates(), parse_direction_level(), parse_permanent_group_code(), parse_planned_end_date(), ParsedPermanentGroup (+14 more)

### Community 55 - "TestProjectViewSet"
Cohesion: 0.18
Nodes (4): _create_approved_app(), django_db, ЦПДС в причастных не должно подменять основное подразделение проекта., TestProjectViewSet

### Community 56 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 57 - "TestProjectApplicationReadDTO"
Cohesion: 0.09
Nodes (13): Exception, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None., target_institutes сериализуется как список словарей с code и name., tags сериализуется как список словарей с id, name и category., involved_users сериализуется с данными пользователя, added_at и added_by. (+5 more)

### Community 58 - "APIView"
Cohesion: 0.15
Nodes (10): APIView, Request, Проверяет наличие прав у пользователя., Проверяет наличие прав у пользователя., Проверяет наличие прав у пользователя., Проверяет права на чтение или запись пользователей., Проверяет наличие прав у пользователя. Args: request: текущий запрос view:…, Проверяет, что у текущего пользователя установлена роль с кодом `cpds`. Args:… (+2 more)

### Community 59 - "test_institute_access.py"
Cohesion: 0.18
Nodes (11): Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., application_available_for_institute(), application_belongs_to_institutes(), Проверяет доступность заявки институту для проектных треков. Заявка доступна,…, Проверяет принадлежность заявки к институтам по причастным подразделениям.…, _create_approved_app(), django_db (+3 more)

### Community 60 - "UserType"
Cohesion: 0.20
Nodes (10): atomic, UserType, Студент отклоняет приглашение., Возвращает команду капитана или бросает ошибку., Капитан одобряет заявку и назначает роль., Капитан отклоняет заявку., Капитан приглашает одногруппника., Капитан удаляет участника. (+2 more)

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.08
Nodes (16): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя., Проверяет, может ли пользователь управлять проектными треками., Коды институтов пользователя; None — без ограничения (admin/cpds). (+8 more)

### Community 62 - "TagUpdateDTO"
Cohesion: 0.14
Nodes (11): DTO для обновления тега., TagUpdateDTO, Тесты для метода update_tag сервиса., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+3 more)

### Community 63 - "test_project_track_viewset.py"
Cohesion: 0.09
Nodes (29): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+21 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "TeamLobbyRepository"
Cohesion: 0.03
Nodes (39): Заявка должна быть в статусе pending., Приглашение должно быть в статусе pending., Заявка студента на вступление в команду в семестре., Приглашение капитана студенту вступить в команду., Лог действий по команде., Status, TeamEventLog, TeamInvitation (+31 more)

### Community 66 - "TeamLobbyDomain"
Cohesion: 0.05
Nodes (31): Удаление: капитан, forming, в составе только он., Подтверждение состава: капитан, forming, размер в лимитах трека., Проверяет, что пользователь из нужной учебной группы., Чистая бизнес-логика лобби и «Моей команды»., True, если студент без команды и есть свободный слот., Запрещает изменения состава при подтверждённом составе., Приглашение не может назначать роль leader., При одобрении заявки нельзя назначить второго leader. (+23 more)

### Community 67 - ".can_change_status"
Cohesion: 0.08
Nodes (23): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, atomic, Бизнес-операция: отправка заявки на доработку., Бизнес-операция: отзыв заявки автором., Бизнес-операция: одобрение заявки., Бизнес-операция: отклонение заявки., Бизнес-операция: передача заявки в институт. Доступно только для роли cpds для…, Бизнес-операция: получение доступных действий для заявки. Args: application_id:… (+15 more)

### Community 68 - "TestUserManagementDomain"
Cohesion: 0.14
Nodes (7): Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., Role, django_db, TestUserManagementDomain

### Community 69 - "Settings"
Cohesion: 0.11
Nodes (22): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+14 more)

### Community 70 - "MentorTeamService"
Cohesion: 0.05
Nodes (31): PreRegisteredStudentRepository, Репозиторий предрегистрации студентов., Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по табельному номеру., Возвращает предрегистрацию по нормализованному СНИЛС., Возвращает предрегистрацию по первичному ключу., Удаляет предрегистрации без привязанного пользователя. (+23 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.14
Nodes (11): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Тесты для проверки доступа пользователя к заявке., Автор всегда имеет доступ к своей заявке., Админ имеет доступ ко всем заявкам., Модератор имеет доступ ко всем заявкам., CPDS имеет доступ ко всем заявкам., Валидатор подразделения имеет доступ ко всем заявкам., Валидатор института имеет доступ ко всем заявкам. (+3 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.12
Nodes (9): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения., institute_validator без подразделения видит только общие теги., admin видит все теги. (+1 more)

### Community 73 - "showcase/urls.py"
Cohesion: 0.05
Nodes (39): ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…, DepartmentPlanSerializer (+31 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.08
Nodes (12): ProjectTrackRepository, Создаёт проектный трек., Удаляет группу из трека; True если связь была., Возвращает id заявок, уже привязанных к треку., Добавляет заявки в трек; возвращает число созданных связей., Удаляет заявку из трека; True если связь была., Количество групп в треке., Доступ к данным проектных треков. (+4 more)

### Community 75 - "PermissionError"
Cohesion: 0.08
Nodes (16): PermissionError, Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации. (+8 more)

### Community 76 - "._authorize_and_load"
Cohesion: 0.14
Nodes (14): Any, atomic, Обновляет название команды., Назначает нового капитана из состава команды., Подтверждает состав команды (forming → assembled)., Возвращает состав на редактирование (assembled → forming)., Добавляет зарегистрированного или незарегистрированного студента., Возвращает пользователя для добавления в команду. (+6 more)

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - "Any"
Cohesion: 0.12
Nodes (10): Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Преобразование в словарь., Сериализатор для создания тега., Преобразование в DTO., Сериализатор для обновления тега., Преобразование в DTO. (+2 more)

### Community 79 - "Tag.py"
Cohesion: 0.16
Nodes (10): DTO для работы с тегами., DepartmentNestedSerializer, Meta, Вложенный сериализатор для подразделения., Сериализатор для тегов., TagSerializer, Репозиторий для работы с тегами в БД. Изолирует всю работу с базой данных от…, Сервис для оркестрации операций с тегами. Координирует Domain, Repository и DTO. (+2 more)

### Community 80 - "Витрина проектов (студент) — API для фронта"
Cohesion: 0.14
Nodes (13): 1. Список треков с проектами, 2. Детали проекта, 3. Записать команду на проект, Витрина проектов (студент) — API для фронта, Ответ `200`, Ответ `200`, Ответ `200`, Ошибки (+5 more)

### Community 81 - "TestLogStatusChange"
Cohesion: 0.12
Nodes (9): Первый переход (from_status=None) помечает заявку, если актор не автор., Логирование с указанием предыдущего лога для создания цепочки., Тесты для log_status_change., Если application равен None, выбрасывается ValueError., Успешное логирование изменения статуса (не автор — флаг выставляется)., Если to_status равен None, выбрасывается ValueError., Смена статуса автором не помечает заявку для самого автора., Одинаковый from/to статус не помечает заявку как изменённую. (+1 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.11
Nodes (10): AccountsApiTests, override_settings, Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Создание заявки без подразделения возвращает ошибку валидации., Создание заявки с несуществующим подразделением возвращает ошибку валидации., После отклонения заявки можно подать новую с тем же email., Повторная подача при активной заявке возвращает ошибку валидации., Нельзя подать заявку, если пользователь с таким email уже зарегистрирован. (+2 more)

### Community 84 - ".can_delete_tag"
Cohesion: 0.12
Nodes (8): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения., admin может удалять любые теги., Остальные роли не могут удалять теги.

### Community 85 - "build_user_indexes"
Cohesion: 0.10
Nodes (29): main(), Сверка преподавателей из Excel со списком пользователей prod API. ..…, Отмечает преподавателей из Excel, которые есть в prod., build_user_indexes(), find_user(), normalize_name(), Сопоставление ФИО преподавателей с пользователями PD., Нормализует ФИО для сравнения. (+21 more)

### Community 86 - "TestProjectApplicationListDTO"
Cohesion: 0.13
Nodes (9): django_db, Тесты для ProjectApplicationListDTO., Базовые поля DTO для списка заполняются из модели., Если статус None, DTO.status тоже None., to_dict преобразует DTO в словарь с ISO форматированием даты., is_internal_customer включается в ProjectApplicationListDTO., Новые поля трека включаются в ProjectApplicationListDTO., is_internal_customer включается в ProjectApplicationReadDTO. (+1 more)

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "Управление командой"
Cohesion: 0.08
Nodes (24): Query-параметры, Query-параметры, Query-параметры, Вернуть состав на редактирование, Витрина проектов, Детали группы наставника, Добавить участника, Карточка команды (+16 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.04
Nodes (37): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы. (+29 more)

### Community 90 - ".validate_update"
Cohesion: 0.19
Nodes (8): Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Тесты для валидации при обновлении заявки., Валидные поля при обновлении проходят проверку., Название короче 5 символов вызывает ошибку., Email без символа @ вызывает ошибку., Валидация проверяет только переданные поля (None игнорируются)., Пустые строки вызывают ошибки валидации., TestValidateUpdate

### Community 91 - "TeamLobbyViewSet"
Cohesion: 0.18
Nodes (10): CreateTeamSerializer, action, extend_schema_view, POST /api/teams/lobby/teams/{id}/join-requests/., POST /api/teams/lobby/invitations/{id}/accept/., POST /api/teams/lobby/invitations/{id}/reject/., Создание команды в лобби., Студенческое лобби: треки, команды, заявки, приглашения. (+2 more)

### Community 92 - "test_institute_responsible_viewset.py"
Cohesion: 0.16
Nodes (12): InstituteResponsibleGroupMentorsDTO, Ответ: группы с назначениями наставников., api_client(), direction(), APIClient, django_db, fixture, Тесты API ответственного по институтам. (+4 more)

### Community 93 - "test_mentor_group_detail_viewset.py"
Cohesion: 0.23
Nodes (12): api_client(), _detail_url(), direction(), _enrollment_with_mentors(), APIClient, django_db, fixture, Тесты GET /api/teams/study-groups/{id}/mentor-detail/. (+4 more)

### Community 94 - "TestTagViewSet"
Cohesion: 0.14
Nodes (8): Тесты для TagViewSet., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level)., Список тегов возвращается без пагинации (все теги сразу)., Эндпоинт доступен без авторизации (AllowAny)., TestTagViewSet

### Community 95 - "extract.py"
Cohesion: 0.22
Nodes (16): main(), run(), export_marked_xlsx(), export_to_xlsx(), _group_columns(), Any, Экспортирует результаты парсинга с колонками сверки с PD., _collect_events() (+8 more)

### Community 96 - "User"
Cohesion: 0.04
Nodes (31): AbstractBaseUser, QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., User, Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает номер студенческого билета для роли student. (+23 more)

### Community 97 - "InstituteResponsibleService"
Cohesion: 0.11
Nodes (24): delete, InstituteResponsibleViewSet, action, extend_schema, Request, Response, GET /api/teams/institute-responsible/employees/., GET /api/teams/institute-responsible/group-mentors/. (+16 more)

### Community 98 - "teams/admin.py"
Cohesion: 0.27
Nodes (11): DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin, TeamSemesterAdmin (+3 more)

### Community 99 - "TestProjectApplicationViewSetTransferToInstitute"
Cohesion: 0.17
Nodes (8): Тесты для действия передачи заявки в институт по коду института., POST /api/showcase/project-applications/{id}/transfer_to_institute/ с…, Отсутствующий параметр code возвращает 400., Несуществующий код института возвращает 400 от сервиса., Институт без связанного подразделения возвращает 400., GET /api/showcase/project-applications/external/?status=... фильтрует внешние…, GET /api/showcase/project-applications/external/?status=... с несуществующим…, TestProjectApplicationViewSetTransferToInstitute

### Community 100 - "refresh_prod_users_json"
Cohesion: 0.20
Nodes (11): fetch_users(), Any, Path, Загружает список пользователей с prod API., Обновляет JSON-снимок пользователей prod., refresh_prod_users_json(), Path, Загружает список пользователей с API. (+3 more)

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - "ProjectApplication"
Cohesion: 0.04
Nodes (55): Репозиторий для управления пользователями., Доменная логика студенческой витрины проектов., ViewSet для работы с планами подразделений по проектным заявкам., Генерация тестовых одобренных проектов и учебных групп для института IEF., ApplicationInvolvedDepartment, ApplicationStatus, DepartmentPlan, Institute (+47 more)

### Community 103 - "API Документация - Проектные заявки"
Cohesion: 0.18
Nodes (9): API Документация - Проектные заявки, Аутентификация, Базовый URL, Валидационные правила, Общая информация, Обязательные поля, Обязательные поля:, Типы данных (+1 more)

### Community 104 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

### Community 105 - "Any"
Cohesion: 0.08
Nodes (14): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationUpdateSerializer, Сериализатор только для валидации HTTP данных при обновлении., Проверяет согласованность min/max, если оба переданы. (+6 more)

### Community 106 - ".get_dashboard"
Cohesion: 0.17
Nodes (9): ApplicationDashboardDTO, Any, DTO для дашборда проектных заявок., Преобразует DTO в словарь для API., DTO блока KPI-карточек., DTO полного ответа дашборда., Преобразует DTO в словарь для API., SummaryCardsDTO (+1 more)

### Community 107 - "ProjectTrackApplicationItemDTO"
Cohesion: 0.18
Nodes (6): ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO, Преобразует DTO в словарь для API., DTO заявки в проектном треке., Преобразует DTO в словарь для API., DTO группы в проектном треке.

### Community 108 - "ProjectTrackPermission"
Cohesion: 0.33
Nodes (5): DenyStudentPermission, ProjectTrackPermission, Разрешает доступ к проектным трекам для admin, cpds и institute_validator., Запрещает доступ пользователям с ролью student., Список/создание — staff; свой план подразделения — не student.

### Community 109 - "TestProjectApplicationListSemesterFilter"
Cohesion: 0.09
Nodes (14): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Фильтр ?semester_id= в GET-списке заявок., Автоподстановка семестра при создании заявки., Тесты для проверки наличия поля is_external в ответах API., POST /api/showcase/project-applications/ возвращает is_external в ответе. (+6 more)

### Community 110 - ".validate_create"
Cohesion: 0.12
Nodes (13): Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Носитель проблемы короче 5 символов вызывает ошибку., Барьер короче 10 символов вызывает ошибку., Имя и фамилия автора короче 2 символов вызывают ошибки., Тесты для валидации при создании заявки., Телефон короче 10 символов вызывает ошибку., Валидный DTO проходит проверку без ошибок., Все ошибки валидации собираются в одном результате. (+5 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - "StudyGroup"
Cohesion: 0.08
Nodes (22): MyStudyGroupDTO, Возвращает наставников: из семестра или fallback на StudyGroup.mentor., Полные данные учебной группы для текущего студента., StudyGroup, QuerySet, Группа с наставником и контингентом без N+1., Any, Возвращает данные учебной группы текущего студента. (+14 more)

### Community 113 - "TestGetLogs"
Cohesion: 0.05
Nodes (25): django_db, Тесты для логирования причастных пользователей., Логирование добавления причастного пользователя., Проверка валидации при добавлении причастного пользователя., Логирование удаления причастного пользователя., Тесты для логирования причастных подразделений., Логирование добавления причастного подразделения., Проверка валидации при добавлении подразделения. (+17 more)

### Community 114 - "test_project_application_new_fields.py"
Cohesion: 0.06
Nodes (26): ProjectManagementPermission, Разрешает просмотр проектов для admin, cpds и institute_validator., get_root_department(), is_cpds_department(), Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, ProjectListDTO, Any (+18 more)

### Community 115 - "get_error_message"
Cohesion: 0.24
Nodes (6): get_error_message(), GET /api/project-applications/external/ Получение списка всех внешних заявок…, Возвращает сообщение об ошибке в зависимости от режима DEBUG. Args: exception:…, GET /api/project-applications/by_status/?status=created Получение заявок по…, GET /api/project-applications/recent/ Получение последних заявок (только для…, GET /api/project-applications/coordination/ Заявки для координации: где…

### Community 116 - "test_sync_departments_institutes.py"
Cohesion: 0.29
Nodes (10): Any, django_db, Экспорт и последующий импорт институтов восстанавливают данные., Экспорт и последующий импорт подразделений восстанавливают данные., Импорт институтов удаляет те, которых нет в файле., Импорт подразделений удаляет те, которых нет в файле., test_export_import_departments_roundtrip(), test_export_import_institutes_roundtrip() (+2 more)

### Community 117 - "institute_access.py"
Cohesion: 0.07
Nodes (32): Доменная логика управления пользователями., ID подразделений для фильтрации; None — без ограничения., ProjectDomain, Доменная логика для списка проектов., Проверяет, может ли пользователь получать список проектов., Коды институтов для фильтрации; None — без ограничения., Правила доступа и фильтрации для списка проектов., Доменная логика для проектных треков. (+24 more)

### Community 118 - "StudentShowcaseService"
Cohesion: 0.04
Nodes (44): Any, DTO студенческой витрины проектов., Результат записи команды на проект., Преобразует DTO в словарь для API., Карточка проекта в списке трека витрины., Преобразует DTO в словарь для API., Трек с вложенными проектами для витрины., Преобразует DTO в словарь для API. (+36 more)

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → effective max(min)/min(max)., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "sync_project_teachers.py"
Cohesion: 0.15
Nodes (14): load_project_env(), Загружает переменные из .env в корне проекта., main(), parse_all_groups(), _print_parse_summary(), Path, Парсинг расписания РУТ и сверка преподавателей с пользователями prod PD., Парсит преподавателей «Проектная деятельность» по всем группам. (+6 more)

### Community 121 - ".get_filtered_queryset"
Cohesion: 0.25
Nodes (5): Q, Базовый queryset заявок с учётом всех фильтров., Доли заявок по группам статусов (согласовано / в работе / отклонено)., Доли внутренних/внешних заявок по полю is_internal_customer., Q-фильтр: заявка доступна институту.

### Community 122 - ".should_require_consultation"
Cohesion: 0.17
Nodes (9): Определение необходимости консультации на основе данных заявки. Чистая функция…, Тесты для определения необходимости консультации., Если уровень проекта не указан, нужна консультация., Если целевые институты не указаны, нужна консультация., Если цель проекта короче 50 символов, нужна консультация., Если все условия выполнены, консультация не требуется., Если project_level равен None, нужна консультация., Если target_institutes равен None, нужна консультация. (+1 more)

### Community 123 - "Поддержка multipart/form-data"
Cohesion: 0.33
Nodes (6): Допустимые форматы файлов, Заголовки, Загрузка файлов, Максимальный размер файла, Поддержка multipart/form-data, Тело запроса

### Community 124 - "test_import_institutes.py"
Cohesion: 0.54
Nodes (7): django_db, Path, Тесты команды import_institutes., test_import_institutes_clear_removes_missing(), test_import_institutes_is_idempotent(), test_import_institutes_updates_existing(), _write_institutes_csv()

### Community 125 - "build_fgos_napravleniya_csv.py"
Cohesion: 0.43
Nodes (6): collect_codes(), fetch(), main(), parse_table_rows(), Собрать fgos_specialitet_napravleniya.csv: level, code, name (без групп…, middle: '03' — бакалавриат, '05' — специалитет.

### Community 126 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

### Community 127 - "Command"
Cohesion: 0.33
Nodes (5): Command, BaseCommand, Экспорт возможных статусов заявок в Excel., Считывает статусы из базы и сохраняет в Excel., Возвращает статусы, отсортированные по позиции и коду.

### Community 128 - "Command"
Cohesion: 0.38
Nodes (3): Command, BaseCommand, Path

### Community 129 - "TestInstituteViewSet"
Cohesion: 0.29
Nodes (5): django_db, Проверяем выдачу списка институтов с полем department_id., Эндпоинт возвращает department_id, если институт связан с подразделением., Если подразделение не задано, department_id равно None., TestInstituteViewSet

### Community 130 - "update_prod.sh"
Cohesion: 0.52
Nodes (6): log_error(), log_info(), log_warn(), read_env_value(), update_prod.sh script, usage()

### Community 131 - "Command"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Возвращает абсолютный путь к CSV (относительный — от папки commands).

### Community 132 - "ProjectApplicationCreateDTO"
Cohesion: 0.05
Nodes (43): create_test_applications(), Создаем тестовые заявки, ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Явное выражение бизнес-намерений (не технических операций). Этот модуль…, Domain слой - чистая бизнес-логика без побочных эффектов. Этот слой содержит…, build_author_short_name() (+35 more)

### Community 133 - "0014_add_intermediate_approved_statuses.py"
Cohesion: 0.33
Nodes (5): add_intermediate_approved_statuses(), Migration, Удаляет промежуточные статусы одобрения из БД., Добавляет промежуточные статусы одобрения в БД., remove_intermediate_approved_statuses()

### Community 134 - "TestDepartmentPlanViewSetMyDepartmentPlan"
Cohesion: 0.13
Nodes (9): django_db, Тесты для GET /api/showcase/department-plans/my-department-plan/ - план…, Успешное получение плана и статистики для подразделения пользователя., Если план отсутствует, возвращается 0, но статистика заявок учитывается., Ошибка: отсутствует semester_id., Ошибка: семестр не найден., Ошибка: у пользователя не указано подразделение., Ошибка: неавторизованный пользователь. (+1 more)

### Community 135 - "StudyGroupService"
Cohesion: 0.22
Nodes (6): Оркестрация Domain + Repository для StudyGroup., StudyGroupService, django_db, TestMyStudyGroupService, django_db, TestStudyGroupService

### Community 136 - "Руководство по ручному развертыванию Project Activity Server"
Cohesion: 0.15
Nodes (12): 10. Проверка и сопровождение, 11. Настройка nginx (backend + SPA), 1. Подготовка окружения, 2. Получение исходного кода, 3. Создание и активация виртуального окружения, 4. Настройка переменных окружения (.env), 5. Настройка PostgreSQL, 6. Миграции и статические файлы (+4 more)

### Community 137 - "4. Список проектов"
Cohesion: 0.29
Nodes (7): 4. Список проектов, Query-параметры, Заголовки, Ошибки, Поведение по ролям, Примеры запросов, Успешный ответ (200)

### Community 138 - "ProjectApplicationViewSet"
Cohesion: 0.11
Nodes (12): ProjectApplicationViewSet, Упрощенный ViewSet - только обработка HTTP запросов. Вся бизнес-логика вынесена…, Переопределяем права доступа в зависимости от действия. `simple` — публичное…, DELETE отключён: заявки не удаляются через API., Выбор сериализатора в зависимости от действия, Возвращает QuerySet для списка заявок. DRF автоматически применит пагинацию., PK семестра из ?semester_id= (id | next | actual) или None, если параметра нет., GET /api/project-applications/ Получение списка заявок с пагинацией. Query:… (+4 more)

### Community 139 - "deploy.sh"
Cohesion: 0.70
Nodes (4): log_error(), log_info(), log_warn(), deploy.sh script

### Community 140 - "action_types.py"
Cohesion: 0.50
Nodes (4): Enum, Типы действий с заявками., Типы действий с заявками по ролям., RoleActionType

### Community 141 - "export_client_sources_to_docx.py"
Cohesion: 0.70
Nodes (4): add_code_paragraph(), is_source_file(), main(), walk_client_files()

### Community 142 - "make_source_docx.py"
Cohesion: 0.70
Nodes (4): add_code_paragraph(), is_source_file(), main(), walk_py_files()

### Community 143 - ".auth"
Cohesion: 0.17
Nodes (6): Без токена возвращается 401, с токеном — профиль текущего пользователя., Админ отклоняет заявку: статус становится REJECTED и уходит письмо., Пользователь ЦПДС может отклонять заявки (IsCpdsUser)., Если отправка письма при reject падает, возвращаем 200 и оставляем статус…, Детальный просмотр роли по коду (lookup_field=code) требует авторизации., Логинится и проставляет Bearer-токен в заголовках клиента.

### Community 144 - "parse_miit_ief_groups.py"
Cohesion: 0.60
Nodes (4): extract_block(), main(), parse_groups(), Парсинг групп ИЭФ со страницы miit.ru/timetable.

### Community 146 - "test_mentor_showcase_viewset.py"
Cohesion: 0.15
Nodes (18): Наставники учебной группы в конкретном семестре., StudyGroupSemester, api_client(), _approved_app(), _create_assembled_team(), direction(), _enrollment_with_mentors(), mentor_showcase_setup() (+10 more)

### Community 147 - "schema.py"
Cohesion: 0.50
Nodes (3): exclude_auth_api_duplicate(), Хуки и расширения для drf-spectacular., Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*). В…

### Community 149 - "format_validation_errors"
Cohesion: 0.33
Nodes (4): format_validation_errors(), POST /api/project-applications/ Создание заявки - только обработка HTTP, Форматирует ошибки валидации используя стандартные DRF механизмы. Args: errors:…, POST /api/project-applications/simple/ Создание заявки без авторизации

### Community 151 - "0013_refactor_comments.py"
Cohesion: 0.50
Nodes (3): delete_all_comments(), Migration, Удаляем все существующие комментарии

### Community 152 - "0031_refactor_projecttrack.py"
Cohesion: 0.50
Nodes (3): clear_project_tracks(), Migration, Удаляет все записи старой модели ProjectTrack перед рефакторингом.

### Community 153 - "0033_alter_recommended_teams_count_default.py"
Cohesion: 0.50
Nodes (3): Migration, Проставляет 3 для всех существующих проектных заявок., set_recommended_teams_count_to_three()

### Community 154 - "0036_projecttrack_team_member_limits.py"
Cohesion: 0.50
Nodes (3): backfill_track_limits_from_applications(), Migration, Проставляет лимиты трека из первой связанной заявки.

### Community 155 - "0037_projecttrack_recommended_teams_count.py"
Cohesion: 0.50
Nodes (3): backfill_track_recommended_teams_count(), Migration, Проставляет сумму recommended_teams_count из связанных заявок.

### Community 156 - "student_user"
Cohesion: 0.27
Nodes (8): api_client(), Any, APIClient, django_db, fixture, student_user(), study_group(), TestUserMeStudent

### Community 157 - "test_study_group_viewset.py"
Cohesion: 0.47
Nodes (5): direction(), other_institute(), fixture, Тесты StudyGroupViewSet., study_groups()

### Community 159 - "Текущий статус реализации"
Cohesion: 0.40
Nodes (5): ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации, 🔧 Требует доработки

### Community 164 - "repositories/application_dashboard.py"
Cohesion: 0.21
Nodes (9): get_department_subtree_ids(), Утилиты для работы с подразделениями., Возвращает id корневого подразделения и всех его потомков., DashboardFilters, Доменная логика дашборда проектных заявок., Параметры фильтрации дашборда., Репозиторий агрегаций для дашборда проектных заявок., Листовые подразделения в поддереве, если прямых дочерних нет. (+1 more)

### Community 165 - "test_study_group_domain.py"
Cohesion: 0.12
Nodes (15): QuerySet, Фильтрация учебных групп по роли пользователя., institute_validator — только группы своих институтов., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., StudyGroupDomain, direction(), other_institute() (+7 more)

### Community 166 - "other_institute"
Cohesion: 0.40
Nodes (5): directions(), other_institute(), fixture, Три направления для сценариев фильтрации., Второй институт на другом подразделении.

### Community 170 - "TeamEventLogPagination"
Cohesion: 0.67
Nodes (3): PageNumberPagination, Пагинация ленты событий команды (фиксированный page_size=50)., TeamEventLogPagination

### Community 189 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 190 - "QuerySet"
Cohesion: 0.18
Nodes (6): QuerySet, Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки.

### Community 191 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 192 - ".get_or_create_placeholder"
Cohesion: 0.40
Nodes (3): atomic, Возвращает существующего или создаёт псевдо-user для предрегистрации. Raises:…, Уникальный внутренний email для псевдо-аккаунта.

### Community 193 - "ProjectApplicationListSerializer"
Cohesion: 0.67
Nodes (3): Meta, ProjectApplicationListSerializer, Простой сериализатор для списка заявок

### Community 198 - "Command"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Сбрасывает счетчик ID для таблицы тегов.

### Community 199 - "dto/mentor_groups.py"
Cohesion: 0.09
Nodes (15): MentorGroupDetailDTO, MentorGroupListDTO, MentorGroupListItemDTO, MentorGroupStudentDTO, MentorGroupTeamDTO, Any, DTO для эндпоинта «Мои группы» наставника., Строка списка групп наставника. (+7 more)

### Community 200 - "TagService"
Cohesion: 0.09
Nodes (21): Бизнес-операция: получение списка тегов с фильтрацией по ролям. Для…, Сервис - оркестрация всех операций с тегами. Координирует Domain, Repository и…, TagService, django_db, Тесты для метода delete_tag сервиса., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять теги своего подразделения. (+13 more)

### Community 201 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 202 - "teams/models.py"
Cohesion: 0.05
Nodes (45): Доменная логика для учебных групп., DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DTO для эндпоинта «Моя группа»., DirectionSerializer, Meta (+37 more)

### Community 203 - "ApplicationDashboard.py"
Cohesion: 0.20
Nodes (7): ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 206 - "1. Создание заявки (авторизованные пользователи)"
Cohesion: 0.33
Nodes (6): 1. Создание заявки (авторизованные пользователи), Заголовки, Пример запроса, Тело запроса, Успешный ответ (201), Эндпоинты создания заявок

### Community 240 - "TestSemesterAssignViewSet"
Cohesion: 0.29
Nodes (3): Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, TestSemesterAssignViewSet

### Community 242 - "._resolve_institute_semester"
Cohesion: 0.11
Nodes (10): ProjectTrackGroupListDTO, ProjectTrackProjectListDTO, DTO группы со счётчиком назначенных проектов., Преобразует DTO в словарь для API., DTO проекта со счётчиком назначенных групп., Преобразует DTO в словарь для API., Список групп института со счётчиком назначенных проектов., Список проектов семестра со счётчиком назначенных групп. (+2 more)

### Community 245 - "TestProjectApplicationNewFieldsCreateUpdate"
Cohesion: 0.27
Nodes (4): _base_create_payload(), django_db, TestMyApplicationsNewFields, TestProjectApplicationNewFieldsCreateUpdate

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 279 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 280 - "ProjectApplicationRepository"
Cohesion: 0.02
Nodes (59): ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты…, Получение заявки по ID без дополнительных связанных объектов. Для простых…, Репозиторий - вся работа с БД здесь, Получение заявок для координации по причастному подразделению. Заявки, где…, Получение заявок по статусу. Для административных операций., Получение QuerySet заявок по статусу для пагинации., Получение всех заявок, кроме указанных по статусу. Используется, например, для… (+51 more)

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 289 - "Парсинг «Проектная деятельность» — РУТ (МИИТ)"
Cohesion: 0.40
Nodes (4): Источник данных, Парсинг «Проектная деятельность» — РУТ (МИИТ), Полный пайплайн (парсинг + сверка с PD), Только парсинг (без сверки)

### Community 292 - "Semester"
Cohesion: 0.07
Nodes (20): Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Следующий семестр для новых заявок (Settings.next_semester_code)., Semester, Один запрос к Settings на ответ — код активного семестра для is_active., Command, BaseCommand, Добавляет причастные подразделения института к заявке. (+12 more)

### Community 294 - "StudyGroupSemesterRepository"
Cohesion: 0.11
Nodes (13): QuerySet, Репозиторий для StudyGroupSemester и связанных выборок., Снимает наставника с группы в семестре; возвращает актуальные mentorIds., Возвращает отсортированные ID наставников группы в семестре., Доступ к данным групп в семестре и сотрудников института., Активные группы института., Активные группы с prefetch наставников в семестре., Возвращает группу по ID или None. (+5 more)

### Community 297 - "ProjectRepository"
Cohesion: 0.29
Nodes (5): ProjectRepository, QuerySet, Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

### Community 300 - "ProjectTrackUpdateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackUpdateSerializer, Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

### Community 303 - "Endpoints"
Cohesion: 0.33
Nodes (6): 1. Проектные заявки (ProjectApplicationViewSet), 2. Справочники, 3. Управление пользователями (admin / cpds / institute_validator), 4. Список проектов (admin / cpds / institute_validator), Endpoints, Система статусов и логов:

### Community 304 - "6. Маппинг разделов UI → сущности БД"
Cohesion: 0.33
Nodes (6): 6.1. Раздел 1 — детализация данных, 6.2. Раздел 2 — строка таблицы группы, 6.3. Раздел 3 — карточка команды в списке, 6.4. Раздел 4 — роли, 6.5. Раздел 5 — витрина, 6. Маппинг разделов UI → сущности БД

### Community 305 - "1. Список пользователей"
Cohesion: 0.33
Nodes (6): 1. Список пользователей, Query-параметры, Заголовки, Примеры запросов, Примечания, Успешный ответ (200)

### Community 306 - "3. Изменение пользователя"
Cohesion: 0.17
Nodes (12): 2. Получение пользователя, 3. Изменение пользователя, Заголовки, Ошибки, Ошибки, Права доступа, Примеры запросов, Примеры запросов (+4 more)

### Community 308 - "Вариант 1: импорт схемы с автообновлением"
Cohesion: 0.33
Nodes (5): Postman и OpenAPI, Вариант 1: импорт схемы с автообновлением, Импорт в Postman, Обновить локальный файл схемы (опционально), Ручная коллекция с ролями

### Community 311 - "4. State machine статусов команды и блокировки"
Cohesion: 0.40
Nodes (5): 4.1. Диаграмма переходов, 4.2. Кто что может, 4.3. Условия переходов, 4.4. Регистрация на проект, 4. State machine статусов команды и блокировки

### Community 312 - "5. Вычисляемые лимиты размера команды (effective_min / effective_max)"
Cohesion: 0.40
Nodes (5): 5.1. Формулы, 5.2. Краевые случаи, 5.3. Где считаются, 5.4. Связь с существующими полями, 5. Вычисляемые лимиты размера команды (effective_min / effective_max)

### Community 313 - "Обработка ошибок"
Cohesion: 0.40
Nodes (5): 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error, Обработка ошибок

### Community 315 - "1. Введение и scope"
Cohesion: 0.50
Nodes (4): 1. Введение и scope, Out of scope (эта итерация), Разделы UI (взгляд студента), Решения, зафиксированные на этапе проектирования

### Community 316 - "2. As-is: текущее состояние"
Cohesion: 0.50
Nodes (4): 2.1. ER-диаграмма (сейчас), 2.2. Существующие сущности (релевантные), 2.3. Ключевые пробелы, 2. As-is: текущее состояние

### Community 317 - "3.5. Изменения `Team` и семестровый контекст (`teams`)"
Cohesion: 0.50
Nodes (4): 3.5. Изменения `Team` и семестровый контекст (`teams`), `Team`, `TeamSemester`, `TeamSemesterMember`

### Community 318 - "8. Сводка: новые vs изменённые сущности"
Cohesion: 0.50
Nodes (4): 8. Сводка: новые vs изменённые сущности, Без изменений схемы (используются as-is), Изменённые модели, Новые модели

### Community 319 - "РАСПОРЯЖЕНИЕ"
Cohesion: 0.50
Nodes (3): Кому, О проведении сбора и верификации заявок по проектной деятельности на 2026–2027 учебный год, РАСПОРЯЖЕНИЕ

### Community 320 - "MentorTeamAddMemberSerializer"
Cohesion: 0.50
Nodes (3): MentorTeamAddMemberSerializer, Тело POST добавления участника., Требует ровно один идентификатор участника.

### Community 324 - "InstituteSerializer"
Cohesion: 0.67
Nodes (3): InstituteSerializer, Meta, Сериализатор для институтов/академий.

### Community 329 - "TeamSemester"
Cohesion: 0.06
Nodes (21): Репозиторий студенческой витрины проектов (без N+1)., Команда пользователя в семестре с блокировкой строки., Запросы и запись для студенческой витрины проектов., Команда пользователя в семестре (без блокировки)., Связь проект↔трек с проверкой семестра и статуса approved., Треки группы в семестре с одобренными проектами и тегами., Счётчик записанных команд с блокировкой строк TeamSemester проекта., Привязывает проект к команде и пишет лог. (+13 more)

### Community 331 - "TeamLobby.py"
Cohesion: 0.10
Nodes (25): MyTeamViewSet, API лобби формирования команд и «Моей команды»., Раздел «Моя команда» для капитана и участника., _is_staff_or_admin(), APIView, BasePermission, Request, Разрешения для приложения teams. (+17 more)

## Knowledge Gaps
- **267 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+262 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **112 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `Department`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `ProjectTrackService`, `Any`, `import_applications_from_excel.py`, `ApplicationDashboardService`, `test_mentor_team_viewset.py`, `StudyGroupMemberDTO`, `ProjectTrack`, `UserManagementService`, `ApplicationDashboardDomain`, `ProjectApplicationRepository`, `test_project_track_service.py`, `repositories/application_dashboard.py`, `test_study_group_domain.py`, `ProjectApplicationService`, `StudentShowcaseDomain`, `StudyGroupSemesterRepository`, `TeamLobbyService`, `.calculate_initial_status`, `Tag`, `CommentService`, `dto/institute_responsible.py`, `._get_track_with_access`, `.can_update_tag`, `.resolve_list_semester_id`, `DirectionService`, `ProjectTrackDomain`, `.get_or_create_placeholder`, `TeamLobbyRepository`, `TeamLobbyDomain`, `.can_change_status`, `TestUserManagementDomain`, `Settings`, `dto/mentor_groups.py`, `.get_filtered_queryset`, `TagService`, `teams/models.py`, `PermissionError`, `TeamLobby.py`, `._authorize_and_load`, `.can_delete_tag`, `ApplicationCapabilities`, `InstituteResponsibleService`, `ProjectApplication`, `.get_dashboard`, `ProjectTrackPermission`, `StudyGroup`, `test_project_application_new_fields.py`, `._resolve_institute_semester`, `institute_access.py`, `StudentShowcaseService`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `Department`, `ProjectApplicationCreateDTO`, `ProjectTrackService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `StudyGroupService`, `ApplicationDashboardService`, `test_mentor_groups_viewset.py`, `ApplicationNotificationService`, `test_mentor_team_viewset.py`, `test_mentor_showcase_viewset.py`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `student_user`, `test_team_lobby_viewset.py`, `TestProjectApplicationViewSetIsInternalCustomer`, `TagCreateDTO`, `TestTagViewSetCreate`, `TestTagViewSetDelete`, `ProjectService`, `ProjectApplicationService`, `test_study_group_domain.py`, `PreRegisteredStudent`, `CommentService`, `dto/institute_responsible.py`, `.can_update_tag`, `DirectionService`, `TestDepartmentPlanViewSetList`, `TestProjectViewSet`, `TestProjectApplicationReadDTO`, `ProjectTrackDomain`, `TagUpdateDTO`, `test_project_track_viewset.py`, `TestUserManagementDomain`, `Settings`, `.get_filtered_queryset`, `TagService`, `TestApplicationDashboardViewSet`, `TestLogStatusChange`, `.can_delete_tag`, `TestProjectApplicationListDTO`, `test_institute_responsible_viewset.py`, `test_mentor_group_detail_viewset.py`, `TestProjectApplicationViewSetTransferToInstitute`, `TestProjectApplicationListSemesterFilter`, `StudyGroup`, `TestSemesterAssignViewSet`, `TestGetLogs`, `TestProjectApplicationNewFieldsCreateUpdate`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `make_user`, `Department`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `ProjectTrackService`, `StudyGroupService`, `import_applications_from_excel.py`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `ProjectApplicationViewSet`, `ApplicationDashboardService`, `test_mentor_groups_viewset.py`, `test_mentor_team_viewset.py`, `test_mentor_showcase_viewset.py`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `test_team_lobby_viewset.py`, `test_project_track_service.py`, `repositories/application_dashboard.py`, `ProjectService`, `ProjectApplicationService`, `TeamLobbyService`, `.resolve_list_semester_id`, `TestDepartmentPlanViewSetList`, `test_import_study_groups_from_contingent.py`, `TestProjectViewSet`, `test_institute_access.py`, `Command`, `test_project_track_viewset.py`, `TeamLobbyDomain`, `Settings`, `MentorTeamService`, `showcase/urls.py`, `teams/models.py`, `TeamLobby.py`, `AccountsApiTests`, `test_institute_responsible_viewset.py`, `test_mentor_group_detail_viewset.py`, `InstituteResponsibleService`, `ProjectApplication`, `TestProjectApplicationListSemesterFilter`, `TestSemesterAssignViewSet`, `StudyGroup`, `test_project_application_new_fields.py`, `institute_access.py`, `StudentShowcaseService`, `TestProjectApplicationNewFieldsCreateUpdate`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Are the 526 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 526 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 74 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 74 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._