# Graph Report - project_activity_server  (2026-08-31)

## Corpus Check
- 346 files · ~161,058 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5218 nodes · 10548 edges · 365 communities (251 shown, 114 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1035 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `62650a91`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ._handle_errors
- make_user
- TestCanCreateTag
- Ответственный по институту — API для фронта
- ProjectTrackService
- accounts/views.py
- ApplicationDashboardService
- Any
- application_import.py
- TagRepository
- TestApplicationDashboardService
- ProjectApplication
- test_mentor_groups_viewset.py
- ._collect_group_rows
- ApplicationNotificationService
- APIClient
- prepare_study_groups_xlsx.py
- StudyGroupMemberDTO
- TagCreateDTO
- UserManagementService
- TestDepartmentPlanViewSetCreate
- TestDepartmentPlanViewSetList
- PreRegisteredStudentService
- PermissionError
- StudyGroupViewSet
- test_student_showcase_viewset.py
- normalize_cell
- Request
- TestTeamLobbyViewSet
- UserManagementViewSet
- TestProjectApplicationViewSetIsInternalCustomer
- AvailableActionDTO
- MentorGroupsDomain
- ProjectTrack
- ProjectTrackViewSet
- ._get_track_with_access
- TestTagViewSetCreate
- MentorTeamDomain
- ProjectApplicationService
- StudentShowcaseDomain
- PreRegisteredStudent
- Tag
- .calculate_initial_status
- .post
- test_institute_responsible_viewset.py
- Institute
- TestProjectApplicationCreateDTO
- TeamLobbyService
- prod_users_client.py
- TestCanUpdateTag
- Tag.py
- teams/views.py
- DirectionService
- TestTagViewSet
- test_import_study_groups_from_contingent.py
- UserType
- ValidationResult
- showcase/models.py
- APIView
- ProjectApplicationCreateDTO
- UserSerializer
- ProjectTrackDomain
- InstituteResponsibleGroupDTO
- showcase/admin.py
- Примеры использования поля is_internal_customer
- TeamLobbyRepository
- TeamLobbyDomain
- .approve_application
- UserManagementDomain
- Semester
- tests/conftest.py
- .can_user_access_application
- .get_filtered_queryset
- DepartmentPlanViewSet
- ProjectTrackRepository
- .view_application
- MentorTeamService
- TestApplicationDashboardViewSet
- .can_change_status
- accounts/permissions.py
- Витрина проектов (студент) — API для фронта
- MentorTeamRepository
- API для работы с проектными заявками
- AccountsApiTests
- TestCanDeleteTag
- build_user_indexes
- .handle
- Command
- Управление командой
- ApplicationCapabilities
- test_import_preregistered_students.py
- MentorTeamViewSet
- serialize_comment_author
- StudyGroup
- MentorGroupsRepository
- extract.py
- InstituteResponsibleService
- InstituteResponsibleViewSet
- teams/admin.py
- TestProjectApplicationViewSetTransferToInstitute
- refresh_prod_users_json
- extract_group_abbrev.py
- .can_edit_application
- API Документация - Проектные заявки
- Command
- .update_application
- Direction
- Direction.py
- StudyGroup.py
- test_project_application_viewset.py
- StudentShowcaseViewSet
- _generate_collection.py
- test_my_study_group_viewset.py
- ApplicationLoggingService
- ProjectListDTO
- TeamLobbyViewSet
- .get_filtered_queryset
- institute_access.py
- StudentShowcaseService
- test_my_team_viewset.py
- sync_project_teachers.py
- ProjectService
- .resolve_list_semester_id
- Поддержка multipart/form-data
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- User
- Command
- Command
- TestInstituteViewSet
- update_prod.sh
- Command
- TestProjectViewSet
- 0014_add_intermediate_approved_statuses.py
- TestDepartmentPlanViewSetMyDepartmentPlan
- StudyGroupService
- Руководство по ручному развертыванию Project Activity Server
- 4. Список проектов
- action
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
- Any
- test_study_group_viewset.py
- 0011_migrate_team_data.py
- test_project_track_viewset.py
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- test_study_group_domain.py
- Role
- test_direction_domain.py
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- get_error_message
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
- test_user_me_student.py
- accounts/admin.py
- InvolvedManager
- RutMiitClient
- ProjectTrackProjectDetailDTO
- .test_departments_list_allow_any_detail_requires_auth
- .test_registration_request_create_anonymous_allowed
- test_sync_departments_institutes.py
- MentorGroupDetailDTO
- TagService
- ._track_detail_queryset
- TeamSemester
- ProjectTrackPermission
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
- APIClient
- .test_semester_list_is_active_from_settings
- test_team_semester_models.py
- .test_user_me_institute_code_from_department_institute
- .test_user_roles_list_requires_auth_and_returns
- DirectionViewSet
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
- UserListDTO
- Command
- ProjectTrackGroupDetailDTO
- ProjectApplicationRepository
- Схема БД: студенческий портал
- Справочные эндпоинты
- Парсинг «Проектная деятельность» — РУТ (МИИТ)
- generate_ief_test_data.py
- TestApproveRejectRequest
- test_tag_viewset.py
- Department
- TestTagViewSetDelete
- repositories/project.py
- 0017_copy_studygroup_mentors_to_semester.py
- test_team_lobby_viewset.py
- TeamEventLogPagination
- test_application_import.py
- .recalculate_recommended_teams_count
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- .list_active_groups
- Вариант 1: импорт схемы с автообновлением
- DepartmentPlan.py
- ProjectApplicationViewSet
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- 0016_studygroupsemester.py
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- ProjectViewSet
- .get_existing_application_ids
- .update_team_member_limits
- ApplicationInvolvedDepartment
- showcase/urls.py
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- StudentShowcaseRepository
- .test_password_change_success
- ProjectTrackApplication
- .test_password_change_wrong_current_password
- .test_password_reset_sends_email
- .test_registration_request_approve_allowed_for_cpds_user
- .test_registration_request_approve_creates_user_and_sends_email
- .test_registration_request_approve_forbidden_for_regular_user
- .test_registration_request_approve_mail_failure_returns_400_and_no_user_created
- ProjectTrackGroup
- .test_registration_request_list_requires_privileged_user
- .test_registration_request_race_condition_integrity_error
- ProjectTrackProjectListDTO
- .get_group_by_id
- ProjectTrackAddApplicationItemSerializer
- 0018_studygroupsemester_mentors_m2m.py
- .test_semester_create_allowed_for_admin_and_cpds
- .test_semester_list_requires_auth
- .test_user_me_institute_code_none_if_no_institute
- ProjectTrackUpdateSerializer
- format_validation_errors
- .list
- .update
- django_db
- PasswordResetSerializer
- Текущий статус реализации
- UserManager
- .ensure_student_with_group
- .ensure_is_captain
- ProjectTrackAddApplicationsSerializer
- ProjectTrackCreateSerializer
- CustomResetPasswordForm
- data/conftest.py
- timetable

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 540 edges
2. `User` - 264 edges
3. `ProjectApplication` - 151 edges
4. `Department` - 145 edges
5. `Semester` - 136 edges
6. `ProjectApplicationService` - 136 edges
7. `StudyGroup` - 133 edges
8. `ProjectApplicationCreateDTO` - 111 edges
9. `PreRegisteredStudent` - 80 edges
10. `Institute` - 76 edges

## Surprising Connections (you probably didn't know these)
- `create_test_applications()` --uses--> `User`  [INFERRED]
  create_test_applications.py → accounts/models.py
- `create_test_user()` --uses--> `User`  [INFERRED]
  create_test_user.py → accounts/models.py
- `ApplicationDashboardDomain` --uses--> `User`  [INFERRED]
  showcase/domain/application_dashboard.py → accounts/models.py
- `ProjectDomain` --uses--> `User`  [INFERRED]
  showcase/domain/project.py → accounts/models.py
- `ProjectTrackDomain` --uses--> `User`  [INFERRED]
  showcase/domain/project_track.py → accounts/models.py

## Import Cycles
- None detected.

## Communities (365 total, 114 thin omitted)

### Community 0 - "._handle_errors"
Cohesion: 0.09
Nodes (21): MentorTeamAddMemberSerializer, MentorTeamCreateSerializer, MentorTeamSetCaptainSerializer, MentorTeamUpdateNameSerializer, Request, Response, PATCH /study-groups/{groupId}/teams/{teamSemesterId}/ — название., DELETE /study-groups/{groupId}/teams/{teamSemesterId}/ — удалить команду. (+13 more)

### Community 1 - "make_user"
Cohesion: 0.03
Nodes (20): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, _base_create_payload(), TestProjectApplicationNewFieldsCreateUpdate, TestProjectTrackViewSet, django_db (+12 more)

### Community 2 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 3 - "Ответственный по институту — API для фронта"
Cohesion: 0.07
Nodes (27): 1. Список активных групп института, 2. Обзор групп института (со счётчиками), 3. Сотрудники института, 4. Группы с назначенными наставниками, 5. Назначить наставника группе, 6. Снять наставника с группы, Значения `semester_id`, Общие query-параметры (+19 more)

### Community 4 - "ProjectTrackService"
Cohesion: 0.13
Nodes (6): Создаёт DTO из словаря., ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), django_db, TestProjectTrackService

