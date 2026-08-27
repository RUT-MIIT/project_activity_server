# Graph Report - project_activity_server  (2026-08-27)

## Corpus Check
- 291 files · ~133,160 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4246 nodes · 8271 edges · 342 communities (226 shown, 116 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 826 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b9ad2288`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TestRepositoryCreate
- make_user
- ProjectApplication
- ProjectApplicationRepository
- ProjectApplicationCreateDTO
- accounts/views.py
- ProjectApplicationViewSet
- Any
- Direction
- Tag
- ApplicationDashboardService
- ApplicationDashboardRepository
- Department
- test_project_track_service.py
- User
- test_study_group_domain.py
- prepare_study_groups_xlsx.py
- StudyGroup
- ProjectTrack
- TagService
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- Any
- .validate_create
- ValidationResult
- test_sync_departments_institutes.py
- test_import_study_groups_from_contingent.py
- TeamLobby.py
- test_team_lobby_viewset.py
- ApplicationDashboardDomain
- TestProjectApplicationReadDTO
- AvailableActionDTO
- TeamLobbyService
- ._resolve_institute_semester
- ProjectTrackViewSet
- TestTagViewSet
- ProjectService
- ProjectApplicationService
- ._create_app
- normalize_cell
- APIClient
- TestCoordinationAndDtosService
- ProjectTrackReadDTO
- PreRegisteredStudent
- CommentService
- TestTagViewSetCreate
- Semester
- .approve_application
- teams/views.py
- TestCanUpdateTag
- TagViewSet
- ProjectTrackService
- Any
- TestDepartmentPlanViewSetList
- UserManagementService
- application_dashboard_service.py
- TestValidationResult
- StudyGroupService
- APIView
- PreRegisteredStudentViewSet
- test_study_group_viewset.py
- ProjectTrackDomain
- TestLogStatusChange
- .can_change_status
- Примеры использования поля is_internal_customer
- PasswordResetSerializer
- ApplicationNotificationService
- TestProjectApplicationListSemesterFilter
- UserManagementDomain
- PreRegisteredStudentService
- .update_application
- .can_user_access_application
- .get_filtered_queryset
- DepartmentPlanViewSet
- ProjectTrackRepository
- DirectionService
- TestTagServiceUpdate
- TestApplicationDashboardViewSet
- TestTagViewSetDelete
- TestCanCreateTag
- TestProjectApplicationListDTO
- TeamLobbyDomain
- API для работы с проектными заявками
- AccountsApiTests
- TestCanDeleteTag
- Path
- .resolve_list_semester_id
- Command
- TeamLobbyRepository
- ApplicationCapabilities
- test_import_preregistered_students.py
- TestProjectViewSet
- .calculate_initial_status
- .validate_update
- .get_filtered_queryset
- accounts/admin.py
- Any
- TestProjectApplicationViewSetIsInternalCustomer
- TestProjectApplicationNewFieldsCreateUpdate
- TestProjectApplicationViewSetTransferToInstitute
- .can_edit_application
- extract_group_abbrev.py
- TestApproveRejectRequest
- StudyGroup.py
- Role
- .should_require_consultation
- direction_service.py
- .auth
- StudyGroupViewSet
- ProjectTrackGroupListDTO
- ProjectApplicationUpdateDTO
- _generate_collection.py
- .view_application
- TestGetLogs
- InvolvedManager
- django_db
- .post
- institute_access.py
- UserSerializer
- TestMyTeamViewSet
- StudyGroupMemberDTO
- TestSemesterAssignViewSet
- TestTagServiceDelete
- API Документация - Проектные заявки
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- ProjectTrackCreateSerializer
- Command
- Command
- TestInstituteViewSet
- update_prod.sh
- Command
- Command
- 0014_add_intermediate_approved_statuses.py
- TestDepartmentPlanViewSetMyDepartmentPlan
- 1. Создание заявки (авторизованные пользователи)
- Руководство по ручному развертыванию Project Activity Server
- 4. Список проектов
- TestStudentBlockedFromStaffApi
- deploy.sh
- action_types.py
- export_client_sources_to_docx.py
- make_source_docx.py
- test_direction_domain.py
- parse_miit_ief_groups.py
- Command
- ._format_external_share_chart
- schema.py
- ShowcaseConfig
- ProjectTrackAddApplicationsSerializer
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- ProjectTrackGroupDetailDTO
- teams/admin.py
- 0011_migrate_team_data.py
- TestRepositoryUpdate
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- .get_daily_dynamics
- tests/conftest.py
- showcase/urls.py
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- ProjectTrackProjectDetailDTO
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
- Command
- .test_password_change_success
- .test_password_change_wrong_current_password
- .test_password_reset_sends_email
- .test_registration_request_approve_allowed_for_cpds_user
- .test_registration_request_approve_creates_user_and_sends_email
- .test_registration_request_approve_forbidden_for_regular_user
- .test_registration_request_approve_mail_failure_returns_400_and_no_user_created
- student_user
- .test_registration_request_list_requires_privileged_user
- .test_registration_request_race_condition_integrity_error
- TestRepositoryApplicationNumbering
- .test_semester_create_allowed_for_admin_and_cpds
- ProjectTrackUpdateDTO
- .test_semester_list_requires_auth
- TestTagServiceGetTag
- .test_user_me_institute_code_none_if_no_institute
- .list_applications
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
- TestProjectApplicationViewSetIsExternalInResponses
- test_my_team_viewset.py
- PasswordChangeSerializer
- TestProjectApplicationViewSetSimple
- TestRepositoryFilter
- teams/models.py
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
- ApplicationDashboard.py
- TestRepositoryDeleteAndExists
- TestLogInvolvedDepartment
- TestTagServiceListTags
- Схема БД: студенческий портал
- Справочные эндпоинты
- DirectionViewSet
- test_team_semester_viewset.py
- ApplicationStatusReadSerializer
- .register
- test_preregistered_student_viewset.py
- ProjectViewSet
- ProjectRepository
- TestRepositoryGetById
- Текущий статус реализации
- .test_departments_list_allow_any_detail_requires_auth
- .test_registration_request_create_anonymous_allowed
- .test_registration_request_reject_forbidden_for_regular_user
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- Поддержка multipart/form-data
- Вариант 1: импорт схемы с автообновлением
- .test_semester_list_is_active_from_settings
- .test_user_me_institute_code_from_department_institute
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- .test_user_roles_list_requires_auth_and_returns
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- .list_unregistered
- CustomResetPasswordForm
- ProjectTrackAddApplicationItemSerializer
- ProjectTrackUpdateSerializer
- Command
- project_application.md
- project_activity_server
- .get_all
- 0038_alter_team_member_limits_default_4_7.py
- .filter_all_except_status
- .filter_by_status_queryset
- .filter_by_user_queryset
- .filter_coordination_by_user_queryset
- .filter_external_applications
- .get_all_applications_queryset
- .test_validation_result_str_invalid
- .test_validation_result_multiple_errors_same_field
- .test_validation_result_add_error_overwrites_existing
- .test_validation_result_add_errors
- .test_validation_result_add_errors_merges_with_existing
- .test_validation_result_get_errors_list

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 481 edges
2. `User` - 206 edges
3. `Department` - 138 edges
4. `ProjectApplication` - 137 edges
5. `ProjectApplicationService` - 136 edges
6. `ProjectApplicationCreateDTO` - 109 edges
7. `Semester` - 100 edges
8. `ProjectTrackService` - 70 edges
9. `StudyGroup` - 68 edges
10. `Institute` - 66 edges

## Surprising Connections (you probably didn't know these)
- `create_test_applications()` --uses--> `User`  [INFERRED]
  create_test_applications.py → accounts/models.py
- `create_test_user()` --uses--> `User`  [INFERRED]
  create_test_user.py → accounts/models.py
- `ApplicationDashboardDomain` --uses--> `User`  [INFERRED]
  showcase/domain/application_dashboard.py → accounts/models.py
- `ProjectTrackDomain` --uses--> `User`  [INFERRED]
  showcase/domain/project_track.py → accounts/models.py
- `TagDomain` --uses--> `User`  [INFERRED]
  showcase/domain/tag.py → accounts/models.py

## Import Cycles
- None detected.

## Communities (342 total, 116 thin omitted)

### Community 0 - "TestRepositoryCreate"
Cohesion: 0.12
Nodes (9): Создание заявки без тегов: проверяем, что пустой список не вызывает ошибок., Создание заявки с is_external=True: проверяем установку флага., Создание заявки с is_external=False: проверяем установку флага по умолчанию., Создание заявки без указания is_external: проверяем значение по умолчанию…, Тесты для метода create репозитория., Создание заявки с целевыми институтами: проверяем установку M2M связи.…, Создание заявки без целевых институтов: проверяем, что пустой список не…, Создание заявки с тегами: проверяем установку M2M связи. Проверяем, что tags… (+1 more)

### Community 1 - "make_user"
Cohesion: 0.04
Nodes (17): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+9 more)

### Community 2 - "ProjectApplication"
Cohesion: 0.04
Nodes (60): Репозиторий для управления пользователями., ViewSet для работы с планами подразделений по проектным заявкам., Генерация тестовых одобренных проектов и учебных групп для института IEF., ApplicationInvolvedDepartment, ApplicationInvolvedUser, ApplicationStatus, DepartmentPlan, Institute (+52 more)

### Community 3 - "ProjectApplicationRepository"
Cohesion: 0.06
Nodes (17): ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты…, Получение заявки по ID без дополнительных связанных объектов. Для простых…, Получение заявок пользователя, где он является автором. Оптимизированный запрос…, Получение заявок для координации пользователя. Заявки, где пользователь…, Репозиторий - вся работа с БД здесь, Получение заявок для координации по причастному подразделению. Заявки, где…, Получение заявок по статусу. Для административных операций. (+9 more)

### Community 4 - "ProjectApplicationCreateDTO"
Cohesion: 0.06
Nodes (25): create_test_applications(), Создаем тестовые заявки, Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, ProjectApplicationCreateDTO, DTO для создания заявки - только данные, никакой логики, Проверяем, что валидный DTO проходит валидацию без ошибок., Невалидные поля аккумулируют ошибки в ValidationResult., TestSubmitApplication (+17 more)

### Community 5 - "accounts/views.py"
Cohesion: 0.06
Nodes (44): AcademicYear, Meta, RegistrationRequest, Status, IsAdminOrCpds, Разрешает доступ только администраторам или пользователям с ролью `cpds`., AcademicYearSerializer, ApproveRequestSerializer (+36 more)

### Community 6 - "ProjectApplicationViewSet"
Cohesion: 0.05
Nodes (33): format_validation_errors(), get_error_message(), ProjectApplicationViewSet, action, extend_schema, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, GET /api/project-applications/external/ Получение списка всех внешних заявок… (+25 more)

### Community 7 - "Any"
Cohesion: 0.08
Nodes (17): ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackStatisticsDTO, Any, Преобразует DTO в словарь для API., DTO заявки в проектном треке., Преобразует DTO в словарь для API. (+9 more)

### Community 8 - "Direction"
Cohesion: 0.16
Nodes (10): DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DirectionSerializer, Meta, Сериализатор направления подготовки., Direction (+2 more)

### Community 9 - "Tag"
Cohesion: 0.03
Nodes (66): Доменная логика для тегов - чистые функции без эффектов., DTO для работы с тегами., DTO для обновления тега., DTO для создания тега., TagCreateDTO, TagUpdateDTO, DepartmentNestedSerializer, Meta (+58 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.06
Nodes (28): ApplicationDashboardService, Оркестрация получения данных дашборда заявок., django_db, Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external., Фильтр по группам статусов., Карточка in_work = total - approved - rejected., Среднее и медиана времени до решения. (+20 more)

### Community 11 - "ApplicationDashboardRepository"
Cohesion: 0.07
Nodes (30): DashboardFilters, Параметры фильтрации дашборда., ApplicationDashboardRepository, Q, QuerySet, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса. (+22 more)

### Community 12 - "Department"
Cohesion: 0.05
Nodes (43): Command, BaseCommand, Department, get_root_department(), is_cpds_department(), Утилиты для работы с подразделениями., Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех… (+35 more)

### Community 13 - "test_project_track_service.py"
Cohesion: 0.07
Nodes (27): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackAggregatedStatisticsDTO, ProjectTrackCreateDTO, DTO для проектных треков., DTO для создания проектного трека., DTO для добавления групп в трек. (+19 more)

### Community 14 - "User"
Cohesion: 0.05
Nodes (48): AbstractBaseUser, Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response (+40 more)

### Community 15 - "test_study_group_domain.py"
Cohesion: 0.12
Nodes (15): QuerySet, Фильтрация учебных групп по роли пользователя., institute_validator — только группы своих институтов., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., StudyGroupDomain, direction(), other_institute() (+7 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroup"
Cohesion: 0.10
Nodes (20): Доменная логика для учебных групп., MyStudyGroupDTO, DTO для эндпоинта «Моя группа»., Полные данные учебной группы для текущего студента., StudyGroup, QuerySet, Репозиторий для учебных групп., Доступ к данным StudyGroup. (+12 more)

### Community 18 - "ProjectTrack"
Cohesion: 0.07
Nodes (32): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+24 more)

### Community 19 - "TagService"
Cohesion: 0.08
Nodes (19): Чистая бизнес-логика для тегов - только функции, никаких эффектов., Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, TagDomain, Бизнес-операция: удаление тега. Args: tag_id: ID тега для удаления user:…, Бизнес-операция: получение списка тегов с фильтрацией по ролям. Для…, Бизнес-операция: получение тега по ID с проверкой доступа. Args: tag_id: ID…, Сервис - оркестрация всех операций с тегами. Координирует Domain, Repository и… (+11 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.08
Nodes (14): ProjectApplicationCreateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы…, Проверяет, что min_team_members не больше max_team_members., Преобразование в DTO - никакой бизнес-логики, Тесты для ProjectApplicationCreateDTO., Создание DTO из словаря через from_dict., Преобразование DTO в словарь через to_dict., Проверяем значения по умолчанию: пустые строки для title, company_contacts,… (+6 more)

### Community 22 - "Any"
Cohesion: 0.08
Nodes (14): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationUpdateSerializer, Сериализатор только для валидации HTTP данных при обновлении., Проверяет согласованность min/max, если оба переданы. (+6 more)

### Community 23 - ".validate_create"
Cohesion: 0.12
Nodes (13): Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Носитель проблемы короче 5 символов вызывает ошибку., Барьер короче 10 символов вызывает ошибку., Имя и фамилия автора короче 2 символов вызывают ошибки., Тесты для валидации при создании заявки., Телефон короче 10 символов вызывает ошибку., Валидный DTO проходит проверку без ошибок., Все ошибки валидации собираются в одном результате. (+5 more)

### Community 24 - "ValidationResult"
Cohesion: 0.13
Nodes (8): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Инициализация ValidationResult создаёт пустой словарь ошибок.

### Community 25 - "test_sync_departments_institutes.py"
Cohesion: 0.29
Nodes (10): Any, django_db, Экспорт и последующий импорт институтов восстанавливают данные., Экспорт и последующий импорт подразделений восстанавливают данные., Импорт институтов удаляет те, которых нет в файле., Импорт подразделений удаляет те, которых нет в файле., test_export_import_departments_roundtrip(), test_export_import_institutes_roundtrip() (+2 more)

### Community 26 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.11
Nodes (22): build_group_import_row(), build_group_name(), calculate_course_number(), GroupImportRow, parse_direction_level(), parse_permanent_group_code(), ParsedPermanentGroup, Чистая логика импорта учебных групп из отчёта контингента 1С. (+14 more)

### Community 27 - "TeamLobby.py"
Cohesion: 0.07
Nodes (34): PageNumberPagination, MyTeamEventLogDTO, ApproveJoinRequestSerializer, CreateInvitationSerializer, CreateTeamSerializer, MyTeamViewSet, action, extend_schema (+26 more)

### Community 28 - "test_team_lobby_viewset.py"
Cohesion: 0.13
Nodes (14): api_client(), _approved_app(), _create_captained_team(), direction(), lobby_setup(), django_db, fixture, Тесты API лобби формирования команд. (+6 more)

### Community 29 - "ApplicationDashboardDomain"
Cohesion: 0.10
Nodes (11): ApplicationDashboardDomain, Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп., Парсит query-параметр application_type., Парсит query-параметр days., Возвращает id подразделения и всех его потомков., Проверяет право пользователя на просмотр дашборда., Коды институтов пользователя; None — без ограничения. (+3 more)

### Community 30 - "TestProjectApplicationReadDTO"
Cohesion: 0.09
Nodes (13): Exception, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None., target_institutes сериализуется как список словарей с code и name., tags сериализуется как список словарей с id, name и category., involved_users сериализуется с данными пользователя, added_at и added_by. (+5 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "TeamLobbyService"
Cohesion: 0.12
Nodes (21): MyTeamReadDTO, atomic, QuerySet, UserType, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент принимает приглашение., Студент отклоняет приглашение. (+13 more)

### Community 33 - "._resolve_institute_semester"
Cohesion: 0.10
Nodes (12): ProjectTrackProjectListDTO, DTO проекта со счётчиком назначенных групп., Преобразует DTO в словарь для API., QuerySet, UserType, Список треков по фильтрам., Список проектов семестра со счётчиком назначенных групп., Подгружает подразделение пользователя для проверки институтов. (+4 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.13
Nodes (23): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+15 more)

### Community 35 - "TestTagViewSet"
Cohesion: 0.10
Nodes (11): Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level). (+3 more)

### Community 36 - "ProjectService"
Cohesion: 0.21
Nodes (5): ProjectService, Оркестрация Domain + Repository для списка проектов., TestProjectApplicationNewFieldsLists, django_db, TestProjectService

### Community 37 - "ProjectApplicationService"
Cohesion: 0.05
Nodes (28): ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка., Бизнес-операция: получение заявок по статусу., Бизнес-операция: получение последних заявок. (+20 more)

### Community 38 - "._create_app"
Cohesion: 0.07
Nodes (22): patch, Нет причастности подразделения — матрица запрещает действие, ожидаем…, department_validator: await_department -> approved_department ->…, institute_validator: await_institute -> approved_institute -> await_cpds…, institute_validator может согласовать await_department, подменяя шаг кафедры., cpds: может одобрять заявки в статусе await_cpds (переход в approved разрешен)., Запрос изменений: await_department -> returned_department, один лог., После отзыва автором: department_validator одобряет -> await_institute. (+14 more)

### Community 39 - "normalize_cell"
Cohesion: 0.07
Nodes (28): build_preregistered_student_import_row(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки., Разбирает ФИО из отчёта контингента. Returns: Кортеж (фамилия, имя, отчество). (+20 more)

### Community 40 - "APIClient"
Cohesion: 0.19
Nodes (8): MonkeyPatch, Any, APIClient, django_db, override_settings, TestPreRegisteredStudentLookup, TestPreRegisteredStudentMismatch, TestPreRegisteredStudentRegister

### Community 41 - "TestCoordinationAndDtosService"
Cohesion: 0.11
Nodes (9): Валидатор получает объединённый список: его причастность пользователя +…, cpds видит все заявки в статусе await_cpds даже без причастности., Преобразователи к DTO возвращают ожидаемые экземпляры., get_external_applications возвращает только заявки с is_external=True., get_external_applications позволяет фильтровать внешние заявки по коду статуса., get_external_applications с несуществующим статусом выбрасывает ValueError., get_external_applications_queryset возвращает QuerySet внешних заявок., get_external_applications требует авторизации. (+1 more)

### Community 42 - "ProjectTrackReadDTO"
Cohesion: 0.11
Nodes (15): ProjectTrackReadDTO, DTO для чтения проектного трека., atomic, Возвращает трек с проверкой доступа., Возвращает детали трека., Создаёт проектный трек., Проставляет лимиты размера команды всем заявкам трека., Обновляет основные поля трека и лимиты команд у заявок. (+7 more)

### Community 43 - "PreRegisteredStudent"
Cohesion: 0.12
Nodes (9): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если предрегистрация уже привязана к User., Репозиторий предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по нормализованному СНИЛС., Возвращает предрегистрацию по первичному ключу., Создаёт или обновляет предрегистрацию по табельному номеру. (+1 more)

### Community 44 - "CommentService"
Cohesion: 0.10
Nodes (17): CommentService, atomic, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db, Пустой текст вызывает ValueError., Тесты для CommentService. (+9 more)

### Community 45 - "TestTagViewSetCreate"
Cohesion: 0.12
Nodes (9): Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем., Нельзя создать общий тег, если имя уже используется (общим или departmental… (+1 more)

### Community 46 - "Semester"
Cohesion: 0.06
Nodes (31): Идемпотентный импорт строк модели Settings из CSV., Ключ–значение настроек приложения (редактируемые из админки / импортом)., Semester, Settings, Сервис управления пользователями., Command, BaseCommand, Добавляет причастные подразделения института к заявке. (+23 more)

### Community 47 - ".approve_application"
Cohesion: 0.08
Nodes (18): atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку., Бизнес-операция: отзыв заявки автором., Бизнес-операция: одобрение заявки. (+10 more)

### Community 48 - "teams/views.py"
Cohesion: 0.14
Nodes (15): Постоянная команда участников проектной деятельности., Team, _is_staff_or_admin(), APIView, BasePermission, Request, Разрешения для приложения teams., Доступ только студенту с привязанной учебной группой. (+7 more)

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+2 more)

### Community 50 - "TagViewSet"
Cohesion: 0.11
Nodes (20): Инициализация из модели Tag., TagReadDTO, DepartmentAttachDetachSerializer, action, Request, Response, GET /api/showcase/tags/{id}/ - получение тега с проверкой доступа., POST /api/showcase/tags/ - создание тега. (+12 more)

### Community 51 - "ProjectTrackService"
Cohesion: 0.14
Nodes (5): ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), django_db, TestProjectTrackService

### Community 52 - "Any"
Cohesion: 0.10
Nodes (13): LobbyInvitationDTO, LobbyReadDTO, LobbyTeamItemDTO, LobbyTrackDTO, MyTeamInvitationDTO, MyTeamJoinRequestDTO, Any, Pending-приглашение студента в лобби. (+5 more)

### Community 53 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 54 - "UserManagementService"
Cohesion: 0.09
Nodes (16): QuerySet, Доступ к данным пользователей для управления., Базовый queryset без администраторов., Список пользователей с оптимизацией запросов., Возвращает пользователя по ID., Сохраняет изменения пользователя., UserRepository, QuerySet (+8 more)

### Community 55 - "application_dashboard_service.py"
Cohesion: 0.16
Nodes (10): ApplicationDashboardDTO, Any, DTO для дашборда проектных заявок., Преобразует DTO в словарь для API., DTO блока KPI-карточек., DTO полного ответа дашборда., Преобразует DTO в словарь для API., SummaryCardsDTO (+2 more)

### Community 56 - "TestValidationResult"
Cohesion: 0.12
Nodes (9): Тесты для ValidationResult., get_errors_list возвращает пустой список когда нет ошибок., __str__ возвращает 'Validation successful' когда валидация прошла., __str__ корректно форматирует сообщение при одной ошибке., is_valid возвращает True когда нет ошибок., is_valid возвращает False когда есть ошибки., add_error добавляет ошибку в словарь., add_error позволяет добавлять несколько ошибок для разных полей. (+1 more)

### Community 57 - "StudyGroupService"
Cohesion: 0.12
Nodes (12): Any, Оркестрация Domain + Repository для StudyGroup., Возвращает данные учебной группы текущего студента., StudyGroupService, django_db, TestMyStudyGroupService, direction(), django_db (+4 more)

### Community 58 - "APIView"
Cohesion: 0.17
Nodes (9): APIView, Request, Проверяет наличие прав у пользователя., Проверяет наличие прав у пользователя., Проверяет права на чтение или запись пользователей., Проверяет наличие прав у пользователя. Args: request: текущий запрос view:…, Проверяет, что у текущего пользователя установлена роль с кодом `cpds`. Args:…, Проверяет, что у пользователя роль institute_validator. (+1 more)

### Community 59 - "PreRegisteredStudentViewSet"
Cohesion: 0.13
Nodes (18): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Публичные операции предрегистрации студентов., Ищет предрегистрацию по студбилету, табельному номеру или СНИЛС. (+10 more)

### Community 60 - "test_study_group_viewset.py"
Cohesion: 0.47
Nodes (5): direction(), other_institute(), fixture, Тесты StudyGroupViewSet., study_groups()

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.08
Nodes (15): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя., Проверяет, может ли пользователь управлять проектными треками., Коды институтов пользователя; None — без ограничения (admin/cpds). (+7 more)

### Community 62 - "TestLogStatusChange"
Cohesion: 0.12
Nodes (9): Первый переход (from_status=None) помечает заявку, если актор не автор., Логирование с указанием предыдущего лога для создания цепочки., Тесты для log_status_change., Если application равен None, выбрасывается ValueError., Успешное логирование изменения статуса (не автор — флаг выставляется)., Если to_status равен None, выбрасывается ValueError., Смена статуса автором не помечает заявку для самого автора., Одинаковый from/to статус не помечает заявку как изменённую. (+1 more)

### Community 63 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 66 - "ApplicationNotificationService"
Cohesion: 0.07
Nodes (20): ApplicationNotificationService, Отправка писем автору при отклонении и отправке на доработку., Email получателя: author_email заявки или email связанного пользователя-автора., Письмо автору: заявка отправлена на доработку., Письмо автору: заявка отклонена., InvolvedManagementService, atomic, Добавляет причастное подразделение по его краткому названию. Args: application:… (+12 more)

### Community 67 - "TestProjectApplicationListSemesterFilter"
Cohesion: 0.14
Nodes (9): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Фильтр ?semester_id= в GET-списке заявок., Автоподстановка семестра при создании заявки., TestProjectApplicationListSemesterFilter, TestProjectApplicationSemesterAutoAssign (+1 more)

### Community 68 - "UserManagementDomain"
Cohesion: 0.12
Nodes (11): QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., Правила доступа и валидации для управления пользователями., Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., UserManagementDomain (+3 more)

### Community 69 - "PreRegisteredStudentService"
Cohesion: 0.13
Nodes (11): PreRegisteredStudentRepository, Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по табельному номеру., Удаляет предрегистрации без привязанного пользователя., PreRegisteredStudentLookupResult, PreRegisteredStudentService, Отправляет администратору письмо о расхождении данных. Raises: ValueError: если…, Результат поиска предрегистрации. (+3 more)

### Community 70 - ".update_application"
Cohesion: 0.13
Nodes (10): Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Бизнес-операция: обновление заявки., Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Не-автор и не-ЦПДС не может редактировать заявку., Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult., CPDS может редактировать одобренные заявки., institute_validator-автор: save совпадает с available_actions (подразделение… (+2 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.14
Nodes (11): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Тесты для проверки доступа пользователя к заявке., Автор всегда имеет доступ к своей заявке., Админ имеет доступ ко всем заявкам., Модератор имеет доступ ко всем заявкам., CPDS имеет доступ ко всем заявкам., Валидатор подразделения имеет доступ ко всем заявкам., Валидатор института имеет доступ ко всем заявкам. (+3 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.14
Nodes (11): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., Тесты для фильтрации queryset тегов по ролям., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения., institute_validator без подразделения видит только общие теги. (+3 more)

### Community 73 - "DepartmentPlanViewSet"
Cohesion: 0.14
Nodes (17): DenyStudentPermission, Запрещает доступ пользователям с ролью student., DepartmentPlanSerializer, DepartmentPlanViewSet, action, extend_schema, Request, Response (+9 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.04
Nodes (34): ProjectTrackRepository, Q, QuerySet, Возвращает трек по id или None., Создаёт проектный трек., Обновляет поля трека., Возвращает id групп, уже привязанных к треку., Добавляет группы в трек; возвращает число созданных связей. (+26 more)

### Community 75 - "DirectionService"
Cohesion: 0.17
Nodes (9): DirectionService, Оркестрация Domain + Repository для Direction., Список направлений с фильтрацией по роли., Направление по коду с проверкой доступа., directions(), django_db, fixture, Тесты DirectionService. (+1 more)

### Community 76 - "TestTagServiceUpdate"
Cohesion: 0.12
Nodes (9): Тесты для метода update_tag сервиса., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги., Нельзя обновить тег, если имя и набор departments уже заняты другим тегом., Обновление несуществующего тега вызывает ошибку. (+1 more)

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - "TestTagViewSetDelete"
Cohesion: 0.08
Nodes (16): django_db, Тесты для обновления тегов через API., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., admin может обновлять любые теги., Тесты для удаления тегов через API., cpds может удалять общие теги., cpds не может удалять теги с подразделением. (+8 more)

### Community 79 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 80 - "TestProjectApplicationListDTO"
Cohesion: 0.13
Nodes (9): django_db, Тесты для ProjectApplicationListDTO., Базовые поля DTO для списка заполняются из модели., Если статус None, DTO.status тоже None., to_dict преобразует DTO в словарь с ISO форматированием даты., is_internal_customer включается в ProjectApplicationListDTO., Новые поля трека включаются в ProjectApplicationListDTO., is_internal_customer включается в ProjectApplicationReadDTO. (+1 more)

### Community 81 - "TeamLobbyDomain"
Cohesion: 0.08
Nodes (14): Заявка должна быть в статусе pending., Приглашение должно быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды»., True, если студент без команды и есть свободный слот., Запрещает изменения состава при подтверждённом составе., Проверяет, что пользователь — капитан команды., Приглашение не может назначать роль leader., При одобрении заявки нельзя назначить второго leader. (+6 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.11
Nodes (10): AccountsApiTests, override_settings, Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Создание заявки без подразделения возвращает ошибку валидации., Создание заявки с несуществующим подразделением возвращает ошибку валидации., После отклонения заявки можно подать новую с тем же email., Повторная подача при активной заявке возвращает ошибку валидации., Нельзя подать заявку, если пользователь с таким email уже зарегистрирован. (+2 more)

### Community 84 - "TestCanDeleteTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, django_db, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения. (+3 more)

### Community 85 - "Path"
Cohesion: 0.17
Nodes (11): direction(), Any, django_db, fixture, Path, Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта., Создаёт минимальный отчёт контингента для тестов. (+3 more)

### Community 86 - ".resolve_list_semester_id"
Cohesion: 0.08
Nodes (17): Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Следующий семестр для новых заявок (Settings.next_semester_code)., Разбор query-параметра semester_id для GET-списков: id, next, actual., Один запрос к Settings на ответ — код активного семестра для is_active., Создание заявки в БД. Принимает DTO и пользователя, возвращает созданную…, action, Request (+9 more)

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "TeamLobbyRepository"
Cohesion: 0.04
Nodes (30): QuerySet, Лог событий команды в семестре (новые сверху)., Pending-заявки студента в семестре., Pending-приглашения студента в семестре., Карта team_semester_id → id pending-заявки текущего пользователя., Трек, доступный группе в семестре., Число команд группы в треке в семестре., True, если студент уже в команде в семестре. (+22 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.13
Nodes (12): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы., Возвращает список доступных действий согласно матрице. (+4 more)

### Community 90 - "test_import_preregistered_students.py"
Cohesion: 0.20
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 91 - "TestProjectViewSet"
Cohesion: 0.18
Nodes (4): _create_approved_app(), django_db, ЦПДС в причастных не должно подменять основное подразделение проекта., TestProjectViewSet

### Community 92 - ".calculate_initial_status"
Cohesion: 0.17
Nodes (9): Определение начального статуса на основе роли пользователя. Чистая функция -…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds., Обычный пользователь создаёт заявки в статусе await_department., Неизвестная роль возвращает статус await_department по умолчанию. (+1 more)

### Community 93 - ".validate_update"
Cohesion: 0.19
Nodes (8): Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Тесты для валидации при обновлении заявки., Валидные поля при обновлении проходят проверку., Название короче 5 символов вызывает ошибку., Email без символа @ вызывает ошибку., Валидация проверяет только переданные поля (None игнорируются)., Пустые строки вызывают ошибки валидации., TestValidateUpdate

### Community 94 - ".get_filtered_queryset"
Cohesion: 0.24
Nodes (5): QuerySet, Фильтрует направления: institute_validator — только из групп своего института., parametrize, Фильтрация queryset направлений по ролям., TestGetFilteredQueryset

### Community 95 - "accounts/admin.py"
Cohesion: 0.24
Nodes (11): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+3 more)

### Community 96 - "Any"
Cohesion: 0.12
Nodes (10): Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Преобразование в словарь., Сериализатор для создания тега., Преобразование в DTO., Сериализатор для обновления тега., Преобразование в DTO. (+2 more)

### Community 97 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 98 - "TestProjectApplicationNewFieldsCreateUpdate"
Cohesion: 0.27
Nodes (4): _base_create_payload(), django_db, TestMyApplicationsNewFields, TestProjectApplicationNewFieldsCreateUpdate

### Community 99 - "TestProjectApplicationViewSetTransferToInstitute"
Cohesion: 0.17
Nodes (8): Тесты для действия передачи заявки в институт по коду института., POST /api/showcase/project-applications/{id}/transfer_to_institute/ с…, Отсутствующий параметр code возвращает 400., Несуществующий код института возвращает 400 от сервиса., Институт без связанного подразделения возвращает 400., GET /api/showcase/project-applications/external/?status=... фильтрует внешние…, GET /api/showcase/project-applications/external/?status=... с несуществующим…, TestProjectApplicationViewSetTransferToInstitute

### Community 100 - ".can_edit_application"
Cohesion: 0.16
Nodes (9): Проверка права на редактирование заявки. Бизнес-правило: редактировать может…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку., Не-автор и не-ЦПДС не может редактировать чужую заявку., Нельзя редактировать заявки со статусом rejected (даже автору и cpds)., Нельзя редактировать одобренные заявки (кроме админов и cpds)., Автор может редактировать заявку в статусе returned_*., CPDS может редактировать заявки в статусе rejected_department. (+1 more)

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - "TestApproveRejectRequest"
Cohesion: 0.27
Nodes (6): parametrize, Матрица прав определяет доступность reject., Для returned_* действует агрегирующее правило returned_(all)., Отзыв доступен только автору и не для финальных approved/rejected., Матрица прав определяет доступность approve для ролей и статусов., TestApproveRejectRequest

### Community 103 - "StudyGroup.py"
Cohesion: 0.19
Nodes (10): Any, DTO для учебных групп., DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, Компактная выдача для списка учебных групп. (+2 more)

### Community 104 - "Role"
Cohesion: 0.14
Nodes (8): Command, BaseCommand, Role, UserManager, Сервис предрегистрации и регистрации студентов из контингента., BaseUserManager, Command, BaseCommand

### Community 105 - ".should_require_consultation"
Cohesion: 0.17
Nodes (9): Определение необходимости консультации на основе данных заявки. Чистая функция…, Тесты для определения необходимости консультации., Если уровень проекта не указан, нужна консультация., Если целевые институты не указаны, нужна консультация., Если цель проекта короче 50 символов, нужна консультация., Если все условия выполнены, консультация не требуется., Если project_level равен None, нужна консультация., Если target_institutes равен None, нужна консультация. (+1 more)

### Community 106 - "direction_service.py"
Cohesion: 0.19
Nodes (8): DirectionDomain, Доменная логика для направлений подготовки., Фильтрация направлений по роли пользователя., DirectionRepository, Репозиторий для направлений подготовки., Направление по коду (PK)., Доступ к данным Direction., Сервис для операций с направлениями подготовки.

### Community 107 - ".auth"
Cohesion: 0.17
Nodes (6): Без токена возвращается 401, с токеном — профиль текущего пользователя., Админ отклоняет заявку: статус становится REJECTED и уходит письмо., Пользователь ЦПДС может отклонять заявки (IsCpdsUser)., Если отправка письма при reject падает, возвращаем 200 и оставляем статус…, Детальный просмотр роли по коду (lookup_field=code) требует авторизации., Логинится и проставляет Bearer-токен в заголовках клиента.

### Community 108 - "StudyGroupViewSet"
Cohesion: 0.22
Nodes (7): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/ — список и просмотр учебных групп., Парсит query-параметр is_end; None — фильтр не применяется., StudyGroupViewSet

### Community 109 - "ProjectTrackGroupListDTO"
Cohesion: 0.29
Nodes (4): ProjectTrackGroupListDTO, DTO группы со счётчиком назначенных проектов., Преобразует DTO в словарь для API., Список групп института со счётчиком назначенных проектов.

### Community 110 - "ProjectApplicationUpdateDTO"
Cohesion: 0.06
Nodes (35): Общие константы приложения showcase., ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Явное выражение бизнес-намерений (не технических операций). Этот модуль…, Domain слой - чистая бизнес-логика без побочных эффектов. Этот слой содержит…, build_author_short_name(), ProjectApplicationListDTO (+27 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - ".view_application"
Cohesion: 0.15
Nodes (8): Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Автор всегда имеет доступ к просмотру своей заявки., Обычному пользователю чужая заявка недоступна., Список заявок разрешён всем (возвращает True)., TestViewAndList

### Community 113 - "TestGetLogs"
Cohesion: 0.06
Nodes (20): django_db, Тесты для логирования причастных пользователей., Логирование добавления причастного пользователя., Проверка валидации при добавлении причастного пользователя., Логирование удаления причастного пользователя., Тесты для получения логов., Получение всех логов по заявке., Если application равен None, выбрасывается ValueError. (+12 more)

### Community 114 - "InvolvedManager"
Cohesion: 0.43
Nodes (3): InvolvedManager, atomic, Менеджер для управления причастными пользователями и подразделениями.

### Community 115 - "django_db"
Cohesion: 0.15
Nodes (9): django_db, Тесты для методов подсчёта заявок., count_by_user возвращает количество заявок автора., count_by_status возвращает количество заявок с указанным статусом., Тесты для методов фильтрации внешних заявок., filter_external_applications возвращает только заявки с is_external=True., filter_external_applications_queryset возвращает QuerySet внешних заявок., TestRepositoryCount (+1 more)

### Community 116 - ".post"
Cohesion: 0.31
Nodes (4): extend_schema, Request, Response, Сменяет пароль текущего пользователя после проверки текущего пароля.

### Community 117 - "institute_access.py"
Cohesion: 0.08
Nodes (31): Доменная логика управления пользователями., ID подразделений для фильтрации; None — без ограничения., get_department_subtree_ids(), Возвращает id корневого подразделения и всех его потомков., Доменная логика дашборда проектных заявок., Доменная логика для списка проектов., Доменная логика для проектных треков., Репозиторий агрегаций для дашборда проектных заявок. (+23 more)

### Community 118 - "UserSerializer"
Cohesion: 0.18
Nodes (9): Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., UserSerializer, CustomTokenObtainPairSerializer (+1 more)

### Community 120 - "StudyGroupMemberDTO"
Cohesion: 0.22
Nodes (5): Any, Карточка наставника учебной группы., Строка списка группы из контингента., StudyGroupMemberDTO, StudyGroupMentorDTO

### Community 121 - "TestSemesterAssignViewSet"
Cohesion: 0.29
Nodes (3): Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, TestSemesterAssignViewSet

### Community 122 - "TestTagServiceDelete"
Cohesion: 0.17
Nodes (7): Тесты для метода delete_tag сервиса., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять теги своего подразделения., admin может удалять любые теги., Удаление несуществующего тега вызывает ошибку., TestTagServiceDelete

### Community 123 - "API Документация - Проектные заявки"
Cohesion: 0.18
Nodes (9): API Документация - Проектные заявки, Аутентификация, Базовый URL, Валидационные правила, Общая информация, Обязательные поля, Обязательные поля:, Типы данных (+1 more)

### Community 124 - "test_import_institutes.py"
Cohesion: 0.54
Nodes (7): django_db, Path, Тесты команды import_institutes., test_import_institutes_clear_removes_missing(), test_import_institutes_is_idempotent(), test_import_institutes_updates_existing(), _write_institutes_csv()

### Community 125 - "build_fgos_napravleniya_csv.py"
Cohesion: 0.43
Nodes (6): collect_codes(), fetch(), main(), parse_table_rows(), Собрать fgos_specialitet_napravleniya.csv: level, code, name (без групп…, middle: '03' — бакалавриат, '05' — специалитет.

### Community 126 - "ProjectTrackCreateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackCreateSerializer, Сериализатор для создания проектного трека., Проверяет согласованность лимитов размера команды.

### Community 127 - "Command"
Cohesion: 0.33
Nodes (5): Command, BaseCommand, Экспорт возможных статусов заявок в Excel., Считывает статусы из базы и сохраняет в Excel., Возвращает статусы, отсортированные по позиции и коду.

### Community 128 - "Command"
Cohesion: 0.32
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

### Community 132 - "Command"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Сбрасывает счетчик ID для таблицы тегов.

### Community 133 - "0014_add_intermediate_approved_statuses.py"
Cohesion: 0.33
Nodes (5): add_intermediate_approved_statuses(), Migration, Удаляет промежуточные статусы одобрения из БД., Добавляет промежуточные статусы одобрения в БД., remove_intermediate_approved_statuses()

### Community 134 - "TestDepartmentPlanViewSetMyDepartmentPlan"
Cohesion: 0.13
Nodes (9): django_db, Тесты для GET /api/showcase/department-plans/my-department-plan/ - план…, Успешное получение плана и статистики для подразделения пользователя., Если план отсутствует, возвращается 0, но статистика заявок учитывается., Ошибка: отсутствует semester_id., Ошибка: семестр не найден., Ошибка: у пользователя не указано подразделение., Ошибка: неавторизованный пользователь. (+1 more)

### Community 135 - "1. Создание заявки (авторизованные пользователи)"
Cohesion: 0.33
Nodes (6): 1. Создание заявки (авторизованные пользователи), Заголовки, Пример запроса, Тело запроса, Успешный ответ (201), Эндпоинты создания заявок

### Community 136 - "Руководство по ручному развертыванию Project Activity Server"
Cohesion: 0.15
Nodes (12): 10. Проверка и сопровождение, 11. Настройка nginx (backend + SPA), 1. Подготовка окружения, 2. Получение исходного кода, 3. Создание и активация виртуального окружения, 4. Настройка переменных окружения (.env), 5. Настройка PostgreSQL, 6. Миграции и статические файлы (+4 more)

### Community 137 - "4. Список проектов"
Cohesion: 0.29
Nodes (7): 4. Список проектов, Query-параметры, Заголовки, Ошибки, Поведение по ролям, Примеры запросов, Успешный ответ (200)

### Community 138 - "TestStudentBlockedFromStaffApi"
Cohesion: 0.13
Nodes (4): django_db, TestApplicationCommentAccess, TestApplicationDestroyDisabled, TestStudentBlockedFromStaffApi

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

### Community 143 - "test_direction_domain.py"
Cohesion: 0.20
Nodes (9): directions(), other_institute(), django_db, fixture, Тесты доменной логики DirectionDomain., Разрешение институтов по подразделению пользователя., Три направления для сценариев фильтрации., Второй институт на другом подразделении. (+1 more)

### Community 144 - "parse_miit_ief_groups.py"
Cohesion: 0.60
Nodes (4): extract_block(), main(), parse_groups(), Парсинг групп ИЭФ со страницы miit.ru/timetable.

### Community 147 - "schema.py"
Cohesion: 0.50
Nodes (3): exclude_auth_api_duplicate(), Хуки и расширения для drf-spectacular., Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*). В…

### Community 149 - "ProjectTrackAddApplicationsSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationsSerializer, Список заявок с рекомендуемым числом команд и лимитами размера., Проверяет отсутствие дубликатов id в одном запросе.

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

### Community 156 - "ProjectTrackGroupDetailDTO"
Cohesion: 0.20
Nodes (6): ProjectTrackGroupDetailDTO, ProjectTrackGroupProjectDTO, DTO проекта в деталях группы., Преобразует DTO в словарь для API., DTO деталей группы с назначенными проектами., Преобразует DTO в словарь для API.

### Community 157 - "teams/admin.py"
Cohesion: 0.27
Nodes (11): DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin, TeamSemesterAdmin (+3 more)

### Community 159 - "TestRepositoryUpdate"
Cohesion: 0.20
Nodes (6): Тесты для методов обновления заявок., Обновление заявки с изменением целевых институтов: проверяем установку M2M…, Обновление заявки с изменением тегов: проверяем установку M2M связи., Обновление заявки без полей: проверяем вызов save() без update_fields., update_status изменяет статус заявки., TestRepositoryUpdate

### Community 165 - "tests/conftest.py"
Cohesion: 0.23
Nodes (11): departments(), institute(), fixture, Возвращает класс модели пользователя для удобства., Создаёт набор ролей, используемых в тестах. Возвращает dict: code -> Role, Создаёт иерархию подразделений: parent -> child., Создаёт все необходимые статусы для сценариев сервисов., Создаёт институт, связанный с родительским подразделением. (+3 more)

### Community 166 - "showcase/urls.py"
Cohesion: 0.20
Nodes (8): ApplicationStatusViewSet, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, InstituteSerializer, InstituteViewSet, Meta, ViewSet только для чтения институтов/академий. Доступен для всех пользователей.…, Переопределяем list для возврата всех институтов без пагинации., Сериализатор для институтов/академий.

### Community 170 - "ProjectTrackProjectDetailDTO"
Cohesion: 0.17
Nodes (7): ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, DTO группы в деталях проекта., Преобразует DTO в словарь для API., DTO деталей проекта с назначенными группами., Преобразует DTO в словарь для API., Детали проекта с назначенными группами.

### Community 189 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 197 - "student_user"
Cohesion: 0.27
Nodes (8): api_client(), Any, APIClient, django_db, fixture, student_user(), study_group(), TestUserMeStudent

### Community 200 - "TestRepositoryApplicationNumbering"
Cohesion: 0.20
Nodes (6): Тесты для генерации номеров заявок., Первая заявка в году получает номер 1., Номера последовательно увеличиваются в пределах одного года., Нумерация учитывает пропуски - использует максимальный номер, а не count()., Нумерация сбрасывается при смене года., TestRepositoryApplicationNumbering

### Community 202 - "ProjectTrackUpdateDTO"
Cohesion: 0.22
Nodes (5): ProjectTrackUpdateDTO, DTO для обновления проектного трека., Создаёт DTO из словаря., Возвращает только переданные поля трека для обновления., True, если переданы лимиты размера команды для заявок трека.

### Community 204 - "TestTagServiceGetTag"
Cohesion: 0.22
Nodes (6): django_db, Тесты для метода get_tag сервиса., get_tag возвращает тег, если есть доступ., get_tag вызывает ошибку, если нет доступа., get_tag для несуществующего тега вызывает ошибку., TestTagServiceGetTag

### Community 206 - ".list_applications"
Cohesion: 0.25
Nodes (4): Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации., Бизнес-операция: получение заявок для координации пользователя. Для обычных…

### Community 240 - "TestProjectApplicationViewSetIsExternalInResponses"
Cohesion: 0.25
Nodes (5): Тесты для проверки наличия поля is_external в ответах API., POST /api/showcase/project-applications/ возвращает is_external в ответе., GET /api/showcase/project-applications/{id}/ возвращает is_external в ответе., GET /api/showcase/project-applications/ возвращает is_external в списке., TestProjectApplicationViewSetIsExternalInResponses

### Community 241 - "test_my_team_viewset.py"
Cohesion: 0.39
Nodes (7): api_client(), direction(), my_team_setup(), fixture, Тесты API «Моя команда»., semester(), study_group()

### Community 242 - "PasswordChangeSerializer"
Cohesion: 0.29
Nodes (4): PasswordChangeSerializer, Any, Возвращает учебную группу пользователя или None., Сериализатор для смены пароля аутентифицированного пользователя.

### Community 243 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

### Community 244 - "TestRepositoryFilter"
Cohesion: 0.25
Nodes (5): Тесты для методов фильтрации заявок., filter_coordination_by_user_queryset возвращает QuerySet заявок для координации…, filter_by_status_queryset возвращает QuerySet заявок по статусу., filter_by_company ищет заявки по названию компании (case-insensitive)., TestRepositoryFilter

### Community 245 - "teams/models.py"
Cohesion: 0.10
Nodes (24): Доменные правила лобби формирования команд., LobbyJoinRequestDTO, DTO лобби формирования команд и «Моей команды»., Pending-заявка студента в лобби., Meta, Участие команды в конкретном семестре: проект, наставник, капитан., Участник команды в конкретном семестре., Заявка студента на вступление в команду в семестре. (+16 more)

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 277 - "ApplicationDashboard.py"
Cohesion: 0.20
Nodes (7): ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 278 - "TestRepositoryDeleteAndExists"
Cohesion: 0.25
Nodes (5): Тесты для методов удаления и проверки существования., delete удаляет заявку и возвращает True., exists возвращает True для существующей заявки., exists возвращает False для несуществующей заявки., TestRepositoryDeleteAndExists

### Community 279 - "TestLogInvolvedDepartment"
Cohesion: 0.25
Nodes (5): Тесты для логирования причастных подразделений., Логирование добавления причастного подразделения., Проверка валидации при добавлении подразделения., Логирование удаления причастного подразделения., TestLogInvolvedDepartment

### Community 280 - "TestTagServiceListTags"
Cohesion: 0.25
Nodes (5): Тесты для метода list_tags сервиса., list_tags фильтрует теги для роли cpds., list_tags фильтрует теги для роли institute_validator., list_tags для admin возвращает все теги., TestTagServiceListTags

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 289 - "DirectionViewSet"
Cohesion: 0.43
Nodes (4): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений.

### Community 292 - "test_team_semester_viewset.py"
Cohesion: 0.43
Nodes (6): api_client(), direction(), fixture, Тесты API TeamSemester., semester(), study_group()

### Community 293 - "ApplicationStatusReadSerializer"
Cohesion: 0.40
Nodes (5): ApplicationStatusReadSerializer, ApplicationStatusSerializer, Meta, Сериализатор для статусов заявок, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…

### Community 294 - ".register"
Cohesion: 0.33
Nodes (3): atomic, Отправляет студенту письмо после успешной регистрации., Создаёт пользователя по предрегистрации и возвращает JWT + профиль. Raises:…

### Community 295 - "test_preregistered_student_viewset.py"
Cohesion: 0.47
Nodes (5): api_client(), pre_registered_student(), fixture, Тесты API предрегистрации студентов., study_group()

### Community 296 - "ProjectViewSet"
Cohesion: 0.25
Nodes (5): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией.

### Community 297 - "ProjectRepository"
Cohesion: 0.29
Nodes (5): ProjectRepository, QuerySet, Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

### Community 298 - "TestRepositoryGetById"
Cohesion: 0.33
Nodes (4): Тесты для методов получения заявок по ID., get_by_id возвращает заявку с оптимизированными запросами (prefetch_related)., get_by_id_simple возвращает заявку без дополнительных prefetch., TestRepositoryGetById

### Community 299 - "Текущий статус реализации"
Cohesion: 0.40
Nodes (5): ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации, 🔧 Требует доработки

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

### Community 307 - "Поддержка multipart/form-data"
Cohesion: 0.33
Nodes (6): Допустимые форматы файлов, Заголовки, Загрузка файлов, Максимальный размер файла, Поддержка multipart/form-data, Тело запроса

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

### Community 322 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 323 - "ProjectTrackUpdateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackUpdateSerializer, Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

## Knowledge Gaps
- **215 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+210 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **116 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `make_user()` connect `make_user` to `TestRepositoryCreate`, `ProjectApplicationCreateDTO`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `TestStudentBlockedFromStaffApi`, `ApplicationDashboardService`, `test_project_track_service.py`, `test_direction_domain.py`, `test_study_group_domain.py`, `StudyGroup`, `ProjectTrack`, `TagService`, `TestDepartmentPlanViewSetCreate`, `TestRepositoryDeleteAndExists`, `TestLogInvolvedDepartment`, `TestTagServiceListTags`, `test_team_lobby_viewset.py`, `TestProjectApplicationReadDTO`, `TestRepositoryUpdate`, `TestTagViewSet`, `ProjectService`, `tests/conftest.py`, `._create_app`, `ProjectApplicationService`, `APIClient`, `TestCoordinationAndDtosService`, `TestRepositoryGetById`, `CommentService`, `TestTagViewSetCreate`, `TestCanUpdateTag`, `ProjectTrackService`, `TestDepartmentPlanViewSetList`, `UserManagementService`, `StudyGroupService`, `ProjectTrackDomain`, `TestLogStatusChange`, `ApplicationNotificationService`, `TestProjectApplicationListSemesterFilter`, `UserManagementDomain`, `student_user`, `.get_filtered_queryset`, `TestRepositoryApplicationNumbering`, `DirectionService`, `TestTagServiceGetTag`, `TestApplicationDashboardViewSet`, `TestTagViewSetDelete`, `TestCanCreateTag`, `TestProjectApplicationListDTO`, `TestTagServiceUpdate`, `TestCanDeleteTag`, `test_import_preregistered_students.py`, `TestProjectViewSet`, `.get_filtered_queryset`, `TestProjectApplicationViewSetIsInternalCustomer`, `TestProjectApplicationNewFieldsCreateUpdate`, `TestProjectApplicationViewSetTransferToInstitute`, `TestProjectApplicationViewSetIsExternalInResponses`, `TestGetLogs`, `test_my_team_viewset.py`, `django_db`, `TestRepositoryFilter`, `TestSemesterAssignViewSet`, `TestTagServiceDelete`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `ProjectApplication`, `ProjectApplicationRepository`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `Tag`, `ApplicationDashboardService`, `Department`, `test_project_track_service.py`, `test_study_group_domain.py`, `StudyGroup`, `TagService`, `ApplicationDashboardDomain`, `TeamLobbyService`, `._resolve_institute_semester`, `ProjectApplicationService`, `ProjectTrackReadDTO`, `ProjectTrackProjectDetailDTO`, `CommentService`, `Semester`, `.approve_application`, `teams/views.py`, `TestCanUpdateTag`, `ProjectTrackService`, `UserManagementService`, `application_dashboard_service.py`, `StudyGroupService`, `ProjectTrackDomain`, `PasswordResetSerializer`, `ApplicationNotificationService`, `UserManagementDomain`, `.update_application`, `.get_filtered_queryset`, `DepartmentPlanViewSet`, `.filter_by_user_queryset`, `.filter_coordination_by_user_queryset`, `DirectionService`, `.list_applications`, `TestCanCreateTag`, `TeamLobbyDomain`, `TestCanDeleteTag`, `.resolve_list_semester_id`, `.get_filtered_queryset`, `accounts/admin.py`, `direction_service.py`, `ProjectTrackGroupListDTO`, `ProjectApplicationUpdateDTO`, `.view_application`, `PasswordChangeSerializer`, `InvolvedManager`, `institute_access.py`, `UserSerializer`, `teams/models.py`, `StudyGroupMemberDTO`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `make_user`, `ProjectApplication`, `ProjectApplicationRepository`, `accounts/views.py`, `ProjectApplicationViewSet`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `ApplicationDashboardService`, `TestStudentBlockedFromStaffApi`, `test_project_track_service.py`, `StudyGroup`, `ProjectTrack`, `TestDepartmentPlanViewSetCreate`, `test_import_study_groups_from_contingent.py`, `test_team_lobby_viewset.py`, `TeamLobbyService`, `ProjectService`, `ProjectApplicationService`, `test_team_semester_viewset.py`, `teams/views.py`, `ProjectTrackService`, `TestDepartmentPlanViewSetList`, `UserManagementService`, `application_dashboard_service.py`, `StudyGroupService`, `Command`, `TestProjectApplicationListSemesterFilter`, `DepartmentPlanViewSet`, `AccountsApiTests`, `.resolve_list_semester_id`, `TestProjectViewSet`, `accounts/admin.py`, `TestProjectApplicationNewFieldsCreateUpdate`, `ProjectApplicationUpdateDTO`, `test_my_team_viewset.py`, `teams/models.py`, `institute_access.py`, `TestSemesterAssignViewSet`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 478 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 478 INFERRED edges - model-reasoned connections that need verification._
- **Are the 42 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 72 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._