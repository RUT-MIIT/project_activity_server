# Graph Report - project_activity_server  (2026-08-28)

## Corpus Check
- 311 files · ~143,382 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4627 nodes · 9040 edges · 326 communities (220 shown, 106 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 877 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c0cd017b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .create_tag
- make_user
- Department
- Ответственный по институту — API для фронта
- InstituteResponsibleService
- accounts/views.py
- ProjectApplicationViewSet
- Any
- test_institute_responsible_viewset.py
- TagRepository
- ApplicationDashboardService
- QuerySet
- ProjectApplication
- ProjectTrackAddApplicationItemSerializer
- UserManagementService
- Semester
- prepare_study_groups_xlsx.py
- StudyGroup
- ProjectTrack
- Direction
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- ProjectTrackService
- StudentShowcaseDomain
- StudyGroupService
- test_student_showcase_viewset.py
- test_import_study_groups_from_contingent.py
- MyTeamViewSet
- TestTeamLobbyViewSet
- PreRegisteredStudentRepository
- TestProjectApplicationReadDTO
- AvailableActionDTO
- TeamLobbyService
- .get_group_detail
- ProjectTrackViewSet
- TestTagViewSet
- ProjectService
- StudyGroupViewSet
- ProjectApplicationService
- normalize_cell
- PreRegisteredStudent
- TestApproveRejectRequest
- ApplicationDashboardRepository
- .update_application
- TestCommentService
- Path
- test_link_institutes_by_name_simple
- .approve_application
- test_project_track_service.py
- TestCanUpdateTag
- TagViewSet
- TagUpdateDTO
- team_lobby_service.py
- TestDepartmentPlanViewSetList
- Any
- test_import_preregistered_students.py
- ValidationResult
- .validate_update
- accounts/permissions.py
- accounts/serializers.py
- is_cpds_department
- ProjectTrackDomain
- ._application_institute_access_q
- UserSerializer
- Примеры использования поля is_internal_customer
- .can_change_status
- Command
- .resolve_list_semester_id
- UserManagementDomain
- accounts/admin.py
- StudentShowcaseService
- .can_user_access_application
- .get_filtered_queryset
- DepartmentPlanViewSet
- ProjectTrackRepository
- CommentService
- InstituteResponsibleDomain
- TestApplicationDashboardViewSet
- TestTagViewSetCreate
- TestCanCreateTag
- Витрина проектов (студент) — API для фронта
- ProjectApplicationCreateDTO
- API для работы с проектными заявками
- AccountsApiTests
- TestCanDeleteTag
- mark_teachers_in_system.py
- TeamSemesterViewSet
- Command
- Command
- ApplicationCapabilities
- ._resolve_context
- TestProjectViewSet
- .calculate_initial_status
- QuerySet
- .get_filtered_queryset
- DirectionService
- Tag.py
- TestProjectApplicationViewSetIsInternalCustomer
- TestProjectApplicationNewFieldsCreateUpdate
- TestProjectApplicationViewSetTransferToInstitute
- test_institute_access.py
- extract_group_abbrev.py
- TestTagServiceDelete
- Валидационные правила
- Role
- Command
- student_user
- .auth
- ApplicationNotificationService
- ._track_detail_queryset
- .validate_create
- _generate_collection.py
- .list_applications
- ApplicationLoggingService
- test_export_import_departments_roundtrip
- ProjectTrackAddApplicationsSerializer
- .post
- institute_access.py
- User
- TestMyTeamViewSet
- StudyGroupMemberDTO
- TestProjectApplicationListSemesterFilter
- StudentShowcaseEnrollResultDTO
- Поддержка multipart/form-data
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- test_study_group_domain.py
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
- ProjectTrackCreateSerializer
- deploy.sh
- action_types.py
- export_client_sources_to_docx.py
- make_source_docx.py
- application_dashboard_service.py
- parse_miit_ief_groups.py
- Command
- ._resolve_institute_semester
- schema.py
- ShowcaseConfig
- .recalculate_recommended_teams_count
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- teams/models.py
- teams/admin.py
- 0011_migrate_team_data.py
- StudyGroup.py
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- test_study_group_viewset.py
- PasswordChangeSerializer
- showcase/urls.py
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- Settings
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
- ProjectTrackUpdateSerializer
- .test_registration_request_list_requires_privileged_user
- .test_registration_request_race_condition_integrity_error
- TagService
- .test_semester_create_allowed_for_admin_and_cpds
- Direction.py
- .test_semester_list_requires_auth
- PasswordResetSerializer
- .test_user_me_institute_code_none_if_no_institute
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
- ApplicationDashboard.py
- .get_filtered_queryset
- .submit_application
- TestProjectApplicationViewSetSimple
- InstituteSerializer
- Command
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
- TestTagViewSetDelete
- Схема БД: студенческий портал
- Справочные эндпоинты
- DirectionViewSet
- test_preregistered_student_viewset.py
- institute_responsible_service.py
- TeamSemester
- ProjectRepository
- 0017_copy_studygroup_mentors_to_semester.py
- TestGetUserInstituteCodes
- .test_departments_list_allow_any_detail_requires_auth
- .test_registration_request_create_anonymous_allowed
- .test_registration_request_reject_forbidden_for_regular_user
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- .get_existing_application_ids
- Вариант 1: импорт схемы с автообновлением
- .test_semester_list_is_active_from_settings
- .test_user_me_institute_code_from_department_institute
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- 0016_studygroupsemester.py
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- UserListDTO
- .test_user_roles_list_requires_auth_and_returns
- .add_applications
- .add_groups
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- .get_linked_applications
- .get_external_share_chart_data

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 502 edges
2. `User` - 238 edges
3. `ProjectApplication` - 146 edges
4. `Department` - 142 edges
5. `ProjectApplicationService` - 136 edges
6. `ProjectApplicationCreateDTO` - 109 edges
7. `Semester` - 108 edges
8. `StudyGroup` - 84 edges
9. `Institute` - 70 edges
10. `ProjectTrackService` - 70 edges

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

## Communities (326 total, 106 thin omitted)

### Community 0 - ".create_tag"
Cohesion: 0.18
Nodes (6): atomic, Бизнес-операция: удаление тега. Args: tag_id: ID тега для удаления user:…, Бизнес-операция: присоединение подразделения к тегу. Args: tag_id: ID тега…, Бизнес-операция: отцепление подразделения от тега. Если тег не базовый…, Бизнес-операция: создание тега. Args: dto: DTO с данными для создания тега…, Бизнес-операция: обновление тега. Args: tag_id: ID тега для обновления dto: DTO…

### Community 1 - "make_user"
Cohesion: 0.03
Nodes (22): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+14 more)