### Community 5 - "accounts/views.py"
Cohesion: 0.07
Nodes (41): AcademicYear, Meta, RegistrationRequest, Status, IsCpdsUser, Разрешает доступ только сотрудникам, администраторам или роли ЦПДС., Разрешает доступ только пользователям с ролью ЦПДС (код роли `cpds`)., RegistrationRequestManagePermission (+33 more)

### Community 6 - "ApplicationDashboardService"
Cohesion: 0.05
Nodes (33): get_department_subtree_ids(), Возвращает id корневого подразделения и всех его потомков., ApplicationDashboardDomain, DashboardFilters, Доменная логика дашборда проектных заявок., Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп., Парсит query-параметр application_type. (+25 more)

### Community 7 - "Any"
Cohesion: 0.07
Nodes (19): ProjectTrackAggregatedStatisticsDTO, ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackStatisticsDTO, Any, Преобразует DTO в словарь для API., DTO заявки в проектном треке. (+11 more)

### Community 8 - "application_import.py"
Cohesion: 0.13
Nodes (20): ApplicationImportRow, build_import_row(), is_data_row(), iter_application_import_rows(), normalize_cell(), parse_customer_type(), parse_institute_codes(), Any (+12 more)

### Community 9 - "TagRepository"
Cohesion: 0.06
Nodes (34): DTO для обновления тега., TagUpdateDTO, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., Обновление тега. Обновляет только переданные поля. Args: tag: Тег для…, TagRepository, django_db (+26 more)

### Community 10 - "TestApplicationDashboardService"
Cohesion: 0.05
Nodes (27): _create_app(), django_db, Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external., Фильтр по группам статусов., Карточка in_work = total - approved - rejected., Среднее и медиана времени до решения., Топ старых заявок включает заявки в статусе in_progress. (+19 more)

### Community 11 - "ProjectApplication"
Cohesion: 0.04
Nodes (42): ProjectApplication, ApplicationDashboardRepository, Q, QuerySet, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению. (+34 more)

### Community 12 - "test_mentor_groups_viewset.py"
Cohesion: 0.15
Nodes (13): MentorGroupListDTO, Список групп наставника., api_client(), direction(), _enrollment_with_mentors(), APIClient, django_db, fixture (+5 more)

### Community 13 - "._collect_group_rows"
Cohesion: 0.19
Nodes (9): Command, BaseCommand, DataFrame, date, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Дедуплицирует строки по коду постоянной группы., Возвращает направление подготовки, создавая при необходимости. (+1 more)

### Community 14 - "ApplicationNotificationService"
Cohesion: 0.19
Nodes (8): ApplicationNotificationService, Отправка писем автору при отклонении и отправке на доработку., Email получателя: author_email заявки или email связанного пользователя-автора., Письмо автору: заявка отправлена на доработку., Письмо автору: заявка отклонена., django_db, patch, TestApplicationNotificationService

