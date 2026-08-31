# Graph Report - project_activity_server  (2026-08-31)

## Corpus Check
- 346 files · ~159,715 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5172 nodes · 10399 edges · 348 communities (235 shown, 113 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1021 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `39b86d0f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MentorTeamViewSet
- make_user
- TestCanCreateTag
- Ответственный по институту — API для фронта
- ProjectTrackService
- accounts/views.py
- APIClient
- project_track_service.py
- application_import.py
- TagRepository
- ApplicationDashboardService
- ApplicationDashboardRepository
- test_mentor_groups_viewset.py
- import_study_groups_from_contingent.py
- TestApplicationNotificationService
- MentorTeamRepository
- prepare_study_groups_xlsx.py
- MyStudyGroupDTO
- ProjectTrack
- UserManagementService
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- PreRegisteredStudentService
- ApplicationDashboardDomain
- StudyGroupViewSet
- TestStudentShowcaseEnroll
- normalize_cell
- TeamLobby.py
- TestTeamLobbyViewSet
- UserListDTO
- TestProjectApplicationViewSetIsInternalCustomer
- AvailableActionDTO
- MentorTeamService
- test_project_track_service.py
- ProjectTrackViewSet
- TestTagViewSetCreate
- TestTagViewSet
- ProjectService
- ProjectApplicationService
- StudentShowcaseDomain
- PreRegisteredStudent
- TeamLobbyService
- .calculate_initial_status
- accounts/urls.py
- TestCommentService
- Path
- dto/institute_responsible.py
- PermissionError
- prod_users_client.py
- TestCanUpdateTag
- TagViewSet
- teams/views.py
- DirectionService
- TestDepartmentPlanViewSetList
- test_import_study_groups_from_contingent.py
- TestProjectViewSet
- ValidationResult
- TestProjectApplicationReadDTO
- APIView
- TestSubmitApplicationService
- TeamLobbyDomain
- ProjectTrackDomain
- ._resolve_context
- showcase/admin.py
- Примеры использования поля is_internal_customer
- TeamSemester
- team_lobby_service.py
- .approve_application
- TestUserManagementDomain
- accounts/admin.py
- PreRegisteredStudentRepository
- .can_user_access_application
- .get_filtered_queryset
- DepartmentPlanViewSet
- ProjectTrackRepository
- .view_application
- ._authorize_and_load
- TestApplicationDashboardViewSet
- .can_change_status
- TagSerializer
- Витрина проектов (студент) — API для фронта
- MentorTeamDomain
- API для работы с проектными заявками
- AccountsApiTests
- TestCanDeleteTag
- build_user_indexes
- test_mentor_team_viewset.py
- Command
- Управление командой
- ApplicationCapabilities
- test_import_preregistered_students.py
- .resolve_list_semester_id
- InstituteResponsibleDomain
- test_mentor_group_detail_viewset.py
- TestCoordinationAndDtosService
- extract.py
- User
- InstituteResponsibleService
- teams/admin.py
- TestProjectApplicationViewSetTransferToInstitute
- refresh_prod_users_json
- extract_group_abbrev.py
- Department
- Общая информация
- Command
- Role
- .get_dashboard
- Direction
- StudyGroup.py
- TestProjectApplicationListSemesterFilter
- StudentShowcaseViewSet
- _generate_collection.py
- StudyGroup
- ApplicationLoggingService
- get_root_department
- direction_service.py
- .get_filtered_queryset
- institute_access.py
- StudentShowcaseService
- TestMyTeamViewSet
- sync_project_teachers.py
- .get_filtered_queryset
- django_db
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
- Any
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- student_user
- test_study_group_viewset.py
- 0011_migrate_team_data.py
- test_student_showcase_viewset.py
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- TestTagViewSetDelete
- test_study_group_domain.py
- test_direction_domain.py
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- test_team_lobby_viewset.py
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
- fixture
- Settings
- RutMiitClient
- ProjectApplication
- .test_departments_list_allow_any_detail_requires_auth
- .test_registration_request_create_anonymous_allowed
- Command
- MentorGroupDetailDTO
- TagService
- ._track_detail_queryset
- teams/models.py
- ApplicationDashboard.py
- 0021_user_placeholder_preregistered_flag.py
- .test_registration_request_reject_forbidden_for_regular_user
- API Документация - Проектные заявки
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
- ProjectTrackProjectDetailDTO
- .test_user_me_institute_code_from_department_institute
- .test_user_roles_list_requires_auth_and_returns
- ProjectViewSet
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
- DirectionViewSet
- test_team_semester_viewset.py
- ProjectTrack.py
- ProjectApplicationRepository
- Схема БД: студенческий портал
- Справочные эндпоинты
- Парсинг «Проектная деятельность» — РУТ (МИИТ)
- Command
- ProjectDomain
- test_institute_responsible_viewset.py
- test_link_institutes_by_name_simple
- ProjectTrackAddGroupsDTO
- ProjectRepository
- 0017_copy_studygroup_mentors_to_semester.py
- Валидационные правила
- .get_daily_dynamics
- CustomResetPasswordForm
- .recalculate_recommended_teams_count
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- .handle
- Вариант 1: импорт схемы с автообновлением
- .get_all
- .create
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- 0016_studygroupsemester.py
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- MentorTeam.py
- .get_existing_application_ids
- .update_team_member_limits
- showcase/urls.py
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- StudentShowcaseRepository
- .test_password_change_success
- teams/permissions.py
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
- .update
- data/conftest.py
- timetable

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 530 edges
2. `User` - 255 edges
3. `ProjectApplication` - 151 edges
4. `Department` - 145 edges
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

## Communities (348 total, 113 thin omitted)

### Community 0 - "MentorTeamViewSet"
Cohesion: 0.18
Nodes (13): MentorTeamViewSet, Request, Response, DELETE /study-groups/{groupId}/teams/{teamSemesterId}/ — удалить команду., PATCH /study-groups/{groupId}/teams/{teamSemesterId}/captain/., POST /study-groups/{groupId}/teams/{teamSemesterId}/confirm-composition/., POST .../unconfirm-composition/ — вернуть состав на редактирование., POST /study-groups/{groupId}/teams/{teamSemesterId}/members/. (+5 more)

### Community 1 - "make_user"
Cohesion: 0.03
Nodes (24): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+16 more)

### Community 2 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 3 - "Ответственный по институту — API для фронта"
Cohesion: 0.08
Nodes (24): 1. Список активных групп института, 2. Сотрудники института, 3. Группы с назначенными наставниками, 4. Назначить наставника группе, 5. Снять наставника с группы, Значения `semester_id`, Общие query-параметры, Ответ `200` (+16 more)

### Community 4 - "ProjectTrackService"
Cohesion: 0.14
Nodes (5): ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), django_db, TestProjectTrackService

### Community 5 - "accounts/views.py"
Cohesion: 0.06
Nodes (41): AcademicYear, Meta, RegistrationRequest, Status, IsCpdsUser, IsInstituteValidator, ProjectManagementPermission, ProjectTrackPermission (+33 more)

### Community 6 - "APIClient"
Cohesion: 0.21
Nodes (9): Any, APIClient, django_db, parametrize, _team_url(), TestMentorTeamAccess, TestMentorTeamMutations, TestMentorTeamProjectEnrollmentBlock (+1 more)

### Community 7 - "project_track_service.py"
Cohesion: 0.04
Nodes (36): ProjectTrackAggregatedStatisticsDTO, ProjectTrackApplicationItemDTO, ProjectTrackCreateDTO, ProjectTrackGroupDetailDTO, ProjectTrackGroupItemDTO, ProjectTrackGroupListDTO, ProjectTrackGroupProjectDTO, ProjectTrackInstituteStatisticsDTO (+28 more)

### Community 8 - "application_import.py"
Cohesion: 0.19
Nodes (17): ApplicationImportRow, build_import_row(), is_data_row(), iter_application_import_rows(), normalize_cell(), parse_customer_type(), parse_institute_codes(), Any (+9 more)

### Community 9 - "TagRepository"
Cohesion: 0.04
Nodes (40): Repository слой для изоляции работы с базой данных. Этот слой содержит все…, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, TagRepository, django_db (+32 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.06
Nodes (28): ApplicationDashboardService, Оркестрация получения данных дашборда заявок., django_db, Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external., Фильтр по группам статусов., Карточка in_work = total - approved - rejected., Среднее и медиана времени до решения. (+20 more)

### Community 11 - "ApplicationDashboardRepository"
Cohesion: 0.08
Nodes (24): ApplicationDashboardRepository, QuerySet, Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению., Цвет столбца по порогам доли внешних заявок., Строит карту institute_code -> множество id заявок., ORM-запросы и агрегации для дашборда заявок., Строит карту department_id -> множество id заявок (как в DepartmentPlan). (+16 more)

### Community 12 - "test_mentor_groups_viewset.py"
Cohesion: 0.19
Nodes (11): api_client(), direction(), _enrollment_with_mentors(), APIClient, django_db, fixture, Тесты GET /api/teams/study-groups/my-groups/., semester() (+3 more)

### Community 13 - "import_study_groups_from_contingent.py"
Cohesion: 0.16
Nodes (12): GroupImportRow, Строка отчёта, подготовленная к импорту одной учебной группы., Command, BaseCommand, DataFrame, date, Path, Идемпотентный импорт учебных групп из отчёта контингента 1С (.xls/.xlsx). (+4 more)

### Community 14 - "TestApplicationNotificationService"
Cohesion: 0.32
Nodes (4): Email получателя: author_email заявки или email связанного пользователя-автора., django_db, patch, TestApplicationNotificationService

### Community 15 - "MentorTeamRepository"
Cohesion: 0.06
Nodes (17): MentorTeamRepository, Удаляет участника любой роли., Меняет статус состава., Удаляет семестровый контекст и постоянную команду при необходимости., Запросы и записи для API команд наставника., Пишет запись в лог команды., True, если пользователь уже в команде в семестре., Пользователь по id или None. (+9 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "MyStudyGroupDTO"
Cohesion: 0.13
Nodes (11): MyStudyGroupDTO, Any, DTO для эндпоинта «Моя группа»., Карточка наставника учебной группы., Возвращает наставников: из семестра или fallback на StudyGroup.mentor., Строка списка группы из контингента., Полные данные учебной группы для текущего студента., StudyGroupMemberDTO (+3 more)

### Community 18 - "ProjectTrack"
Cohesion: 0.11
Nodes (15): display, Количество групп в треке., Количество заявок в треке., ProjectTrack, Проектный трек — контейнер для назначения групп и заявок в рамках семестра., Лимиты размера команды. Приоритет: 1) трек команды; 2) effective по трекам…, Трек, доступный группе в семестре., Треки группы в семестре (recommended_teams_count уже на модели трека). (+7 more)

### Community 19 - "UserManagementService"
Cohesion: 0.08
Nodes (21): Правила доступа и валидации для управления пользователями., UserManagementDomain, ViewSet для управления пользователями., Просмотр пользователей — admin/cpds/institute_validator; запись — admin/cpds., UserManagementPermission, QuerySet, Доступ к данным пользователей для управления., Базовый queryset без администраторов. (+13 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (28): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationCreateSerializer, ProjectApplicationUpdateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы… (+20 more)

### Community 22 - "PreRegisteredStudentService"
Cohesion: 0.07
Nodes (29): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Отправляет администратору письмо о расхождении данных., Публичные операции предрегистрации студентов. (+21 more)

### Community 23 - "ApplicationDashboardDomain"
Cohesion: 0.08
Nodes (18): get_department_subtree_ids(), Возвращает id корневого подразделения и всех его потомков., ApplicationDashboardDomain, DashboardFilters, Доменная логика дашборда проектных заявок., Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп., Парсит query-параметр application_type. (+10 more)

### Community 24 - "StudyGroupViewSet"
Cohesion: 0.19
Nodes (10): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/my-groups/ — группы наставника в семестре., GET /api/teams/study-groups/{id}/mentor-detail/ — детали группы наставника., GET /api/teams/study-groups/{id}/project-showcase/ — витрина проектов группы., GET /api/teams/study-groups/ — список и просмотр учебных групп. (+2 more)

### Community 25 - "TestStudentShowcaseEnroll"
Cohesion: 0.22
Nodes (4): _create_assembled_team(), После заполнения последнего слота вторая команда получает 400., Один участник при min_team_members=2., TestStudentShowcaseEnroll

### Community 26 - "normalize_cell"
Cohesion: 0.13
Nodes (16): build_preregistered_student_import_row(), last_names_match(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки. (+8 more)

### Community 27 - "TeamLobby.py"
Cohesion: 0.08
Nodes (33): PageNumberPagination, ApproveJoinRequestSerializer, CreateInvitationSerializer, CreateTeamSerializer, MyTeamViewSet, action, extend_schema, extend_schema_view (+25 more)

### Community 28 - "TestTeamLobbyViewSet"
Cohesion: 0.14
Nodes (7): _create_captained_team(), django_db, Команда без трека при одном треке у группы → min/max с трека группы., После создания своей команды pending-заявка в чужую → obsolete., При нескольких треках track_id не проставляется; лимиты — effective по трекам., Если группе доступен один трек — он проставляется без track_id в body., TestTeamLobbyViewSet

### Community 29 - "UserListDTO"
Cohesion: 0.12
Nodes (16): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, API управления пользователями: список, деталь, частичное обновление. (+8 more)

### Community 30 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "MentorTeamService"
Cohesion: 0.12
Nodes (15): MentorGroupsDomain, Доменная логика доступа наставника к учебной группе., Проверяет, что пользователь назначен наставником группы в семестре., Проверки для API «Мои группы» наставника., MentorGroupsRepository, Репозиторий списка групп наставника в семестре., Выборка учебных групп, где пользователь назначен наставником., Возвращает True, если пользователь — наставник группы в семестре. (+7 more)

### Community 33 - "test_project_track_service.py"
Cohesion: 0.11
Nodes (16): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, Элемент добавления заявки в трек., DTO для добавления заявок в трек., Создаёт DTO из списка элементов API., Список id заявок для валидации и привязки., Карта id заявки → рекомендуемое число команд., Карта id заявки → минимум участников команды. (+8 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.13
Nodes (22): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+14 more)

### Community 35 - "TestTagViewSetCreate"
Cohesion: 0.12
Nodes (9): Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем., Нельзя создать общий тег, если имя уже используется (общим или departmental… (+1 more)

### Community 36 - "TestTagViewSet"
Cohesion: 0.06
Nodes (21): django_db, Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Тесты для обновления тегов через API., cpds может обновлять общие теги. (+13 more)

### Community 37 - "ProjectService"
Cohesion: 0.12
Nodes (9): ProjectService, Оркестрация Domain + Repository для списка проектов., _base_create_payload(), django_db, TestMyApplicationsNewFields, TestProjectApplicationNewFieldsCreateUpdate, TestProjectApplicationNewFieldsLists, django_db (+1 more)

### Community 38 - "ProjectApplicationService"
Cohesion: 0.03
Nodes (54): ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка., Бизнес-операция: получение заявок по статусу., Бизнес-операция: получение последних заявок. (+46 more)

### Community 39 - "StudentShowcaseDomain"
Cohesion: 0.11
Nodes (20): Доменная логика студенческой витрины проектов., Правила доступа и записи команды на проект витрины., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI). (+12 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.12
Nodes (17): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если студент прошёл полную регистрацию (не псевдо-user)., MonkeyPatch, Контингент группы с командой студента в семестре (без N+1)., api_client(), pre_registered_student(), Any (+9 more)

### Community 41 - "TeamLobbyService"
Cohesion: 0.11
Nodes (22): atomic, QuerySet, UserType, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент принимает приглашение., Оркестрация Domain + Repository для студенческого лобби., Студент отклоняет приглашение. (+14 more)

### Community 42 - ".calculate_initial_status"
Cohesion: 0.17
Nodes (9): Определение начального статуса на основе роли пользователя. Чистая функция -…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds., Обычный пользователь создаёт заявки в статусе await_department., Неизвестная роль возвращает статус await_department по умолчанию. (+1 more)

### Community 43 - "accounts/urls.py"
Cohesion: 0.12
Nodes (14): PasswordResetSerializer, LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView, APIView, extend_schema, Request (+6 more)

### Community 44 - "TestCommentService"
Cohesion: 0.10
Nodes (12): django_db, Пустой текст вызывает ValueError., Тесты для CommentService., Несуществующая заявка вызывает ValueError., Успешное получение комментариев к заявке., Успешное добавление комментария к заявке., Если комментариев нет, возвращается пустой список., Несуществующая заявка вызывает ValueError. (+4 more)

### Community 45 - "Path"
Cohesion: 0.15
Nodes (13): aga_institute(), direction(), Any, django_db, fixture, Path, Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта. (+5 more)

### Community 46 - "dto/institute_responsible.py"
Cohesion: 0.11
Nodes (12): InstituteResponsibleEmployeeDTO, InstituteResponsibleGroupDTO, InstituteResponsibleGroupMentorsDTO, InstituteResponsibleGroupWithMentorDTO, InstituteResponsibleMentorDTO, Any, DTO для API ответственного по институтам., Компактное представление учебной группы. (+4 more)

### Community 47 - "PermissionError"
Cohesion: 0.08
Nodes (24): PermissionError, ProjectTrackReadDTO, DTO для чтения проектного трека., atomic, QuerySet, UserType, Возвращает трек с проверкой доступа., Список треков по фильтрам. (+16 more)

### Community 48 - "prod_users_client.py"
Cohesion: 0.11
Nodes (23): Client, _http_client(), obtain_token(), Клиент prod API для обновления снимка пользователей., Возвращает базовый URL prod API., HTTP-клиент с поддержкой редиректов prod., Получает JWT access token по email и паролю., Возвращает Bearer token из CLI, env или login. (+15 more)

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+2 more)

### Community 50 - "TagViewSet"
Cohesion: 0.06
Nodes (32): Разрешает доступ к управлению тегами только для ролей cpds, admin и…, TagManagePermission, Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Инициализация из модели Tag., Преобразование в словарь., TagReadDTO (+24 more)

### Community 51 - "teams/views.py"
Cohesion: 0.12
Nodes (20): Meta, Краткое представление пользователя в составе команды., Сериализатор постоянной команды., Сериализатор участника команды в семестре., Сериализатор участия команды в семестре., TeamMemberUserSerializer, TeamSemesterMemberSerializer, TeamSemesterSerializer (+12 more)

### Community 52 - "DirectionService"
Cohesion: 0.17
Nodes (9): DirectionService, Оркестрация Domain + Repository для Direction., Список направлений с фильтрацией по роли., Направление по коду с проверкой доступа., directions(), django_db, fixture, Тесты DirectionService. (+1 more)

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
Cohesion: 0.05
Nodes (22): Exception, django_db, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None., target_institutes сериализуется как список словарей с code и name., tags сериализуется как список словарей с id, name и category. (+14 more)

### Community 58 - "APIView"
Cohesion: 0.10
Nodes (16): IsAdminOrCpds, APIView, Request, Проверяет наличие прав у пользователя., Проверяет наличие прав у пользователя., Проверяет наличие прав у пользователя., Проверяет права на чтение или запись пользователей., Проверяет наличие прав у пользователя. Args: request: текущий запрос view:… (+8 more)

### Community 59 - "TestSubmitApplicationService"
Cohesion: 0.08
Nodes (13): django_db, Если needs_consultation не передан, значение остается False по умолчанию., При создании упрощенной заявки устанавливается is_external=True и статус…, При создании упрощенной заявки добавляется причастное подразделение ЦПДС., При создании обычной заявки is_external=False по умолчанию., Заявка автоматически переходит в await_institute, если в подразделении нет…, Заявка остаётся в await_department, если в подразделении есть…, Успешная подача заявки: создаётся со статусом created, затем переводится в… (+5 more)

### Community 60 - "TeamLobbyDomain"
Cohesion: 0.09
Nodes (12): Проверяет роль student и наличие учебной группы; возвращает group_id., Проверяет, что пользователь — капитан команды., Удаление: капитан, forming, в составе только он., Приглашение должно быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды»., Проверяет роль student и наличие учебной группы; возвращает group_id., True, если студент без команды и есть свободный слот., Запрещает изменения состава при подтверждённом составе. (+4 more)

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.08
Nodes (15): ProjectTrackDomain, Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя., Проверяет, может ли пользователь управлять проектными треками., Коды институтов пользователя; None — без ограничения (admin/cpds). (+7 more)

### Community 62 - "._resolve_context"
Cohesion: 0.11
Nodes (12): InstituteResponsibleAssignMentorDTO, Ответ после изменения состава наставников., Any, Список активных групп института., Список сотрудников института., Группы с ID назначенных наставников в семестре., Назначает наставника группе в семестре., Снимает наставника с группы в семестре. (+4 more)

### Community 63 - "showcase/admin.py"
Cohesion: 0.08
Nodes (25): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+17 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "TeamSemester"
Cohesion: 0.04
Nodes (32): Заявка должна быть в статусе pending., Участие команды в конкретном семестре: проект, наставник, капитан., Заявка студента на вступление в команду в семестре., Приглашение капитана студенту вступить в команду., Status, TeamInvitation, TeamJoinRequest, TeamSemester (+24 more)

### Community 66 - "team_lobby_service.py"
Cohesion: 0.07
Nodes (22): Подтверждение состава: капитан, forming, размер в лимитах трека., LobbyInvitationDTO, LobbyJoinRequestDTO, LobbyReadDTO, LobbyTeamItemDTO, LobbyTrackDTO, MyTeamEventLogDTO, MyTeamInvitationDTO (+14 more)

### Community 67 - ".approve_application"
Cohesion: 0.08
Nodes (18): atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку., Бизнес-операция: отзыв заявки автором., Бизнес-операция: одобрение заявки. (+10 more)

### Community 68 - "TestUserManagementDomain"
Cohesion: 0.14
Nodes (7): Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., Role, django_db, TestUserManagementDomain

### Community 69 - "accounts/admin.py"
Cohesion: 0.33
Nodes (9): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin, UserAdmin (+1 more)

### Community 70 - "PreRegisteredStudentRepository"
Cohesion: 0.07
Nodes (19): PreRegisteredStudentRepository, QuerySet, Репозиторий предрегистрации студентов., Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по табельному номеру., Возвращает предрегистрацию по нормализованному СНИЛС., Возвращает предрегистрацию по первичному ключу. (+11 more)

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
Cohesion: 0.09
Nodes (12): ProjectTrackRepository, Возвращает id групп, уже привязанных к треку., Добавляет группы в трек; возвращает число созданных связей., Удаляет группу из трека; True если связь была., Добавляет заявки в трек; возвращает число созданных связей., Удаляет заявку из трека; True если связь была., Количество групп в треке., Доступ к данным проектных треков. (+4 more)

### Community 75 - ".view_application"
Cohesion: 0.09
Nodes (12): Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации., Бизнес-операция: получение заявок для координации пользователя. Для обычных… (+4 more)

### Community 76 - "._authorize_and_load"
Cohesion: 0.14
Nodes (14): Any, atomic, Обновляет название команды., Назначает нового капитана из состава команды., Подтверждает состав команды (forming → assembled)., Возвращает состав на редактирование (assembled → forming)., Добавляет зарегистрированного или незарегистрированного студента., Возвращает пользователя для добавления в команду. (+6 more)

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 79 - "TagSerializer"
Cohesion: 0.67
Nodes (3): Meta, Сериализатор для тегов., TagSerializer

### Community 80 - "Витрина проектов (студент) — API для фронта"
Cohesion: 0.14
Nodes (13): 1. Список треков с проектами, 2. Детали проекта, 3. Записать команду на проект, Витрина проектов (студент) — API для фронта, Ответ `200`, Ответ `200`, Ответ `200`, Ошибки (+5 more)

### Community 81 - "MentorTeamDomain"
Cohesion: 0.10
Nodes (11): MentorTeamDomain, Чистая бизнес-логика API команд наставника., Проверяет, что команда принадлежит учебной группе., Проверяет возможность подтверждения состава., Проверяет возможность разутверждения состава., Удаление возможно только при пустом составе., Новый капитан должен быть участником команды., Нельзя удалить текущего капитана без смены капитана. (+3 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.11
Nodes (10): AccountsApiTests, override_settings, Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Создание заявки без подразделения возвращает ошибку валидации., Создание заявки с несуществующим подразделением возвращает ошибку валидации., После отклонения заявки можно подать новую с тем же email., Повторная подача при активной заявке возвращает ошибку валидации., Нельзя подать заявку, если пользователь с таким email уже зарегистрирован. (+2 more)

### Community 84 - "TestCanDeleteTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, django_db, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения. (+3 more)

### Community 85 - "build_user_indexes"
Cohesion: 0.10
Nodes (29): main(), Сверка преподавателей из Excel со списком пользователей prod API. ..…, Отмечает преподавателей из Excel, которые есть в prod., build_user_indexes(), find_user(), normalize_name(), Сопоставление ФИО преподавателей с пользователями PD., Нормализует ФИО для сравнения. (+21 more)

### Community 86 - "test_mentor_team_viewset.py"
Cohesion: 0.20
Nodes (14): MentorTeamDetailDTO, Any, Карточка команды для ответов мутаций наставника., api_client(), _approved_app(), direction(), _enrollment_with_mentors(), mentor_team_setup() (+6 more)

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "Управление командой"
Cohesion: 0.08
Nodes (24): Query-параметры, Query-параметры, Query-параметры, Вернуть состав на редактирование, Витрина проектов, Детали группы наставника, Добавить участника, Карточка команды (+16 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.04
Nodes (37): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы. (+29 more)

### Community 90 - "test_import_preregistered_students.py"
Cohesion: 0.19
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 91 - ".resolve_list_semester_id"
Cohesion: 0.15
Nodes (8): Разбор query-параметра semester_id для GET-списков: id, next, actual., Any, Список групп наставника с количеством студентов и команд., Детали группы: студенты контингента и команды в семестре., Any, Список треков с проектами для группы наставника в семестре., django_db, TestSemesterResolveListSemesterId

### Community 92 - "InstituteResponsibleDomain"
Cohesion: 0.11
Nodes (9): Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., InstituteResponsibleDomain, Правила доступа и валидации для ответственного по институтам., Проверяет, может ли пользователь работать с API ответственного., Определяет код института из параметра или по умолчанию., ID подразделений института для фильтрации сотрудников., Проверяет доступ к учебной группе. (+1 more)

### Community 93 - "test_mentor_group_detail_viewset.py"
Cohesion: 0.23
Nodes (12): api_client(), _detail_url(), direction(), _enrollment_with_mentors(), APIClient, django_db, fixture, Тесты GET /api/teams/study-groups/{id}/mentor-detail/. (+4 more)

### Community 94 - "TestCoordinationAndDtosService"
Cohesion: 0.11
Nodes (9): Валидатор получает объединённый список: его причастность пользователя +…, cpds видит все заявки в статусе await_cpds даже без причастности., Преобразователи к DTO возвращают ожидаемые экземпляры., get_external_applications возвращает только заявки с is_external=True., get_external_applications позволяет фильтровать внешние заявки по коду статуса., get_external_applications с несуществующим статусом выбрасывает ValueError., get_external_applications_queryset возвращает QuerySet внешних заявок., get_external_applications требует авторизации. (+1 more)

### Community 95 - "extract.py"
Cohesion: 0.22
Nodes (16): main(), run(), export_marked_xlsx(), export_to_xlsx(), _group_columns(), Any, Экспортирует результаты парсинга с колонками сверки с PD., _collect_events() (+8 more)

### Community 96 - "User"
Cohesion: 0.05
Nodes (31): AbstractBaseUser, QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., User, Возвращает пользователя по ID., Сохраняет изменения пользователя., PasswordChangeSerializer, PasswordResetConfirmSerializer (+23 more)

### Community 97 - "InstituteResponsibleService"
Cohesion: 0.15
Nodes (20): delete, AssignMentorSerializer, InstituteResponsiblePermission, InstituteResponsibleViewSet, action, BasePermission, extend_schema, Request (+12 more)

### Community 98 - "teams/admin.py"
Cohesion: 0.14
Nodes (16): DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin, TeamSemesterAdmin (+8 more)

### Community 99 - "TestProjectApplicationViewSetTransferToInstitute"
Cohesion: 0.17
Nodes (8): Тесты для действия передачи заявки в институт по коду института., POST /api/showcase/project-applications/{id}/transfer_to_institute/ с…, Отсутствующий параметр code возвращает 400., Несуществующий код института возвращает 400 от сервиса., Институт без связанного подразделения возвращает 400., GET /api/showcase/project-applications/external/?status=... фильтрует внешние…, GET /api/showcase/project-applications/external/?status=... с несуществующим…, TestProjectApplicationViewSetTransferToInstitute

### Community 100 - "refresh_prod_users_json"
Cohesion: 0.20
Nodes (11): fetch_users(), Any, Path, Загружает список пользователей с prod API., Обновляет JSON-снимок пользователей prod., refresh_prod_users_json(), Path, Загружает список пользователей с API. (+3 more)

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - "Department"
Cohesion: 0.03
Nodes (92): Command, BaseCommand, Department, Semester, create_test_user(), Создаем тестового пользователя, DTO для списка проектов., ViewSet для работы с планами подразделений по проектным заявкам. (+84 more)

### Community 103 - "Общая информация"
Cohesion: 0.50
Nodes (4): Аутентификация, Базовый URL, Общая информация, Форматы данных

### Community 104 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

### Community 105 - "Role"
Cohesion: 0.14
Nodes (8): Command, BaseCommand, Role, UserManager, BaseUserManager, Command, BaseCommand, Тесты UserManagementDomain.

### Community 106 - ".get_dashboard"
Cohesion: 0.17
Nodes (9): ApplicationDashboardDTO, Any, DTO для дашборда проектных заявок., Преобразует DTO в словарь для API., DTO блока KPI-карточек., DTO полного ответа дашборда., Преобразует DTO в словарь для API., SummaryCardsDTO (+1 more)

### Community 107 - "Direction"
Cohesion: 0.16
Nodes (10): DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DirectionSerializer, Meta, Сериализатор направления подготовки., Direction (+2 more)

### Community 108 - "StudyGroup.py"
Cohesion: 0.19
Nodes (10): Any, DTO для учебных групп., DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, Компактная выдача для списка учебных групп. (+2 more)

### Community 109 - "TestProjectApplicationListSemesterFilter"
Cohesion: 0.09
Nodes (14): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Фильтр ?semester_id= в GET-списке заявок., Автоподстановка семестра при создании заявки., Тесты для проверки наличия поля is_external в ответах API., POST /api/showcase/project-applications/ возвращает is_external в ответе. (+6 more)

### Community 110 - "StudentShowcaseViewSet"
Cohesion: 0.23
Nodes (10): action, extend_schema, extend_schema_view, Request, Response, Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/., GET /api/showcase/student-showcase/projects/{id}/. (+2 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - "StudyGroup"
Cohesion: 0.09
Nodes (20): Проверяет, что учебная группа существует., Проверяет, что учебная группа не завершила обучение., StudyGroup, QuerySet, Группы наставника в семестре со счётчиками студентов и команд., Возвращает заголовок группы (id, name) или None., QuerySet, Репозиторий для учебных групп. (+12 more)

### Community 113 - "ApplicationLoggingService"
Cohesion: 0.03
Nodes (58): find_existing_imported_application(), parse_author_name(), Ищет уже импортированную заявку по автору, названию и заказчику., Разбирает строку вида «Фамилия Имя» на фамилию и имя., Command, BaseCommand, Импорт проектных заявок из Excel-файла., Формирует контактные поля автора для DTO из пользователя системы. (+50 more)

### Community 114 - "get_root_department"
Cohesion: 0.12
Nodes (15): get_root_department(), is_cpds_department(), Утилиты для работы с подразделениями., Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, django_db, Unit-тесты для утилит работы с подразделениями., Тесты для функции get_root_department. (+7 more)

### Community 115 - "direction_service.py"
Cohesion: 0.19
Nodes (8): DirectionDomain, Доменная логика для направлений подготовки., Фильтрация направлений по роли пользователя., DirectionRepository, Репозиторий для направлений подготовки., Направление по коду (PK)., Доступ к данным Direction., Сервис для операций с направлениями подготовки.

### Community 116 - ".get_filtered_queryset"
Cohesion: 0.23
Nodes (5): QuerySet, Фильтрует направления: institute_validator — только из групп своего института., parametrize, Фильтрация queryset направлений по ролям., TestGetFilteredQueryset

### Community 117 - "institute_access.py"
Cohesion: 0.09
Nodes (28): Доменная логика управления пользователями., ID подразделений для фильтрации; None — без ограничения., Доменная логика для списка проектов., Доменная логика для проектных треков., application_available_for_institute(), application_belongs_to_institutes(), get_accessible_institute_codes(), get_department_ids_by_institute_code() (+20 more)

### Community 118 - "StudentShowcaseService"
Cohesion: 0.11
Nodes (16): Результат записи команды на проект., StudentShowcaseEnrollResultDTO, ViewSet студенческой витрины проектов., atomic, UserType, Сервис студенческой витрины проектов., Записывает команду капитана на проект., Оркестрация Domain + Repository для студенческой витрины. (+8 more)

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → effective max(min)/min(max)., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "sync_project_teachers.py"
Cohesion: 0.15
Nodes (14): load_project_env(), Загружает переменные из .env в корне проекта., main(), parse_all_groups(), _print_parse_summary(), Path, Парсинг расписания РУТ и сверка преподавателей с пользователями prod PD., Парсит преподавателей «Проектная деятельность» по всем группам. (+6 more)

### Community 121 - ".get_filtered_queryset"
Cohesion: 0.20
Nodes (6): Q, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Доли заявок по группам статусов (согласовано / в работе / отклонено)., Доли внутренних/внешних заявок по полю is_internal_customer., Q-фильтр: заявка доступна институту.

### Community 122 - "django_db"
Cohesion: 0.15
Nodes (5): django_db, Число SQL не растёт пропорционально числу проектов., TestStudentShowcaseAccess, TestStudentShowcaseDetail, TestStudentShowcaseList

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

### Community 132 - "ProjectApplicationCreateDTO"
Cohesion: 0.03
Nodes (79): create_test_applications(), Создаем тестовые заявки, Общие константы приложения showcase., ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,… (+71 more)

### Community 133 - "0014_add_intermediate_approved_statuses.py"
Cohesion: 0.33
Nodes (5): add_intermediate_approved_statuses(), Migration, Удаляет промежуточные статусы одобрения из БД., Добавляет промежуточные статусы одобрения в БД., remove_intermediate_approved_statuses()

### Community 134 - "TestDepartmentPlanViewSetMyDepartmentPlan"
Cohesion: 0.13
Nodes (9): django_db, Тесты для GET /api/showcase/department-plans/my-department-plan/ - план…, Успешное получение плана и статистики для подразделения пользователя., Если план отсутствует, возвращается 0, но статистика заявок учитывается., Ошибка: отсутствует semester_id., Ошибка: семестр не найден., Ошибка: у пользователя не указано подразделение., Ошибка: неавторизованный пользователь. (+1 more)

### Community 135 - "StudyGroupService"
Cohesion: 0.11
Nodes (14): Доменная логика для учебных групп., Фильтрация учебных групп по роли пользователя., StudyGroupDomain, Сервис для операций с учебными группами., Оркестрация Domain + Repository для StudyGroup., StudyGroupService, django_db, TestMyStudyGroupService (+6 more)

### Community 136 - "Руководство по ручному развертыванию Project Activity Server"
Cohesion: 0.15
Nodes (12): 10. Проверка и сопровождение, 11. Настройка nginx (backend + SPA), 1. Подготовка окружения, 2. Получение исходного кода, 3. Создание и активация виртуального окружения, 4. Настройка переменных окружения (.env), 5. Настройка PostgreSQL, 6. Миграции и статические файлы (+4 more)

### Community 137 - "4. Список проектов"
Cohesion: 0.15
Nodes (13): 2. Получение пользователя, 4. Список проектов, Query-параметры, Заголовки, Ошибки, Ошибки, Поведение по ролям, Права доступа (+5 more)

### Community 138 - "ProjectApplicationViewSet"
Cohesion: 0.05
Nodes (33): format_validation_errors(), get_error_message(), ProjectApplicationViewSet, action, extend_schema, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, GET /api/project-applications/external/ Получение списка всех внешних заявок… (+25 more)

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
Cohesion: 0.17
Nodes (16): api_client(), _approved_app(), _create_assembled_team(), direction(), _enrollment_with_mentors(), mentor_showcase_setup(), APIClient, django_db (+8 more)

### Community 147 - "schema.py"
Cohesion: 0.50
Nodes (3): exclude_auth_api_duplicate(), Хуки и расширения для drf-spectacular., Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*). В…

### Community 149 - "Any"
Cohesion: 0.18
Nodes (7): Any, Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Трек с вложенными проектами для витрины., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., StudentShowcaseTrackDTO

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

### Community 159 - "test_student_showcase_viewset.py"
Cohesion: 0.31
Nodes (10): api_client(), _approved_app(), direction(), other_group(), fixture, Тесты API студенческой витрины проектов., semester(), showcase_setup() (+2 more)

### Community 164 - "TestTagViewSetDelete"
Cohesion: 0.20
Nodes (6): Тесты для удаления тегов через API., cpds может удалять общие теги., cpds не может удалять теги с подразделением., admin может удалять любые теги., Остальные роли не могут удалять теги., TestTagViewSetDelete

### Community 165 - "test_study_group_domain.py"
Cohesion: 0.12
Nodes (13): QuerySet, institute_validator — только группы своих институтов., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., direction(), other_institute(), django_db, fixture (+5 more)

### Community 166 - "test_direction_domain.py"
Cohesion: 0.20
Nodes (9): directions(), other_institute(), django_db, fixture, Тесты доменной логики DirectionDomain., Три направления для сценариев фильтрации., Разрешение институтов по подразделению пользователя., Второй институт на другом подразделении. (+1 more)

### Community 170 - "test_team_lobby_viewset.py"
Cohesion: 0.33
Nodes (9): api_client(), _approved_app(), direction(), lobby_setup(), fixture, Тесты API лобби формирования команд., semester(), study_group() (+1 more)

### Community 189 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 190 - "QuerySet"
Cohesion: 0.18
Nodes (6): QuerySet, Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки.

### Community 191 - "Command"
Cohesion: 0.20
Nodes (5): Command, BaseCommand, Path, Идемпотентный импорт строк модели Settings из CSV., Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 192 - "fixture"
Cohesion: 0.22
Nodes (9): institute(), fixture, Возвращает класс модели пользователя для удобства., Создаёт набор ролей, используемых в тестах. Возвращает dict: code -> Role, Создаёт все необходимые статусы для сценариев сервисов., Создаёт институт, связанный с родительским подразделением., roles(), statuses() (+1 more)

### Community 193 - "Settings"
Cohesion: 0.29
Nodes (5): display, SettingsAdmin, Ключ–значение настроек приложения (редактируемые из админки / импортом)., Settings, Тесты разбора semester_id для GET-списков.

### Community 195 - "ProjectApplication"
Cohesion: 0.04
Nodes (37): Репозиторий для управления пользователями., ProjectListDTO, Any, DTO для списка проектов., Возвращает причастное подразделение верхнего уровня (без родителя). ЦПДС…, DTO студенческой витрины проектов., Карточка проекта в списке трека витрины., Детали проекта для студента (без контактов). (+29 more)

### Community 198 - "Command"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Сбрасывает счетчик ID для таблицы тегов.

### Community 199 - "MentorGroupDetailDTO"
Cohesion: 0.11
Nodes (11): MentorGroupDetailDTO, MentorGroupListDTO, MentorGroupListItemDTO, MentorGroupStudentDTO, MentorGroupTeamDTO, Any, Строка списка групп наставника., Список групп наставника. (+3 more)

### Community 200 - "TagService"
Cohesion: 0.03
Nodes (69): get_or_create_institute_tag(), Возвращает тег направления и флаг, был ли тег создан. Сначала ищет общий…, Доменная логика для тегов - чистые функции без эффектов., Чистая бизнес-логика для тегов - только функции, никаких эффектов., Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, TagDomain, DTO для работы с тегами. (+61 more)

### Community 201 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 202 - "teams/models.py"
Cohesion: 0.08
Nodes (21): Репозиторий студенческой витрины проектов (без N+1)., Доменные правила лобби формирования команд., ФИО пользователя для лога., DTO для эндпоинта «Мои группы» наставника., MentorTeamMemberDTO, DTO карточки команды для API наставника., Участник команды в карточке наставника., Meta (+13 more)

### Community 203 - "ApplicationDashboard.py"
Cohesion: 0.20
Nodes (7): ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 206 - "API Документация - Проектные заявки"
Cohesion: 0.14
Nodes (12): 1. Создание заявки (авторизованные пользователи), API Документация - Проектные заявки, Заголовки, Пример запроса, ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации (+4 more)

### Community 240 - "TestSemesterAssignViewSet"
Cohesion: 0.29
Nodes (3): Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, TestSemesterAssignViewSet

### Community 242 - "ProjectTrackProjectDetailDTO"
Cohesion: 0.17
Nodes (7): ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, DTO группы в деталях проекта., Преобразует DTO в словарь для API., DTO деталей проекта с назначенными группами., Преобразует DTO в словарь для API., Детали проекта с назначенными группами.

### Community 245 - "ProjectViewSet"
Cohesion: 0.25
Nodes (5): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией.

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 277 - "DirectionViewSet"
Cohesion: 0.43
Nodes (4): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений.

### Community 278 - "test_team_semester_viewset.py"
Cohesion: 0.43
Nodes (6): api_client(), direction(), fixture, Тесты API TeamSemester., semester(), study_group()

### Community 279 - "ProjectTrack.py"
Cohesion: 0.07
Nodes (21): ProjectTrackUpdateDTO, DTO для обновления проектного трека., Создаёт DTO из словаря., Возвращает только переданные поля трека для обновления., True, если переданы лимиты размера команды для заявок трека., ProjectTrackAddApplicationItemSerializer, ProjectTrackAddApplicationsSerializer, ProjectTrackAddGroupsSerializer (+13 more)

### Community 280 - "ProjectApplicationRepository"
Cohesion: 0.02
Nodes (59): ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты…, Получение заявки по ID без дополнительных связанных объектов. Для простых…, Получение заявок пользователя, где он является автором. Оптимизированный запрос…, Получение заявок для координации пользователя. Заявки, где пользователь…, Репозиторий - вся работа с БД здесь, Получение заявок для координации по причастному подразделению. Заявки, где…, Получение заявок по статусу. Для административных операций. (+51 more)

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 289 - "Парсинг «Проектная деятельность» — РУТ (МИИТ)"
Cohesion: 0.40
Nodes (4): Источник данных, Парсинг «Проектная деятельность» — РУТ (МИИТ), Полный пайплайн (парсинг + сверка с PD), Только парсинг (без сверки)

### Community 292 - "Command"
Cohesion: 0.12
Nodes (7): Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Следующий семестр для новых заявок (Settings.next_semester_code)., Command, BaseCommand, Добавляет причастные подразделения института к заявке., Создание заявки в БД. Принимает DTO и пользователя, возвращает созданную…

### Community 293 - "ProjectDomain"
Cohesion: 0.33
Nodes (4): ProjectDomain, Проверяет, может ли пользователь получать список проектов., Коды институтов для фильтрации; None — без ограничения., Правила доступа и фильтрации для списка проектов.

### Community 294 - "test_institute_responsible_viewset.py"
Cohesion: 0.07
Nodes (26): Наставники учебной группы в конкретном семестре., StudyGroupSemester, QuerySet, Репозиторий для StudyGroupSemester и связанных выборок., Снимает наставника с группы в семестре; возвращает актуальные mentorIds., Возвращает отсортированные ID наставников группы в семестре., Доступ к данным групп в семестре и сотрудников института., Активные группы института. (+18 more)

### Community 295 - "test_link_institutes_by_name_simple"
Cohesion: 0.40
Nodes (6): Any, django_db, Простейший сценарий: для каждого института есть одноимённое подразделение., Институты без одноимённого подразделения остаются без связанного подразделения., test_link_institutes_by_name_simple(), test_link_institutes_without_matching_department()

### Community 296 - "ProjectTrackAddGroupsDTO"
Cohesion: 0.40
Nodes (3): ProjectTrackAddGroupsDTO, DTO для добавления групп в трек., Создаёт DTO из словаря.

### Community 297 - "ProjectRepository"
Cohesion: 0.29
Nodes (5): ProjectRepository, QuerySet, Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

### Community 299 - "Валидационные правила"
Cohesion: 0.50
Nodes (4): Валидационные правила, Обязательные поля, Обязательные поля:, Типы данных

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
Cohesion: 0.33
Nodes (6): 3. Изменение пользователя, Заголовки, Ошибки, Примеры запросов, Тело запроса, Успешный ответ (200)

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

### Community 320 - "MentorTeam.py"
Cohesion: 0.13
Nodes (12): Доменные правила управления командой наставником., Запрещает изменения, если команда записана на проект., Команда записана на проект — мутации запрещены., TeamEnrolledInProjectError, MentorTeamAddMemberSerializer, MentorTeamSetCaptainSerializer, MentorTeamUpdateNameSerializer, ViewSet управления командой учебной группы для наставника. (+4 more)

### Community 324 - "showcase/urls.py"
Cohesion: 0.13
Nodes (13): ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…, InstituteSerializer (+5 more)

### Community 329 - "StudentShowcaseRepository"
Cohesion: 0.10
Nodes (11): Команда пользователя в семестре с блокировкой строки., Запросы и запись для студенческой витрины проектов., Команда пользователя в семестре (без блокировки)., Связь проект↔трек с проверкой семестра и статуса approved., Треки группы в семестре с одобренными проектами и тегами., Счётчик записанных команд с блокировкой строк TeamSemester проекта., Привязывает проект к команде и пишет лог., Карта (track_id, application_id) → число записанных команд. (+3 more)

### Community 331 - "teams/permissions.py"
Cohesion: 0.21
Nodes (11): _is_staff_or_admin(), APIView, BasePermission, Request, Разрешения для приложения teams., Доступ только студенту с привязанной учебной группой., Чтение — любой аутентифицированный пользователь. Изменение постоянной команды —…, Изменение семестрового контекста — капитан, admin или cpds. (+3 more)

## Knowledge Gaps
- **267 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+262 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **113 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `TestCanCreateTag`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `ProjectTrackService`, `project_track_service.py`, `StudyGroupService`, `ApplicationDashboardService`, `MyStudyGroupDTO`, `UserManagementService`, `ApplicationDashboardDomain`, `ProjectApplicationRepository`, `UserListDTO`, `Command`, `ProjectDomain`, `ProjectApplicationService`, `StudentShowcaseDomain`, `test_study_group_domain.py`, `test_institute_responsible_viewset.py`, `TeamLobbyService`, `accounts/urls.py`, `dto/institute_responsible.py`, `PermissionError`, `TestCanUpdateTag`, `TagViewSet`, `DirectionService`, `APIView`, `TeamLobbyDomain`, `ProjectTrackDomain`, `._resolve_context`, `showcase/admin.py`, `team_lobby_service.py`, `.approve_application`, `TestUserManagementDomain`, `accounts/admin.py`, `PreRegisteredStudentRepository`, `ProjectApplication`, `TagService`, `DepartmentPlanViewSet`, `.get_filtered_queryset`, `.view_application`, `teams/models.py`, `MentorGroupDetailDTO`, `teams/permissions.py`, `._authorize_and_load`, `TestCanDeleteTag`, `test_mentor_team_viewset.py`, `ApplicationCapabilities`, `.resolve_list_semester_id`, `InstituteResponsibleDomain`, `Department`, `.get_dashboard`, `ApplicationLoggingService`, `ProjectTrackProjectDetailDTO`, `direction_service.py`, `.get_filtered_queryset`, `institute_access.py`, `StudentShowcaseService`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `Semester` connect `Department` to `make_user`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `ProjectTrackService`, `project_track_service.py`, `StudyGroupService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `ProjectApplicationViewSet`, `ApplicationDashboardService`, `test_mentor_groups_viewset.py`, `APIClient`, `test_mentor_showcase_viewset.py`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `ProjectTrack`, `test_team_semester_viewset.py`, `ApplicationDashboardDomain`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `MentorTeamService`, `test_project_track_service.py`, `Command`, `ProjectService`, `ProjectApplicationService`, `test_institute_responsible_viewset.py`, `TeamLobbyService`, `test_team_lobby_viewset.py`, `teams/views.py`, `TestDepartmentPlanViewSetList`, `test_import_study_groups_from_contingent.py`, `TestProjectViewSet`, `APIView`, `Command`, `Settings`, `team_lobby_service.py`, `accounts/admin.py`, `DepartmentPlanViewSet`, `teams/models.py`, `AccountsApiTests`, `test_mentor_team_viewset.py`, `.resolve_list_semester_id`, `test_mentor_group_detail_viewset.py`, `InstituteResponsibleService`, `TestProjectApplicationListSemesterFilter`, `TestSemesterAssignViewSet`, `ApplicationLoggingService`, `StudyGroup`, `institute_access.py`, `StudentShowcaseService`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `TestCanCreateTag`, `ProjectApplicationCreateDTO`, `ProjectTrackService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `APIClient`, `StudyGroupService`, `ApplicationDashboardService`, `test_mentor_groups_viewset.py`, `TestApplicationNotificationService`, `test_mentor_showcase_viewset.py`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `ProjectTrack`, `ProjectApplicationRepository`, `TestStudentShowcaseEnroll`, `student_user`, `TestProjectApplicationViewSetIsInternalCustomer`, `test_student_showcase_viewset.py`, `test_project_track_service.py`, `TestTagViewSetCreate`, `TestTagViewSet`, `ProjectService`, `TestTagViewSetDelete`, `ProjectApplicationService`, `PreRegisteredStudent`, `test_direction_domain.py`, `test_institute_responsible_viewset.py`, `test_study_group_domain.py`, `TestCommentService`, `test_team_lobby_viewset.py`, `TestCanUpdateTag`, `DirectionService`, `TestDepartmentPlanViewSetList`, `TestProjectViewSet`, `TestProjectApplicationReadDTO`, `TestSubmitApplicationService`, `ProjectTrackDomain`, `fixture`, `TestUserManagementDomain`, `.get_filtered_queryset`, `TagService`, `TestApplicationDashboardViewSet`, `TestCanDeleteTag`, `test_mentor_team_viewset.py`, `test_import_preregistered_students.py`, `test_mentor_group_detail_viewset.py`, `TestCoordinationAndDtosService`, `TestProjectApplicationViewSetTransferToInstitute`, `Department`, `TestProjectApplicationListSemesterFilter`, `TestSemesterAssignViewSet`, `ApplicationLoggingService`, `StudyGroup`, `.get_filtered_queryset`, `django_db`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Are the 527 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 527 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 76 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 76 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._