### Community 2 - "Department"
Cohesion: 0.04
Nodes (69): Command, BaseCommand, Department, get_root_department(), Утилиты для работы с подразделениями., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, create_test_user(), Создаем тестового пользователя (+61 more)

### Community 3 - "Ответственный по институту — API для фронта"
Cohesion: 0.08
Nodes (24): 1. Список активных групп института, 2. Сотрудники института, 3. Группы с назначенными наставниками, 4. Назначить наставника группе, 5. Снять наставника с группы, Значения `semester_id`, Общие query-параметры, Ответ `200` (+16 more)

### Community 4 - "InstituteResponsibleService"
Cohesion: 0.15
Nodes (20): delete, AssignMentorSerializer, InstituteResponsiblePermission, InstituteResponsibleViewSet, action, BasePermission, extend_schema, Request (+12 more)

### Community 5 - "accounts/views.py"
Cohesion: 0.07
Nodes (36): RegistrationRequest, Status, IsCpdsUser, Разрешает доступ только сотрудникам, администраторам или роли ЦПДС., Разрешает доступ только пользователям с ролью ЦПДС (код роли `cpds`)., RegistrationRequestManagePermission, ApproveRequestSerializer, DepartmentSerializer (+28 more)

### Community 6 - "ProjectApplicationViewSet"
Cohesion: 0.05
Nodes (33): format_validation_errors(), get_error_message(), ProjectApplicationViewSet, action, extend_schema, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, GET /api/project-applications/external/ Получение списка всех внешних заявок… (+25 more)

### Community 7 - "Any"
Cohesion: 0.06
Nodes (21): ProjectTrackAggregatedStatisticsDTO, ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackStatisticsDTO, Any, Преобразует DTO в словарь для API., DTO заявки в проектном треке. (+13 more)

### Community 8 - "test_institute_responsible_viewset.py"
Cohesion: 0.07
Nodes (23): QuerySet, Репозиторий для StudyGroupSemester и связанных выборок., Снимает наставника с группы в семестре., Возвращает наставника группы в семестре., Доступ к данным групп в семестре и сотрудников института., Активные группы института., Активные группы с prefetch наставника в семестре., Возвращает группу по ID или None. (+15 more)

### Community 9 - "TagRepository"
Cohesion: 0.05
Nodes (34): DTO для работы с тегами., Репозиторий для работы с тегами в БД. Изолирует всю работу с базой данных от…, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., Создание тега в БД. Args: dto: DTO с данными для создания тега Returns:…, Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:… (+26 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.06
Nodes (28): ApplicationDashboardService, Оркестрация получения данных дашборда заявок., django_db, Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external., Фильтр по группам статусов., Карточка in_work = total - approved - rejected., Среднее и медиана времени до решения. (+20 more)

### Community 11 - "QuerySet"
Cohesion: 0.10
Nodes (15): QuerySet, Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению., Строит карту institute_code -> множество id заявок., Строит карту department_id -> множество id заявок (как в DepartmentPlan)., Заявки из queryset, не попавшие ни в одну дочернюю категорию рейтинга., Данные для горизонтального stacked bar., Собирает данные категорий для рейтинга и доли внешних заявок. (+7 more)

### Community 12 - "ProjectApplication"
Cohesion: 0.03
Nodes (54): Репозиторий для управления пользователями., ProjectListDTO, Any, DTO для списка проектов., Возвращает причастное подразделение верхнего уровня (без родителя). ЦПДС…, ProjectApplication, ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты… (+46 more)

### Community 13 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 14 - "UserManagementService"
Cohesion: 0.08
Nodes (19): ViewSet для управления пользователями., QuerySet, Доступ к данным пользователей для управления., Базовый queryset без администраторов., Список пользователей с оптимизацией запросов., Возвращает пользователя по ID., Сохраняет изменения пользователя., UserRepository (+11 more)

### Community 15 - "Semester"
Cohesion: 0.10
Nodes (13): Идемпотентный импорт строк модели Settings из CSV., Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Следующий семестр для новых заявок (Settings.next_semester_code)., Semester, Command, BaseCommand, Добавляет причастные подразделения института к заявке. (+5 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroup"
Cohesion: 0.08
Nodes (25): DTO для API ответственного по институтам., MyStudyGroupDTO, DTO для эндпоинта «Моя группа»., Возвращает наставника: из семестра или fallback на StudyGroup.mentor., Полные данные учебной группы для текущего студента., StudyGroup, QuerySet, Репозиторий для учебных групп. (+17 more)

### Community 18 - "ProjectTrack"
Cohesion: 0.05
Nodes (47): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+39 more)

### Community 19 - "Direction"
Cohesion: 0.14
Nodes (13): DirectionDomain, Доменная логика для направлений подготовки., Фильтрация направлений по роли пользователя., Direction, Level, Направление подготовки (ФГОС ВО)., DirectionRepository, QuerySet (+5 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (28): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationCreateSerializer, ProjectApplicationUpdateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы… (+20 more)

### Community 22 - "ProjectTrackService"
Cohesion: 0.13
Nodes (6): Создаёт DTO из словаря., ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), django_db, TestProjectTrackService

### Community 23 - "StudentShowcaseDomain"
Cohesion: 0.06
Nodes (30): Правила доступа и записи команды на проект витрины., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI)., StudentShowcaseDomain (+22 more)