### Community 15 - "APIClient"
Cohesion: 0.12
Nodes (21): api_client(), _approved_app(), _create_team_url(), direction(), _enrollment_with_mentors(), mentor_team_setup(), Any, APIClient (+13 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroupMemberDTO"
Cohesion: 0.22
Nodes (5): Any, Карточка наставника учебной группы., Строка списка группы из контингента., StudyGroupMemberDTO, StudyGroupMentorDTO

### Community 18 - "TagCreateDTO"
Cohesion: 0.08
Nodes (19): DTO для создания тега., TagCreateDTO, Тесты для метода create репозитория., Создание общего тега (без departments)., Создание тега с подразделением., Создание тега с несуществующим подразделением вызывает ошибку., Нельзя создать тег с таким же именем и таким же набором подразделений., Можно создать тег с таким же именем, но другим набором подразделений. (+11 more)

### Community 19 - "UserManagementService"
Cohesion: 0.07
Nodes (20): ViewSet для управления пользователями., QuerySet, Репозиторий для управления пользователями., Доступ к данным пользователей для управления., Базовый queryset без администраторов., Список пользователей с оптимизацией запросов., Возвращает пользователя по ID., Сохраняет изменения пользователя. (+12 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 22 - "PreRegisteredStudentService"
Cohesion: 0.07
Nodes (29): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Отправляет администратору письмо о расхождении данных., Публичные операции предрегистрации студентов. (+21 more)

### Community 23 - "PermissionError"
Cohesion: 0.08
Nodes (17): PermissionError, Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, ProjectTrackGroupListDTO, DTO группы со счётчиком назначенных проектов., Преобразует DTO в словарь для API., Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации., Бизнес-операция: получение заявок для координации пользователя. Для обычных… (+9 more)

### Community 24 - "StudyGroupViewSet"
Cohesion: 0.19
Nodes (10): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/my-groups/ — группы наставника в семестре., GET /api/teams/study-groups/{id}/mentor-detail/ — детали группы наставника., GET /api/teams/study-groups/{id}/project-showcase/ — витрина проектов группы., GET /api/teams/study-groups/ — список и просмотр учебных групп. (+2 more)

### Community 25 - "test_student_showcase_viewset.py"
Cohesion: 0.08
Nodes (19): api_client(), _approved_app(), _create_assembled_team(), direction(), other_group(), django_db, fixture, Тесты API студенческой витрины проектов. (+11 more)

### Community 26 - "normalize_cell"
Cohesion: 0.13
Nodes (16): build_preregistered_student_import_row(), last_names_match(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки. (+8 more)

### Community 27 - "Request"
Cohesion: 0.12
Nodes (17): ApproveJoinRequestSerializer, CreateInvitationSerializer, extend_schema, Request, Response, GET /api/teams/my-team/., GET /api/teams/my-team/event-log/ — пагинированный лог (page_size=50)., DELETE /api/teams/my-team/ — удалить свою команду. (+9 more)

### Community 28 - "TestTeamLobbyViewSet"
Cohesion: 0.14
Nodes (7): _create_captained_team(), django_db, Команда без трека при одном треке у группы → min/max с трека группы., После создания своей команды pending-заявка в чужую → obsolete., При нескольких треках track_id не проставляется; лимиты — effective по трекам., Если группе доступен один трек — он проставляется без track_id в body., TestTeamLobbyViewSet

### Community 29 - "UserManagementViewSet"
Cohesion: 0.18
Nodes (12): extend_schema_view, Request, Response, API управления пользователями: список, деталь, частичное обновление., Проверяет query-параметр include_authored_projects., GET /api/accounts/users/ — список пользователей., GET /api/accounts/users/{id}/ — деталь пользователя., PATCH /api/accounts/users/{id}/ — частичное обновление. (+4 more)

### Community 30 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.11
Nodes (11): django_db, Тесты для проверки поля is_internal_customer при создании заявки., Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer… (+3 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.07
Nodes (25): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+17 more)

### Community 32 - "MentorGroupsDomain"
Cohesion: 0.11
Nodes (13): MentorGroupsDomain, Доменная логика доступа наставника к учебной группе., Проверки для API «Мои группы» наставника., Проверяет, что учебная группа существует., Проверяет, что учебная группа не завершила обучение., Возвращает True, если пользователь — ответственный по институту., Коды институтов ответственного по институту., Проверяет доступ к группе: наставник или ответственный по институту. (+5 more)

### Community 33 - "ProjectTrack"
Cohesion: 0.05
Nodes (34): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackCreateDTO, ProjectTrackUpdateDTO, DTO для проектных треков., DTO для создания проектного трека., DTO для добавления групп в трек. (+26 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.13
Nodes (23): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+15 more)

### Community 35 - "._get_track_with_access"
Cohesion: 0.11
Nodes (15): ProjectTrackReadDTO, DTO для чтения проектного трека., atomic, Возвращает трек с проверкой доступа., Возвращает детали трека., Создаёт проектный трек., Проставляет лимиты размера команды всем заявкам трека., Обновляет основные поля трека и лимиты команд у заявок. (+7 more)

### Community 36 - "TestTagViewSetCreate"
Cohesion: 0.12
Nodes (9): Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем., Нельзя создать общий тег, если имя уже используется (общим или departmental… (+1 more)

### Community 37 - "MentorTeamDomain"
Cohesion: 0.09
Nodes (12): MentorTeamDomain, Чистая бизнес-логика API команд наставника., Проверяет, что команда принадлежит учебной группе., Проверяет возможность подтверждения состава., Проверяет возможность разутверждения состава., Удаление возможно только при пустом составе., Новый капитан должен быть участником команды., Нельзя удалить текущего капитана без смены капитана. (+4 more)

### Community 38 - "ProjectApplicationService"
Cohesion: 0.02
Nodes (78): Meta, ProjectApplicationListSerializer, Упрощенный ViewSet для проектных заявок с использованием новой архитектуры.…, Простой сериализатор для списка заявок, ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationComment, ProjectApplicationService (+70 more)

### Community 39 - "StudentShowcaseDomain"
Cohesion: 0.12
Nodes (19): Правила доступа и записи команды на проект витрины., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI)., StudentShowcaseDomain (+11 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.06
Nodes (35): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если студент прошёл полную регистрацию (не псевдо-user)., PreRegisteredStudentRepository, QuerySet, Репозиторий предрегистрации студентов., Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета. (+27 more)

### Community 41 - "Tag"
Cohesion: 0.09
Nodes (14): Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, Теги для проектных заявок, Tag, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Создание тега в БД. Args: dto: DTO с данными для создания тега Returns:…, Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, atomic (+6 more)

### Community 42 - ".calculate_initial_status"
Cohesion: 0.11
Nodes (12): Определение начального статуса на основе роли пользователя. Чистая функция -…, Бизнес-операция: подача заявки. Новая логика: 1. Валидация через Domain 2.…, Проверяет наличие пользователя с ролью department_validator в причастных…, Проверяет и корректирует статус заявки при необходимости. Если целевой статус -…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute. (+4 more)

### Community 43 - ".post"
Cohesion: 0.24
Nodes (7): LoginView, extend_schema, Request, Response, Сменяет пароль текущего пользователя после проверки текущего пароля., Получение JWT токена по email и паролю., TokenObtainPairView

### Community 44 - "test_institute_responsible_viewset.py"
Cohesion: 0.14
Nodes (14): InstituteResponsibleGroupMentorsDTO, DTO для API ответственного по институтам., Ответ: группы с назначениями наставников., api_client(), direction(), other_institute(), APIClient, django_db (+6 more)

### Community 45 - "Institute"
Cohesion: 0.15
Nodes (15): Institute, Справочник институтов/академий для выбора целевых институтов в заявках, aga_institute(), direction(), Any, django_db, fixture, Path (+7 more)

### Community 46 - "TestProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (28): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationCreateSerializer, ProjectApplicationUpdateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы… (+20 more)

### Community 47 - "TeamLobbyService"
Cohesion: 0.13
Nodes (12): QuerySet, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент принимает приглашение., Оркестрация Domain + Repository для студенческого лобби., Queryset лога «Моей команды» (новые сверху); 404 если нет команды., Резолвит semester_id; по умолчанию actual., Лимиты команды: свой трек → effective по трекам группы → дефолты. (+4 more)

### Community 48 - "prod_users_client.py"
Cohesion: 0.11
Nodes (23): Client, _http_client(), obtain_token(), Клиент prod API для обновления снимка пользователей., Возвращает базовый URL prod API., HTTP-клиент с поддержкой редиректов prod., Получает JWT access token по email и паролю., Возвращает Bearer token из CLI, env или login. (+15 more)

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+2 more)

### Community 50 - "Tag.py"
Cohesion: 0.08
Nodes (28): Инициализация из модели Tag., TagReadDTO, DepartmentAttachDetachSerializer, DepartmentNestedSerializer, Meta, action, Request, Response (+20 more)

### Community 51 - "teams/views.py"
Cohesion: 0.12
Nodes (20): _is_staff_or_admin(), APIView, BasePermission, Request, Разрешения для приложения teams., Доступ только студенту с привязанной учебной группой., Чтение — любой аутентифицированный пользователь. Изменение постоянной команды —…, Изменение семестрового контекста — капитан, admin или cpds. (+12 more)

### Community 52 - "DirectionService"
Cohesion: 0.17
Nodes (9): DirectionService, Оркестрация Domain + Repository для Direction., Список направлений с фильтрацией по роли., Направление по коду с проверкой доступа., directions(), django_db, fixture, Тесты DirectionService. (+1 more)

### Community 53 - "TestTagViewSet"
Cohesion: 0.10
Nodes (11): Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level). (+3 more)

### Community 54 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.09
Nodes (25): build_group_import_row(), build_group_name(), calculate_course_number(), group_ended_by_planned_dates(), GroupImportRow, parse_direction_level(), parse_permanent_group_code(), parse_planned_end_date() (+17 more)

### Community 55 - "UserType"
Cohesion: 0.20
Nodes (10): atomic, UserType, Студент отклоняет приглашение., Возвращает команду капитана или бросает ошибку., Капитан одобряет заявку и назначает роль., Капитан отклоняет заявку., Капитан приглашает одногруппника., Капитан удаляет участника. (+2 more)

### Community 56 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 57 - "showcase/models.py"
Cohesion: 0.03
Nodes (76): Общие константы приложения showcase., ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Явное выражение бизнес-намерений (не технических операций). Этот модуль…, Domain слой - чистая бизнес-логика без побочных эффектов. Этот слой содержит…, build_author_short_name() (+68 more)

### Community 58 - "APIView"
Cohesion: 0.11
Nodes (14): IsAdminOrCpds, APIView, Request, Проверяет наличие прав у пользователя., Проверяет наличие прав у пользователя., Проверяет наличие прав у пользователя., Проверяет права на чтение или запись пользователей., Проверяет наличие прав у пользователя. Args: request: текущий запрос view:… (+6 more)

### Community 59 - "ProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (43): create_test_applications(), Создаем тестовые заявки, Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Определение необходимости консультации на основе данных заявки. Чистая функция…, Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, ProjectApplicationCreateDTO, DTO для создания заявки - только данные, никакой логики, Носитель проблемы короче 5 символов вызывает ошибку. (+35 more)

### Community 60 - "UserSerializer"
Cohesion: 0.18
Nodes (10): Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., UserSerializer, CustomTokenObtainPairSerializer, APIView (+2 more)

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.07
Nodes (18): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя. (+10 more)

### Community 62 - "InstituteResponsibleGroupDTO"
Cohesion: 0.14
Nodes (7): InstituteResponsibleGroupDTO, InstituteResponsibleGroupWithMentorDTO, InstituteResponsibleMentorDTO, Any, Компактное представление учебной группы., Назначенный наставник группы (полная карточка)., Учебная группа с ID назначенных наставников в семестре.

### Community 63 - "showcase/admin.py"
Cohesion: 0.12
Nodes (18): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+10 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "TeamLobbyRepository"
Cohesion: 0.04
Nodes (28): QuerySet, Лог событий команды в семестре (новые сверху)., Pending-заявки студента в семестре., Pending-приглашения студента в семестре., Карта team_semester_id → id pending-заявки текущего пользователя., Число команд группы в треке в семестре., True, если студент уже в команде в семестре., Команда в семестре с базовыми связями. (+20 more)

### Community 66 - "TeamLobbyDomain"
Cohesion: 0.04
Nodes (34): Удаление: капитан, forming, в составе только он., Подтверждение состава: капитан, forming, размер в лимитах трека., Заявка должна быть в статусе pending., Приглашение должно быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды»., True, если студент без команды и есть свободный слот., Запрещает изменения состава при подтверждённом составе., Приглашение не может назначать роль leader. (+26 more)

### Community 67 - ".approve_application"
Cohesion: 0.10
Nodes (15): atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку., Бизнес-операция: отзыв заявки автором., Бизнес-операция: одобрение заявки. (+7 more)

### Community 68 - "UserManagementDomain"
Cohesion: 0.10
Nodes (14): Доменная логика управления пользователями., Правила доступа и валидации для управления пользователями., Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., ID подразделений для фильтрации; None — без ограничения., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., UserManagementDomain (+6 more)

### Community 69 - "Semester"
Cohesion: 0.06
Nodes (33): Идемпотентный импорт строк модели Settings из CSV., Ключ–значение настроек приложения (редактируемые из админки / импортом)., Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Semester, Settings, Тесты UserManagementViewSet., Тесты разбора semester_id для GET-списков. (+25 more)

### Community 70 - "tests/conftest.py"
Cohesion: 0.13
Nodes (15): PasswordChangeSerializer, Any, Возвращает учебную группу пользователя или None., Сериализатор для смены пароля аутентифицированного пользователя., departments(), institute(), fixture, Возвращает класс модели пользователя для удобства. (+7 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.11
Nodes (9): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Автор всегда имеет доступ к своей заявке., Админ имеет доступ ко всем заявкам., Модератор имеет доступ ко всем заявкам., CPDS имеет доступ ко всем заявкам., Валидатор подразделения имеет доступ ко всем заявкам., Валидатор института имеет доступ ко всем заявкам., Обычный пользователь не имеет доступа к чужой заявке. (+1 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.13
Nodes (12): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, django_db, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., Тесты для фильтрации queryset тегов по ролям., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения. (+4 more)

### Community 73 - "DepartmentPlanViewSet"
Cohesion: 0.20
Nodes (12): DepartmentPlanViewSet, action, extend_schema, Request, Response, Получить словарь планов по подразделениям для указанного семестра., Получить статистику заявок по статусам для каждого подразделения., GET /api/showcase/department-plans/?institute_code=INST&semester_id=1 Получение… (+4 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.11
Nodes (10): ProjectTrackRepository, Создаёт проектный трек., Возвращает id групп, уже привязанных к треку., Удаляет группу из трека; True если связь была., Удаляет заявку из трека; True если связь была., Количество групп в треке., Доступ к данным проектных треков., Обновляет лимиты команд у переданных заявок. Обновляет recommended_teams_count,… (+2 more)

### Community 75 - ".view_application"
Cohesion: 0.15
Nodes (8): Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Автор всегда имеет доступ к просмотру своей заявки., Обычному пользователю чужая заявка недоступна., Список заявок разрешён всем (возвращает True)., TestViewAndList

### Community 76 - "MentorTeamService"
Cohesion: 0.14
Nodes (18): MentorTeamService, Any, atomic, Создаёт команду в группе с указанным капитаном., Лимиты размера команды для группы в семестре., Обновляет название команды., Назначает нового капитана из состава команды., Подтверждает состав команды (forming → assembled). (+10 more)

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 79 - "accounts/permissions.py"
Cohesion: 0.14
Nodes (14): IsInstituteValidator, ProjectManagementPermission, BasePermission, Пользовательские permissions для приложения accounts., Разрешает доступ к управлению тегами только для ролей cpds, admin и…, Разрешает просмотр проектов для admin, cpds и institute_validator., Просмотр пользователей — admin/cpds/institute_validator; запись — admin/cpds., Разрешает доступ только пользователям с ролью institute_validator. (+6 more)

### Community 80 - "Витрина проектов (студент) — API для фронта"
Cohesion: 0.14
Nodes (13): 1. Список треков с проектами, 2. Детали проекта, 3. Записать команду на проект, Витрина проектов (студент) — API для фронта, Ответ `200`, Ответ `200`, Ответ `200`, Ошибки (+5 more)

### Community 81 - "MentorTeamRepository"
Cohesion: 0.06
Nodes (18): MentorTeamRepository, Удаляет участника любой роли., Меняет статус состава., Удаляет семестровый контекст и постоянную команду при необходимости., Запросы и записи для API команд наставника., Пишет запись в лог команды., True, если пользователь уже в команде в семестре., Пользователь по id или None. (+10 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.11
Nodes (10): AccountsApiTests, override_settings, Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Создание заявки без подразделения возвращает ошибку валидации., Создание заявки с несуществующим подразделением возвращает ошибку валидации., После отклонения заявки можно подать новую с тем же email., Повторная подача при активной заявке возвращает ошибку валидации., Нельзя подать заявку, если пользователь с таким email уже зарегистрирован. (+2 more)

### Community 84 - "TestCanDeleteTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения., admin может удалять любые теги. (+2 more)

### Community 85 - "build_user_indexes"
Cohesion: 0.10
Nodes (29): main(), Сверка преподавателей из Excel со списком пользователей prod API. ..…, Отмечает преподавателей из Excel, которые есть в prod., build_user_indexes(), find_user(), normalize_name(), Сопоставление ФИО преподавателей с пользователями PD., Нормализует ФИО для сравнения. (+21 more)

### Community 86 - ".handle"
Cohesion: 0.13
Nodes (11): Следующий семестр для новых заявок (Settings.next_semester_code)., find_existing_imported_application(), parse_author_name(), Ищет уже импортированную заявку по автору, названию и заказчику., Разбирает строку вида «Фамилия Имя» на фамилию и имя., Command, BaseCommand, Формирует контактные поля автора для DTO из пользователя системы. (+3 more)

### Community 87 - "Command"
Cohesion: 0.15
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "Управление командой"
Cohesion: 0.07
Nodes (26): Query-параметры, Query-параметры, Query-параметры, Вернуть состав на редактирование, Витрина проектов, Детали группы наставника, Добавить участника, Карточка команды (+18 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.13
Nodes (12): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы., Возвращает список доступных действий согласно матрице. (+4 more)

### Community 90 - "test_import_preregistered_students.py"
Cohesion: 0.19
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 91 - "MentorTeamViewSet"
Cohesion: 0.10
Nodes (19): Запрещает изменения, если команда записана на проект., Команда записана на проект — мутации запрещены., TeamEnrolledInProjectError, MentorTeamViewSet, ViewSet управления командой учебной группы для наставника., API наставника для управления командой группы в семестре., MyTeamViewSet, Раздел «Моя команда» для капитана и участника. (+11 more)

### Community 92 - "serialize_comment_author"
Cohesion: 0.14
Nodes (11): Сериализует автора комментария с role и department. Args: author: User объект…, serialize_comment_author(), POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, Тесты для функции serialize_comment_author., Если author равен None, возвращаются None значения., Сериализация автора с полными данными: имя, фамилия, отчество, роль,…, Сериализация автора без отчества. (+3 more)

### Community 93 - "StudyGroup"
Cohesion: 0.17
Nodes (13): StudyGroup, Возвращает заголовок группы (id, name) или None., QuerySet, Группа с наставником и контингентом без N+1., api_client(), _detail_url(), direction(), _enrollment_with_mentors() (+5 more)

### Community 94 - "MentorGroupsRepository"
Cohesion: 0.14
Nodes (11): MentorGroupsRepository, QuerySet, Команды группы в семестре с числом участников (без N+1)., Выборка учебных групп, где пользователь назначен наставником., Добавляет счётчики студентов и команд в семестре., Группы наставника в семестре со счётчиками студентов и команд., Активные группы институтов со счётчиками студентов и команд., Возвращает True, если пользователь — наставник группы в семестре. (+3 more)

### Community 95 - "extract.py"
Cohesion: 0.22
Nodes (16): main(), run(), export_marked_xlsx(), export_to_xlsx(), _group_columns(), Any, Экспортирует результаты парсинга с колонками сверки с PD., _collect_events() (+8 more)

### Community 96 - "InstituteResponsibleService"
Cohesion: 0.05
Nodes (34): InstituteResponsibleDomain, Правила доступа и валидации для ответственного по институтам., Проверяет, может ли пользователь работать с API ответственного., Определяет код института из параметра или по умолчанию., ID подразделений института для фильтрации сотрудников., Подгружает parent подразделения для resolve институтов., InstituteResponsibleAssignMentorDTO, InstituteResponsibleEmployeeDTO (+26 more)

### Community 97 - "InstituteResponsibleViewSet"
Cohesion: 0.19
Nodes (16): delete, InstituteResponsiblePermission, InstituteResponsibleViewSet, action, BasePermission, extend_schema, Request, Response (+8 more)

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

### Community 102 - ".can_edit_application"
Cohesion: 0.16
Nodes (9): Проверка права на редактирование заявки. Бизнес-правило: редактировать может…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку., Не-автор и не-ЦПДС не может редактировать чужую заявку., Нельзя редактировать заявки со статусом rejected (даже автору и cpds)., Нельзя редактировать одобренные заявки (кроме админов и cpds)., Автор может редактировать заявку в статусе returned_*., CPDS может редактировать заявки в статусе rejected_department. (+1 more)

### Community 103 - "API Документация - Проектные заявки"
Cohesion: 0.18
Nodes (9): API Документация - Проектные заявки, Аутентификация, Базовый URL, Валидационные правила, Общая информация, Обязательные поля, Обязательные поля:, Типы данных (+1 more)

### Community 104 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

### Community 105 - ".update_application"
Cohesion: 0.15
Nodes (9): Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Не-автор и не-ЦПДС не может редактировать заявку., Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult., CPDS может редактировать одобренные заявки., institute_validator-автор: save совпадает с available_actions (подразделение…, institute_validator без причастного подразделения не может сохранить. (+1 more)

### Community 106 - "Direction"
Cohesion: 0.14
Nodes (13): DirectionDomain, Доменная логика для направлений подготовки., Фильтрация направлений по роли пользователя., Direction, Level, Направление подготовки (ФГОС ВО)., DirectionRepository, QuerySet (+5 more)

### Community 107 - "Direction.py"
Cohesion: 0.20
Nodes (7): DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DirectionSerializer, Meta, Сериализатор направления подготовки.

### Community 108 - "StudyGroup.py"
Cohesion: 0.19
Nodes (10): Any, DTO для учебных групп., DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, Компактная выдача для списка учебных групп. (+2 more)

### Community 109 - "test_project_application_viewset.py"
Cohesion: 0.06
Nodes (23): django_db, Тесты для ProjectApplicationViewSet - проверка API endpoints., Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Тесты для упрощенного создания заявок (simple endpoint)., Тесты для ручки массового назначения семестра., POST /api/showcase/project-applications/simple/ устанавливает is_external=True… (+15 more)

### Community 110 - "StudentShowcaseViewSet"
Cohesion: 0.23
Nodes (10): action, extend_schema, extend_schema_view, Request, Response, Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/., GET /api/showcase/student-showcase/projects/{id}/. (+2 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - "test_my_study_group_viewset.py"
Cohesion: 0.10
Nodes (17): MyStudyGroupDTO, DTO для эндпоинта «Моя группа»., Возвращает наставников: из семестра или fallback на StudyGroup.mentor., Полные данные учебной группы для текущего студента., Репозиторий для учебных групп., Доступ к данным StudyGroup., StudyGroupRepository, Сервис для операций с учебными группами. (+9 more)

### Community 113 - "ApplicationLoggingService"
Cohesion: 0.04
Nodes (46): ApplicationLoggingService, atomic, Логирование удаления причастного пользователя. Args: application: Заявка user:…, Логирование добавления причастного подразделения. Args: application: Заявка…, Логирование удаления причастного подразделения. Args: application: Заявка…, Сервис для логирования изменений в проектных заявках. Обеспечивает полное…, Получение всех логов по заявке. Args: application: Заявка Returns:…, Получение последнего лога заявки. Args: application: Заявка Returns:… (+38 more)

### Community 114 - "ProjectListDTO"
Cohesion: 0.09
Nodes (20): get_root_department(), is_cpds_department(), Утилиты для работы с подразделениями., Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, ProjectListDTO, Any, DTO для списка проектов. (+12 more)

### Community 115 - "TeamLobbyViewSet"
Cohesion: 0.18
Nodes (10): CreateTeamSerializer, action, extend_schema_view, POST /api/teams/lobby/teams/{id}/join-requests/., POST /api/teams/lobby/invitations/{id}/accept/., POST /api/teams/lobby/invitations/{id}/reject/., Создание команды в лобби., Студенческое лобби: треки, команды, заявки, приглашения. (+2 more)

### Community 116 - ".get_filtered_queryset"
Cohesion: 0.23
Nodes (5): QuerySet, Фильтрует направления: institute_validator — только из групп своего института., parametrize, Фильтрация queryset направлений по ролям., TestGetFilteredQueryset

### Community 117 - "institute_access.py"
Cohesion: 0.10
Nodes (24): Доменная логика для списка проектов., Доменная логика для проектных треков., Репозиторий для проектных треков., application_available_for_institute(), application_belongs_to_institutes(), get_accessible_institute_codes(), get_department_ids_by_institute_code(), get_department_ids_for_institute_codes() (+16 more)

### Community 118 - "StudentShowcaseService"
Cohesion: 0.12
Nodes (16): Карточка проекта в списке трека витрины., StudentShowcaseProjectListItemDTO, ViewSet студенческой витрины проектов., atomic, UserType, Сервис студенческой витрины проектов., Записывает команду капитана на проект., Оркестрация Domain + Repository для студенческой витрины. (+8 more)

### Community 119 - "test_my_team_viewset.py"
Cohesion: 0.10
Nodes (12): api_client(), direction(), my_team_setup(), django_db, fixture, Тесты API «Моя команда»., Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → effective max(min)/min(max). (+4 more)

### Community 120 - "sync_project_teachers.py"
Cohesion: 0.15
Nodes (14): load_project_env(), Загружает переменные из .env в корне проекта., main(), parse_all_groups(), _print_parse_summary(), Path, Парсинг расписания РУТ и сверка преподавателей с пользователями prod PD., Парсит преподавателей «Проектная деятельность» по всем группам. (+6 more)

### Community 121 - "ProjectService"
Cohesion: 0.18
Nodes (8): ProjectService, Сервис для операций со списком проектов., Оркестрация Domain + Repository для списка проектов., other_institute(), django_db, fixture, Тесты ProjectService., TestProjectService

### Community 122 - ".resolve_list_semester_id"
Cohesion: 0.10
Nodes (12): Разбор query-параметра semester_id для GET-списков: id, next, actual., Подгружает parent подразделения пользователя., Список проектов с учётом роли пользователя., Any, Список групп наставника с количеством студентов и команд., Детали группы: студенты контингента и команды в семестре., Any, Список треков с проектами для группы наставника в семестре. (+4 more)

### Community 123 - "Поддержка multipart/form-data"
Cohesion: 0.33
Nodes (6): Допустимые форматы файлов, Заголовки, Загрузка файлов, Максимальный размер файла, Поддержка multipart/form-data, Тело запроса

### Community 124 - "test_import_institutes.py"
Cohesion: 0.54
Nodes (7): django_db, Path, Тесты команды import_institutes., test_import_institutes_clear_removes_missing(), test_import_institutes_is_idempotent(), test_import_institutes_updates_existing(), _write_institutes_csv()

### Community 125 - "build_fgos_napravleniya_csv.py"
Cohesion: 0.43
Nodes (6): collect_codes(), fetch(), main(), parse_table_rows(), Собрать fgos_specialitet_napravleniya.csv: level, code, name (без групп…, middle: '03' — бакалавриат, '05' — специалитет.

### Community 126 - "User"
Cohesion: 0.04
Nodes (34): AbstractBaseUser, QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., User, Возвращает код института пользователя. Приоритет: институт подразделения, затем…, check_and_fix_user(), Проверяем и исправляем пользователя, PermissionsMixin (+26 more)

### Community 127 - "Command"
Cohesion: 0.33
Nodes (5): Command, BaseCommand, Экспорт возможных статусов заявок в Excel., Считывает статусы из базы и сохраняет в Excel., Возвращает статусы, отсортированные по позиции и коду.

### Community 128 - "Command"
Cohesion: 0.32
Nodes (3): Command, BaseCommand, Path

### Community 129 - "TestInstituteViewSet"
Cohesion: 0.22
Nodes (6): django_db, Тесты для InstituteViewSet., Проверяем выдачу списка институтов с полем department_id., Эндпоинт возвращает department_id, если институт связан с подразделением., Если подразделение не задано, department_id равно None., TestInstituteViewSet

### Community 130 - "update_prod.sh"
Cohesion: 0.52
Nodes (6): log_error(), log_info(), log_warn(), read_env_value(), update_prod.sh script, usage()

### Community 131 - "Command"
Cohesion: 0.33
Nodes (3): Command, BaseCommand, Возвращает абсолютный путь к CSV (относительный — от папки commands).

### Community 132 - "TestProjectViewSet"
Cohesion: 0.18
Nodes (4): _create_approved_app(), django_db, ЦПДС в причастных не должно подменять основное подразделение проекта., TestProjectViewSet

### Community 133 - "0014_add_intermediate_approved_statuses.py"
Cohesion: 0.33
Nodes (5): add_intermediate_approved_statuses(), Migration, Удаляет промежуточные статусы одобрения из БД., Добавляет промежуточные статусы одобрения в БД., remove_intermediate_approved_statuses()

### Community 134 - "TestDepartmentPlanViewSetMyDepartmentPlan"
Cohesion: 0.13
Nodes (9): django_db, Тесты для GET /api/showcase/department-plans/my-department-plan/ - план…, Успешное получение плана и статистики для подразделения пользователя., Если план отсутствует, возвращается 0, но статистика заявок учитывается., Ошибка: отсутствует semester_id., Ошибка: семестр не найден., Ошибка: у пользователя не указано подразделение., Ошибка: неавторизованный пользователь. (+1 more)

### Community 135 - "StudyGroupService"
Cohesion: 0.14
Nodes (10): Оркестрация Domain + Repository для StudyGroup., StudyGroupService, django_db, TestMyStudyGroupService, direction(), django_db, fixture, Тесты StudyGroupService. (+2 more)

### Community 136 - "Руководство по ручному развертыванию Project Activity Server"
Cohesion: 0.15
Nodes (12): 10. Проверка и сопровождение, 11. Настройка nginx (backend + SPA), 1. Подготовка окружения, 2. Получение исходного кода, 3. Создание и активация виртуального окружения, 4. Настройка переменных окружения (.env), 5. Настройка PostgreSQL, 6. Миграции и статические файлы (+4 more)

### Community 137 - "4. Список проектов"
Cohesion: 0.29
Nodes (7): 4. Список проектов, Query-параметры, Заголовки, Ошибки, Поведение по ролям, Примеры запросов, Успешный ответ (200)

### Community 138 - "action"
Cohesion: 0.12
Nodes (9): action, extend_schema, POST /api/semesters/{id}/assign-empty-applications Присваивает переданный…, POST /api/project-applications/{id}/approve/ Одобрение заявки, POST /api/project-applications/{id}/reject/ Отклонение заявки, POST /api/project-applications/{id}/request_changes/ Запрос изменений (отправка…, POST /api/project-applications/{id}/transfer_to_institute/ Передача заявки в…, POST /api/project-applications/{id}/return_by_author/ Отзыв заявки автором… (+1 more)

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
Cohesion: 0.26
Nodes (11): api_client(), _approved_app(), direction(), _enrollment_with_mentors(), mentor_showcase_setup(), django_db, fixture, Тесты GET /api/teams/study-groups/{id}/project-showcase/. (+3 more)

### Community 147 - "schema.py"
Cohesion: 0.50
Nodes (3): exclude_auth_api_duplicate(), Хуки и расширения для drf-spectacular., Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*). В…

### Community 149 - "Any"
Cohesion: 0.13
Nodes (10): Any, Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Трек с вложенными проектами для витрины., Преобразует DTO в словарь для API., Детали проекта для студента (без контактов)., Преобразует DTO в словарь для API., StudentShowcaseProjectDetailDTO (+2 more)

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

### Community 156 - "Any"
Cohesion: 0.15
Nodes (6): Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Преобразование в словарь., Преобразование в DTO., Преобразование в DTO.

### Community 157 - "test_study_group_viewset.py"
Cohesion: 0.47
Nodes (5): direction(), other_institute(), fixture, Тесты StudyGroupViewSet., study_groups()

### Community 159 - "test_project_track_viewset.py"
Cohesion: 0.15
Nodes (12): _create_approved_app(), _create_track_with_links(), direction(), other_institute(), django_db, fixture, Тесты ProjectTrackViewSet., semester() (+4 more)

### Community 164 - "test_study_group_domain.py"
Cohesion: 0.11
Nodes (16): QuerySet, Доменная логика для учебных групп., Фильтрация учебных групп по роли пользователя., institute_validator — только группы своих институтов., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., StudyGroupDomain, direction() (+8 more)

### Community 165 - "Role"
Cohesion: 0.18
Nodes (7): Command, BaseCommand, Role, create_test_user(), Создаем тестового пользователя, Command, BaseCommand

### Community 166 - "test_direction_domain.py"
Cohesion: 0.20
Nodes (9): directions(), other_institute(), django_db, fixture, Тесты доменной логики DirectionDomain., Три направления для сценариев фильтрации., Разрешение институтов по подразделению пользователя., Второй институт на другом подразделении. (+1 more)

### Community 170 - "get_error_message"
Cohesion: 0.18
Nodes (8): Exception, get_error_message(), GET /api/project-applications/external/ Получение списка всех внешних заявок…, Возвращает сообщение об ошибке в зависимости от режима DEBUG. Args: exception:…, PK семестра из ?semester_id= (id | next | actual) или None, если параметра нет., GET /api/project-applications/by_status/?status=created Получение заявок по…, GET /api/project-applications/recent/ Получение последних заявок (только для…, GET /api/project-applications/coordination/ Заявки для координации: где…

### Community 189 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 190 - "QuerySet"
Cohesion: 0.18
Nodes (6): QuerySet, Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки.

### Community 191 - "test_user_me_student.py"
Cohesion: 0.26
Nodes (9): api_client(), Any, APIClient, django_db, fixture, Тесты GET /api/accounts/user/ для роли student., student_user(), study_group() (+1 more)

### Community 192 - "accounts/admin.py"
Cohesion: 0.24
Nodes (11): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+3 more)

### Community 193 - "InvolvedManager"
Cohesion: 0.43
Nodes (3): InvolvedManager, atomic, Менеджер для управления причастными пользователями и подразделениями.

### Community 195 - "ProjectTrackProjectDetailDTO"
Cohesion: 0.17
Nodes (7): ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, DTO группы в деталях проекта., Преобразует DTO в словарь для API., DTO деталей проекта с назначенными группами., Преобразует DTO в словарь для API., Детали проекта с назначенными группами.

### Community 198 - "test_sync_departments_institutes.py"
Cohesion: 0.29
Nodes (10): Any, django_db, Экспорт и последующий импорт институтов восстанавливают данные., Экспорт и последующий импорт подразделений восстанавливают данные., Импорт институтов удаляет те, которых нет в файле., Импорт подразделений удаляет те, которых нет в файле., test_export_import_departments_roundtrip(), test_export_import_institutes_roundtrip() (+2 more)

### Community 199 - "MentorGroupDetailDTO"
Cohesion: 0.14
Nodes (9): MentorGroupDetailDTO, MentorGroupListItemDTO, MentorGroupStudentDTO, MentorGroupTeamDTO, Any, Строка списка групп наставника., Студент контингента для деталей группы наставника., Команда группы в семестре для деталей наставника. (+1 more)

### Community 200 - "TagService"
Cohesion: 0.05
Nodes (35): Доменная логика для тегов - чистые функции без эффектов., Чистая бизнес-логика для тегов - только функции, никаких эффектов., TagDomain, Сервис для оркестрации операций с тегами. Координирует Domain, Repository и DTO., Сервис - оркестрация всех операций с тегами. Координирует Domain, Repository и…, TagService, Unit-тесты для доменной логики TagDomain. Проверяем все чистые функции бизнес-…, django_db (+27 more)

### Community 201 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 202 - "TeamSemester"
Cohesion: 0.07
Nodes (37): Доменная логика студенческой витрины проектов., DTO студенческой витрины проектов., Результат записи команды на проект., StudentShowcaseEnrollResultDTO, Репозиторий студенческой витрины проектов (без N+1)., Доменные правила управления командой наставником., Доменные правила лобби формирования команд., DTO для эндпоинта «Мои группы» наставника. (+29 more)

### Community 203 - "ProjectTrackPermission"
Cohesion: 0.18
Nodes (9): ProjectTrackPermission, Разрешает доступ к проектным трекам для admin, cpds и institute_validator., ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок. (+1 more)

### Community 206 - "1. Создание заявки (авторизованные пользователи)"
Cohesion: 0.33
Nodes (6): 1. Создание заявки (авторизованные пользователи), Заголовки, Пример запроса, Тело запроса, Успешный ответ (201), Эндпоинты создания заявок

### Community 240 - "APIClient"
Cohesion: 0.40
Nodes (4): _create_assembled_team(), APIClient, _showcase_url(), TestMentorShowcaseViewSet

### Community 242 - "test_team_semester_models.py"
Cohesion: 0.24
Nodes (7): direction(), django_db, fixture, Тесты моделей TeamSemester и TeamSemesterMember., semester(), study_group(), TestTeamSemesterModels

### Community 245 - "DirectionViewSet"
Cohesion: 0.43
Nodes (4): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений.

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 277 - "UserListDTO"
Cohesion: 0.31
Nodes (4): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO

### Community 278 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 279 - "ProjectTrackGroupDetailDTO"
Cohesion: 0.20
Nodes (6): ProjectTrackGroupDetailDTO, ProjectTrackGroupProjectDTO, DTO проекта в деталях группы., Преобразует DTO в словарь для API., DTO деталей группы с назначенными проектами., Преобразует DTO в словарь для API.

### Community 280 - "ProjectApplicationRepository"
Cohesion: 0.03
Nodes (53): ProjectApplicationRepository, Репозиторий - вся работа с БД здесь, Получение QuerySet заявок по статусу для пагинации., Обновление заявки. Обновляет только переданные поля., Проверка существования заявки. Быстрая проверка без загрузки объекта., Подсчет заявок по статусу. Для аналитики и отчетов., Присваивает семестр всем заявкам без установленного семестра. Args:…, Получение QuerySet всех заявок для пагинации. Для административных операций и… (+45 more)

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 289 - "Парсинг «Проектная деятельность» — РУТ (МИИТ)"
Cohesion: 0.40
Nodes (4): Источник данных, Парсинг «Проектная деятельность» — РУТ (МИИТ), Полный пайплайн (парсинг + сверка с PD), Только парсинг (без сверки)

### Community 292 - "generate_ief_test_data.py"
Cohesion: 0.21
Nodes (4): Command, BaseCommand, Генерация тестовых одобренных проектов и учебных групп для института IEF., Добавляет причастные подразделения института к заявке.

### Community 293 - "TestApproveRejectRequest"
Cohesion: 0.27
Nodes (6): parametrize, Матрица прав определяет доступность reject., Для returned_* действует агрегирующее правило returned_(all)., Отзыв доступен только автору и не для финальных approved/rejected., Матрица прав определяет доступность approve для ролей и статусов., TestApproveRejectRequest

### Community 294 - "test_tag_viewset.py"
Cohesion: 0.20
Nodes (6): Unit-тесты для TagViewSet API эндпоинта. Проверяем получение списка тегов,…, Тесты для обновления тегов через API., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., admin может обновлять любые теги., TestTagViewSetUpdate

### Community 295 - "Department"
Cohesion: 0.09
Nodes (20): Command, BaseCommand, Department, Command, BaseCommand, Сбрасывает счетчик ID для таблицы тегов., Command, Any (+12 more)

### Community 296 - "TestTagViewSetDelete"
Cohesion: 0.20
Nodes (6): Тесты для удаления тегов через API., cpds может удалять общие теги., cpds не может удалять теги с подразделением., admin может удалять любые теги., Остальные роли не могут удалять теги., TestTagViewSetDelete

### Community 297 - "repositories/project.py"
Cohesion: 0.22
Nodes (6): ProjectRepository, QuerySet, Репозиторий для списка проектов., Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

### Community 299 - "test_team_lobby_viewset.py"
Cohesion: 0.33
Nodes (9): api_client(), _approved_app(), direction(), lobby_setup(), fixture, Тесты API лобби формирования команд., semester(), study_group() (+1 more)

### Community 300 - "TeamEventLogPagination"
Cohesion: 0.67
Nodes (3): PageNumberPagination, Пагинация ленты событий команды (фиксированный page_size=50)., TeamEventLogPagination

### Community 301 - "test_application_import.py"
Cohesion: 0.31
Nodes (8): get_or_create_institute_tag(), Возвращает тег направления и флаг, был ли тег создан. Сначала ищет общий…, django_db, Тесты доменной логики импорта заявок из Excel., Если есть базовый тег с таким именем, создавать институтский не нужно., Отсутствующий тег создаётся как институтский и привязывается к подразделению., test_get_or_create_institute_tag_creates_department_tag(), test_get_or_create_institute_tag_returns_base_tag()

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

### Community 307 - ".list_active_groups"
Cohesion: 0.25
Nodes (5): QuerySet, Активные группы института., Активные группы с prefetch наставников в семестре., Сотрудники института (не студенты, не админы, не staff)., Возвращает сотрудника института по ID.

### Community 308 - "Вариант 1: импорт схемы с автообновлением"
Cohesion: 0.33
Nodes (5): Postman и OpenAPI, Вариант 1: импорт схемы с автообновлением, Импорт в Postman, Обновить локальный файл схемы (опционально), Ручная коллекция с ролями

### Community 309 - "DepartmentPlan.py"
Cohesion: 0.25
Nodes (6): DenyStudentPermission, Запрещает доступ пользователям с ролью student., DepartmentPlanSerializer, ViewSet для работы с планами подразделений по проектным заявкам., Сериализатор для создания/обновления плана подразделения., Список/создание — staff; свой план подразделения — не student.

### Community 310 - "ProjectApplicationViewSet"
Cohesion: 0.14
Nodes (8): ProjectApplicationViewSet, Упрощенный ViewSet - только обработка HTTP запросов. Вся бизнес-логика вынесена…, Переопределяем права доступа в зависимости от действия. `simple` — публичное…, DELETE отключён: заявки не удаляются через API., Выбор сериализатора в зависимости от действия, GET /api/project-applications/{id}/ Получение заявки по ID с доступными…, PUT /api/project-applications/{id}/ Полное обновление заявки, PATCH /api/project-applications/{id}/ Частичное обновление заявки

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

### Community 320 - "ProjectViewSet"
Cohesion: 0.25
Nodes (5): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией.

### Community 323 - "ApplicationInvolvedDepartment"
Cohesion: 0.29
Nodes (6): ApplicationInvolvedDepartment, Причастные подразделения к заявке, direction(), fixture, Тесты ProjectTrackDomain., semester()

### Community 324 - "showcase/urls.py"
Cohesion: 0.20
Nodes (8): ApplicationStatusViewSet, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, InstituteSerializer, InstituteViewSet, Meta, ViewSet только для чтения институтов/академий. Доступен для всех пользователей.…, Переопределяем list для возврата всех институтов без пагинации., Сериализатор для институтов/академий.

### Community 329 - "StudentShowcaseRepository"
Cohesion: 0.10
Nodes (11): Команда пользователя в семестре с блокировкой строки., Запросы и запись для студенческой витрины проектов., Команда пользователя в семестре (без блокировки)., Связь проект↔трек с проверкой семестра и статуса approved., Треки группы в семестре с одобренными проектами и тегами., Счётчик записанных команд с блокировкой строк TeamSemester проекта., Привязывает проект к команде и пишет лог., Карта (track_id, application_id) → число записанных команд. (+3 more)

### Community 331 - "ProjectTrackApplication"
Cohesion: 0.29
Nodes (5): ProjectTrackApplicationInline, Инлайн проектных заявок в проектном треке., ProjectTrackApplication, Связь проектного трека с проектной заявкой., Добавляет заявки в трек; возвращает число созданных связей.

### Community 338 - "ProjectTrackGroup"
Cohesion: 0.29
Nodes (5): ProjectTrackGroupInline, Инлайн учебных групп в проектном треке., ProjectTrackGroup, Связь проектного трека с учебной группой., Добавляет группы в трек; возвращает число созданных связей.

### Community 341 - "ProjectTrackProjectListDTO"
Cohesion: 0.29
Nodes (4): ProjectTrackProjectListDTO, DTO проекта со счётчиком назначенных групп., Преобразует DTO в словарь для API., Список проектов семестра со счётчиком назначенных групп.

### Community 344 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 349 - "ProjectTrackUpdateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackUpdateSerializer, Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

### Community 350 - "format_validation_errors"
Cohesion: 0.33
Nodes (4): format_validation_errors(), POST /api/project-applications/ Создание заявки - только обработка HTTP, Форматирует ошибки валидации используя стандартные DRF механизмы. Args: errors:…, POST /api/project-applications/simple/ Создание заявки без авторизации

### Community 351 - ".list"
Cohesion: 0.33
Nodes (3): Возвращает QuerySet для списка заявок. DRF автоматически применит пагинацию., GET /api/project-applications/ Получение списка заявок с пагинацией. Query:…, GET /api/project-applications/my_applications/

### Community 353 - "django_db"
Cohesion: 0.29
Nodes (5): django_db, Тесты для получения конкретного тега через API., Получение тега с доступом возвращает тег., Получение тега без доступа возвращает 403., TestTagViewSetRetrieve

### Community 355 - "Текущий статус реализации"
Cohesion: 0.40
Nodes (5): ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации, 🔧 Требует доработки

### Community 359 - "ProjectTrackAddApplicationsSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationsSerializer, Список заявок с рекомендуемым числом команд и лимитами размера., Проверяет отсутствие дубликатов id в одном запросе.

### Community 360 - "ProjectTrackCreateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackCreateSerializer, Сериализатор для создания проектного трека., Проверяет согласованность лимитов размера команды.

## Knowledge Gaps
- **271 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+266 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **114 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `TestCanCreateTag`, `ProjectTrackService`, `accounts/views.py`, `ApplicationDashboardService`, `StudyGroupService`, `APIClient`, `StudyGroupMemberDTO`, `UserManagementService`, `UserListDTO`, `PermissionError`, `UserManagementViewSet`, `AvailableActionDTO`, `MentorGroupsDomain`, `ProjectTrack`, `._get_track_with_access`, `test_study_group_domain.py`, `Role`, `StudentShowcaseDomain`, `PreRegisteredStudent`, `Tag`, `.calculate_initial_status`, `test_institute_responsible_viewset.py`, `TeamLobbyService`, `TestCanUpdateTag`, `teams/views.py`, `.list_active_groups`, `DepartmentPlan.py`, `DirectionService`, `showcase/models.py`, `APIView`, `ProjectApplicationCreateDTO`, `UserSerializer`, `ProjectTrackDomain`, `InstituteResponsibleGroupDTO`, `accounts/admin.py`, `InvolvedManager`, `TeamLobbyDomain`, `.approve_application`, `UserManagementDomain`, `Semester`, `tests/conftest.py`, `ProjectTrackProjectDetailDTO`, `TagService`, `.get_filtered_queryset`, `TeamSemester`, `ProjectTrackPermission`, `.view_application`, `MentorGroupDetailDTO`, `MentorTeamService`, `accounts/permissions.py`, `TestCanDeleteTag`, `ProjectTrackProjectListDTO`, `.handle`, `InstituteResponsibleService`, `PasswordResetSerializer`, `.ensure_student_with_group`, `.ensure_is_captain`, `Direction`, `test_my_study_group_viewset.py`, `ApplicationLoggingService`, `.get_filtered_queryset`, `institute_access.py`, `StudentShowcaseService`, `.resolve_list_semester_id`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `TestCanCreateTag`, `TestProjectViewSet`, `ProjectTrackService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `StudyGroupService`, `TestApplicationDashboardService`, `test_mentor_groups_viewset.py`, `ApplicationNotificationService`, `APIClient`, `TagCreateDTO`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `TestDepartmentPlanViewSetList`, `test_mentor_showcase_viewset.py`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `TestProjectApplicationViewSetIsInternalCustomer`, `test_project_track_viewset.py`, `ProjectTrack`, `TestTagViewSetCreate`, `test_study_group_domain.py`, `test_tag_viewset.py`, `ProjectApplicationService`, `PreRegisteredStudent`, `TestTagViewSetDelete`, `test_direction_domain.py`, `test_team_lobby_viewset.py`, `test_institute_responsible_viewset.py`, `TestCanUpdateTag`, `DirectionService`, `TestTagViewSet`, `showcase/models.py`, `ProjectApplicationCreateDTO`, `ProjectTrackDomain`, `test_user_me_student.py`, `UserManagementDomain`, `Semester`, `tests/conftest.py`, `.get_filtered_queryset`, `TagService`, `TestApplicationDashboardViewSet`, `TestCanDeleteTag`, `.handle`, `test_import_preregistered_students.py`, `StudyGroup`, `MentorGroupsRepository`, `InstituteResponsibleService`, `django_db`, `TestProjectApplicationViewSetTransferToInstitute`, `test_project_application_viewset.py`, `APIClient`, `ApplicationLoggingService`, `test_my_study_group_viewset.py`, `test_team_semester_models.py`, `.get_filtered_queryset`, `test_my_team_viewset.py`, `ProjectService`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `make_user`, `ProjectTrackService`, `accounts/views.py`, `ApplicationDashboardService`, `StudyGroupService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `TestProjectViewSet`, `TestApplicationDashboardService`, `test_mentor_groups_viewset.py`, `APIClient`, `test_mentor_showcase_viewset.py`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `TestDepartmentPlanViewSetList`, `Command`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `test_project_track_viewset.py`, `MentorGroupsDomain`, `ProjectTrack`, `generate_ief_test_data.py`, `ProjectApplicationService`, `test_team_lobby_viewset.py`, `test_institute_responsible_viewset.py`, `TeamLobbyService`, `teams/views.py`, `DepartmentPlan.py`, `ProjectApplicationViewSet`, `test_import_study_groups_from_contingent.py`, `showcase/models.py`, `accounts/admin.py`, `ApplicationInvolvedDepartment`, `DepartmentPlanViewSet`, `TeamSemester`, `MentorTeamService`, `AccountsApiTests`, `.handle`, `MentorTeamViewSet`, `StudyGroup`, `InstituteResponsibleService`, `test_project_application_viewset.py`, `test_my_study_group_viewset.py`, `test_team_semester_models.py`, `institute_access.py`, `StudentShowcaseService`, `test_my_team_viewset.py`, `ProjectService`, `.resolve_list_semester_id`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 537 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 537 INFERRED edges - model-reasoned connections that need verification._
- **Are the 50 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Are the 76 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 76 INFERRED edges - model-reasoned connections that need verification._
- **Are the 70 inferred relationships involving `Semester` (e.g. with `Command` and `SemesterSerializer`) actually correct?**
  _`Semester` has 70 INFERRED edges - model-reasoned connections that need verification._