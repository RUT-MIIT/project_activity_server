# Graph Report - project_activity_server  (2026-08-31)

## Corpus Check
- 343 files · ~154,976 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5122 nodes · 10269 edges · 373 communities (238 shown, 135 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1013 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9dcb8800`
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
- test_institute_responsible_viewset.py
- TagRepository
- ApplicationDashboardService
- ApplicationDashboardRepository
- _enrollment_with_mentors
- ._collect_group_rows
- MentorTeamRepository
- APIClient
- prepare_study_groups_xlsx.py
- StudyGroupMemberDTO
- ProjectTrack
- UserManagementService
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- PreRegisteredStudentService
- ApplicationDashboardDomain
- StudyGroupViewSet
- TestStudentShowcaseEnroll
- normalize_cell
- TeamLobbyService
- TestTeamLobbyViewSet
- PreRegisteredStudentRepository
- TestProjectApplicationViewSetIsInternalCustomer
- AvailableActionDTO
- TagCreateDTO
- project_track_service.py
- ProjectTrackViewSet
- TestTagViewSetCreate
- TestTagViewSet
- ProjectService
- ProjectApplicationService
- StudentShowcaseDomain
- PreRegisteredStudent
- .update_application
- .calculate_initial_status
- .create_tag
- CommentService
- Path
- InstituteResponsibleEmployeeDTO
- ._get_track_with_access
- test_prod_users_client.py
- TagDomain
- Tag.py
- TeamSemesterViewSet
- DirectionService
- TestDepartmentPlanViewSetList
- test_import_study_groups_from_contingent.py
- TestProjectViewSet
- ValidationResult
- ProjectApplicationReadDTO
- ProjectTrackPermission
- PreRegisteredStudentViewSet
- showcase/urls.py
- ProjectTrackDomain
- TagUpdateDTO
- showcase/admin.py
- Примеры использования поля is_internal_customer
- TeamLobbyRepository
- TeamLobbyDomain
- .can_change_status
- Role
- accounts/admin.py
- MentorTeamService
- .can_user_access_application
- .get_filtered_queryset
- DepartmentPlanViewSet
- ProjectTrackRepository
- .view_application
- ._authorize_and_load
- TestApplicationDashboardViewSet
- TestSubmitApplicationService
- TestCanCreateTag
- Витрина проектов (студент) — API для фронта
- serialize_comment_author
- API для работы с проектными заявками
- AccountsApiTests
- TestCanDeleteTag
- build_user_indexes
- PermissionError
- Command
- Управление командой
- ApplicationCapabilities
- .approve_application
- Any
- TestInstituteResponsibleViewSet
- mentor_team_service.py
- .get_filtered_queryset
- extract.py
- User
- InstituteResponsibleViewSet
- .can_edit_application
- TestProjectApplicationViewSetTransferToInstitute
- UserRepository
- extract_group_abbrev.py
- ProjectApplication
- API Документация - Проектные заявки
- Command
- Any
- .get_dashboard
- .resolve_list_semester_id
- ProjectApplication.py
- TestProjectApplicationListSemesterFilter
- .validate_create
- _generate_collection.py
- StudyGroup
- ApplicationLoggingService
- get_root_department
- ._resolve_context
- accounts/urls.py
- institute_access.py
- StudentShowcaseService
- TestMyTeamViewSet
- sync_project_teachers.py
- StudentShowcaseViewSet
- .should_require_consultation
- Поддержка multipart/form-data
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- ProjectTrackStatisticsDTO
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
- APIClient
- schema.py
- ShowcaseConfig
- UserSerializer
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- test_user_me_student.py
- .list_event_logs
- 0011_migrate_team_data.py
- test_import_preregistered_students.py
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- utils.py
- .get_filtered_queryset
- test_student_showcase_viewset.py
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- test_mentor_showcase_viewset.py
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
- PlaceholderUserService
- PasswordChangeSerializer
- RutMiitClient
- ProjectListDTO
- TestTagViewSetDelete
- ProjectViewSet
- Command
- MentorGroupStudentDTO
- TagService
- ._track_detail_queryset
- teams/models.py
- ApplicationDashboard.py
- 0021_user_placeholder_preregistered_flag.py
- MentorGroupsService
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
- load_users_from_json
- ProjectTrackGroupListDTO
- ProjectTrackProjectListDTO
- ProjectTrackGroupProjectDTO
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
- PasswordResetSerializer
- UserManager
- ProjectTrackAddApplicationItemSerializer
- ProjectApplicationRepository
- Схема БД: студенческий портал
- Справочные эндпоинты
- Парсинг «Проектная деятельность» — РУТ (МИИТ)
- Semester
- Валидационные правила
- InstituteResponsibleService
- ProjectTrackAddApplicationsSerializer
- .handle
- ProjectRepository
- 0017_copy_studygroup_mentors_to_semester.py
- ProjectTrackCreateSerializer
- ProjectTrackUpdateSerializer
- ._format_external_share_chart
- .recalculate_recommended_teams_count
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- ._ensure_valid_status_after_department_check
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
- .reload_team_semester
- CustomResetPasswordForm
- dto/project.py
- InstituteSerializer
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- TeamSemester
- .test_password_change_success
- TeamPermission
- .test_password_change_wrong_current_password
- .test_password_reset_sends_email
- .test_registration_request_approve_allowed_for_cpds_user
- .test_registration_request_approve_creates_user_and_sends_email
- .test_registration_request_approve_forbidden_for_regular_user
- .test_registration_request_approve_mail_failure_returns_400_and_no_user_created
- .test_registration_request_create_invalid_department
- .test_registration_request_list_requires_privileged_user
- .test_registration_request_race_condition_integrity_error
- .test_registration_request_reject_allowed_for_cpds_user
- .test_registration_request_reject_changes_status_and_sends_email
- .test_registration_request_reject_mail_failure_still_returns_200_and_keeps_rejected_status
- 0018_studygroupsemester_mentors_m2m.py
- .test_semester_create_allowed_for_admin_and_cpds
- .test_semester_list_requires_auth
- .test_user_me_institute_code_none_if_no_institute
- .test_user_me_requires_auth_and_returns_profile
- .test_user_roles_retrieve_by_code
- .get_statistics_overall
- .update
- .list_pending_join_requests_for_user
- .map_pending_join_request_ids
- .get_track_for_group
- .user_has_team_in_semester
- .get_team_semester
- .create_join_request
- .create_invitation
- .mark_user_requests_obsolete
- .update_join_request_status
- .update_invitation_status
- .remove_member_force
- .delete_team_semester
- .group_team_semesters_by_track
- .get_user
- .list_group_team_semesters
- .get_user_team_semester
- .get_my_team_detail
- data/conftest.py
- timetable

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 529 edges
2. `User` - 253 edges
3. `ProjectApplication` - 148 edges
4. `Department` - 142 edges
5. `ProjectApplicationService` - 136 edges
6. `Semester` - 133 edges
7. `StudyGroup` - 121 edges
8. `ProjectApplicationCreateDTO` - 109 edges
9. `PreRegisteredStudent` - 78 edges
10. `Institute` - 74 edges

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

## Communities (373 total, 135 thin omitted)

### Community 0 - "MentorTeamViewSet"
Cohesion: 0.14
Nodes (17): MentorTeamSetCaptainSerializer, MentorTeamUpdateNameSerializer, MentorTeamViewSet, Request, Response, DELETE /study-groups/{groupId}/teams/{teamSemesterId}/ — удалить команду., PATCH /study-groups/{groupId}/teams/{teamSemesterId}/captain/., Тело PATCH переименования команды. (+9 more)

### Community 1 - "make_user"
Cohesion: 0.04
Nodes (21): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+13 more)

### Community 2 - "Department"
Cohesion: 0.03
Nodes (76): Command, BaseCommand, Department, create_test_user(), Создаем тестового пользователя, Общие константы приложения showcase., Доменная логика студенческой витрины проектов., Доменная логика для тегов - чистые функции без эффектов. (+68 more)

### Community 3 - "Ответственный по институту — API для фронта"
Cohesion: 0.08
Nodes (24): 1. Список активных групп института, 2. Сотрудники института, 3. Группы с назначенными наставниками, 4. Назначить наставника группе, 5. Снять наставника с группы, Значения `semester_id`, Общие query-параметры, Ответ `200` (+16 more)

### Community 4 - "ProjectTrackService"
Cohesion: 0.13
Nodes (6): Создаёт DTO из словаря., ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), django_db, TestProjectTrackService

### Community 5 - "accounts/views.py"
Cohesion: 0.08
Nodes (31): AcademicYear, Meta, RegistrationRequest, Status, IsCpdsUser, Пользовательские permissions для приложения accounts., Разрешает доступ только сотрудникам, администраторам или роли ЦПДС., Разрешает доступ только пользователям с ролью ЦПДС (код роли `cpds`). (+23 more)

### Community 6 - "action"
Cohesion: 0.12
Nodes (9): action, extend_schema, POST /api/semesters/{id}/assign-empty-applications Присваивает переданный…, POST /api/project-applications/{id}/approve/ Одобрение заявки, POST /api/project-applications/{id}/reject/ Отклонение заявки, POST /api/project-applications/{id}/request_changes/ Запрос изменений (отправка…, POST /api/project-applications/{id}/transfer_to_institute/ Передача заявки в…, POST /api/project-applications/{id}/return_by_author/ Отзыв заявки автором… (+1 more)

### Community 7 - "Any"
Cohesion: 0.07
Nodes (16): ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO, ProjectTrackProjectGroupDTO, Any, Преобразует DTO в словарь для API., DTO заявки в проектном треке., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API. (+8 more)

### Community 8 - "test_institute_responsible_viewset.py"
Cohesion: 0.23
Nodes (9): DTO для API ответственного по институтам., Репозиторий для StudyGroupSemester и связанных выборок., api_client(), direction(), other_institute(), fixture, Тесты API ответственного по институтам., semester() (+1 more)

### Community 9 - "TagRepository"
Cohesion: 0.06
Nodes (29): Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, TagRepository, django_db, get_by_id возвращает общий тег. (+21 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.06
Nodes (33): ApplicationDashboardService, Оркестрация получения данных дашборда заявок., _create_app(), django_db, fixture, Тесты ApplicationDashboardService., Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external. (+25 more)

### Community 11 - "ApplicationDashboardRepository"
Cohesion: 0.07
Nodes (30): ApplicationDashboardRepository, Q, QuerySet, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению., Строит карту institute_code -> множество id заявок. (+22 more)

### Community 12 - "_enrollment_with_mentors"
Cohesion: 0.27
Nodes (5): _enrollment_with_mentors(), APIClient, django_db, TestMentorGroupsQueryPerformance, TestMentorGroupsViewSet

### Community 13 - "._collect_group_rows"
Cohesion: 0.18
Nodes (11): GroupImportRow, Строка отчёта, подготовленная к импорту одной учебной группы., Command, BaseCommand, DataFrame, date, Path, Читает отчёт контингента; заголовок колонок — вторая строка. (+3 more)

### Community 14 - "MentorTeamRepository"
Cohesion: 0.07
Nodes (15): MentorTeamRepository, Удаляет участника любой роли., Меняет статус состава., Удаляет семестровый контекст и постоянную команду при необходимости., Запросы и записи для API команд наставника., Пишет запись в лог команды., True, если пользователь уже в команде в семестре., Пользователь по id или None. (+7 more)

### Community 15 - "APIClient"
Cohesion: 0.14
Nodes (18): api_client(), _approved_app(), direction(), _enrollment_with_mentors(), mentor_team_setup(), Any, APIClient, django_db (+10 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroupMemberDTO"
Cohesion: 0.38
Nodes (3): Any, Строка списка группы из контингента., StudyGroupMemberDTO

### Community 18 - "ProjectTrack"
Cohesion: 0.08
Nodes (31): Трек с вложенными проектами для витрины., StudentShowcaseTrackDTO, ProjectTrack, ProjectTrackApplication, ProjectTrackGroup, Проектный трек — контейнер для назначения групп и заявок в рамках семестра., Связь проектного трека с учебной группой., Связь проектного трека с проектной заявкой. (+23 more)

### Community 19 - "UserManagementService"
Cohesion: 0.08
Nodes (25): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, ViewSet для управления пользователями. (+17 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.10
Nodes (11): Преобразование в DTO - никакой бизнес-логики, Тесты для ProjectApplicationCreateDTO., Создание DTO из словаря через from_dict., Преобразование DTO в словарь через to_dict., Проверяем значения по умолчанию: пустые строки для title, company_contacts,…, Явно переданное значение needs_consultation сохраняется., По умолчанию is_internal_customer равен False., Явно переданное значение is_internal_customer=True сохраняется. (+3 more)

### Community 22 - "PreRegisteredStudentService"
Cohesion: 0.13
Nodes (11): PreRegisteredStudentLookupResult, PreRegisteredStudentService, atomic, Сервис предрегистрации и регистрации студентов из контингента., Отправляет администратору письмо о расхождении данных. Raises: ValueError: если…, Отправляет студенту письмо после успешной регистрации., Результат поиска предрегистрации., Сериализует результат для API. (+3 more)

### Community 23 - "ApplicationDashboardDomain"
Cohesion: 0.08
Nodes (20): get_department_subtree_ids(), Возвращает id корневого подразделения и всех его потомков., ApplicationDashboardDomain, DashboardFilters, Доменная логика дашборда проектных заявок., Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп., Парсит query-параметр application_type. (+12 more)

### Community 24 - "StudyGroupViewSet"
Cohesion: 0.13
Nodes (13): Any, DTO для чтения учебной группы., StudyGroupReadDTO, action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/my-groups/ — группы наставника в семестре. (+5 more)

### Community 25 - "TestStudentShowcaseEnroll"
Cohesion: 0.09
Nodes (10): _approved_app(), _create_assembled_team(), django_db, Число SQL не растёт пропорционально числу проектов., После заполнения последнего слота вторая команда получает 400., Один участник при min_team_members=2., TestStudentShowcaseAccess, TestStudentShowcaseDetail (+2 more)

### Community 26 - "normalize_cell"
Cohesion: 0.13
Nodes (16): build_preregistered_student_import_row(), last_names_match(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки. (+8 more)

### Community 27 - "TeamLobbyService"
Cohesion: 0.05
Nodes (54): PageNumberPagination, ApproveJoinRequestSerializer, CreateInvitationSerializer, CreateTeamSerializer, MyTeamViewSet, action, extend_schema, extend_schema_view (+46 more)

### Community 28 - "TestTeamLobbyViewSet"
Cohesion: 0.14
Nodes (7): _create_captained_team(), django_db, Команда без трека при одном треке у группы → min/max с трека группы., После создания своей команды pending-заявка в чужую → obsolete., При нескольких треках track_id не проставляется; лимиты — effective по трекам., Если группе доступен один трек — он проставляется без track_id в body., TestTeamLobbyViewSet

### Community 29 - "PreRegisteredStudentRepository"
Cohesion: 0.10
Nodes (11): PreRegisteredStudentRepository, QuerySet, Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по табельному номеру., Возвращает предрегистрацию по нормализованному СНИЛС., Возвращает предрегистрацию по первичному ключу., Удаляет предрегистрации без привязанного пользователя. (+3 more)

### Community 30 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "TagCreateDTO"
Cohesion: 0.11
Nodes (13): DTO для создания тега., TagCreateDTO, Создание тега в БД. Args: dto: DTO с данными для создания тега Returns:…, Нельзя создать тег с таким же именем и таким же набором подразделений., Остальные роли не могут создавать теги., Тесты для метода create_tag сервиса., cpds может создавать общие теги., cpds не может создавать теги с подразделением. (+5 more)

### Community 33 - "project_track_service.py"
Cohesion: 0.07
Nodes (27): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackAggregatedStatisticsDTO, ProjectTrackCreateDTO, ProjectTrackGroupDetailDTO, ProjectTrackProjectDetailDTO, ProjectTrackUpdateDTO (+19 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.13
Nodes (23): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+15 more)

### Community 35 - "TestTagViewSetCreate"
Cohesion: 0.12
Nodes (9): Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем., Нельзя создать общий тег, если имя уже используется (общим или departmental… (+1 more)

### Community 36 - "TestTagViewSet"
Cohesion: 0.06
Nodes (21): django_db, Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Тесты для обновления тегов через API., cpds может обновлять общие теги. (+13 more)

### Community 37 - "ProjectService"
Cohesion: 0.21
Nodes (5): ProjectService, Оркестрация Domain + Repository для списка проектов., TestProjectApplicationNewFieldsLists, django_db, TestProjectService

### Community 38 - "ProjectApplicationService"
Cohesion: 0.03
Nodes (64): ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка., Бизнес-операция: получение заявок по статусу., Бизнес-операция: получение последних заявок. (+56 more)

### Community 39 - "StudentShowcaseDomain"
Cohesion: 0.05
Nodes (32): Правила доступа и записи команды на проект витрины., Проверяет роль student и наличие учебной группы; возвращает group_id., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI). (+24 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.14
Nodes (12): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если студент прошёл полную регистрацию (не псевдо-user)., MonkeyPatch, Контингент группы с командой студента в семестре (без N+1)., Any, APIClient, django_db (+4 more)

### Community 41 - ".update_application"
Cohesion: 0.15
Nodes (9): Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Не-автор и не-ЦПДС не может редактировать заявку., Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult., CPDS может редактировать одобренные заявки., institute_validator-автор: save совпадает с available_actions (подразделение…, institute_validator без причастного подразделения не может сохранить. (+1 more)

### Community 42 - ".calculate_initial_status"
Cohesion: 0.17
Nodes (9): Определение начального статуса на основе роли пользователя. Чистая функция -…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds., Обычный пользователь создаёт заявки в статусе await_department., Неизвестная роль возвращает статус await_department по умолчанию. (+1 more)

### Community 43 - ".create_tag"
Cohesion: 0.18
Nodes (6): atomic, Бизнес-операция: удаление тега. Args: tag_id: ID тега для удаления user:…, Бизнес-операция: присоединение подразделения к тегу. Args: tag_id: ID тега…, Бизнес-операция: отцепление подразделения от тега. Если тег не базовый…, Бизнес-операция: создание тега. Args: dto: DTO с данными для создания тега…, Бизнес-операция: обновление тега. Args: tag_id: ID тега для обновления dto: DTO…

### Community 44 - "CommentService"
Cohesion: 0.08
Nodes (20): ProjectApplicationComment, CommentService, atomic, Сервис для управления комментариями к проектным заявкам. Обеспечивает…, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db (+12 more)

### Community 45 - "Path"
Cohesion: 0.15
Nodes (13): aga_institute(), direction(), Any, django_db, fixture, Path, Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта. (+5 more)

### Community 46 - "InstituteResponsibleEmployeeDTO"
Cohesion: 0.10
Nodes (11): InstituteResponsibleEmployeeDTO, InstituteResponsibleGroupDTO, InstituteResponsibleGroupMentorsDTO, InstituteResponsibleGroupWithMentorDTO, InstituteResponsibleMentorDTO, Any, Компактное представление учебной группы., Сотрудник института (id + ФИО). (+3 more)

### Community 47 - "._get_track_with_access"
Cohesion: 0.11
Nodes (15): ProjectTrackReadDTO, DTO для чтения проектного трека., atomic, Возвращает трек с проверкой доступа., Возвращает детали трека., Создаёт проектный трек., Проставляет лимиты размера команды всем заявкам трека., Обновляет основные поля трека и лимиты команд у заявок. (+7 more)

### Community 48 - "test_prod_users_client.py"
Cohesion: 0.11
Nodes (23): fetch_users(), obtain_token(), Any, Path, Клиент prod API для обновления снимка пользователей., Получает JWT access token по email и паролю., Возвращает Bearer token из CLI, env или login., Загружает список пользователей с prod API. (+15 more)

### Community 49 - "TagDomain"
Cohesion: 0.10
Nodes (14): Чистая бизнес-логика для тегов - только функции, никаких эффектов., Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, TagDomain, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением. (+6 more)

### Community 50 - "Tag.py"
Cohesion: 0.05
Nodes (37): Разрешает доступ к управлению тегами только для ролей cpds, admin и…, TagManagePermission, Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Инициализация из модели Tag., Преобразование в словарь., TagReadDTO (+29 more)

### Community 51 - "TeamSemesterViewSet"
Cohesion: 0.22
Nodes (9): action, Request, Response, POST /api/teams/team-semesters/{id}/members/ — добавить участника., DELETE /api/teams/team-semesters/{id}/members/{member_id}/., GET /api/teams/teams/my/?semester_id= — команды пользователя в семестре., CRUD для участия команды в семестре и управления составом., GET /api/teams/team-semesters/my/?semester_id= — команды пользователя. (+1 more)

### Community 52 - "DirectionService"
Cohesion: 0.16
Nodes (10): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений., DirectionService, Оркестрация Domain + Repository для Direction., Список направлений с фильтрацией по роли., Направление по коду с проверкой доступа. (+2 more)

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

### Community 57 - "ProjectApplicationReadDTO"
Cohesion: 0.06
Nodes (26): Exception, build_author_short_name(), ProjectApplicationReadDTO, Формирует короткое имя вида 'Фамилия И.О.' или возвращает None., DTO для чтения заявки - оптимизированный набор полей, django_db, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки. (+18 more)

### Community 58 - "ProjectTrackPermission"
Cohesion: 0.08
Nodes (23): IsAdminOrCpds, IsInstituteValidator, ProjectManagementPermission, ProjectTrackPermission, APIView, BasePermission, Request, Разрешает доступ к проектным трекам для admin, cpds и institute_validator. (+15 more)

### Community 59 - "PreRegisteredStudentViewSet"
Cohesion: 0.13
Nodes (18): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Отправляет администратору письмо о расхождении данных., Публичные операции предрегистрации студентов. (+10 more)

### Community 60 - "showcase/urls.py"
Cohesion: 0.18
Nodes (10): ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…, InstituteViewSet (+2 more)

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.07
Nodes (18): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя. (+10 more)

### Community 62 - "TagUpdateDTO"
Cohesion: 0.11
Nodes (13): DTO для обновления тега., TagUpdateDTO, Обновление тега. Обновляет только переданные поля. Args: tag: Тег для…, Тесты для метода update репозитория., Обновление названия тега., Обновление категории тега., Обновление подразделений тега., Удаление подразделений из тега (установка departments=[]). (+5 more)

### Community 63 - "showcase/admin.py"
Cohesion: 0.11
Nodes (20): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+12 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "TeamLobbyRepository"
Cohesion: 0.08
Nodes (12): Pending-приглашения студента в семестре., Число команд группы в треке в семестре., Создаёт Team + TeamSemester + капитана-участника., Заявка с командой и заявителем., Запросы и записи для студенческого лобби команд., Приглашение со связями., Добавляет участника в команду семестра., Треки группы в семестре (recommended_teams_count уже на модели трека). (+4 more)

### Community 66 - "TeamLobbyDomain"
Cohesion: 0.04
Nodes (42): ViewSet студенческой витрины проектов., Удаление: капитан, forming, в составе только он., Подтверждение состава: капитан, forming, размер в лимитах трека., Заявка должна быть в статусе pending., Приглашение должно быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды»., Лимиты размера команды. Приоритет: 1) трек команды; 2) effective по трекам…, True, если студент без команды и есть свободный слот. (+34 more)

### Community 67 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 68 - "Role"
Cohesion: 0.07
Nodes (18): QuerySet, Доменная логика управления пользователями., Проверяет, что пользователь доступен в отфильтрованном queryset., Правила доступа и валидации для управления пользователями., Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя. (+10 more)

### Community 69 - "accounts/admin.py"
Cohesion: 0.24
Nodes (11): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+3 more)

### Community 70 - "MentorTeamService"
Cohesion: 0.06
Nodes (19): MentorGroupsDomain, Проверяет, что учебная группа существует., Проверяет, что учебная группа не завершила обучение., Проверяет, что пользователь назначен наставником группы в семестре., Проверки для API «Мои группы» наставника., MentorTeamDomain, Чистая бизнес-логика API команд наставника., Проверяет, что команда принадлежит учебной группе. (+11 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.14
Nodes (11): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Тесты для проверки доступа пользователя к заявке., Автор всегда имеет доступ к своей заявке., Админ имеет доступ ко всем заявкам., Модератор имеет доступ ко всем заявкам., CPDS имеет доступ ко всем заявкам., Валидатор подразделения имеет доступ ко всем заявкам., Валидатор института имеет доступ ко всем заявкам. (+3 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.14
Nodes (11): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., Тесты для фильтрации queryset тегов по ролям., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения., institute_validator без подразделения видит только общие теги. (+3 more)

### Community 73 - "DepartmentPlanViewSet"
Cohesion: 0.17
Nodes (14): DepartmentPlanSerializer, DepartmentPlanViewSet, action, extend_schema, Request, Response, Получить словарь планов по подразделениям для указанного семестра., Получить статистику заявок по статусам для каждого подразделения. (+6 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.08
Nodes (12): ProjectTrackRepository, Создаёт проектный трек., Удаляет группу из трека; True если связь была., Возвращает id заявок, уже привязанных к треку., Добавляет заявки в трек; возвращает число созданных связей., Удаляет заявку из трека; True если связь была., Количество групп в треке., Доступ к данным проектных треков. (+4 more)

### Community 75 - ".view_application"
Cohesion: 0.15
Nodes (8): Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Автор всегда имеет доступ к просмотру своей заявки., Обычному пользователю чужая заявка недоступна., Список заявок разрешён всем (возвращает True)., TestViewAndList

### Community 76 - "._authorize_and_load"
Cohesion: 0.16
Nodes (13): Any, atomic, Обновляет название команды., Назначает нового капитана из состава команды., Подтверждает состав команды (forming → assembled)., Возвращает состав на редактирование (assembled → forming)., Добавляет зарегистрированного или незарегистрированного студента., Удаляет участника из команды. (+5 more)

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - "TestSubmitApplicationService"
Cohesion: 0.09
Nodes (12): Если needs_consultation не передан, значение остается False по умолчанию., При создании упрощенной заявки устанавливается is_external=True и статус…, При создании упрощенной заявки добавляется причастное подразделение ЦПДС., При создании обычной заявки is_external=False по умолчанию., Заявка автоматически переходит в await_institute, если в подразделении нет…, Заявка остаётся в await_department, если в подразделении есть…, Успешная подача заявки: создаётся со статусом created, затем переводится в…, Заявка остаётся в await_department, если валидатор есть в родительском… (+4 more)

### Community 79 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 80 - "Витрина проектов (студент) — API для фронта"
Cohesion: 0.14
Nodes (13): 1. Список треков с проектами, 2. Детали проекта, 3. Записать команду на проект, Витрина проектов (студент) — API для фронта, Ответ `200`, Ответ `200`, Ответ `200`, Ошибки (+5 more)

### Community 81 - "serialize_comment_author"
Cohesion: 0.14
Nodes (11): Сериализует автора комментария с role и department. Args: author: User объект…, serialize_comment_author(), POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, Тесты для функции serialize_comment_author., Если author равен None, возвращаются None значения., Сериализация автора с полными данными: имя, фамилия, отчество, роль,…, Сериализация автора без отчества. (+3 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.11
Nodes (10): AccountsApiTests, override_settings, Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Аноним может создать заявку на регистрацию и она сохраняется в БД., Создание заявки без подразделения возвращает ошибку валидации., После отклонения заявки можно подать новую с тем же email., Повторная подача при активной заявке возвращает ошибку валидации., Нельзя подать заявку, если пользователь с таким email уже зарегистрирован. (+2 more)

### Community 84 - "TestCanDeleteTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, django_db, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения. (+3 more)

### Community 85 - "build_user_indexes"
Cohesion: 0.12
Nodes (26): main(), Сверка преподавателей из Excel со списком пользователей prod API. ..…, Отмечает преподавателей из Excel, которые есть в prod., build_user_indexes(), find_user(), normalize_name(), Сопоставление ФИО преподавателей с пользователями PD., Нормализует ФИО для сравнения. (+18 more)

### Community 86 - "PermissionError"
Cohesion: 0.10
Nodes (14): PermissionError, Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации., Бизнес-операция: получение заявок для координации пользователя. Для обычных…, QuerySet, UserType, Список треков по фильтрам. (+6 more)

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "Управление командой"
Cohesion: 0.08
Nodes (24): Query-параметры, Query-параметры, Query-параметры, Вернуть состав на редактирование, Витрина проектов, Детали группы наставника, Добавить участника, Карточка команды (+16 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.10
Nodes (18): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы., Возвращает список доступных действий согласно матрице. (+10 more)

### Community 90 - ".approve_application"
Cohesion: 0.10
Nodes (16): atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку., Бизнес-операция: отзыв заявки автором., Бизнес-операция: одобрение заявки. (+8 more)

### Community 91 - "Any"
Cohesion: 0.14
Nodes (10): Any, Преобразует DTO в словарь для API., Карточка проекта в списке трека витрины., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Детали проекта для студента (без контактов)., Преобразует DTO в словарь для API., StudentShowcaseProjectDetailDTO (+2 more)

### Community 92 - "TestInstituteResponsibleViewSet"
Cohesion: 0.10
Nodes (7): _enrollment_with_mentors(), APIClient, django_db, Создаёт запись группы в семестре с наставниками., TestInstituteResponsibleQueryPerformance, TestInstituteResponsibleViewSet, TestMyStudyGroupSemesterMentor

### Community 93 - "mentor_team_service.py"
Cohesion: 0.06
Nodes (40): Репозиторий предрегистрации студентов., Создание псевдо-аккаунтов для незарегистрированных студентов контингента., Доменная логика доступа наставника к учебной группе., MentorGroupDetailDTO, MentorGroupListDTO, MentorGroupListItemDTO, DTO для эндпоинта «Мои группы» наставника., Строка списка групп наставника. (+32 more)

### Community 94 - ".get_filtered_queryset"
Cohesion: 0.16
Nodes (8): QuerySet, Фильтрует направления: institute_validator — только из групп своего института., django_db, parametrize, Разрешение институтов по подразделению пользователя., Фильтрация queryset направлений по ролям., TestGetFilteredQueryset, TestGetUserInstituteCodes

### Community 95 - "extract.py"
Cohesion: 0.22
Nodes (16): main(), run(), export_marked_xlsx(), export_to_xlsx(), _group_columns(), Any, Экспортирует результаты парсинга с колонками сверки с PD., _collect_events() (+8 more)

### Community 96 - "User"
Cohesion: 0.05
Nodes (25): AbstractBaseUser, User, Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., QuerySet (+17 more)

### Community 97 - "InstituteResponsibleViewSet"
Cohesion: 0.17
Nodes (17): delete, AssignMentorSerializer, InstituteResponsiblePermission, InstituteResponsibleViewSet, action, BasePermission, extend_schema, Request (+9 more)

### Community 98 - ".can_edit_application"
Cohesion: 0.16
Nodes (9): Проверка права на редактирование заявки. Бизнес-правило: редактировать может…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку., Не-автор и не-ЦПДС не может редактировать чужую заявку., Нельзя редактировать заявки со статусом rejected (даже автору и cpds)., Нельзя редактировать одобренные заявки (кроме админов и cpds)., Автор может редактировать заявку в статусе returned_*., CPDS может редактировать заявки в статусе rejected_department. (+1 more)

### Community 99 - "TestProjectApplicationViewSetTransferToInstitute"
Cohesion: 0.17
Nodes (8): Тесты для действия передачи заявки в институт по коду института., POST /api/showcase/project-applications/{id}/transfer_to_institute/ с…, Отсутствующий параметр code возвращает 400., Несуществующий код института возвращает 400 от сервиса., Институт без связанного подразделения возвращает 400., GET /api/showcase/project-applications/external/?status=... фильтрует внешние…, GET /api/showcase/project-applications/external/?status=... с несуществующим…, TestProjectApplicationViewSetTransferToInstitute

### Community 100 - "UserRepository"
Cohesion: 0.16
Nodes (8): QuerySet, Репозиторий для управления пользователями., Доступ к данным пользователей для управления., Базовый queryset без администраторов., Список пользователей с оптимизацией запросов., Возвращает пользователя по ID., Сохраняет изменения пользователя., UserRepository

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - "ProjectApplication"
Cohesion: 0.05
Nodes (36): Command, BaseCommand, ApplicationInvolvedUser, ApplicationStatus, ProjectApplication, Причастные пользователи к заявке, Совместимость с кодом, используемым как первичный ключ., ApplicationNotificationService (+28 more)

### Community 103 - "API Документация - Проектные заявки"
Cohesion: 0.17
Nodes (10): API Документация - Проектные заявки, Аутентификация, Базовый URL, Общая информация, ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации (+2 more)

### Community 104 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

### Community 105 - "Any"
Cohesion: 0.10
Nodes (11): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, Преобразование в DTO - никакой бизнес-логики, Тесты для ProjectApplicationUpdateDTO., Создание DTO для обновления из словаря. (+3 more)

### Community 106 - ".get_dashboard"
Cohesion: 0.17
Nodes (9): ApplicationDashboardDTO, Any, DTO для дашборда проектных заявок., Преобразует DTO в словарь для API., DTO блока KPI-карточек., DTO полного ответа дашборда., Преобразует DTO в словарь для API., SummaryCardsDTO (+1 more)

### Community 107 - ".resolve_list_semester_id"
Cohesion: 0.14
Nodes (8): Следующий семестр для новых заявок (Settings.next_semester_code)., Разбор query-параметра semester_id для GET-списков: id, next, actual., Any, Список треков с проектами для группы наставника в семестре., Any, Возвращает данные учебной группы текущего студента., django_db, TestSemesterResolveListSemesterId

### Community 108 - "ProjectApplication.py"
Cohesion: 0.12
Nodes (13): DenyStudentPermission, Запрещает доступ пользователям с ролью student., Список/создание — staff; свой план подразделения — не student., Meta, ProjectApplicationCreateSerializer, ProjectApplicationListSerializer, ProjectApplicationUpdateSerializer, Упрощенный ViewSet для проектных заявок с использованием новой архитектуры.… (+5 more)

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
Cohesion: 0.07
Nodes (35): Доменная логика для учебных групп., Фильтрация учебных групп по роли пользователя., StudyGroupDomain, MyStudyGroupDTO, DTO для эндпоинта «Моя группа»., Возвращает наставников: из семестра или fallback на StudyGroup.mentor., Полные данные учебной группы для текущего студента., StudyGroup (+27 more)

### Community 113 - "ApplicationLoggingService"
Cohesion: 0.04
Nodes (47): ProjectApplicationStatusLog, ApplicationLoggingService, atomic, Логирование удаления причастного пользователя. Args: application: Заявка user:…, Логирование добавления причастного подразделения. Args: application: Заявка…, Логирование удаления причастного подразделения. Args: application: Заявка…, Сервис для логирования изменений в проектных заявках. Обеспечивает полное…, Получение всех логов по заявке. Args: application: Заявка Returns:… (+39 more)

### Community 114 - "get_root_department"
Cohesion: 0.19
Nodes (9): get_root_department(), Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, django_db, Тесты для функции get_root_department., Подразделение без parent возвращает само себя., Подразделение с одним уровнем parent возвращает корневое., Подразделение с несколькими уровнями parent возвращает корневое., None на входе возвращает None. (+1 more)

### Community 115 - "._resolve_context"
Cohesion: 0.11
Nodes (12): InstituteResponsibleAssignMentorDTO, Ответ после изменения состава наставников., Any, Список активных групп института., Список сотрудников института., Группы с ID назначенных наставников в семестре., Назначает наставника группе в семестре., Снимает наставника с группы в семестре. (+4 more)

### Community 116 - "accounts/urls.py"
Cohesion: 0.13
Nodes (14): DepartmentViewSet, LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView, extend_schema, Request, Response (+6 more)

### Community 117 - "institute_access.py"
Cohesion: 0.09
Nodes (28): ID подразделений для фильтрации; None — без ограничения., ProjectDomain, Доменная логика для списка проектов., Проверяет, может ли пользователь получать список проектов., Коды институтов для фильтрации; None — без ограничения., Правила доступа и фильтрации для списка проектов., Доменная логика для проектных треков., application_available_for_institute() (+20 more)

### Community 118 - "StudentShowcaseService"
Cohesion: 0.17
Nodes (11): atomic, UserType, Записывает команду капитана на проект., Оркестрация Domain + Repository для студенческой витрины., Резолвит semester_id; по умолчанию actual., Список треков группы студента с проектами и счётчиками записи., Треки группы с проектами и enrolledTeamsCount (без проверки роли)., Детали проекта, доступного группе студента. (+3 more)

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → effective max(min)/min(max)., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "sync_project_teachers.py"
Cohesion: 0.15
Nodes (14): Возвращает базовый URL prod API., resolve_api_url(), main(), parse_all_groups(), _print_parse_summary(), Path, Парсинг расписания РУТ и сверка преподавателей с пользователями prod PD., Парсит преподавателей «Проектная деятельность» по всем группам. (+6 more)

### Community 121 - "StudentShowcaseViewSet"
Cohesion: 0.23
Nodes (10): action, extend_schema, extend_schema_view, Request, Response, Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/., GET /api/showcase/student-showcase/projects/{id}/. (+2 more)

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

### Community 126 - "ProjectTrackStatisticsDTO"
Cohesion: 0.18
Nodes (7): ProjectTrackInstituteStatisticsDTO, ProjectTrackStatisticsDTO, DTO статистики распределения проектов по группам., Преобразует DTO в словарь для API., DTO статистики по одному институту., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API.

### Community 127 - "Command"
Cohesion: 0.29
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
Cohesion: 0.06
Nodes (40): create_test_applications(), Создаем тестовые заявки, ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Явное выражение бизнес-намерений (не технических операций). Этот модуль…, Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи… (+32 more)

### Community 133 - "0014_add_intermediate_approved_statuses.py"
Cohesion: 0.33
Nodes (5): add_intermediate_approved_statuses(), Migration, Удаляет промежуточные статусы одобрения из БД., Добавляет промежуточные статусы одобрения в БД., remove_intermediate_approved_statuses()

### Community 134 - "TestDepartmentPlanViewSetMyDepartmentPlan"
Cohesion: 0.13
Nodes (9): django_db, Тесты для GET /api/showcase/department-plans/my-department-plan/ - план…, Успешное получение плана и статистики для подразделения пользователя., Если план отсутствует, возвращается 0, но статистика заявок учитывается., Ошибка: отсутствует semester_id., Ошибка: семестр не найден., Ошибка: у пользователя не указано подразделение., Ошибка: неавторизованный пользователь. (+1 more)

### Community 135 - "StudyGroupService"
Cohesion: 0.26
Nodes (4): Оркестрация Domain + Repository для StudyGroup., StudyGroupService, django_db, TestStudyGroupService

### Community 136 - "Руководство по ручному развертыванию Project Activity Server"
Cohesion: 0.15
Nodes (12): 10. Проверка и сопровождение, 11. Настройка nginx (backend + SPA), 1. Подготовка окружения, 2. Получение исходного кода, 3. Создание и активация виртуального окружения, 4. Настройка переменных окружения (.env), 5. Настройка PostgreSQL, 6. Миграции и статические файлы (+4 more)

### Community 137 - "4. Список проектов"
Cohesion: 0.15
Nodes (13): 2. Получение пользователя, 4. Список проектов, Query-параметры, Заголовки, Ошибки, Ошибки, Поведение по ролям, Права доступа (+5 more)

### Community 138 - "ProjectApplicationViewSet"
Cohesion: 0.07
Nodes (22): format_validation_errors(), get_error_message(), ProjectApplicationViewSet, GET /api/project-applications/external/ Получение списка всех внешних заявок…, Возвращает сообщение об ошибке в зависимости от режима DEBUG. Args: exception:…, Упрощенный ViewSet - только обработка HTTP запросов. Вся бизнес-логика вынесена…, Переопределяем права доступа в зависимости от действия. `simple` — публичное…, DELETE отключён: заявки не удаляются через API. (+14 more)

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
Nodes (6): GET /api/accounts/user/ возвращает код института, сопоставленного с…, Список департаментов доступен всем, детальный просмотр требует авторизации., Обычный пользователь не может отклонять заявки (ожидается 403)., Список ролей требует авторизации и возвращает хотя бы одну роль., is_active вычисляется по active_semester_code, без поля в БД., Логинится и проставляет Bearer-токен в заголовках клиента.

### Community 144 - "parse_miit_ief_groups.py"
Cohesion: 0.60
Nodes (4): extract_block(), main(), parse_groups(), Парсинг групп ИЭФ со страницы miit.ru/timetable.

### Community 146 - "APIClient"
Cohesion: 0.30
Nodes (6): _create_assembled_team(), APIClient, django_db, _showcase_url(), TestMentorShowcaseQueryPerformance, TestMentorShowcaseViewSet

### Community 147 - "schema.py"
Cohesion: 0.50
Nodes (3): exclude_auth_api_duplicate(), Хуки и расширения для drf-spectacular., Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*). В…

### Community 149 - "UserSerializer"
Cohesion: 0.11
Nodes (16): Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает учебную группу пользователя или None., UserSerializer, CustomTokenObtainPairSerializer, APIView, UserMeView, institute(), fixture (+8 more)

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

### Community 156 - "test_user_me_student.py"
Cohesion: 0.26
Nodes (9): api_client(), Any, APIClient, django_db, fixture, Тесты GET /api/accounts/user/ для роли student., student_user(), study_group() (+1 more)

### Community 159 - "test_import_preregistered_students.py"
Cohesion: 0.19
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 164 - "utils.py"
Cohesion: 0.25
Nodes (6): is_cpds_department(), Утилиты для работы с подразделениями., Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Unit-тесты для утилит работы с подразделениями., Тесты для функции is_cpds_department., TestIsCpdsDepartment

### Community 165 - ".get_filtered_queryset"
Cohesion: 0.16
Nodes (8): QuerySet, institute_validator — только группы своих институтов., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., django_db, parametrize, TestStudyGroupGetFilteredQueryset, TestStudyGroupMyGroupAccess

### Community 166 - "test_student_showcase_viewset.py"
Cohesion: 0.09
Nodes (28): Идемпотентный импорт строк модели Settings из CSV., Ключ–значение настроек приложения (редактируемые из админки / импортом)., Settings, Тесты разбора semester_id для GET-списков., api_client(), direction(), other_group(), fixture (+20 more)

### Community 170 - "test_mentor_showcase_viewset.py"
Cohesion: 0.31
Nodes (10): api_client(), _approved_app(), direction(), _enrollment_with_mentors(), mentor_showcase_setup(), fixture, Тесты GET /api/teams/study-groups/{id}/project-showcase/., semester() (+2 more)

### Community 189 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 190 - "QuerySet"
Cohesion: 0.18
Nodes (6): QuerySet, Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки.

### Community 191 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 192 - "PlaceholderUserService"
Cohesion: 0.24
Nodes (6): PlaceholderUserService, atomic, Создаёт и возвращает псевдо-user для предрегистрации., Возвращает существующего или создаёт псевдо-user для предрегистрации. Raises:…, Уникальный внутренний email для псевдо-аккаунта., TestPlaceholderUserRegistration

### Community 193 - "PasswordChangeSerializer"
Cohesion: 0.29
Nodes (4): PasswordChangeSerializer, PasswordResetConfirmSerializer, Any, Сериализатор для смены пароля аутентифицированного пользователя.

### Community 195 - "ProjectListDTO"
Cohesion: 0.33
Nodes (4): ProjectListDTO, Any, DTO для списка проектов., Возвращает причастное подразделение верхнего уровня (без родителя). ЦПДС…

### Community 196 - "TestTagViewSetDelete"
Cohesion: 0.20
Nodes (6): Тесты для удаления тегов через API., cpds может удалять общие теги., cpds не может удалять теги с подразделением., admin может удалять любые теги., Остальные роли не могут удалять теги., TestTagViewSetDelete

### Community 197 - "ProjectViewSet"
Cohesion: 0.25
Nodes (5): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией.

### Community 198 - "Command"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Сбрасывает счетчик ID для таблицы тегов.

### Community 199 - "MentorGroupStudentDTO"
Cohesion: 0.32
Nodes (3): MentorGroupStudentDTO, Any, Студент контингента для деталей группы наставника.

### Community 200 - "TagService"
Cohesion: 0.06
Nodes (29): Бизнес-операция: получение списка тегов с фильтрацией по ролям. Для…, Бизнес-операция: получение тега по ID с проверкой доступа. Args: tag_id: ID…, Сервис - оркестрация всех операций с тегами. Координирует Domain, Repository и…, TagService, django_db, Тесты для метода update_tag сервиса., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением. (+21 more)

### Community 201 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 202 - "teams/models.py"
Cohesion: 0.05
Nodes (46): DirectionDomain, Доменная логика для направлений подготовки., Фильтрация направлений по роли пользователя., DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DTO для учебных групп. (+38 more)

### Community 203 - "ApplicationDashboard.py"
Cohesion: 0.20
Nodes (7): ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 205 - "MentorGroupsService"
Cohesion: 0.29
Nodes (5): MentorGroupsService, Any, Возвращает группы, где текущий пользователь — наставник в семестре., Список групп наставника с количеством студентов и команд., Детали группы: студенты контингента и команды в семестре.

### Community 206 - "1. Создание заявки (авторизованные пользователи)"
Cohesion: 0.33
Nodes (6): 1. Создание заявки (авторизованные пользователи), Заголовки, Пример запроса, Тело запроса, Успешный ответ (201), Эндпоинты создания заявок

### Community 240 - "TestSemesterAssignViewSet"
Cohesion: 0.29
Nodes (3): Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, TestSemesterAssignViewSet

### Community 241 - "load_users_from_json"
Cohesion: 0.29
Nodes (7): load_users_from_json(), Any, Path, Загружает список пользователей из JSON-файла., Path, Загружает пользователей из JSON-файла., test_load_users_from_json()

### Community 242 - "ProjectTrackGroupListDTO"
Cohesion: 0.29
Nodes (4): ProjectTrackGroupListDTO, DTO группы со счётчиком назначенных проектов., Преобразует DTO в словарь для API., Список групп института со счётчиком назначенных проектов.

### Community 243 - "ProjectTrackProjectListDTO"
Cohesion: 0.29
Nodes (4): ProjectTrackProjectListDTO, DTO проекта со счётчиком назначенных групп., Преобразует DTO в словарь для API., Список проектов семестра со счётчиком назначенных групп.

### Community 244 - "ProjectTrackGroupProjectDTO"
Cohesion: 0.33
Nodes (3): ProjectTrackGroupProjectDTO, DTO проекта в деталях группы., Преобразует DTO в словарь для API.

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
Nodes (61): ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты…, Получение заявки по ID без дополнительных связанных объектов. Для простых…, Получение заявок пользователя, где он является автором. Оптимизированный запрос…, Получение заявок для координации пользователя. Заявки, где пользователь…, Репозиторий - вся работа с БД здесь, Получение заявок для координации по причастному подразделению. Заявки, где…, Получение заявок по статусу. Для административных операций. (+53 more)

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
Nodes (26): Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Semester, Command, BaseCommand, Добавляет причастные подразделения института к заявке., Meta, Краткое представление пользователя в составе команды. (+18 more)

### Community 293 - "Валидационные правила"
Cohesion: 0.50
Nodes (4): Валидационные правила, Обязательные поля, Обязательные поля:, Типы данных

### Community 294 - "InstituteResponsibleService"
Cohesion: 0.08
Nodes (20): InstituteResponsibleDomain, Правила доступа и валидации для ответственного по институтам., Проверяет, может ли пользователь работать с API ответственного., Определяет код института из параметра или по умолчанию., ViewSet API ответственного по институтам., QuerySet, Снимает наставника с группы в семестре; возвращает актуальные mentorIds., Возвращает отсортированные ID наставников группы в семестре. (+12 more)

### Community 295 - "ProjectTrackAddApplicationsSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationsSerializer, Список заявок с рекомендуемым числом команд и лимитами размера., Проверяет отсутствие дубликатов id в одном запросе.

### Community 297 - "ProjectRepository"
Cohesion: 0.29
Nodes (5): ProjectRepository, QuerySet, Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

### Community 299 - "ProjectTrackCreateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackCreateSerializer, Сериализатор для создания проектного трека., Проверяет согласованность лимитов размера команды.

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

### Community 320 - "MentorTeamAddMemberSerializer"
Cohesion: 0.50
Nodes (3): MentorTeamAddMemberSerializer, Тело POST добавления участника., Требует ровно один идентификатор участника.

### Community 324 - "InstituteSerializer"
Cohesion: 0.67
Nodes (3): InstituteSerializer, Meta, Сериализатор для институтов/академий.

### Community 329 - "TeamSemester"
Cohesion: 0.04
Nodes (52): Проверяет, что пользователь — капитан команды., Результат записи команды на проект., StudentShowcaseEnrollResultDTO, Репозиторий студенческой витрины проектов (без N+1)., DirectionAdmin, register, StudyGroupAdmin, TeamAdmin (+44 more)

### Community 331 - "TeamPermission"
Cohesion: 0.26
Nodes (8): _is_staff_or_admin(), APIView, BasePermission, Request, Чтение — любой аутентифицированный пользователь. Изменение постоянной команды —…, Изменение семестрового контекста — капитан, admin или cpds., TeamPermission, TeamSemesterPermission

## Knowledge Gaps
- **267 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+262 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **135 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `Department`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `ProjectTrackService`, `test_institute_responsible_viewset.py`, `ApplicationDashboardService`, `APIClient`, `StudyGroupMemberDTO`, `UserManagementService`, `PasswordResetSerializer`, `UserSerializer`, `ApplicationDashboardDomain`, `ProjectApplicationRepository`, `TeamLobbyService`, `project_track_service.py`, `.get_filtered_queryset`, `ProjectApplicationService`, `StudentShowcaseDomain`, `InstituteResponsibleService`, `.create_tag`, `CommentService`, `InstituteResponsibleEmployeeDTO`, `._get_track_with_access`, `TagDomain`, `Tag.py`, `._ensure_valid_status_after_department_check`, `DirectionService`, `ProjectTrackPermission`, `ProjectTrackDomain`, `PlaceholderUserService`, `PasswordChangeSerializer`, `TeamLobbyDomain`, `Role`, `accounts/admin.py`, `MentorTeamService`, `MentorGroupStudentDTO`, `.get_filtered_queryset`, `TeamSemester`, `TagService`, `.view_application`, `teams/models.py`, `TeamPermission`, `MentorGroupsService`, `TestCanCreateTag`, `._authorize_and_load`, `TestCanDeleteTag`, `PermissionError`, `.approve_application`, `mentor_team_service.py`, `.get_filtered_queryset`, `UserRepository`, `ProjectApplication`, `.get_dashboard`, `.resolve_list_semester_id`, `ProjectApplication.py`, `.get_user`, `StudyGroup`, `ApplicationLoggingService`, `ProjectTrackGroupListDTO`, `ProjectTrackProjectListDTO`, `._resolve_context`, `institute_access.py`, `StudentShowcaseService`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `Department`, `ProjectApplicationCreateDTO`, `ProjectTrackService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `StudyGroupService`, `ApplicationDashboardService`, `_enrollment_with_mentors`, `APIClient`, `ProjectTrack`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `UserSerializer`, `APIClient`, `ProjectApplicationRepository`, `TestStudentShowcaseEnroll`, `test_user_me_student.py`, `TestProjectApplicationViewSetIsInternalCustomer`, `test_import_preregistered_students.py`, `TagCreateDTO`, `project_track_service.py`, `TestTagViewSetCreate`, `TestTagViewSet`, `ProjectService`, `test_student_showcase_viewset.py`, `ProjectApplicationService`, `PreRegisteredStudent`, `.get_filtered_queryset`, `test_mentor_showcase_viewset.py`, `CommentService`, `InstituteResponsibleEmployeeDTO`, `TagDomain`, `DirectionService`, `TestDepartmentPlanViewSetList`, `TestProjectViewSet`, `ProjectApplicationReadDTO`, `ProjectTrackDomain`, `Role`, `TestTagViewSetDelete`, `.get_filtered_queryset`, `TagService`, `TeamSemester`, `TestApplicationDashboardViewSet`, `TestSubmitApplicationService`, `TestCanCreateTag`, `TestCanDeleteTag`, `TestInstituteResponsibleViewSet`, `mentor_team_service.py`, `.get_filtered_queryset`, `TestProjectApplicationViewSetTransferToInstitute`, `ProjectApplication`, `TestProjectApplicationListSemesterFilter`, `TestSemesterAssignViewSet`, `ApplicationLoggingService`, `StudyGroup`, `TestProjectApplicationNewFieldsCreateUpdate`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `make_user`, `Department`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `ProjectTrackService`, `StudyGroupService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `test_institute_responsible_viewset.py`, `ProjectApplicationViewSet`, `ApplicationDashboardService`, `_enrollment_with_mentors`, `APIClient`, `ProjectTrack`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `ApplicationDashboardDomain`, `ProjectApplicationRepository`, `TeamLobbyService`, `project_track_service.py`, `ProjectService`, `test_student_showcase_viewset.py`, `ProjectApplicationService`, `InstituteResponsibleService`, `test_mentor_showcase_viewset.py`, `TeamSemesterViewSet`, `TestDepartmentPlanViewSetList`, `test_import_study_groups_from_contingent.py`, `TestProjectViewSet`, `ProjectTrackPermission`, `Command`, `TeamLobbyDomain`, `accounts/admin.py`, `MentorTeamService`, `DepartmentPlanViewSet`, `TeamSemester`, `MentorGroupsService`, `AccountsApiTests`, `TestInstituteResponsibleViewSet`, `mentor_team_service.py`, `.resolve_list_semester_id`, `ProjectApplication.py`, `TestProjectApplicationListSemesterFilter`, `StudyGroup`, `TestSemesterAssignViewSet`, `TestProjectApplicationNewFieldsCreateUpdate`, `StudentShowcaseService`, `institute_access.py`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 526 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 526 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 74 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 74 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._