### Community 24 - "StudyGroupService"
Cohesion: 0.18
Nodes (6): Оркестрация Domain + Repository для StudyGroup., StudyGroupService, django_db, TestMyStudyGroupService, django_db, TestStudyGroupService

### Community 25 - "test_student_showcase_viewset.py"
Cohesion: 0.08
Nodes (19): api_client(), _approved_app(), _create_assembled_team(), direction(), other_group(), django_db, fixture, Тесты API студенческой витрины проектов. (+11 more)

### Community 26 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.12
Nodes (20): build_group_import_row(), build_group_name(), calculate_course_number(), GroupImportRow, parse_direction_level(), parse_permanent_group_code(), ParsedPermanentGroup, Чистая логика импорта учебных групп из отчёта контингента 1С. (+12 more)

### Community 27 - "MyTeamViewSet"
Cohesion: 0.08
Nodes (32): PageNumberPagination, ApproveJoinRequestSerializer, CreateInvitationSerializer, CreateTeamSerializer, MyTeamViewSet, action, extend_schema, extend_schema_view (+24 more)

### Community 28 - "TestTeamLobbyViewSet"
Cohesion: 0.14
Nodes (7): _create_captained_team(), django_db, Команда без трека при одном треке у группы → min/max с трека группы., После создания своей команды pending-заявка в чужую → obsolete., При нескольких треках track_id не проставляется; лимиты — effective по трекам., Если группе доступен один трек — он проставляется без track_id в body., TestTeamLobbyViewSet

### Community 29 - "PreRegisteredStudentRepository"
Cohesion: 0.09
Nodes (12): PreRegisteredStudentRepository, QuerySet, Репозиторий предрегистрации студентов., Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по табельному номеру., Возвращает предрегистрацию по нормализованному СНИЛС., Возвращает предрегистрацию по первичному ключу. (+4 more)

### Community 30 - "TestProjectApplicationReadDTO"
Cohesion: 0.05
Nodes (22): Exception, django_db, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None., target_institutes сериализуется как список словарей с code и name., tags сериализуется как список словарей с id, name и category. (+14 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "TeamLobbyService"
Cohesion: 0.11
Nodes (22): atomic, QuerySet, UserType, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент принимает приглашение., Оркестрация Domain + Repository для студенческого лобби., Студент отклоняет приглашение. (+14 more)

### Community 33 - ".get_group_detail"
Cohesion: 0.13
Nodes (9): ProjectTrackGroupDetailDTO, ProjectTrackGroupProjectDTO, DTO проекта в деталях группы., Преобразует DTO в словарь для API., DTO деталей группы с назначенными проектами., Преобразует DTO в словарь для API., UserType, Подгружает подразделение пользователя для проверки институтов. (+1 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.13
Nodes (23): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+15 more)

### Community 35 - "TestTagViewSet"
Cohesion: 0.10
Nodes (11): Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level). (+3 more)

### Community 36 - "ProjectService"
Cohesion: 0.21
Nodes (5): ProjectService, Оркестрация Domain + Repository для списка проектов., TestProjectApplicationNewFieldsLists, django_db, TestProjectService

### Community 37 - "StudyGroupViewSet"
Cohesion: 0.22
Nodes (7): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/ — список и просмотр учебных групп., Парсит query-параметр is_end; None — фильтр не применяется., StudyGroupViewSet

### Community 38 - "ProjectApplicationService"
Cohesion: 0.02
Nodes (76): ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка., Бизнес-операция: получение заявок по статусу., Бизнес-операция: получение последних заявок. (+68 more)

