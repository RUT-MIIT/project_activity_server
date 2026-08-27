# Graph Report - project_activity_server  (2026-08-27)

## Corpus Check
- 299 files · ~137,028 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4411 nodes · 8603 edges · 327 communities (216 shown, 111 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 846 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b5752e24`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .create_tag
- make_user
- Department
- ProjectApplicationRepository
- ProjectApplicationService
- accounts/views.py
- ProjectApplicationViewSet
- Any
- Direction.py
- test_tag_repository.py
- TestApplicationDashboardService
- ProjectApplication
- ProjectListDTO
- test_project_track_service.py
- UserListDTO
- .get_filtered_queryset
- prepare_study_groups_xlsx.py
- StudyGroup
- test_project_track_viewset.py
- TagService
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- ProjectTrackService
- .validate_create
- StudentShowcaseDomain
- test_student_showcase_viewset.py
- test_import_study_groups_from_contingent.py
- Request
- TestTeamLobbyViewSet
- ApplicationDashboardService
- TestProjectApplicationReadDTO
- AvailableActionDTO
- TeamLobbyService
- ProjectTrackProjectListDTO
- ProjectTrackViewSet
- TestTagViewSet
- ProjectService
- TestUpdateAndQueriesService
- ._create_app
- build_preregistered_student_import_row
- PreRegisteredStudent
- TestSubmitApplicationService
- ProjectTrack
- PreRegisteredStudentRepository
- CommentService
- UserSerializer
- Semester
- .approve_application
- StudentWithStudyGroupPermission
- TestCanUpdateTag
- TagViewSet
- .update_application
- team_lobby_service.py
- TestDepartmentPlanViewSetList
- UserManagementService
- test_import_preregistered_students.py
- ValidationResult
- StudyGroupService
- ProjectTrackPermission
- PreRegisteredStudentService
- .submit_application
- ProjectTrackDomain
- ._application_institute_access_q
- .can_change_status
- Примеры использования поля is_internal_customer
- TagUpdateDTO
- InvolvedManagementService
- TestProjectApplicationListSemesterFilter
- TestUserManagementDomain
- accounts/admin.py
- StudentShowcaseService
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
- direction_service.py
- API для работы с проектными заявками
- AccountsApiTests
- TestCanDeleteTag
- TeamLobbyViewSet
- TeamSemesterViewSet
- Command
- TeamSemester
- ApplicationCapabilities
- Direction
- TestProjectViewSet
- .calculate_initial_status
- QuerySet
- .get_filtered_queryset
- .resolve_list_semester_id
- Tag.py
- TestProjectApplicationViewSetIsInternalCustomer
- TestProjectApplicationNewFieldsCreateUpdate
- TestProjectApplicationViewSetTransferToInstitute
- StudyGroupViewSet
- extract_group_abbrev.py
- TestTagServiceDelete
- StudyGroup.py
- Command
- ProjectTrackApplicationItemDTO
- student_user
- .auth
- ApplicationNotificationService
- ._track_detail_queryset
- ProjectApplicationCreateDTO
- _generate_collection.py
- .view_application
- ApplicationLoggingService
- test_export_import_departments_roundtrip
- TestApproveRejectRequest
- .post
- institute_access.py
- User
- TestMyTeamViewSet
- StudyGroupMemberDTO
- TestProjectApplicationSemesterAutoAssign
- TestTagViewSetDelete
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
- test_team_lobby_viewset.py
- deploy.sh
- action_types.py
- export_client_sources_to_docx.py
- make_source_docx.py
- PasswordChangeSerializer
- parse_miit_ief_groups.py
- Command
- TestSemesterAssignViewSet
- schema.py
- ShowcaseConfig
- .recalculate_recommended_teams_count
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- DirectionViewSet
- teams/admin.py
- 0011_migrate_team_data.py
- ProjectApplicationComment
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- ._my_team_dict
- fixture
- showcase/urls.py
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- Command
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
- test_link_institutes_by_name_simple
- .test_registration_request_list_requires_privileged_user
- .test_registration_request_race_condition_integrity_error
- other_institute
- .test_semester_create_allowed_for_admin_and_cpds
- test_study_group_service.py
- .test_semester_list_requires_auth
- UserManager
- .test_user_me_institute_code_none_if_no_institute
- TestGetUserInstituteCodes
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
- CustomResetPasswordForm
- PasswordResetSerializer
- Текущий статус реализации
- TestProjectApplicationViewSetSimple
- TeamEventLogPagination
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
- ProjectTrackAddApplicationItemSerializer
- InstituteSerializer
- .get_my_team_event_logs
- ProjectTrackCreateSerializer
- Схема БД: студенческий портал
- Справочные эндпоинты
- .get_existing_application_ids
- test_my_team_viewset.py
- .test_departments_list_allow_any_detail_requires_auth
- .test_registration_request_create_anonymous_allowed
- .test_registration_request_reject_forbidden_for_regular_user
- ProjectViewSet
- project_service.py
- .update_team_member_limits
- .test_semester_list_is_active_from_settings
- .test_user_me_institute_code_from_department_institute
- .test_user_roles_list_requires_auth_and_returns
- .get_group_by_id
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- Поддержка multipart/form-data
- Вариант 1: импорт схемы с автообновлением
- .remove_group
- .update_recommended_teams_counts
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- .update
- ProjectTrackUpdateSerializer
- Command
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py

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
- `TestUserManagementDomain` --uses--> `UserManagementDomain`  [INFERRED]
  tests/accounts/domain/test_user_management.py → accounts/domain/user_management.py
- `create_test_applications()` --uses--> `User`  [INFERRED]
  create_test_applications.py → accounts/models.py
- `ApplicationDashboardDomain` --uses--> `User`  [INFERRED]
  showcase/domain/application_dashboard.py → accounts/models.py
- `ProjectDomain` --uses--> `User`  [INFERRED]
  showcase/domain/project.py → accounts/models.py
- `ProjectTrackDomain` --uses--> `User`  [INFERRED]
  showcase/domain/project_track.py → accounts/models.py

## Import Cycles
- None detected.

## Communities (327 total, 111 thin omitted)

### Community 0 - ".create_tag"
Cohesion: 0.18
Nodes (6): atomic, Бизнес-операция: удаление тега. Args: tag_id: ID тега для удаления user:…, Бизнес-операция: присоединение подразделения к тегу. Args: tag_id: ID тега…, Бизнес-операция: отцепление подразделения от тега. Если тег не базовый…, Бизнес-операция: создание тега. Args: dto: DTO с данными для создания тега…, Бизнес-операция: обновление тега. Args: tag_id: ID тега для обновления dto: DTO…

### Community 1 - "make_user"
Cohesion: 0.04
Nodes (21): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+13 more)

### Community 2 - "Department"
Cohesion: 0.05
Nodes (43): Command, BaseCommand, Department, Доменная логика для тегов - чистые функции без эффектов., ViewSet для работы с планами подразделений по проектным заявкам., Генерация тестовых одобренных проектов и учебных групп для института IEF., ApplicationInvolvedDepartment, ApplicationInvolvedUser (+35 more)

### Community 3 - "ProjectApplicationRepository"
Cohesion: 0.03
Nodes (49): ProjectApplicationRepository, Репозиторий - вся работа с БД здесь, Получение QuerySet заявок по статусу для пагинации., Обновление заявки. Обновляет только переданные поля., Создание заявки в БД. Принимает DTO и пользователя, возвращает созданную…, Проверка существования заявки. Быстрая проверка без загрузки объекта., Подсчет заявок по статусу. Для аналитики и отчетов., Присваивает семестр всем заявкам без установленного семестра. Args:… (+41 more)

### Community 4 - "ProjectApplicationService"
Cohesion: 0.06
Nodes (21): ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка., Бизнес-операция: получение заявок по статусу., Бизнес-операция: получение последних заявок. (+13 more)

### Community 5 - "accounts/views.py"
Cohesion: 0.06
Nodes (46): Command, BaseCommand, AcademicYear, Meta, RegistrationRequest, Role, Status, IsCpdsUser (+38 more)

### Community 6 - "ProjectApplicationViewSet"
Cohesion: 0.05
Nodes (33): format_validation_errors(), get_error_message(), ProjectApplicationViewSet, action, extend_schema, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, GET /api/project-applications/external/ Получение списка всех внешних заявок… (+25 more)

### Community 7 - "Any"
Cohesion: 0.04
Nodes (29): ProjectTrackGroupDetailDTO, ProjectTrackGroupListDTO, ProjectTrackGroupProjectDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, ProjectTrackStatisticsDTO, Any (+21 more)

### Community 8 - "Direction.py"
Cohesion: 0.20
Nodes (7): DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DirectionSerializer, Meta, Сериализатор направления подготовки.

### Community 9 - "test_tag_repository.py"
Cohesion: 0.08
Nodes (19): DTO для работы с тегами., Репозиторий для работы с тегами в БД. Изолирует всю работу с базой данных от…, django_db, Unit-тесты для репозитория TagRepository. Проверяем все методы работы с БД:…, get_by_id возвращает общий тег., get_by_id для несуществующего тега вызывает ошибку., Тесты для метода delete репозитория., delete удаляет тег и возвращает True. (+11 more)

### Community 10 - "TestApplicationDashboardService"
Cohesion: 0.05
Nodes (31): _create_app(), django_db, fixture, Тесты ApplicationDashboardService., Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external., Фильтр по группам статусов., Карточка in_work = total - approved - rejected. (+23 more)

### Community 11 - "ProjectApplication"
Cohesion: 0.04
Nodes (44): ProjectApplication, ApplicationDashboardRepository, Q, QuerySet, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению. (+36 more)

### Community 12 - "ProjectListDTO"
Cohesion: 0.09
Nodes (19): get_root_department(), is_cpds_department(), Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, ProjectListDTO, Any, DTO для списка проектов., DTO для списка проектов. (+11 more)

### Community 13 - "test_project_track_service.py"
Cohesion: 0.05
Nodes (41): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackAggregatedStatisticsDTO, ProjectTrackCreateDTO, ProjectTrackReadDTO, ProjectTrackUpdateDTO, DTO для проектных треков. (+33 more)

### Community 14 - "UserListDTO"
Cohesion: 0.12
Nodes (16): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, API управления пользователями: список, деталь, частичное обновление. (+8 more)

### Community 15 - ".get_filtered_queryset"
Cohesion: 0.29
Nodes (4): QuerySet, institute_validator — только группы своих институтов., parametrize, TestStudyGroupGetFilteredQueryset

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroup"
Cohesion: 0.11
Nodes (20): MyStudyGroupDTO, DTO для эндпоинта «Моя группа»., Полные данные учебной группы для текущего студента., StudyGroup, QuerySet, Репозиторий для учебных групп., Доступ к данным StudyGroup., Группа с наставником и контингентом без N+1. (+12 more)

### Community 18 - "test_project_track_viewset.py"
Cohesion: 0.07
Nodes (33): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+25 more)

### Community 19 - "TagService"
Cohesion: 0.06
Nodes (33): Чистая бизнес-логика для тегов - только функции, никаких эффектов., Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, TagDomain, DTO для создания тега., TagCreateDTO, Сервис для оркестрации операций с тегами. Координирует Domain, Repository и DTO., Бизнес-операция: получение списка тегов с фильтрацией по ролям. Для… (+25 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (28): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationCreateSerializer, ProjectApplicationUpdateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы… (+20 more)

### Community 22 - "ProjectTrackService"
Cohesion: 0.07
Nodes (17): Создаёт DTO из словаря., PATCH /api/showcase/project-tracks/{id}/., ProjectTrackService, QuerySet, UserType, Список треков по фильтрам., Проставляет лимиты размера команды всем заявкам трека., Оркестрация Domain + Repository для проектных треков. (+9 more)

### Community 23 - ".validate_create"
Cohesion: 0.12
Nodes (13): Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Носитель проблемы короче 5 символов вызывает ошибку., Барьер короче 10 символов вызывает ошибку., Имя и фамилия автора короче 2 символов вызывают ошибки., Тесты для валидации при создании заявки., Телефон короче 10 символов вызывает ошибку., Валидный DTO проходит проверку без ошибок., Все ошибки валидации собираются в одном результате. (+5 more)

### Community 24 - "StudentShowcaseDomain"
Cohesion: 0.06
Nodes (36): Доменная логика студенческой витрины проектов., Правила доступа и записи команды на проект витрины., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI). (+28 more)

### Community 25 - "test_student_showcase_viewset.py"
Cohesion: 0.08
Nodes (19): api_client(), _approved_app(), _create_assembled_team(), direction(), other_group(), django_db, fixture, Тесты API студенческой витрины проектов. (+11 more)

### Community 26 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.05
Nodes (45): Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Идемпотентный импорт предрегистрации студентов из отчёта контингента 1С., build_group_import_row(), build_group_name(), calculate_course_number(), GroupImportRow, normalize_cell(), parse_direction_level() (+37 more)

### Community 27 - "Request"
Cohesion: 0.12
Nodes (17): ApproveJoinRequestSerializer, CreateInvitationSerializer, extend_schema, Request, Response, GET /api/teams/my-team/., GET /api/teams/my-team/event-log/ — пагинированный лог (page_size=50)., DELETE /api/teams/my-team/ — удалить свою команду. (+9 more)

### Community 28 - "TestTeamLobbyViewSet"
Cohesion: 0.15
Nodes (6): _create_captained_team(), django_db, После создания своей команды pending-заявка в чужую → obsolete., При нескольких треках команды track_id не проставляется сам., Если группе доступен один трек — он проставляется без track_id в body., TestTeamLobbyViewSet

### Community 29 - "ApplicationDashboardService"
Cohesion: 0.05
Nodes (37): get_department_subtree_ids(), Утилиты для работы с подразделениями., Возвращает id корневого подразделения и всех его потомков., ApplicationDashboardDomain, DashboardFilters, Доменная логика дашборда проектных заявок., Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп. (+29 more)

### Community 30 - "TestProjectApplicationReadDTO"
Cohesion: 0.09
Nodes (13): Exception, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None., target_institutes сериализуется как список словарей с code и name., tags сериализуется как список словарей с id, name и category., involved_users сериализуется с данными пользователя, added_at и added_by. (+5 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "TeamLobbyService"
Cohesion: 0.14
Nodes (17): atomic, UserType, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент отклоняет приглашение., Оркестрация Domain + Repository для студенческого лобби., Возвращает команду капитана или бросает ошибку., Капитан одобряет заявку и назначает роль. (+9 more)

### Community 33 - "ProjectTrackProjectListDTO"
Cohesion: 0.29
Nodes (4): ProjectTrackProjectListDTO, DTO проекта со счётчиком назначенных групп., Преобразует DTO в словарь для API., Список проектов семестра со счётчиком назначенных групп.

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.11
Nodes (27): ProjectTrackAddApplicationsSerializer, ProjectTrackAddGroupsSerializer, ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response (+19 more)

### Community 35 - "TestTagViewSet"
Cohesion: 0.10
Nodes (11): Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level). (+3 more)

### Community 36 - "ProjectService"
Cohesion: 0.21
Nodes (6): ProjectService, Оркестрация Domain + Repository для списка проектов., Подгружает parent подразделения пользователя., Список проектов с учётом роли пользователя., django_db, TestProjectService

### Community 37 - "TestUpdateAndQueriesService"
Cohesion: 0.06
Nodes (17): Автор не может редактировать заявку в статусе await_department (матрица…, Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Автор может отозвать заявку: статус -> returned_author, пишется лог., Не-автор не может отозвать заявку — PermissionError., Отозвать одобренную заявку нельзя (PermissionError по матрице)., Автор видит действие 'Отозвать' в await_department и может вернуть в…, institute_validator-автор сохраняет заявку на доработке…, department_validator может редактировать свою заявку (как автор). (+9 more)

### Community 38 - "._create_app"
Cohesion: 0.06
Nodes (25): patch, Ошибки валидации института: несуществующий код или отсутствие связанного…, Нет причастности подразделения — матрица запрещает действие, ожидаем…, department_validator: await_department -> approved_department ->…, institute_validator: await_institute -> approved_institute -> await_cpds…, institute_validator может согласовать await_department, подменяя шаг кафедры., cpds: может одобрять заявки в статусе await_cpds (переход в approved разрешен)., Полный цикл: заявка создается, одобряется department_validator, затем… (+17 more)

### Community 39 - "build_preregistered_student_import_row"
Cohesion: 0.11
Nodes (16): build_preregistered_student_import_row(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки., Разбирает ФИО из отчёта контингента. Returns: Кортеж (фамилия, имя, отчество)., Собирает DTO одной предрегистрации из полей строки отчёта. (+8 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.14
Nodes (16): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если предрегистрация уже привязана к User., MonkeyPatch, api_client(), pre_registered_student(), Any, APIClient (+8 more)

### Community 41 - "TestSubmitApplicationService"
Cohesion: 0.08
Nodes (13): django_db, Если needs_consultation не передан, значение остается False по умолчанию., При создании упрощенной заявки устанавливается is_external=True и статус…, При создании упрощенной заявки добавляется причастное подразделение ЦПДС., При создании обычной заявки is_external=False по умолчанию., Заявка автоматически переходит в await_institute, если в подразделении нет…, Заявка остаётся в await_department, если в подразделении есть…, Успешная подача заявки: создаётся со статусом created, затем переводится в… (+5 more)

### Community 42 - "ProjectTrack"
Cohesion: 0.06
Nodes (20): display, Количество групп в треке., Количество заявок в треке., ProjectTrack, Проектный трек — контейнер для назначения групп и заявок в рамках семестра., Репозиторий студенческой витрины проектов (без N+1)., Число команд, записанных на проект в треке/семестре., Команда пользователя в семестре с блокировкой строки. (+12 more)

### Community 43 - "PreRegisteredStudentRepository"
Cohesion: 0.09
Nodes (12): PreRegisteredStudentRepository, QuerySet, Репозиторий предрегистрации студентов., Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по табельному номеру., Возвращает предрегистрацию по нормализованному СНИЛС., Возвращает предрегистрацию по первичному ключу. (+4 more)

### Community 44 - "CommentService"
Cohesion: 0.10
Nodes (17): CommentService, atomic, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db, Пустой текст вызывает ValueError., Тесты для CommentService. (+9 more)

### Community 45 - "UserSerializer"
Cohesion: 0.17
Nodes (9): Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., UserSerializer, CustomTokenObtainPairSerializer (+1 more)

### Community 46 - "Semester"
Cohesion: 0.07
Nodes (24): Идемпотентный импорт строк модели Settings из CSV., Ключ–значение настроек приложения (редактируемые из админки / импортом)., Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Следующий семестр для новых заявок (Settings.next_semester_code)., Semester, Settings, Command (+16 more)

### Community 47 - ".approve_application"
Cohesion: 0.09
Nodes (18): Any, Возвращает список доступных действий согласно матрице., atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку. (+10 more)

### Community 48 - "StudentWithStudyGroupPermission"
Cohesion: 0.22
Nodes (10): _is_staff_or_admin(), APIView, BasePermission, Request, Доступ только студенту с привязанной учебной группой., Чтение — любой аутентифицированный пользователь. Изменение постоянной команды —…, Изменение семестрового контекста — капитан, admin или cpds., StudentWithStudyGroupPermission (+2 more)

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+2 more)

### Community 50 - "TagViewSet"
Cohesion: 0.11
Nodes (20): Инициализация из модели Tag., TagReadDTO, DepartmentAttachDetachSerializer, action, Request, Response, GET /api/showcase/tags/{id}/ - получение тега с проверкой доступа., POST /api/showcase/tags/ - создание тега. (+12 more)

### Community 51 - ".update_application"
Cohesion: 0.15
Nodes (9): Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Не-автор и не-ЦПДС не может редактировать заявку., Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult., CPDS может редактировать одобренные заявки., institute_validator-автор: save совпадает с available_actions (подразделение…, institute_validator без причастного подразделения не может сохранить. (+1 more)

### Community 52 - "team_lobby_service.py"
Cohesion: 0.05
Nodes (31): Подтверждение состава: капитан, forming, размер в лимитах трека., Чистая бизнес-логика лобби и «Моей команды»., Лимиты: трек команды, иначе единственный трек группы, иначе дефолты., True, если студент без команды и есть свободный слот., Запрещает изменения состава при подтверждённом составе., Приглашение не может назначать роль leader., При одобрении заявки нельзя назначить второго leader., ФИО пользователя для лога. (+23 more)

### Community 53 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 54 - "UserManagementService"
Cohesion: 0.08
Nodes (23): Правила доступа и валидации для управления пользователями., UserManagementDomain, ViewSet для управления пользователями., Пользовательские permissions для приложения accounts., Просмотр пользователей — admin/cpds/institute_validator; запись — admin/cpds., UserManagementPermission, QuerySet, Репозиторий для управления пользователями. (+15 more)

### Community 55 - "test_import_preregistered_students.py"
Cohesion: 0.20
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 56 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 57 - "StudyGroupService"
Cohesion: 0.21
Nodes (5): Оркестрация Domain + Repository для StudyGroup., StudyGroupService, TestMyStudyGroupService, django_db, TestStudyGroupService

### Community 58 - "ProjectTrackPermission"
Cohesion: 0.08
Nodes (25): DenyStudentPermission, IsAdminOrCpds, IsInstituteValidator, ProjectManagementPermission, ProjectTrackPermission, APIView, BasePermission, Request (+17 more)

### Community 59 - "PreRegisteredStudentService"
Cohesion: 0.07
Nodes (29): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Публичные операции предрегистрации студентов., Ищет предрегистрацию по студбилету, табельному номеру или СНИЛС. (+21 more)

### Community 60 - ".submit_application"
Cohesion: 0.16
Nodes (7): Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, Бизнес-операция: подача заявки. Новая логика: 1. Валидация через Domain 2.…, Проверяет наличие пользователя с ролью department_validator в причастных…, Проверяет и корректирует статус заявки при необходимости. Если целевой статус -…, Проверяем, что валидный DTO проходит валидацию без ошибок., Невалидные поля аккумулируют ошибки в ValidationResult., TestSubmitApplication

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.07
Nodes (17): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя. (+9 more)

### Community 62 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 63 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "TagUpdateDTO"
Cohesion: 0.12
Nodes (12): DTO для обновления тега., TagUpdateDTO, Обновление тега. Обновляет только переданные поля. Args: tag: Тег для…, Тесты для метода update_tag сервиса., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения. (+4 more)

### Community 66 - "InvolvedManagementService"
Cohesion: 0.12
Nodes (12): InvolvedManagementService, atomic, Добавляет причастное подразделение по его краткому названию. Args: application:…, Добавляет причастное подразделение по его ID. Args: application: Заявка, к…, Добавляет пользователя как причастного к заявке. Args: application: Заявка…, Добавляет подразделение как причастное к заявке. Args: application: Заявка…, Получает всех причастных пользователей заявки. Args: application: Заявка…, Сервис для управления причастными пользователями и подразделениями.… (+4 more)

### Community 68 - "TestUserManagementDomain"
Cohesion: 0.13
Nodes (8): Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., Проверяет права на чтение или запись пользователей., Role, django_db, TestUserManagementDomain

### Community 69 - "accounts/admin.py"
Cohesion: 0.24
Nodes (11): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+3 more)

### Community 70 - "StudentShowcaseService"
Cohesion: 0.12
Nodes (19): action, extend_schema, extend_schema_view, Request, Response, ViewSet студенческой витрины проектов., Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/. (+11 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.14
Nodes (11): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Тесты для проверки доступа пользователя к заявке., Автор всегда имеет доступ к своей заявке., Админ имеет доступ ко всем заявкам., Модератор имеет доступ ко всем заявкам., CPDS имеет доступ ко всем заявкам., Валидатор подразделения имеет доступ ко всем заявкам., Валидатор института имеет доступ ко всем заявкам. (+3 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.13
Nodes (12): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, django_db, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., Тесты для фильтрации queryset тегов по ролям., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения. (+4 more)

### Community 73 - "DepartmentPlanViewSet"
Cohesion: 0.17
Nodes (14): DepartmentPlanSerializer, DepartmentPlanViewSet, action, extend_schema, Request, Response, Получить словарь планов по подразделениям для указанного семестра., Получить статистику заявок по статусам для каждого подразделения. (+6 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.11
Nodes (10): ProjectTrackRepository, Создаёт проектный трек., Возвращает id групп, уже привязанных к треку., Добавляет группы в трек; возвращает число созданных связей., Добавляет заявки в трек; возвращает число созданных связей., Удаляет заявку из трека; True если связь была., Количество групп в треке., Доступ к данным проектных треков. (+2 more)

### Community 75 - "DirectionService"
Cohesion: 0.17
Nodes (9): DirectionService, Оркестрация Domain + Repository для Direction., Список направлений с фильтрацией по роли., Направление по коду с проверкой доступа., directions(), django_db, fixture, Тесты DirectionService. (+1 more)

### Community 76 - "TagRepository"
Cohesion: 0.06
Nodes (24): Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., Создание тега в БД. Args: dto: DTO с данными для создания тега Returns:…, Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, TagRepository, Тесты для метода update репозитория. (+16 more)

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - "TestTagViewSetCreate"
Cohesion: 0.06
Nodes (19): django_db, Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем. (+11 more)

### Community 79 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 80 - "TestProjectApplicationListDTO"
Cohesion: 0.13
Nodes (9): django_db, Тесты для ProjectApplicationListDTO., Базовые поля DTO для списка заполняются из модели., Если статус None, DTO.status тоже None., to_dict преобразует DTO в словарь с ISO форматированием даты., is_internal_customer включается в ProjectApplicationListDTO., Новые поля трека включаются в ProjectApplicationListDTO., is_internal_customer включается в ProjectApplicationReadDTO. (+1 more)

### Community 81 - "direction_service.py"
Cohesion: 0.16
Nodes (9): DirectionDomain, Фильтрация направлений по роли пользователя., DirectionRepository, QuerySet, Репозиторий для направлений подготовки., Все направления (поля модели без связей — prefetch не требуется)., Направление по коду (PK)., Доступ к данным Direction. (+1 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.11
Nodes (10): AccountsApiTests, override_settings, Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Создание заявки без подразделения возвращает ошибку валидации., Создание заявки с несуществующим подразделением возвращает ошибку валидации., После отклонения заявки можно подать новую с тем же email., Повторная подача при активной заявке возвращает ошибку валидации., Нельзя подать заявку, если пользователь с таким email уже зарегистрирован. (+2 more)

### Community 84 - "TestCanDeleteTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения., admin может удалять любые теги. (+2 more)

### Community 85 - "TeamLobbyViewSet"
Cohesion: 0.18
Nodes (10): CreateTeamSerializer, action, extend_schema_view, POST /api/teams/lobby/teams/{id}/join-requests/., POST /api/teams/lobby/invitations/{id}/accept/., POST /api/teams/lobby/invitations/{id}/reject/., Создание команды в лобби., Студенческое лобби: треки, команды, заявки, приглашения. (+2 more)

### Community 86 - "TeamSemesterViewSet"
Cohesion: 0.24
Nodes (8): action, Request, Response, POST /api/teams/team-semesters/{id}/members/ — добавить участника., DELETE /api/teams/team-semesters/{id}/members/{member_id}/., CRUD для участия команды в семестре и управления составом., GET /api/teams/team-semesters/my/?semester_id= — команды пользователя., TeamSemesterViewSet

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "TeamSemester"
Cohesion: 0.04
Nodes (30): Проверяет, что пользователь — капитан команды., Приглашение должно быть в статусе pending., Проверяет, что пользователь — капитан команды., Участие команды в конкретном семестре: проект, наставник, капитан., Приглашение капитана студенту вступить в команду., Status, TeamInvitation, TeamSemester (+22 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.08
Nodes (19): ApplicationCapabilities, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы., УСТАРЕВШЕ: прокси к новой матрице. Считаем, что "управление" означает…, Проверка права на редактирование заявки. Бизнес-правило: редактировать может… (+11 more)

### Community 90 - "Direction"
Cohesion: 0.12
Nodes (17): Direction, Level, Направление подготовки (ФГОС ВО)., directions(), other_institute(), fixture, Тесты DirectionViewSet., direction() (+9 more)

### Community 91 - "TestProjectViewSet"
Cohesion: 0.18
Nodes (4): _create_approved_app(), django_db, ЦПДС в причастных не должно подменять основное подразделение проекта., TestProjectViewSet

### Community 92 - ".calculate_initial_status"
Cohesion: 0.17
Nodes (9): Определение начального статуса на основе роли пользователя. Чистая функция -…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds., Обычный пользователь создаёт заявки в статусе await_department., Неизвестная роль возвращает статус await_department по умолчанию. (+1 more)

### Community 93 - "QuerySet"
Cohesion: 0.18
Nodes (6): QuerySet, Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки.

### Community 94 - ".get_filtered_queryset"
Cohesion: 0.24
Nodes (5): QuerySet, Фильтрует направления: institute_validator — только из групп своего института., parametrize, Фильтрация queryset направлений по ролям., TestGetFilteredQueryset

### Community 95 - ".resolve_list_semester_id"
Cohesion: 0.22
Nodes (5): Разбор query-параметра semester_id для GET-списков: id, next, actual., Any, Возвращает данные учебной группы текущего студента., django_db, TestSemesterResolveListSemesterId

### Community 96 - "Tag.py"
Cohesion: 0.09
Nodes (15): Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Преобразование в словарь., DepartmentNestedSerializer, Meta, Вложенный сериализатор для подразделения., Сериализатор для тегов. (+7 more)

### Community 97 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 98 - "TestProjectApplicationNewFieldsCreateUpdate"
Cohesion: 0.22
Nodes (4): _base_create_payload(), django_db, TestProjectApplicationNewFieldsCreateUpdate, TestProjectApplicationNewFieldsLists

### Community 99 - "TestProjectApplicationViewSetTransferToInstitute"
Cohesion: 0.17
Nodes (8): Тесты для действия передачи заявки в институт по коду института., POST /api/showcase/project-applications/{id}/transfer_to_institute/ с…, Отсутствующий параметр code возвращает 400., Несуществующий код института возвращает 400 от сервиса., Институт без связанного подразделения возвращает 400., GET /api/showcase/project-applications/external/?status=... фильтрует внешние…, GET /api/showcase/project-applications/external/?status=... с несуществующим…, TestProjectApplicationViewSetTransferToInstitute

### Community 100 - "StudyGroupViewSet"
Cohesion: 0.22
Nodes (7): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/ — список и просмотр учебных групп., Парсит query-параметр is_end; None — фильтр не применяется., StudyGroupViewSet

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - "TestTagServiceDelete"
Cohesion: 0.17
Nodes (7): Тесты для метода delete_tag сервиса., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять теги своего подразделения., admin может удалять любые теги., Удаление несуществующего тега вызывает ошибку., TestTagServiceDelete

### Community 103 - "StudyGroup.py"
Cohesion: 0.19
Nodes (10): Any, DTO для учебных групп., DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, Компактная выдача для списка учебных групп. (+2 more)

### Community 105 - "ProjectTrackApplicationItemDTO"
Cohesion: 0.18
Nodes (6): ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO, Преобразует DTO в словарь для API., DTO заявки в проектном треке., Преобразует DTO в словарь для API., DTO группы в проектном треке.

### Community 106 - "student_user"
Cohesion: 0.27
Nodes (8): api_client(), Any, APIClient, django_db, fixture, student_user(), study_group(), TestUserMeStudent

### Community 107 - ".auth"
Cohesion: 0.17
Nodes (6): Без токена возвращается 401, с токеном — профиль текущего пользователя., Админ отклоняет заявку: статус становится REJECTED и уходит письмо., Пользователь ЦПДС может отклонять заявки (IsCpdsUser)., Если отправка письма при reject падает, возвращаем 200 и оставляем статус…, Детальный просмотр роли по коду (lookup_field=code) требует авторизации., Логинится и проставляет Bearer-токен в заголовках клиента.

### Community 108 - "ApplicationNotificationService"
Cohesion: 0.19
Nodes (8): ApplicationNotificationService, Отправка писем автору при отклонении и отправке на доработку., Email получателя: author_email заявки или email связанного пользователя-автора., Письмо автору: заявка отправлена на доработку., Письмо автору: заявка отклонена., django_db, patch, TestApplicationNotificationService

### Community 109 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 110 - "ProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (60): create_test_applications(), Создаем тестовые заявки, Общие константы приложения showcase., ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Определение необходимости консультации на основе данных заявки. Чистая функция… (+52 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - ".view_application"
Cohesion: 0.09
Nodes (12): Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации., Бизнес-операция: получение заявок для координации пользователя. Для обычных… (+4 more)

### Community 113 - "ApplicationLoggingService"
Cohesion: 0.04
Nodes (48): ProjectApplicationStatusLog, ApplicationLoggingService, atomic, Логирование удаления причастного пользователя. Args: application: Заявка user:…, Логирование добавления причастного подразделения. Args: application: Заявка…, Логирование удаления причастного подразделения. Args: application: Заявка…, Сервис для логирования изменений в проектных заявках. Обеспечивает полное…, Получение всех логов по заявке. Args: application: Заявка Returns:… (+40 more)

### Community 114 - "test_export_import_departments_roundtrip"
Cohesion: 0.27
Nodes (10): Any, django_db, Экспорт и последующий импорт институтов восстанавливают данные., Экспорт и последующий импорт подразделений восстанавливают данные., Импорт институтов удаляет те, которых нет в файле., Импорт подразделений удаляет те, которых нет в файле., test_export_import_departments_roundtrip(), test_export_import_institutes_roundtrip() (+2 more)

### Community 115 - "TestApproveRejectRequest"
Cohesion: 0.27
Nodes (6): parametrize, Матрица прав определяет доступность reject., Для returned_* действует агрегирующее правило returned_(all)., Отзыв доступен только автору и не для финальных approved/rejected., Матрица прав определяет доступность approve для ролей и статусов., TestApproveRejectRequest

### Community 116 - ".post"
Cohesion: 0.24
Nodes (7): LoginView, extend_schema, Request, Response, Сменяет пароль текущего пользователя после проверки текущего пароля., Получение JWT токена по email и паролю., TokenObtainPairView

### Community 117 - "institute_access.py"
Cohesion: 0.09
Nodes (27): Доменная логика управления пользователями., ID подразделений для фильтрации; None — без ограничения., Доменная логика для списка проектов., Доменная логика для проектных треков., Доменная логика для направлений подготовки., application_available_for_institute(), application_belongs_to_institutes(), get_accessible_institute_codes() (+19 more)

### Community 118 - "User"
Cohesion: 0.05
Nodes (26): AbstractBaseUser, QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., User, Возвращает пользователя по ID., Сохраняет изменения пользователя., check_and_fix_user(), Проверяем и исправляем пользователя (+18 more)

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → дефолты 4/7., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "StudyGroupMemberDTO"
Cohesion: 0.32
Nodes (3): Any, Строка списка группы из контингента., StudyGroupMemberDTO

### Community 121 - "TestProjectApplicationSemesterAutoAssign"
Cohesion: 0.11
Nodes (12): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Автоподстановка семестра при создании заявки., Тесты для проверки наличия поля is_external в ответах API., POST /api/showcase/project-applications/ возвращает is_external в ответе., GET /api/showcase/project-applications/{id}/ возвращает is_external в ответе. (+4 more)

### Community 122 - "TestTagViewSetDelete"
Cohesion: 0.20
Nodes (6): Тесты для удаления тегов через API., cpds может удалять общие теги., cpds не может удалять теги с подразделением., admin может удалять любые теги., Остальные роли не могут удалять теги., TestTagViewSetDelete

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
Cohesion: 0.27
Nodes (6): Фильтрация учебных групп по роли пользователя., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., StudyGroupDomain, django_db, TestStudyGroupMyGroupAccess

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

### Community 138 - "test_team_lobby_viewset.py"
Cohesion: 0.36
Nodes (8): api_client(), _approved_app(), direction(), lobby_setup(), fixture, Тесты API лобби формирования команд., study_group(), _track()

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

### Community 143 - "PasswordChangeSerializer"
Cohesion: 0.29
Nodes (4): PasswordChangeSerializer, Any, Возвращает учебную группу пользователя или None., Сериализатор для смены пароля аутентифицированного пользователя.

### Community 144 - "parse_miit_ief_groups.py"
Cohesion: 0.60
Nodes (4): extract_block(), main(), parse_groups(), Парсинг групп ИЭФ со страницы miit.ru/timetable.

### Community 146 - "TestSemesterAssignViewSet"
Cohesion: 0.29
Nodes (3): Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, TestSemesterAssignViewSet

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

### Community 156 - "DirectionViewSet"
Cohesion: 0.43
Nodes (4): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений.

### Community 157 - "teams/admin.py"
Cohesion: 0.27
Nodes (11): DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin, TeamSemesterAdmin (+3 more)

### Community 159 - "ProjectApplicationComment"
Cohesion: 0.40
Nodes (3): ProjectApplicationComment, Сервис для управления комментариями к проектным заявкам. Обеспечивает…, Unit-тесты для CommentService. Проверяем добавление комментариев, получение…

### Community 164 - "._my_team_dict"
Cohesion: 0.33
Nodes (3): Студент принимает приглашение., Лимиты команды: свой трек → единственный трек группы → дефолты., Сериализация «Моей команды» с резолвом лимитов без N+1.

### Community 165 - "fixture"
Cohesion: 0.22
Nodes (9): institute(), fixture, Возвращает класс модели пользователя для удобства., Создаёт набор ролей, используемых в тестах. Возвращает dict: code -> Role, Создаёт все необходимые статусы для сценариев сервисов., Создаёт институт, связанный с родительским подразделением., roles(), statuses() (+1 more)

### Community 166 - "showcase/urls.py"
Cohesion: 0.18
Nodes (10): ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…, InstituteViewSet (+2 more)

### Community 170 - "Command"
Cohesion: 0.40
Nodes (4): Command, Any, BaseCommand, Проставляет связи институтов с подразделениями по совпадению названий.

### Community 189 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 197 - "test_link_institutes_by_name_simple"
Cohesion: 0.40
Nodes (6): Any, django_db, Простейший сценарий: для каждого института есть одноимённое подразделение., Институты без одноимённого подразделения остаются без связанного подразделения., test_link_institutes_by_name_simple(), test_link_institutes_without_matching_department()

### Community 200 - "other_institute"
Cohesion: 0.40
Nodes (5): directions(), other_institute(), fixture, Три направления для сценариев фильтрации., Второй институт на другом подразделении.

### Community 202 - "test_study_group_service.py"
Cohesion: 0.50
Nodes (4): direction(), fixture, Тесты StudyGroupService., study_groups()

### Community 206 - "TestGetUserInstituteCodes"
Cohesion: 0.50
Nodes (3): django_db, Разрешение институтов по подразделению пользователя., TestGetUserInstituteCodes

### Community 242 - "Текущий статус реализации"
Cohesion: 0.40
Nodes (5): ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации, 🔧 Требует доработки

### Community 243 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

### Community 244 - "TeamEventLogPagination"
Cohesion: 0.67
Nodes (3): PageNumberPagination, Пагинация ленты событий команды (фиксированный page_size=50)., TeamEventLogPagination

### Community 245 - "teams/models.py"
Cohesion: 0.07
Nodes (33): MyTeamViewSet, API лобби формирования команд и «Моей команды»., Раздел «Моя команда» для капитана и участника., Постоянная команда участников проектной деятельности., Участник команды в конкретном семестре., Role, Team, TeamSemesterMember (+25 more)

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 277 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 278 - "InstituteSerializer"
Cohesion: 0.67
Nodes (3): InstituteSerializer, Meta, Сериализатор для институтов/академий.

### Community 280 - "ProjectTrackCreateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackCreateSerializer, Сериализатор для создания проектного трека., Проверяет согласованность лимитов размера команды.

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 292 - "test_my_team_viewset.py"
Cohesion: 0.08
Nodes (20): Заявка должна быть в статусе pending., Meta, Заявка студента на вступление в команду в семестре., Лог действий по команде., TeamEventLog, TeamJoinRequest, QuerySet, Лог событий команды в семестре (новые сверху). (+12 more)

### Community 296 - "ProjectViewSet"
Cohesion: 0.25
Nodes (5): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией.

### Community 297 - "project_service.py"
Cohesion: 0.14
Nodes (10): ProjectDomain, Коды институтов для фильтрации; None — без ограничения., Правила доступа и фильтрации для списка проектов., ProjectRepository, QuerySet, Репозиторий для списка проектов., Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру. (+2 more)

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

### Community 323 - "ProjectTrackUpdateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackUpdateSerializer, Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

## Knowledge Gaps
- **216 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **111 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `.create_tag`, `Department`, `ProjectApplicationRepository`, `ProjectApplicationService`, `accounts/views.py`, `Any`, `test_project_track_service.py`, `UserListDTO`, `PasswordChangeSerializer`, `.get_filtered_queryset`, `StudyGroup`, `TagService`, `ProjectTrackService`, `StudentShowcaseDomain`, `ApplicationDashboardService`, `TeamLobbyService`, `ProjectTrackProjectListDTO`, `ProjectService`, `project_service.py`, `ProjectTrack`, `CommentService`, `UserSerializer`, `.approve_application`, `StudentWithStudyGroupPermission`, `TestCanUpdateTag`, `team_lobby_service.py`, `UserManagementService`, `StudyGroupService`, `ProjectTrackPermission`, `.submit_application`, `ProjectTrackDomain`, `InvolvedManagementService`, `TestUserManagementDomain`, `accounts/admin.py`, `StudentShowcaseService`, `.get_filtered_queryset`, `DirectionService`, `TestCanCreateTag`, `direction_service.py`, `TestCanDeleteTag`, `TeamSemester`, `.get_filtered_queryset`, `.resolve_list_semester_id`, `ProjectApplicationCreateDTO`, `.view_application`, `PasswordResetSerializer`, `ApplicationLoggingService`, `institute_access.py`, `teams/models.py`, `StudyGroupMemberDTO`, `StudyGroupDomain`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `Department`, `ProjectApplicationRepository`, `ProjectApplicationService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `TestApplicationDashboardService`, `test_team_lobby_viewset.py`, `test_project_track_service.py`, `.get_filtered_queryset`, `StudyGroup`, `TestSemesterAssignViewSet`, `test_project_track_viewset.py`, `TestDepartmentPlanViewSetCreate`, `TagService`, `ProjectTrackService`, `test_student_showcase_viewset.py`, `TestProjectApplicationReadDTO`, `TestTagViewSet`, `ProjectService`, `fixture`, `._create_app`, `TestUpdateAndQueriesService`, `PreRegisteredStudent`, `TestSubmitApplicationService`, `test_my_team_viewset.py`, `CommentService`, `TestCanUpdateTag`, `TestDepartmentPlanViewSetList`, `UserManagementService`, `test_import_preregistered_students.py`, `StudyGroupService`, `ProjectTrackDomain`, `TagUpdateDTO`, `TestProjectApplicationListSemesterFilter`, `TestUserManagementDomain`, `.get_filtered_queryset`, `DirectionService`, `TestApplicationDashboardViewSet`, `TestTagViewSetCreate`, `TestCanCreateTag`, `TestProjectApplicationListDTO`, `TestGetUserInstituteCodes`, `TestCanDeleteTag`, `TestProjectViewSet`, `.get_filtered_queryset`, `TestProjectApplicationViewSetIsInternalCustomer`, `TestProjectApplicationNewFieldsCreateUpdate`, `TestProjectApplicationViewSetTransferToInstitute`, `TestTagServiceDelete`, `student_user`, `ApplicationNotificationService`, `ProjectApplicationCreateDTO`, `ApplicationLoggingService`, `TestProjectApplicationSemesterAutoAssign`, `TestTagViewSetDelete`, `StudyGroupDomain`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `make_user`, `Department`, `ProjectApplicationRepository`, `ProjectApplicationService`, `accounts/views.py`, `ProjectApplicationViewSet`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `TestApplicationDashboardService`, `test_team_lobby_viewset.py`, `test_project_track_service.py`, `StudyGroup`, `test_project_track_viewset.py`, `TestSemesterAssignViewSet`, `TestDepartmentPlanViewSetCreate`, `ProjectTrackService`, `StudentShowcaseDomain`, `test_student_showcase_viewset.py`, `test_import_study_groups_from_contingent.py`, `ApplicationDashboardService`, `TeamLobbyService`, `ProjectService`, `test_my_team_viewset.py`, `project_service.py`, `team_lobby_service.py`, `TestDepartmentPlanViewSetList`, `UserManagementService`, `StudyGroupService`, `Command`, `TestProjectApplicationListSemesterFilter`, `accounts/admin.py`, `StudentShowcaseService`, `DepartmentPlanViewSet`, `AccountsApiTests`, `TeamSemesterViewSet`, `TestProjectViewSet`, `.resolve_list_semester_id`, `TestProjectApplicationNewFieldsCreateUpdate`, `ProjectApplicationCreateDTO`, `teams/models.py`, `institute_access.py`, `TestProjectApplicationSemesterAutoAssign`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 483 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 483 INFERRED edges - model-reasoned connections that need verification._
- **Are the 44 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 44 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 72 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._