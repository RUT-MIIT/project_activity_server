# Graph Report - project_activity_server  (2026-08-27)

## Corpus Check
- 298 files · ~136,619 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4394 nodes · 8564 edges · 355 communities (216 shown, 139 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 839 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b5752e24`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .create_tag
- make_user
- ProjectApplication
- ProjectApplicationRepository
- ProjectApplicationService
- accounts/views.py
- ProjectApplicationViewSet
- Any
- DirectionSerializer
- TestTagRepositoryCreate
- ApplicationDashboardService
- ApplicationDashboardRepository
- test_project_application_new_fields.py
- project_track_service.py
- UserListDTO
- .get_filtered_queryset
- prepare_study_groups_xlsx.py
- TestMyStudyGroupViewSet
- ProjectTrack
- TagService
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- ProjectTrackService
- ProjectApplicationCreateDTO
- student_showcase_service.py
- _create_assembled_team
- study_group_import.py
- MyTeamViewSet
- TestTeamLobbyViewSet
- django_db
- ProjectApplicationReadDTO
- AvailableActionDTO
- TeamLobbyService
- ._resolve_institute_semester
- ProjectTrackViewSet
- TestTagViewSet
- ProjectService
- ProjectApplicationUpdateDTO
- ._create_app
- normalize_cell
- PreRegisteredStudent
- serialize_comment_author
- StudentShowcaseRepository
- TestGetLogs
- CommentService
- Command
- Semester
- .approve_application
- StudentWithStudyGroupPermission
- TestCanUpdateTag
- TagViewSet
- ProjectTrackReadDTO
- Any
- TestDepartmentPlanViewSetList
- UserManagementService
- StudentShowcaseDomain
- ValidationResult
- StudyGroupService
- accounts/permissions.py
- PreRegisteredStudentService
- action
- ProjectTrackDomain
- ._application_institute_access_q
- .can_change_status
- Примеры использования поля is_internal_customer
- TestTagServiceUpdate
- InvolvedManagementService
- TestProjectApplicationListSemesterFilter
- UserManagementDomain
- accounts/admin.py
- StudentShowcaseViewSet
- .can_user_access_application
- .get_filtered_queryset
- DepartmentPlanViewSet
- ProjectTrackRepository
- DirectionService
- TagRepository
- TestApplicationDashboardViewSet
- TestTagViewSetCreate
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
- accounts/models.py
- TestProjectViewSet
- ProjectApplicationDomain
- QuerySet
- .get_filtered_queryset
- Command
- Any
- TestProjectApplicationViewSetIsInternalCustomer
- TestProjectApplicationNewFieldsCreateUpdate
- TestProjectApplicationViewSetTransferToInstitute
- StudyGroupViewSet
- extract_group_abbrev.py
- ProjectApplicationListDTO
- StudyGroup.py
- Role
- .get_group_detail
- ProjectTrackProjectDetailDTO
- .auth
- TestApplicationNotificationService
- ._track_detail_queryset
- .should_require_consultation
- _generate_collection.py
- .view_application
- TestLogStatusChange
- Department
- UserRepository
- .post
- institute_access.py
- User
- TestMyTeamViewSet
- MyStudyGroupDTO
- TestSemesterAssignViewSet
- .enroll
- API Документация - Проектные заявки
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- StudyGroupDomain
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
- TestRepositoryUpdate
- deploy.sh
- action_types.py
- export_client_sources_to_docx.py
- make_source_docx.py
- TestRepositoryApplicationNumbering
- parse_miit_ief_groups.py
- Command
- Any
- schema.py
- ShowcaseConfig
- .recalculate_recommended_teams_count
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- StudyGroupRepository
- teams/admin.py
- 0011_migrate_team_data.py
- TestRepositoryFilter
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- TagSerializer
- fixture
- showcase/urls.py
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- .handle
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
- TestTagRepositoryGetById
- .test_registration_request_list_requires_privileged_user
- .test_registration_request_race_condition_integrity_error
- format_validation_errors
- .test_semester_create_allowed_for_admin_and_cpds
- TestProjectApplicationSemesterAutoAssign
- .test_semester_list_requires_auth
- Tag
- .test_user_me_institute_code_none_if_no_institute
- TestRepositoryGetById
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
- TestTagRepositoryExists
- PasswordResetSerializer
- Текущий статус реализации
- TestProjectApplicationViewSetSimple
- .ensure_is_captain
- TeamSemester
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
- ProjectTrackAddApplicationsSerializer
- .get_existing_group_ids
- ProjectTrackCreateSerializer
- Схема БД: студенческий портал
- Справочные эндпоинты
- ProjectApplicationListSerializer
- .list_event_logs
- .test_departments_list_allow_any_detail_requires_auth
- .test_registration_request_create_anonymous_allowed
- .test_registration_request_reject_forbidden_for_regular_user
- ProjectViewSet
- ProjectRepository
- .update_team_member_limits
- .test_semester_list_is_active_from_settings
- .test_user_me_institute_code_from_department_institute
- .test_user_roles_list_requires_auth_and_returns
- .destroy
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- Поддержка multipart/form-data
- Вариант 1: импорт схемы с автообновлением
- .get_permissions
- .partial_update
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- .retrieve
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- .update
- .add_applications
- .update
- .partial_update
- Command
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- .list_pending_join_requests_for_user
- .list_pending_invitations_for_user
- .map_pending_join_request_ids
- .get_track_for_group
- .count_group_teams_in_track
- .user_has_team_in_semester
- .get_team_semester
- .create_team_with_semester
- .create_join_request
- .get_join_request
- .get_invitation
- .create_invitation
- .list_group_tracks
- .add_member
- .mark_user_requests_obsolete
- .update_join_request_status
- .update_invitation_status
- .remove_member
- .remove_member_force
- .set_status
- .delete_team_semester
- .add_event_log
- .group_team_semesters_by_track
- .get_user
- .get_my_team_detail

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 486 edges
2. `User` - 212 edges
3. `ProjectApplication` - 146 edges
4. `Department` - 138 edges
5. `ProjectApplicationService` - 136 edges
6. `ProjectApplicationCreateDTO` - 109 edges
7. `Semester` - 104 edges
8. `ProjectTrackService` - 70 edges
9. `StudyGroup` - 69 edges
10. `Institute` - 66 edges

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

## Communities (355 total, 139 thin omitted)

### Community 0 - ".create_tag"
Cohesion: 0.18
Nodes (6): atomic, Бизнес-операция: удаление тега. Args: tag_id: ID тега для удаления user:…, Бизнес-операция: присоединение подразделения к тегу. Args: tag_id: ID тега…, Бизнес-операция: отцепление подразделения от тега. Если тег не базовый…, Бизнес-операция: создание тега. Args: dto: DTO с данными для создания тега…, Бизнес-операция: обновление тега. Args: tag_id: ID тега для обновления dto: DTO…

### Community 1 - "make_user"
Cohesion: 0.04
Nodes (21): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+13 more)

### Community 2 - "ProjectApplication"
Cohesion: 0.04
Nodes (61): Репозиторий для управления пользователями., Общие константы приложения showcase., DTO для работы с проектными заявками., ViewSet для работы с планами подразделений по проектным заявкам., Упрощенный ViewSet для проектных заявок с использованием новой архитектуры.…, ApplicationInvolvedDepartment, ApplicationInvolvedUser, ApplicationStatus (+53 more)

### Community 3 - "ProjectApplicationRepository"
Cohesion: 0.04
Nodes (33): ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты…, Получение заявки по ID без дополнительных связанных объектов. Для простых…, Получение заявок пользователя, где он является автором. Оптимизированный запрос…, Получение QuerySet заявок пользователя для пагинации. Возвращает QuerySet…, Получение заявок для координации пользователя. Заявки, где пользователь…, Получение QuerySet заявок для координации пользователя для пагинации., Репозиторий - вся работа с БД здесь (+25 more)

### Community 4 - "ProjectApplicationService"
Cohesion: 0.05
Nodes (31): ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Бизнес-операция: получение заявок по статусу., Бизнес-операция: получение последних заявок., Бизнес-операция: получение QuerySet всех заявок для пагинации., Бизнес-операция: получение списка внешних заявок (is_external=True). Args:… (+23 more)

### Community 5 - "accounts/views.py"
Cohesion: 0.06
Nodes (41): AcademicYear, Meta, RegistrationRequest, Status, IsCpdsUser, Разрешает доступ только сотрудникам, администраторам или роли ЦПДС., Разрешает доступ только пользователям с ролью ЦПДС (код роли `cpds`)., RegistrationRequestManagePermission (+33 more)

### Community 6 - "ProjectApplicationViewSet"
Cohesion: 0.14
Nodes (13): get_error_message(), ProjectApplicationViewSet, GET /api/project-applications/external/ Получение списка всех внешних заявок…, Возвращает сообщение об ошибке в зависимости от режима DEBUG. Args: exception:…, Упрощенный ViewSet - только обработка HTTP запросов. Вся бизнес-логика вынесена…, Выбор сериализатора в зависимости от действия, Возвращает QuerySet для списка заявок. DRF автоматически применит пагинацию., PK семестра из ?semester_id= (id | next | actual) или None, если параметра нет. (+5 more)

### Community 7 - "Any"
Cohesion: 0.07
Nodes (19): ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackStatisticsDTO, Any, Преобразует DTO в словарь для API., DTO заявки в проектном треке., Преобразует DTO в словарь для API. (+11 more)

### Community 8 - "DirectionSerializer"
Cohesion: 0.67
Nodes (3): DirectionSerializer, Meta, Сериализатор направления подготовки.

### Community 9 - "TestTagRepositoryCreate"
Cohesion: 0.10
Nodes (14): django_db, Тесты для метода create репозитория., Создание общего тега (без departments)., Тесты для метода delete репозитория., delete удаляет тег и возвращает True., Тесты для метода get_all репозитория., get_all возвращает queryset с prefetch_related для departments., Создание тега с подразделением. (+6 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.03
Nodes (60): ApplicationDashboardDomain, DashboardFilters, Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп., Парсит query-параметр application_type., Парсит query-параметр days., Возвращает id подразделения и всех его потомков., Параметры фильтрации дашборда. (+52 more)

### Community 11 - "ApplicationDashboardRepository"
Cohesion: 0.06
Nodes (32): ApplicationDashboardRepository, Q, QuerySet, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению., Цвет столбца по порогам доли внешних заявок. (+24 more)

### Community 12 - "test_project_application_new_fields.py"
Cohesion: 0.08
Nodes (23): get_root_department(), is_cpds_department(), Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, ProjectListDTO, Any, DTO для списка проектов., DTO для списка проектов. (+15 more)

### Community 13 - "project_track_service.py"
Cohesion: 0.07
Nodes (23): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackAggregatedStatisticsDTO, ProjectTrackCreateDTO, ProjectTrackUpdateDTO, DTO для проектных треков., DTO для создания проектного трека. (+15 more)

### Community 14 - "UserListDTO"
Cohesion: 0.12
Nodes (17): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, ViewSet для управления пользователями. (+9 more)

### Community 15 - ".get_filtered_queryset"
Cohesion: 0.25
Nodes (5): QuerySet, institute_validator — только группы своих институтов., django_db, parametrize, TestStudyGroupGetFilteredQueryset

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "TestMyStudyGroupViewSet"
Cohesion: 0.18
Nodes (9): api_client(), direction(), _make_preregistered(), Any, APIClient, django_db, fixture, study_group() (+1 more)

### Community 18 - "ProjectTrack"
Cohesion: 0.06
Nodes (46): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+38 more)

### Community 19 - "TagService"
Cohesion: 0.05
Nodes (34): Чистая бизнес-логика для тегов - только функции, никаких эффектов., Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, TagDomain, Бизнес-операция: получение списка тегов с фильтрацией по ролям. Для…, Бизнес-операция: получение тега по ID с проверкой доступа. Args: tag_id: ID…, Сервис - оркестрация всех операций с тегами. Координирует Domain, Repository и…, TagService (+26 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.08
Nodes (14): ProjectApplicationCreateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы…, Проверяет, что min_team_members не больше max_team_members., Преобразование в DTO - никакой бизнес-логики, Тесты для ProjectApplicationCreateDTO., Создание DTO из словаря через from_dict., Преобразование DTO в словарь через to_dict., Проверяем значения по умолчанию: пустые строки для title, company_contacts,… (+6 more)

### Community 22 - "ProjectTrackService"
Cohesion: 0.14
Nodes (5): ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), django_db, TestProjectTrackService

### Community 23 - "ProjectApplicationCreateDTO"
Cohesion: 0.09
Nodes (21): create_test_applications(), Создаем тестовые заявки, Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, ProjectApplicationCreateDTO, DTO для создания заявки - только данные, никакой логики, Носитель проблемы короче 5 символов вызывает ошибку., Барьер короче 10 символов вызывает ошибку. (+13 more)

### Community 24 - "student_showcase_service.py"
Cohesion: 0.11
Nodes (16): Any, DTO студенческой витрины проектов., Результат записи команды на проект., Преобразует DTO в словарь для API., Карточка проекта в списке трека витрины., Преобразует DTO в словарь для API., Трек с вложенными проектами для витрины., Преобразует DTO в словарь для API. (+8 more)

### Community 25 - "_create_assembled_team"
Cohesion: 0.11
Nodes (9): _approved_app(), _create_assembled_team(), django_db, Число SQL не растёт пропорционально числу проектов., После заполнения последнего слота вторая команда получает 400., TestStudentShowcaseAccess, TestStudentShowcaseDetail, TestStudentShowcaseEnroll (+1 more)

### Community 26 - "study_group_import.py"
Cohesion: 0.13
Nodes (16): build_group_import_row(), build_group_name(), calculate_course_number(), parse_direction_level(), parse_permanent_group_code(), ParsedPermanentGroup, Чистая логика импорта учебных групп из отчёта контингента 1С., Рассчитывает номер курса на текущий учебный год и семестр. (+8 more)

### Community 27 - "MyTeamViewSet"
Cohesion: 0.08
Nodes (32): PageNumberPagination, ApproveJoinRequestSerializer, CreateInvitationSerializer, CreateTeamSerializer, MyTeamViewSet, action, extend_schema, extend_schema_view (+24 more)

### Community 28 - "TestTeamLobbyViewSet"
Cohesion: 0.15
Nodes (6): _create_captained_team(), django_db, После создания своей команды pending-заявка в чужую → obsolete., При нескольких треках команды track_id не проставляется сам., Если группе доступен один трек — он проставляется без track_id в body., TestTeamLobbyViewSet

### Community 29 - "django_db"
Cohesion: 0.10
Nodes (14): django_db, Тесты для методов удаления и проверки существования., delete удаляет заявку и возвращает True., exists возвращает True для существующей заявки., exists возвращает False для несуществующей заявки., Тесты для методов подсчёта заявок., count_by_user возвращает количество заявок автора., count_by_status возвращает количество заявок с указанным статусом. (+6 more)

### Community 30 - "ProjectApplicationReadDTO"
Cohesion: 0.10
Nodes (16): Exception, ProjectApplicationReadDTO, DTO для чтения заявки - оптимизированный набор полей, Преобразование модели в DTO для чтения., Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None. (+8 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "TeamLobbyService"
Cohesion: 0.12
Nodes (21): atomic, QuerySet, UserType, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент принимает приглашение., Студент отклоняет приглашение., Оркестрация Domain + Repository для студенческого лобби. (+13 more)

### Community 33 - "._resolve_institute_semester"
Cohesion: 0.11
Nodes (11): ProjectTrackGroupListDTO, ProjectTrackProjectListDTO, DTO группы со счётчиком назначенных проектов., Преобразует DTO в словарь для API., DTO проекта со счётчиком назначенных групп., Преобразует DTO в словарь для API., UserType, Список групп института со счётчиком назначенных проектов. (+3 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.13
Nodes (22): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+14 more)

### Community 35 - "TestTagViewSet"
Cohesion: 0.10
Nodes (11): Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level). (+3 more)

### Community 36 - "ProjectService"
Cohesion: 0.21
Nodes (5): ProjectService, Оркестрация Domain + Repository для списка проектов., TestProjectApplicationNewFieldsLists, django_db, TestProjectService

### Community 37 - "ProjectApplicationUpdateDTO"
Cohesion: 0.03
Nodes (41): Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, ProjectApplicationUpdateDTO, DTO для обновления заявки - только изменяемые поля, ProjectApplicationUpdateSerializer, Сериализатор только для валидации HTTP данных при обновлении., Проверяет согласованность min/max, если оба переданы., Преобразование в DTO - никакой бизнес-логики, Тесты для валидации при обновлении заявки. (+33 more)

### Community 38 - "._create_app"
Cohesion: 0.05
Nodes (27): patch, Ошибки валидации института: несуществующий код или отсутствие связанного…, Нет причастности подразделения — матрица запрещает действие, ожидаем…, Доступ к просмотру: чужому user запрещено, автору разрешено., department_validator: await_department -> approved_department ->…, institute_validator: await_institute -> approved_institute -> await_cpds…, institute_validator может согласовать await_department, подменяя шаг кафедры., cpds: может одобрять заявки в статусе await_cpds (переход в approved разрешен). (+19 more)

### Community 39 - "normalize_cell"
Cohesion: 0.17
Nodes (13): build_preregistered_student_import_row(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки., Разбирает ФИО из отчёта контингента. Returns: Кортеж (фамилия, имя, отчество). (+5 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.06
Nodes (36): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если предрегистрация уже привязана к User., PreRegisteredStudentRepository, QuerySet, Репозиторий предрегистрации студентов., Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета. (+28 more)

### Community 41 - "serialize_comment_author"
Cohesion: 0.14
Nodes (11): Сериализует автора комментария с role и department. Args: author: User объект…, serialize_comment_author(), POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, Тесты для функции serialize_comment_author., Если author равен None, возвращаются None значения., Сериализация автора с полными данными: имя, фамилия, отчество, роль,…, Сериализация автора без отчества. (+3 more)

### Community 42 - "StudentShowcaseRepository"
Cohesion: 0.11
Nodes (10): Число команд, записанных на проект в треке/семестре., Команда пользователя в семестре с блокировкой строки., Команда пользователя в семестре (без блокировки)., Связь проект↔трек с проверкой семестра и статуса approved., Запросы и запись для студенческой витрины проектов., Счётчик записанных команд с блокировкой строк TeamSemester проекта., Треки группы в семестре с одобренными проектами и тегами., Карта (track_id, application_id) → число записанных команд. (+2 more)

### Community 43 - "TestGetLogs"
Cohesion: 0.11
Nodes (10): Тесты для получения логов., Получение всех логов по заявке., Если application равен None, выбрасывается ValueError., Получение последнего лога заявки., Если логов нет, возвращается None., Получение логов по типу действия., Пустой тип действия вызывает ValueError., Получение логов по актору. (+2 more)

### Community 44 - "CommentService"
Cohesion: 0.10
Nodes (17): CommentService, atomic, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db, Пустой текст вызывает ValueError., Тесты для CommentService. (+9 more)

### Community 45 - "Command"
Cohesion: 0.19
Nodes (10): GroupImportRow, Строка отчёта, подготовленная к импорту одной учебной группы., Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Дедуплицирует строки по коду постоянной группы. (+2 more)

### Community 46 - "Semester"
Cohesion: 0.06
Nodes (32): Идемпотентный импорт строк модели Settings из CSV., Ключ–значение настроек приложения (редактируемые из админки / импортом)., Semester, Settings, Command, BaseCommand, Добавляет причастные подразделения института к заявке., Institute (+24 more)

### Community 47 - ".approve_application"
Cohesion: 0.08
Nodes (18): atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку., Бизнес-операция: отзыв заявки автором., Бизнес-операция: одобрение заявки. (+10 more)

### Community 48 - "StudentWithStudyGroupPermission"
Cohesion: 0.22
Nodes (10): _is_staff_or_admin(), APIView, BasePermission, Request, Доступ только студенту с привязанной учебной группой., Чтение — любой аутентифицированный пользователь. Изменение постоянной команды —…, Изменение семестрового контекста — капитан, admin или cpds., StudentWithStudyGroupPermission (+2 more)

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, django_db, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения. (+3 more)

### Community 50 - "TagViewSet"
Cohesion: 0.11
Nodes (20): Инициализация из модели Tag., TagReadDTO, DepartmentAttachDetachSerializer, action, Request, Response, GET /api/showcase/tags/{id}/ - получение тега с проверкой доступа., POST /api/showcase/tags/ - создание тега. (+12 more)

### Community 51 - "ProjectTrackReadDTO"
Cohesion: 0.09
Nodes (18): ProjectTrackReadDTO, DTO для чтения проектного трека., atomic, QuerySet, Возвращает трек с проверкой доступа., Список треков по фильтрам., Возвращает детали трека., Создаёт проектный трек. (+10 more)

### Community 52 - "Any"
Cohesion: 0.08
Nodes (16): LobbyInvitationDTO, LobbyJoinRequestDTO, LobbyReadDTO, LobbyTeamItemDTO, LobbyTrackDTO, MyTeamInvitationDTO, MyTeamJoinRequestDTO, Any (+8 more)

### Community 53 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 54 - "UserManagementService"
Cohesion: 0.16
Nodes (9): QuerySet, Оркестрация Domain + Repository для управления пользователями., Подгружает parent подразделения для корректного resolve институтов., Список пользователей с учётом роли запрашивающего., Возвращает пользователя, если он доступен запрашивающему., Частичное обновление пользователя., UserManagementService, django_db (+1 more)

### Community 55 - "StudentShowcaseDomain"
Cohesion: 0.12
Nodes (10): Правила доступа и записи команды на проект витрины., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI)., StudentShowcaseDomain (+2 more)

### Community 56 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 57 - "StudyGroupService"
Cohesion: 0.21
Nodes (5): Оркестрация Domain + Repository для StudyGroup., StudyGroupService, TestMyStudyGroupService, django_db, TestStudyGroupService

### Community 58 - "accounts/permissions.py"
Cohesion: 0.06
Nodes (32): DenyStudentPermission, IsAdminOrCpds, IsInstituteValidator, ProjectManagementPermission, ProjectTrackPermission, APIView, BasePermission, Request (+24 more)

### Community 59 - "PreRegisteredStudentService"
Cohesion: 0.07
Nodes (29): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Публичные операции предрегистрации студентов., Ищет предрегистрацию по студбилету, табельному номеру или СНИЛС. (+21 more)

### Community 60 - "action"
Cohesion: 0.12
Nodes (9): action, extend_schema, POST /api/semesters/{id}/assign-empty-applications Присваивает переданный…, POST /api/project-applications/{id}/approve/ Одобрение заявки, POST /api/project-applications/{id}/reject/ Отклонение заявки, POST /api/project-applications/{id}/request_changes/ Запрос изменений (отправка…, POST /api/project-applications/{id}/transfer_to_institute/ Передача заявки в…, POST /api/project-applications/{id}/return_by_author/ Отзыв заявки автором… (+1 more)

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.08
Nodes (14): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя., Проверяет, может ли пользователь управлять проектными треками., Коды институтов пользователя; None — без ограничения (admin/cpds). (+6 more)

### Community 62 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 63 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "TestTagServiceUpdate"
Cohesion: 0.12
Nodes (9): Тесты для метода update_tag сервиса., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги., Нельзя обновить тег, если имя и набор departments уже заняты другим тегом., Обновление несуществующего тега вызывает ошибку. (+1 more)

### Community 66 - "InvolvedManagementService"
Cohesion: 0.12
Nodes (12): InvolvedManagementService, atomic, Добавляет причастное подразделение по его краткому названию. Args: application:…, Добавляет причастное подразделение по его ID. Args: application: Заявка, к…, Добавляет пользователя как причастного к заявке. Args: application: Заявка…, Добавляет подразделение как причастное к заявке. Args: application: Заявка…, Получает всех причастных пользователей заявки. Args: application: Заявка…, Сервис для управления причастными пользователями и подразделениями.… (+4 more)

### Community 68 - "UserManagementDomain"
Cohesion: 0.11
Nodes (11): QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., Правила доступа и валидации для управления пользователями., Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., UserManagementDomain (+3 more)

### Community 69 - "accounts/admin.py"
Cohesion: 0.24
Nodes (11): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+3 more)

### Community 70 - "StudentShowcaseViewSet"
Cohesion: 0.23
Nodes (10): action, extend_schema, extend_schema_view, Request, Response, Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/., GET /api/showcase/student-showcase/projects/{id}/. (+2 more)

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
Cohesion: 0.09
Nodes (12): ProjectTrackRepository, Создаёт проектный трек., Добавляет группы в трек; возвращает число созданных связей., Удаляет группу из трека; True если связь была., Возвращает id заявок, уже привязанных к треку., Удаляет заявку из трека; True если связь была., Количество групп в треке., Доступ к данным проектных треков. (+4 more)

### Community 75 - "DirectionService"
Cohesion: 0.09
Nodes (18): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений., DirectionRepository, QuerySet, Все направления (поля модели без связей — prefetch не требуется)., Направление по коду (PK). (+10 more)

### Community 76 - "TagRepository"
Cohesion: 0.09
Nodes (19): DTO для обновления тега., TagUpdateDTO, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, Обновление тега. Обновляет только переданные поля. Args: tag: Тег для… (+11 more)

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - "TestTagViewSetCreate"
Cohesion: 0.05
Nodes (25): django_db, Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем. (+17 more)

### Community 79 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 80 - "TestProjectApplicationListDTO"
Cohesion: 0.15
Nodes (8): django_db, Тесты для ProjectApplicationListDTO., Если статус None, DTO.status тоже None., to_dict преобразует DTO в словарь с ISO форматированием даты., is_internal_customer включается в ProjectApplicationListDTO., Новые поля трека включаются в ProjectApplicationListDTO., is_internal_customer включается в ProjectApplicationReadDTO., TestProjectApplicationListDTO

### Community 81 - "TeamLobbyDomain"
Cohesion: 0.07
Nodes (16): Подтверждение состава: капитан, forming, размер в лимитах трека., Проверяет, что пользователь из нужной учебной группы., Заявка должна быть в статусе pending., Приглашение должно быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды»., Лимиты: трек команды, иначе единственный трек группы, иначе дефолты., True, если студент без команды и есть свободный слот., Запрещает изменения состава при подтверждённом составе. (+8 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.11
Nodes (10): AccountsApiTests, override_settings, Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Создание заявки без подразделения возвращает ошибку валидации., Создание заявки с несуществующим подразделением возвращает ошибку валидации., После отклонения заявки можно подать новую с тем же email., Повторная подача при активной заявке возвращает ошибку валидации., Нельзя подать заявку, если пользователь с таким email уже зарегистрирован. (+2 more)

### Community 84 - "TestCanDeleteTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения., admin может удалять любые теги. (+2 more)

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
Cohesion: 0.25
Nodes (5): Запросы и записи для студенческого лобби команд., Единственный трек группы в семестре или None (если 0 или >1)., Команды учебной группы в семестре (без фильтра по треку)., Команда пользователя в семестре или None (с составом без N+1)., TeamLobbyRepository

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.05
Nodes (31): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы. (+23 more)

### Community 90 - "accounts/models.py"
Cohesion: 0.04
Nodes (59): Идемпотентный импорт предрегистрации студентов из отчёта контингента 1С., Генерация тестовых одобренных проектов и учебных групп для института IEF., DirectionDomain, Доменная логика для направлений подготовки., Фильтрация направлений по роли пользователя., Доменная логика для учебных групп., DirectionReadDTO, Any (+51 more)

### Community 91 - "TestProjectViewSet"
Cohesion: 0.18
Nodes (4): _create_approved_app(), django_db, ЦПДС в причастных не должно подменять основное подразделение проекта., TestProjectViewSet

### Community 92 - "ProjectApplicationDomain"
Cohesion: 0.10
Nodes (16): ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Определение начального статуса на основе роли пользователя. Чистая функция -…, Явное выражение бизнес-намерений (не технических операций). Этот модуль…, Domain слой - чистая бизнес-логика без побочных эффектов. Этот слой содержит…, Результаты валидации для DTO., Unit-тесты для доменной логики ProjectApplicationDomain. Проверяем все чистые… (+8 more)

### Community 93 - "QuerySet"
Cohesion: 0.18
Nodes (6): QuerySet, Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки.

### Community 94 - ".get_filtered_queryset"
Cohesion: 0.17
Nodes (8): QuerySet, Фильтрует направления: institute_validator — только из групп своего института., django_db, parametrize, Разрешение институтов по подразделению пользователя., Фильтрация queryset направлений по ролям., TestGetFilteredQueryset, TestGetUserInstituteCodes

### Community 95 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

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

### Community 100 - "StudyGroupViewSet"
Cohesion: 0.22
Nodes (7): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/ — список и просмотр учебных групп., Парсит query-параметр is_end; None — фильтр не применяется., StudyGroupViewSet

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - "ProjectApplicationListDTO"
Cohesion: 0.17
Nodes (7): build_author_short_name(), ProjectApplicationListDTO, Формирует короткое имя вида 'Фамилия И.О.' или возвращает None., DTO для списка заявок - минимальный набор полей, DTO (Data Transfer Object) слой для передачи данных между слоями. Этот слой…, Преобразование модели в DTO для списка., Базовые поля DTO для списка заполняются из модели.

### Community 103 - "StudyGroup.py"
Cohesion: 0.21
Nodes (9): Any, DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, Компактная выдача для списка учебных групп., StudyGroupListSerializer (+1 more)

### Community 104 - "Role"
Cohesion: 0.14
Nodes (9): Command, BaseCommand, Role, UserManager, BaseUserManager, create_test_user(), Создаем тестового пользователя, Command (+1 more)

### Community 105 - ".get_group_detail"
Cohesion: 0.17
Nodes (7): ProjectTrackGroupDetailDTO, ProjectTrackGroupProjectDTO, DTO проекта в деталях группы., Преобразует DTO в словарь для API., DTO деталей группы с назначенными проектами., Преобразует DTO в словарь для API., Детали группы с назначенными проектами.

### Community 106 - "ProjectTrackProjectDetailDTO"
Cohesion: 0.17
Nodes (7): ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, DTO группы в деталях проекта., Преобразует DTO в словарь для API., DTO деталей проекта с назначенными группами., Преобразует DTO в словарь для API., Детали проекта с назначенными группами.

### Community 107 - ".auth"
Cohesion: 0.17
Nodes (6): Без токена возвращается 401, с токеном — профиль текущего пользователя., Админ отклоняет заявку: статус становится REJECTED и уходит письмо., Пользователь ЦПДС может отклонять заявки (IsCpdsUser)., Если отправка письма при reject падает, возвращаем 200 и оставляем статус…, Детальный просмотр роли по коду (lookup_field=code) требует авторизации., Логинится и проставляет Bearer-токен в заголовках клиента.

### Community 108 - "TestApplicationNotificationService"
Cohesion: 0.32
Nodes (4): Email получателя: author_email заявки или email связанного пользователя-автора., django_db, patch, TestApplicationNotificationService

### Community 109 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 110 - ".should_require_consultation"
Cohesion: 0.17
Nodes (9): Определение необходимости консультации на основе данных заявки. Чистая функция…, Тесты для определения необходимости консультации., Если уровень проекта не указан, нужна консультация., Если целевые институты не указаны, нужна консультация., Если цель проекта короче 50 символов, нужна консультация., Если все условия выполнены, консультация не требуется., Если project_level равен None, нужна консультация., Если target_institutes равен None, нужна консультация. (+1 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - ".view_application"
Cohesion: 0.09
Nodes (12): Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации., Бизнес-операция: получение заявок для координации пользователя. Для обычных… (+4 more)

### Community 113 - "TestLogStatusChange"
Cohesion: 0.06
Nodes (19): django_db, Первый переход (from_status=None) помечает заявку, если актор не автор., Логирование с указанием предыдущего лога для создания цепочки., Тесты для log_status_change., Если application равен None, выбрасывается ValueError., Успешное логирование изменения статуса (не автор — флаг выставляется)., Если to_status равен None, выбрасывается ValueError., Тесты для логирования причастных пользователей. (+11 more)

### Community 114 - "Department"
Cohesion: 0.07
Nodes (34): Command, BaseCommand, Department, Сервис управления пользователями., Command, BaseCommand, Any, django_db (+26 more)

### Community 115 - "UserRepository"
Cohesion: 0.22
Nodes (7): QuerySet, Доступ к данным пользователей для управления., Базовый queryset без администраторов., Список пользователей с оптимизацией запросов., Возвращает пользователя по ID., Сохраняет изменения пользователя., UserRepository

### Community 116 - ".post"
Cohesion: 0.24
Nodes (7): LoginView, extend_schema, Request, Response, Сменяет пароль текущего пользователя после проверки текущего пароля., Получение JWT токена по email и паролю., TokenObtainPairView

### Community 117 - "institute_access.py"
Cohesion: 0.07
Nodes (34): Доменная логика управления пользователями., ID подразделений для фильтрации; None — без ограничения., get_department_subtree_ids(), Утилиты для работы с подразделениями., Возвращает id корневого подразделения и всех его потомков., Доменная логика дашборда проектных заявок., Доменная логика для списка проектов., Доменная логика для проектных треков. (+26 more)

### Community 118 - "User"
Cohesion: 0.05
Nodes (31): AbstractBaseUser, User, PasswordChangeSerializer, PasswordResetConfirmSerializer, Any, Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем… (+23 more)

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → дефолты 4/7., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "MyStudyGroupDTO"
Cohesion: 0.14
Nodes (9): MyStudyGroupDTO, Any, Карточка наставника учебной группы., Строка списка группы из контингента., Полные данные учебной группы для текущего студента., StudyGroupMemberDTO, StudyGroupMentorDTO, Any (+1 more)

### Community 121 - "TestSemesterAssignViewSet"
Cohesion: 0.09
Nodes (13): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, Тесты для проверки наличия поля is_external в ответах API., POST /api/showcase/project-applications/ возвращает is_external в ответе. (+5 more)

### Community 122 - ".enroll"
Cohesion: 0.24
Nodes (6): atomic, UserType, Записывает команду капитана на проект., Резолвит semester_id; по умолчанию actual., Список треков группы студента с проектами и счётчиками записи., Детали проекта, доступного группе студента.

### Community 123 - "API Документация - Проектные заявки"
Cohesion: 0.18
Nodes (9): API Документация - Проектные заявки, Аутентификация, Базовый URL, Валидационные правила, Общая информация, Обязательные поля, Обязательные поля:, Типы данных (+1 more)

### Community 124 - "test_import_institutes.py"
Cohesion: 0.54
Nodes (7): django_db, Path, Тесты команды import_institutes., test_import_institutes_clear_removes_missing(), test_import_institutes_is_idempotent(), test_import_institutes_updates_existing(), _write_institutes_csv()

### Community 125 - "build_fgos_napravleniya_csv.py"
Cohesion: 0.43
Nodes (6): collect_codes(), fetch(), main(), parse_table_rows(), Собрать fgos_specialitet_napravleniya.csv: level, code, name (без групп…, middle: '03' — бакалавриат, '05' — специалитет.

### Community 126 - "StudyGroupDomain"
Cohesion: 0.36
Nodes (5): Фильтрация учебных групп по роли пользователя., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., StudyGroupDomain, TestStudyGroupMyGroupAccess

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

### Community 138 - "TestRepositoryUpdate"
Cohesion: 0.20
Nodes (6): Тесты для методов обновления заявок., Обновление заявки с изменением целевых институтов: проверяем установку M2M…, Обновление заявки с изменением тегов: проверяем установку M2M связи., Обновление заявки без полей: проверяем вызов save() без update_fields., update_status изменяет статус заявки., TestRepositoryUpdate

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

### Community 143 - "TestRepositoryApplicationNumbering"
Cohesion: 0.20
Nodes (6): Тесты для генерации номеров заявок., Первая заявка в году получает номер 1., Номера последовательно увеличиваются в пределах одного года., Нумерация учитывает пропуски - использует максимальный номер, а не count()., Нумерация сбрасывается при смене года., TestRepositoryApplicationNumbering

### Community 144 - "parse_miit_ief_groups.py"
Cohesion: 0.60
Nodes (4): extract_block(), main(), parse_groups(), Парсинг групп ИЭФ со страницы miit.ru/timetable.

### Community 146 - "Any"
Cohesion: 0.22
Nodes (5): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON

### Community 147 - "schema.py"
Cohesion: 0.50
Nodes (3): exclude_auth_api_duplicate(), Хуки и расширения для drf-spectacular., Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*). В…

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

### Community 156 - "StudyGroupRepository"
Cohesion: 0.25
Nodes (4): QuerySet, Доступ к данным StudyGroup., Группа с наставником и контингентом без N+1., StudyGroupRepository

### Community 157 - "teams/admin.py"
Cohesion: 0.27
Nodes (11): DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin, TeamSemesterAdmin (+3 more)

### Community 159 - "TestRepositoryFilter"
Cohesion: 0.25
Nodes (5): Тесты для методов фильтрации заявок., filter_coordination_by_user_queryset возвращает QuerySet заявок для координации…, filter_by_status_queryset возвращает QuerySet заявок по статусу., filter_by_company ищет заявки по названию компании (case-insensitive)., TestRepositoryFilter

### Community 164 - "TagSerializer"
Cohesion: 0.67
Nodes (3): Meta, Сериализатор для тегов., TagSerializer

### Community 165 - "fixture"
Cohesion: 0.22
Nodes (9): institute(), fixture, Возвращает класс модели пользователя для удобства., Создаёт набор ролей, используемых в тестах. Возвращает dict: code -> Role, Создаёт все необходимые статусы для сценариев сервисов., Создаёт институт, связанный с родительским подразделением., roles(), statuses() (+1 more)

### Community 166 - "showcase/urls.py"
Cohesion: 0.12
Nodes (14): ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…, InstituteSerializer (+6 more)

### Community 189 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 197 - "TestTagRepositoryGetById"
Cohesion: 0.25
Nodes (5): get_by_id возвращает общий тег., get_by_id для несуществующего тега вызывает ошибку., Тесты для метода get_by_id репозитория., get_by_id возвращает тег с подразделением (prefetch_related)., TestTagRepositoryGetById

### Community 200 - "format_validation_errors"
Cohesion: 0.33
Nodes (4): format_validation_errors(), POST /api/project-applications/ Создание заявки - только обработка HTTP, Форматирует ошибки валидации используя стандартные DRF механизмы. Args: errors:…, POST /api/project-applications/simple/ Создание заявки без авторизации

### Community 204 - "Tag"
Cohesion: 0.10
Nodes (18): Доменная логика для тегов - чистые функции без эффектов., DTO для работы с тегами., DTO для создания тега., TagCreateDTO, DepartmentNestedSerializer, Вложенный сериализатор для подразделения., Теги для проектных заявок, Tag (+10 more)

### Community 206 - "TestRepositoryGetById"
Cohesion: 0.33
Nodes (4): Тесты для методов получения заявок по ID., get_by_id возвращает заявку с оптимизированными запросами (prefetch_related)., get_by_id_simple возвращает заявку без дополнительных prefetch., TestRepositoryGetById

### Community 240 - "TestTagRepositoryExists"
Cohesion: 0.33
Nodes (4): Тесты для метода exists репозитория., exists возвращает True для существующего тега., exists возвращает False для несуществующего тега., TestTagRepositoryExists

### Community 242 - "Текущий статус реализации"
Cohesion: 0.40
Nodes (5): ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации, 🔧 Требует доработки

### Community 243 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

### Community 245 - "TeamSemester"
Cohesion: 0.05
Nodes (52): Доменная логика студенческой витрины проектов., Репозиторий студенческой витрины проектов (без N+1)., Привязывает проект к команде и пишет лог., Доменные правила лобби формирования команд., MyTeamEventLogDTO, DTO лобби формирования команд и «Моей команды»., API лобби формирования команд и «Моей команды»., Meta (+44 more)

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 277 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 278 - "ProjectTrackAddApplicationsSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationsSerializer, Список заявок с рекомендуемым числом команд и лимитами размера., Проверяет отсутствие дубликатов id в одном запросе.

### Community 280 - "ProjectTrackCreateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackCreateSerializer, Сериализатор для создания проектного трека., Проверяет согласованность лимитов размера команды.

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 289 - "ProjectApplicationListSerializer"
Cohesion: 0.67
Nodes (3): Meta, ProjectApplicationListSerializer, Простой сериализатор для списка заявок

### Community 296 - "ProjectViewSet"
Cohesion: 0.25
Nodes (5): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией.

### Community 297 - "ProjectRepository"
Cohesion: 0.29
Nodes (5): ProjectRepository, QuerySet, Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

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

### Community 323 - ".partial_update"
Cohesion: 0.25
Nodes (5): Создаёт DTO из словаря., ProjectTrackUpdateSerializer, PATCH /api/showcase/project-tracks/{id}/., Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

## Knowledge Gaps
- **216 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **139 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `.create_tag`, `ProjectApplication`, `ProjectApplicationRepository`, `ProjectApplicationService`, `accounts/views.py`, `Any`, `ApplicationDashboardService`, `project_track_service.py`, `UserListDTO`, `.get_filtered_queryset`, `TagService`, `ProjectTrackService`, `ProjectApplicationCreateDTO`, `student_showcase_service.py`, `TeamLobbyService`, `._resolve_institute_semester`, `CommentService`, `.approve_application`, `StudentWithStudyGroupPermission`, `TestCanUpdateTag`, `ProjectTrackReadDTO`, `UserManagementService`, `StudentShowcaseDomain`, `StudyGroupService`, `accounts/permissions.py`, `ProjectTrackDomain`, `InvolvedManagementService`, `UserManagementDomain`, `accounts/admin.py`, `.get_filtered_queryset`, `DirectionService`, `Tag`, `TestCanCreateTag`, `TeamLobbyDomain`, `TestCanDeleteTag`, `.resolve_list_semester_id`, `ApplicationCapabilities`, `accounts/models.py`, `.get_filtered_queryset`, `.get_user`, `Role`, `.get_group_detail`, `ProjectTrackProjectDetailDTO`, `.view_application`, `PasswordResetSerializer`, `UserRepository`, `.ensure_is_captain`, `institute_access.py`, `TeamSemester`, `MyStudyGroupDTO`, `StudyGroupDomain`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `ProjectApplication`, `ProjectApplicationRepository`, `ProjectApplicationService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `TestRepositoryUpdate`, `ApplicationDashboardService`, `project_track_service.py`, `TestRepositoryApplicationNumbering`, `.get_filtered_queryset`, `TestMyStudyGroupViewSet`, `ProjectTrack`, `TagService`, `TestDepartmentPlanViewSetCreate`, `ProjectTrackService`, `_create_assembled_team`, `django_db`, `ProjectApplicationReadDTO`, `TestRepositoryFilter`, `TestTagViewSet`, `ProjectService`, `fixture`, `._create_app`, `ProjectApplicationUpdateDTO`, `PreRegisteredStudent`, `TestGetLogs`, `CommentService`, `Semester`, `TestCanUpdateTag`, `TestDepartmentPlanViewSetList`, `UserManagementService`, `StudyGroupService`, `ProjectTrackDomain`, `TestTagServiceUpdate`, `TestProjectApplicationListSemesterFilter`, `UserManagementDomain`, `.get_filtered_queryset`, `TestProjectApplicationSemesterAutoAssign`, `DirectionService`, `TestApplicationDashboardViewSet`, `TestTagViewSetCreate`, `TestCanCreateTag`, `TestProjectApplicationListDTO`, `TestRepositoryGetById`, `TestCanDeleteTag`, `accounts/models.py`, `TestProjectViewSet`, `.get_filtered_queryset`, `TestProjectApplicationViewSetIsInternalCustomer`, `TestProjectApplicationNewFieldsCreateUpdate`, `TestProjectApplicationViewSetTransferToInstitute`, `ProjectApplicationListDTO`, `TestApplicationNotificationService`, `TestLogStatusChange`, `Department`, `TeamSemester`, `MyStudyGroupDTO`, `TestSemesterAssignViewSet`, `StudyGroupDomain`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `make_user`, `ProjectApplication`, `ProjectApplicationRepository`, `ProjectApplicationService`, `accounts/views.py`, `ProjectApplicationViewSet`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `ApplicationDashboardService`, `test_project_application_new_fields.py`, `project_track_service.py`, `TestMyStudyGroupViewSet`, `ProjectTrack`, `TestDepartmentPlanViewSetCreate`, `ProjectTrackService`, `student_showcase_service.py`, `study_group_import.py`, `TeamLobbyService`, `ProjectService`, `TestDepartmentPlanViewSetList`, `UserManagementService`, `StudentShowcaseDomain`, `StudyGroupService`, `Command`, `TestProjectApplicationListSemesterFilter`, `accounts/admin.py`, `DepartmentPlanViewSet`, `TestProjectApplicationSemesterAutoAssign`, `AccountsApiTests`, `.resolve_list_semester_id`, `accounts/models.py`, `TestProjectViewSet`, `TestProjectApplicationNewFieldsCreateUpdate`, `Department`, `TeamSemester`, `institute_access.py`, `TestSemesterAssignViewSet`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Are the 483 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 483 INFERRED edges - model-reasoned connections that need verification._
- **Are the 44 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 44 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 72 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._