### Community 39 - "normalize_cell"
Cohesion: 0.12
Nodes (16): build_preregistered_student_import_row(), last_names_match(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки. (+8 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.16
Nodes (11): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если предрегистрация уже привязана к User., MonkeyPatch, Any, APIClient, django_db, override_settings (+3 more)

### Community 41 - "TestApproveRejectRequest"
Cohesion: 0.27
Nodes (6): parametrize, Матрица прав определяет доступность reject., Для returned_* действует агрегирующее правило returned_(all)., Отзыв доступен только автору и не для финальных approved/rejected., Матрица прав определяет доступность approve для ролей и статусов., TestApproveRejectRequest

### Community 42 - "ApplicationDashboardRepository"
Cohesion: 0.06
Nodes (20): ApplicationDashboardDomain, Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп., Парсит query-параметр application_type., Парсит query-параметр days., Возвращает id подразделения и всех его потомков., Проверяет право пользователя на просмотр дашборда., Коды институтов пользователя; None — без ограничения. (+12 more)

### Community 43 - ".update_application"
Cohesion: 0.15
Nodes (9): Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Не-автор и не-ЦПДС не может редактировать заявку., Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult., CPDS может редактировать одобренные заявки., institute_validator-автор: save совпадает с available_actions (подразделение…, institute_validator без причастного подразделения не может сохранить. (+1 more)

### Community 44 - "TestCommentService"
Cohesion: 0.10
Nodes (12): django_db, Пустой текст вызывает ValueError., Тесты для CommentService., Несуществующая заявка вызывает ValueError., Успешное получение комментариев к заявке., Успешное добавление комментария к заявке., Если комментариев нет, возвращается пустой список., Несуществующая заявка вызывает ValueError. (+4 more)

### Community 45 - "Path"
Cohesion: 0.16
Nodes (13): aga_institute(), direction(), Any, django_db, fixture, Path, Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта. (+5 more)

### Community 46 - "test_link_institutes_by_name_simple"
Cohesion: 0.40
Nodes (6): Any, django_db, Простейший сценарий: для каждого института есть одноимённое подразделение., Институты без одноимённого подразделения остаются без связанного подразделения., test_link_institutes_by_name_simple(), test_link_institutes_without_matching_department()

### Community 47 - ".approve_application"
Cohesion: 0.09
Nodes (18): Any, Возвращает список доступных действий согласно матрице., atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку. (+10 more)

### Community 48 - "test_project_track_service.py"
Cohesion: 0.07
Nodes (28): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackCreateDTO, ProjectTrackUpdateDTO, DTO для проектных треков., DTO для создания проектного трека., DTO для добавления групп в трек. (+20 more)

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+2 more)

### Community 50 - "TagViewSet"
Cohesion: 0.10
Nodes (22): Разрешает доступ к управлению тегами только для ролей cpds, admin и…, TagManagePermission, Инициализация из модели Tag., TagReadDTO, DepartmentAttachDetachSerializer, action, Request, Response (+14 more)

### Community 51 - "TagUpdateDTO"
Cohesion: 0.07
Nodes (21): DTO для обновления тега., TagUpdateDTO, Тесты для метода update репозитория., Обновление названия тега., Обновление категории тега., Обновление подразделений тега., Удаление подразделений из тега (установка departments=[])., Обновление нескольких полей одновременно. (+13 more)

### Community 52 - "team_lobby_service.py"
Cohesion: 0.05
Nodes (34): Доменная логика студенческой витрины проектов., Доменные правила лобби формирования команд., Удаление: капитан, forming, в составе только он., Подтверждение состава: капитан, forming, размер в лимитах трека., Приглашение должно быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды»., Лимиты размера команды. Приоритет: 1) трек команды; 2) effective по трекам…, True, если студент без команды и есть свободный слот. (+26 more)

### Community 53 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 54 - "Any"
Cohesion: 0.13
Nodes (10): Any, Карточка проекта в списке трека витрины., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Детали проекта для студента (без контактов)., Преобразует DTO в словарь для API., StudentShowcaseProjectDetailDTO, StudentShowcaseProjectListItemDTO (+2 more)

### Community 55 - "test_import_preregistered_students.py"
Cohesion: 0.20
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 56 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 57 - ".validate_update"
Cohesion: 0.19
Nodes (8): Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Тесты для валидации при обновлении заявки., Валидные поля при обновлении проходят проверку., Название короче 5 символов вызывает ошибку., Email без символа @ вызывает ошибку., Валидация проверяет только переданные поля (None игнорируются)., Пустые строки вызывают ошибки валидации., TestValidateUpdate

### Community 58 - "accounts/permissions.py"
Cohesion: 0.06
Nodes (29): IsAdminOrCpds, IsInstituteValidator, ProjectManagementPermission, APIView, BasePermission, Request, Пользовательские permissions для приложения accounts., Проверяет наличие прав у пользователя. (+21 more)

### Community 59 - "accounts/serializers.py"
Cohesion: 0.06
Nodes (33): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Отправляет администратору письмо о расхождении данных., Публичные операции предрегистрации студентов. (+25 more)

### Community 60 - "is_cpds_department"
Cohesion: 0.12
Nodes (11): is_cpds_department(), Проверяет, что подразделение — ЦПДС (координирующее, не основное)., django_db, Тесты для функции get_root_department., Подразделение без parent возвращает само себя., Подразделение с одним уровнем parent возвращает корневое., Подразделение с несколькими уровнями parent возвращает корневое., None на входе возвращает None. (+3 more)

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.10
Nodes (12): ProjectTrackDomain, Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя., Проверяет, может ли пользователь управлять проектными треками., Коды институтов пользователя; None — без ограничения (admin/cpds)., ID подразделений, доступных пользователю; None — без ограничения., True для admin/cpds/staff — статистика без institute_code. (+4 more)

### Community 62 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 63 - "UserSerializer"
Cohesion: 0.18
Nodes (9): Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., UserSerializer, CustomTokenObtainPairSerializer (+1 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 66 - "Command"
Cohesion: 0.21
Nodes (8): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Дедуплицирует строки по коду постоянной группы., Возвращает направление подготовки, создавая при необходимости., Возвращает институт по коду справочника.

### Community 67 - ".resolve_list_semester_id"
Cohesion: 0.22
Nodes (5): Разбор query-параметра semester_id для GET-списков: id, next, actual., Any, Возвращает данные учебной группы текущего студента., django_db, TestSemesterResolveListSemesterId

### Community 68 - "UserManagementDomain"
Cohesion: 0.11
Nodes (12): QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., Правила доступа и валидации для управления пользователями., Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., UserManagementDomain (+4 more)

### Community 69 - "accounts/admin.py"
Cohesion: 0.16
Nodes (15): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+7 more)

### Community 70 - "StudentShowcaseService"
Cohesion: 0.19
Nodes (13): action, extend_schema, extend_schema_view, Request, Response, ViewSet студенческой витрины проектов., Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/. (+5 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.07
Nodes (19): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Тесты для проверки доступа пользователя к заявке., Автор всегда имеет доступ к своей заявке., Админ имеет доступ ко всем заявкам. (+11 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.13
Nodes (12): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, django_db, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., Тесты для фильтрации queryset тегов по ролям., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения. (+4 more)

### Community 73 - "DepartmentPlanViewSet"
Cohesion: 0.15
Nodes (15): DepartmentPlanSerializer, DepartmentPlanViewSet, action, extend_schema, Request, Response, Получить словарь планов по подразделениям для указанного семестра., Получить статистику заявок по статусам для каждого подразделения. (+7 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.08
Nodes (12): ProjectTrackRepository, Создаёт проектный трек., Обновляет поля трека., Возвращает id групп, уже привязанных к треку., Удаляет группу из трека; True если связь была., Удаляет заявку из трека; True если связь была., Количество групп в треке., Доступ к данным проектных треков. (+4 more)

### Community 75 - "CommentService"
Cohesion: 0.21
Nodes (8): ProjectApplicationComment, CommentService, atomic, Сервис для управления комментариями к проектным заявкам. Обеспечивает…, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, Unit-тесты для CommentService. Проверяем добавление комментариев, получение…

### Community 76 - "InstituteResponsibleDomain"
Cohesion: 0.12
Nodes (8): Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., InstituteResponsibleDomain, Правила доступа и валидации для ответственного по институтам., Проверяет, может ли пользователь работать с API ответственного., Определяет код института из параметра или по умолчанию., Проверяет доступ к учебной группе., Подгружает parent подразделения для resolve институтов.

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - "TestTagViewSetCreate"
Cohesion: 0.12
Nodes (9): Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем., Нельзя создать общий тег, если имя уже используется (общим или departmental… (+1 more)

### Community 79 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 80 - "Витрина проектов (студент) — API для фронта"
Cohesion: 0.14
Nodes (13): 1. Список треков с проектами, 2. Детали проекта, 3. Записать команду на проект, Витрина проектов (студент) — API для фронта, Ответ `200`, Ответ `200`, Ответ `200`, Ошибки (+5 more)

### Community 81 - "ProjectApplicationCreateDTO"
Cohesion: 0.03
Nodes (85): DenyStudentPermission, Запрещает доступ пользователям с ролью student., create_test_applications(), Создаем тестовые заявки, Общие константы приложения showcase., ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов (+77 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.11
Nodes (10): AccountsApiTests, override_settings, Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Создание заявки без подразделения возвращает ошибку валидации., Создание заявки с несуществующим подразделением возвращает ошибку валидации., После отклонения заявки можно подать новую с тем же email., Повторная подача при активной заявке возвращает ошибку валидации., Нельзя подать заявку, если пользователь с таким email уже зарегистрирован. (+2 more)

### Community 84 - "TestCanDeleteTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения., admin может удалять любые теги. (+2 more)

### Community 85 - "mark_teachers_in_system.py"
Cohesion: 0.27
Nodes (11): build_user_indexes(), find_user(), main(), normalize_name(), Сверка преподавателей из Excel со списком пользователей prod API., Нормализует ФИО для сравнения., Ключ из набора слов ФИО (устойчив к перестановке частей)., Строит индексы пользователей по ФИО. (+3 more)

### Community 86 - "TeamSemesterViewSet"
Cohesion: 0.24
Nodes (8): action, Request, Response, POST /api/teams/team-semesters/{id}/members/ — добавить участника., DELETE /api/teams/team-semesters/{id}/members/{member_id}/., CRUD для участия команды в семестре и управления составом., GET /api/teams/team-semesters/my/?semester_id= — команды пользователя., TeamSemesterViewSet

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "Command"
Cohesion: 0.40
Nodes (4): Command, Any, BaseCommand, Проставляет связи институтов с подразделениями по совпадению названий.

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.08
Nodes (19): ApplicationCapabilities, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы., УСТАРЕВШЕ: прокси к новой матрице. Считаем, что "управление" означает…, Проверка права на редактирование заявки. Бизнес-правило: редактировать может… (+11 more)

### Community 90 - "._resolve_context"
Cohesion: 0.15
Nodes (9): Any, Возвращает группу после проверки доступа., Список активных групп института., Список сотрудников института., Группы с ID назначенных наставников в семестре., Назначает наставника группе в семестре., Снимает наставника с группы в семестре., Проверяет права пользователя. (+1 more)

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

### Community 95 - "DirectionService"
Cohesion: 0.17
Nodes (9): DirectionService, Оркестрация Domain + Repository для Direction., Список направлений с фильтрацией по роли., Направление по коду с проверкой доступа., directions(), django_db, fixture, Тесты DirectionService. (+1 more)

### Community 96 - "Tag.py"
Cohesion: 0.09
Nodes (15): Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Преобразование в словарь., DepartmentNestedSerializer, Meta, Вложенный сериализатор для подразделения., Сериализатор для тегов. (+7 more)

### Community 97 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 98 - "TestProjectApplicationNewFieldsCreateUpdate"
Cohesion: 0.27
Nodes (4): _base_create_payload(), django_db, TestMyApplicationsNewFields, TestProjectApplicationNewFieldsCreateUpdate

### Community 99 - "TestProjectApplicationViewSetTransferToInstitute"
Cohesion: 0.17
Nodes (8): Тесты для действия передачи заявки в институт по коду института., POST /api/showcase/project-applications/{id}/transfer_to_institute/ с…, Отсутствующий параметр code возвращает 400., Несуществующий код института возвращает 400 от сервиса., Институт без связанного подразделения возвращает 400., GET /api/showcase/project-applications/external/?status=... фильтрует внешние…, GET /api/showcase/project-applications/external/?status=... с несуществующим…, TestProjectApplicationViewSetTransferToInstitute

### Community 100 - "test_institute_access.py"
Cohesion: 0.16
Nodes (13): Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., application_available_for_institute(), application_belongs_to_institutes(), Проверяет доступность заявки институту для проектных треков. Заявка доступна,…, Проверяет принадлежность заявки к институтам по причастным подразделениям.…, _create_approved_app(), django_db (+5 more)

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - "TestTagServiceDelete"
Cohesion: 0.17
Nodes (7): Тесты для метода delete_tag сервиса., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять теги своего подразделения., admin может удалять любые теги., Удаление несуществующего тега вызывает ошибку., TestTagServiceDelete

### Community 103 - "Валидационные правила"
Cohesion: 0.50
Nodes (4): Валидационные правила, Обязательные поля, Обязательные поля:, Типы данных

### Community 104 - "Role"
Cohesion: 0.16
Nodes (7): Command, BaseCommand, Role, UserManager, BaseUserManager, Command, BaseCommand

### Community 105 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

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

### Community 110 - ".validate_create"
Cohesion: 0.12
Nodes (13): Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Носитель проблемы короче 5 символов вызывает ошибку., Барьер короче 10 символов вызывает ошибку., Имя и фамилия автора короче 2 символов вызывают ошибки., Тесты для валидации при создании заявки., Телефон короче 10 символов вызывает ошибку., Валидный DTO проходит проверку без ошибок., Все ошибки валидации собираются в одном результате. (+5 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - ".list_applications"
Cohesion: 0.25
Nodes (4): Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации., Бизнес-операция: получение заявок для координации пользователя. Для обычных…

### Community 113 - "ApplicationLoggingService"
Cohesion: 0.04
Nodes (48): ProjectApplicationStatusLog, ApplicationLoggingService, atomic, Логирование удаления причастного пользователя. Args: application: Заявка user:…, Логирование добавления причастного подразделения. Args: application: Заявка…, Логирование удаления причастного подразделения. Args: application: Заявка…, Сервис для логирования изменений в проектных заявках. Обеспечивает полное…, Получение всех логов по заявке. Args: application: Заявка Returns:… (+40 more)

### Community 114 - "test_export_import_departments_roundtrip"
Cohesion: 0.27
Nodes (10): Any, django_db, Экспорт и последующий импорт институтов восстанавливают данные., Экспорт и последующий импорт подразделений восстанавливают данные., Импорт институтов удаляет те, которых нет в файле., Импорт подразделений удаляет те, которых нет в файле., test_export_import_departments_roundtrip(), test_export_import_institutes_roundtrip() (+2 more)

### Community 115 - "ProjectTrackAddApplicationsSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationsSerializer, Список заявок с рекомендуемым числом команд и лимитами размера., Проверяет отсутствие дубликатов id в одном запросе.

### Community 116 - ".post"
Cohesion: 0.21
Nodes (7): LoginView, extend_schema, Request, Response, Сменяет пароль текущего пользователя после проверки текущего пароля., Получение JWT токена по email и паролю., TokenObtainPairView

### Community 117 - "institute_access.py"
Cohesion: 0.10
Nodes (22): Доменная логика управления пользователями., ID подразделений для фильтрации; None — без ограничения., get_department_subtree_ids(), Возвращает id корневого подразделения и всех его потомков., Доменная логика для списка проектов., Коды институтов для фильтрации; None — без ограничения., Доменная логика для проектных треков., get_accessible_institute_codes() (+14 more)

### Community 118 - "User"
Cohesion: 0.05
Nodes (36): AbstractBaseUser, User, ProjectTrackPermission, Разрешает доступ к проектным трекам для admin, cpds и institute_validator., check_and_fix_user(), Проверяем и исправляем пользователя, PermissionsMixin, Проверяет роль student и наличие учебной группы; возвращает group_id. (+28 more)

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → effective max(min)/min(max)., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "StudyGroupMemberDTO"
Cohesion: 0.32
Nodes (3): Any, Строка списка группы из контингента., StudyGroupMemberDTO

### Community 121 - "TestProjectApplicationListSemesterFilter"
Cohesion: 0.07
Nodes (17): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, Фильтр ?semester_id= в GET-списке заявок., Автоподстановка семестра при создании заявки. (+9 more)

### Community 122 - "StudentShowcaseEnrollResultDTO"
Cohesion: 0.17
Nodes (8): Результат записи команды на проект., Преобразует DTO в словарь для API., StudentShowcaseEnrollResultDTO, atomic, UserType, Записывает команду капитана на проект., Резолвит semester_id; по умолчанию actual., Детали проекта, доступного группе студента.

### Community 123 - "Поддержка multipart/form-data"
Cohesion: 0.33
Nodes (6): Допустимые форматы файлов, Заголовки, Загрузка файлов, Максимальный размер файла, Поддержка multipart/form-data, Тело запроса

### Community 124 - "test_import_institutes.py"
Cohesion: 0.54
Nodes (7): django_db, Path, Тесты команды import_institutes., test_import_institutes_clear_removes_missing(), test_import_institutes_is_idempotent(), test_import_institutes_updates_existing(), _write_institutes_csv()

### Community 125 - "build_fgos_napravleniya_csv.py"
Cohesion: 0.43
Nodes (6): collect_codes(), fetch(), main(), parse_table_rows(), Собрать fgos_specialitet_napravleniya.csv: level, code, name (без групп…, middle: '03' — бакалавриат, '05' — специалитет.

### Community 126 - "test_study_group_domain.py"
Cohesion: 0.12
Nodes (15): QuerySet, Фильтрация учебных групп по роли пользователя., institute_validator — только группы своих институтов., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., StudyGroupDomain, direction(), other_institute() (+7 more)

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
Cohesion: 0.15
Nodes (13): 2. Получение пользователя, 4. Список проектов, Query-параметры, Заголовки, Ошибки, Ошибки, Поведение по ролям, Права доступа (+5 more)

### Community 138 - "ProjectTrackCreateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackCreateSerializer, Сериализатор для создания проектного трека., Проверяет согласованность лимитов размера команды.

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

### Community 143 - "application_dashboard_service.py"
Cohesion: 0.13
Nodes (13): DashboardFilters, Доменная логика дашборда проектных заявок., Параметры фильтрации дашборда., ApplicationDashboardDTO, Any, DTO для дашборда проектных заявок., Преобразует DTO в словарь для API., DTO блока KPI-карточек. (+5 more)

### Community 144 - "parse_miit_ief_groups.py"
Cohesion: 0.60
Nodes (4): extract_block(), main(), parse_groups(), Парсинг групп ИЭФ со страницы miit.ru/timetable.

### Community 146 - "._resolve_institute_semester"
Cohesion: 0.07
Nodes (16): ProjectTrackGroupListDTO, ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, ProjectTrackProjectListDTO, DTO группы со счётчиком назначенных проектов., Преобразует DTO в словарь для API., DTO проекта со счётчиком назначенных групп., Преобразует DTO в словарь для API. (+8 more)

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

### Community 156 - "teams/models.py"
Cohesion: 0.07
Nodes (33): API лобби формирования команд и «Моей команды»., Meta, Наставник учебной группы в конкретном семестре., Постоянная команда участников проектной деятельности., Участник команды в конкретном семестре., Role, StudyGroupSemester, Team (+25 more)

### Community 157 - "teams/admin.py"
Cohesion: 0.14
Nodes (16): DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin, TeamSemesterAdmin (+8 more)

### Community 159 - "StudyGroup.py"
Cohesion: 0.19
Nodes (10): Any, DTO для учебных групп., DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, Компактная выдача для списка учебных групп. (+2 more)

### Community 164 - "test_study_group_viewset.py"
Cohesion: 0.47
Nodes (5): direction(), other_institute(), fixture, Тесты StudyGroupViewSet., study_groups()

### Community 165 - "PasswordChangeSerializer"
Cohesion: 0.11
Nodes (14): PasswordChangeSerializer, PasswordResetConfirmSerializer, Any, Возвращает учебную группу пользователя или None., Сериализатор для смены пароля аутентифицированного пользователя., institute(), fixture, Возвращает класс модели пользователя для удобства. (+6 more)

### Community 166 - "showcase/urls.py"
Cohesion: 0.18
Nodes (10): ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…, InstituteViewSet (+2 more)

### Community 170 - "Settings"
Cohesion: 0.11
Nodes (24): Ключ–значение настроек приложения (редактируемые из админки / импортом)., Settings, api_client(), direction(), my_team_setup(), fixture, Тесты API «Моя команда»., semester() (+16 more)

### Community 189 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 197 - "ProjectTrackUpdateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackUpdateSerializer, Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

### Community 200 - "TagService"
Cohesion: 0.06
Nodes (33): Чистая бизнес-логика для тегов - только функции, никаких эффектов., Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, TagDomain, DTO для создания тега., TagCreateDTO, Сервис для оркестрации операций с тегами. Координирует Domain, Repository и DTO., Бизнес-операция: получение списка тегов с фильтрацией по ролям. Для… (+25 more)

### Community 202 - "Direction.py"
Cohesion: 0.20
Nodes (7): DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DirectionSerializer, Meta, Сериализатор направления подготовки.

### Community 206 - "API Документация - Проектные заявки"
Cohesion: 0.17
Nodes (10): API Документация - Проектные заявки, Аутентификация, Базовый URL, Общая информация, ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации (+2 more)

### Community 240 - "ApplicationDashboard.py"
Cohesion: 0.20
Nodes (7): ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 241 - ".get_filtered_queryset"
Cohesion: 0.25
Nodes (5): Q, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Доли внутренних/внешних заявок по полю is_internal_customer., Q-фильтр: заявка доступна институту.

### Community 242 - ".submit_application"
Cohesion: 0.16
Nodes (7): Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, Бизнес-операция: подача заявки. Новая логика: 1. Валидация через Domain 2.…, Проверяет наличие пользователя с ролью department_validator в причастных…, Проверяет и корректирует статус заявки при необходимости. Если целевой статус -…, Проверяем, что валидный DTO проходит валидацию без ошибок., Невалидные поля аккумулируют ошибки в ValidationResult., TestSubmitApplication

### Community 243 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

### Community 244 - "InstituteSerializer"
Cohesion: 0.67
Nodes (3): InstituteSerializer, Meta, Сериализатор для институтов/академий.

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 278 - "TestTagViewSetDelete"
Cohesion: 0.08
Nodes (16): django_db, Тесты для обновления тегов через API., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., admin может обновлять любые теги., Тесты для удаления тегов через API., cpds может удалять общие теги., cpds не может удалять теги с подразделением. (+8 more)

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 292 - "DirectionViewSet"
Cohesion: 0.43
Nodes (4): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений.

### Community 293 - "test_preregistered_student_viewset.py"
Cohesion: 0.47
Nodes (5): api_client(), pre_registered_student(), fixture, Тесты API предрегистрации студентов., study_group()

### Community 294 - "institute_responsible_service.py"
Cohesion: 0.09
Nodes (14): InstituteResponsibleAssignMentorDTO, InstituteResponsibleEmployeeDTO, InstituteResponsibleGroupDTO, InstituteResponsibleGroupMentorsDTO, InstituteResponsibleGroupWithMentorDTO, InstituteResponsibleMentorDTO, Any, Компактное представление учебной группы. (+6 more)

### Community 295 - "TeamSemester"
Cohesion: 0.03
Nodes (42): Проверяет, что пользователь — капитан команды., Заявка должна быть в статусе pending., Проверяет, что пользователь — капитан команды., Участие команды в конкретном семестре: проект, наставник, капитан., Заявка студента на вступление в команду в семестре., Приглашение капитана студенту вступить в команду., Status, TeamInvitation (+34 more)

### Community 297 - "ProjectRepository"
Cohesion: 0.29
Nodes (5): ProjectRepository, QuerySet, Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

### Community 299 - "TestGetUserInstituteCodes"
Cohesion: 0.50
Nodes (3): django_db, Разрешение институтов по подразделению пользователя., TestGetUserInstituteCodes

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

### Community 320 - "UserListDTO"
Cohesion: 0.12
Nodes (16): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, API управления пользователями: список, деталь, частичное обновление. (+8 more)

### Community 330 - ".get_external_share_chart_data"
Cohesion: 0.33
Nodes (3): Цвет столбца по порогам доли внешних заявок., Доля внешних заявок по подразделениям или институтам., Форматирует данные доли внешних заявок для API.

## Knowledge Gaps
- **242 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+237 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **106 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `.create_tag`, `Department`, `accounts/views.py`, `Any`, `test_institute_responsible_viewset.py`, `ApplicationDashboardService`, `ProjectApplication`, `UserManagementService`, `application_dashboard_service.py`, `StudyGroup`, `._resolve_institute_semester`, `Direction`, `ProjectTrackService`, `StudentShowcaseDomain`, `StudyGroupService`, `teams/models.py`, `TeamLobbyService`, `.get_group_detail`, `PasswordChangeSerializer`, `ProjectApplicationService`, `TeamSemester`, `institute_responsible_service.py`, `ApplicationDashboardRepository`, `.approve_application`, `test_project_track_service.py`, `TestCanUpdateTag`, `TagViewSet`, `team_lobby_service.py`, `accounts/permissions.py`, `accounts/serializers.py`, `ProjectTrackDomain`, `UserSerializer`, `UserListDTO`, `.resolve_list_semester_id`, `UserManagementDomain`, `accounts/admin.py`, `StudentShowcaseService`, `.can_user_access_application`, `TagService`, `.get_filtered_queryset`, `CommentService`, `PasswordResetSerializer`, `InstituteResponsibleDomain`, `TestCanCreateTag`, `ProjectApplicationCreateDTO`, `TestCanDeleteTag`, `._resolve_context`, `.get_filtered_queryset`, `DirectionService`, `.list_applications`, `ApplicationLoggingService`, `.submit_application`, `institute_access.py`, `StudyGroupMemberDTO`, `test_study_group_domain.py`?**
  _High betweenness centrality (0.184) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `Department`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `test_institute_responsible_viewset.py`, `ApplicationDashboardService`, `ProjectApplication`, `UserManagementService`, `StudyGroup`, `ProjectTrack`, `TestDepartmentPlanViewSetCreate`, `TestTagViewSetDelete`, `ProjectTrackService`, `StudyGroupService`, `test_student_showcase_viewset.py`, `TestProjectApplicationReadDTO`, `TestTagViewSet`, `ProjectService`, `PasswordChangeSerializer`, `ProjectApplicationService`, `PreRegisteredStudent`, `Settings`, `TestGetUserInstituteCodes`, `TestCommentService`, `test_project_track_service.py`, `TestCanUpdateTag`, `TagUpdateDTO`, `TestDepartmentPlanViewSetList`, `test_import_preregistered_students.py`, `ProjectTrackDomain`, `UserManagementDomain`, `.get_filtered_queryset`, `TagService`, `TestApplicationDashboardViewSet`, `TestTagViewSetCreate`, `TestCanCreateTag`, `ProjectApplicationCreateDTO`, `TestCanDeleteTag`, `TestProjectViewSet`, `.get_filtered_queryset`, `DirectionService`, `TestProjectApplicationViewSetIsInternalCustomer`, `TestProjectApplicationNewFieldsCreateUpdate`, `TestProjectApplicationViewSetTransferToInstitute`, `TestTagServiceDelete`, `student_user`, `ApplicationNotificationService`, `ApplicationLoggingService`, `TestProjectApplicationListSemesterFilter`, `test_study_group_domain.py`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `make_user`, `Department`, `InstituteResponsibleService`, `accounts/views.py`, `ProjectApplicationViewSet`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `test_institute_responsible_viewset.py`, `ApplicationDashboardService`, `ProjectApplication`, `UserManagementService`, `application_dashboard_service.py`, `StudyGroup`, `ProjectTrack`, `TestDepartmentPlanViewSetCreate`, `ProjectTrackService`, `StudyGroupService`, `test_student_showcase_viewset.py`, `test_import_study_groups_from_contingent.py`, `teams/models.py`, `TeamLobbyService`, `ProjectService`, `ProjectApplicationService`, `institute_responsible_service.py`, `TeamSemester`, `Settings`, `test_project_track_service.py`, `team_lobby_service.py`, `TestDepartmentPlanViewSetList`, `accounts/serializers.py`, `Command`, `.resolve_list_semester_id`, `accounts/admin.py`, `StudentShowcaseService`, `DepartmentPlanViewSet`, `ProjectApplicationCreateDTO`, `AccountsApiTests`, `TeamSemesterViewSet`, `TestProjectViewSet`, `TestProjectApplicationNewFieldsCreateUpdate`, `test_institute_access.py`, `TestProjectApplicationListSemesterFilter`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 499 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 499 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 74 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 74 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._