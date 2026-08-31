# Graph Report - project_activity_server  (2026-08-31)

## Corpus Check
- 351 files · ~163,106 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5293 nodes · 10710 edges · 371 communities (253 shown, 118 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1045 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `62650a91`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MentorTeamService
- make_user
- TestCanCreateTag
- Ответственный по институту — API для фронта
- ProjectTrackService
- accounts/views.py
- ApplicationDashboardDomain
- Any
- application_import.py
- TagRepository
- ApplicationDashboardService
- ApplicationDashboardRepository
- _enrollment_with_mentors
- ._collect_group_rows
- ApplicationStatus
- APIClient
- prepare_study_groups_xlsx.py
- MyStudyGroupDTO
- TagCreateDTO
- UserManagementService
- TestDepartmentPlanViewSetCreate
- TestDepartmentPlanViewSetList
- accounts/serializers.py
- .resolve_list_semester_id
- StudyGroupViewSet
- TestStudentShowcaseEnroll
- normalize_cell
- TeamLobbyService
- TestTeamLobbyViewSet
- ProjectApplication
- TestProjectApplicationViewSetIsInternalCustomer
- AvailableActionDTO
- institute_access.py
- test_project_track_service.py
- ProjectTrackViewSet
- ._get_track_with_access
- TestTagViewSetCreate
- MentorTeamDomain
- ._create_app
- StudentShowcaseDomain
- PreRegisteredStudent
- Tag
- .calculate_initial_status
- .post
- TestInstituteResponsibleViewSet
- Path
- Any
- CommentService
- prod_users_client.py
- test_tag.py
- TagService
- StudentWithStudyGroupPermission
- DirectionService
- TestTagViewSet
- test_import_study_groups_from_contingent.py
- PreRegisteredStudentRepository
- ValidationResult
- ProjectApplicationCreateDTO
- APIView
- .validate_create
- UserSerializer
- ProjectTrackDomain
- test_mentor_team_viewset.py
- showcase/admin.py
- Примеры использования поля is_internal_customer
- TeamLobbyRepository
- Any
- ProjectApplicationService
- Role
- Semester
- tests/conftest.py
- .can_user_access_application
- .get_filtered_queryset
- .my_department_plan
- ProjectTrackRepository
- PermissionError
- import_preregistered_mentors.py
- TestApplicationDashboardViewSet
- .can_change_status
- preregistered_mentor_import.py
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
- TeamSemesterViewSet
- serialize_comment_author
- StudyGroup
- InvolvedManagementService
- extract.py
- ._resolve_context
- InstituteResponsibleService
- teams/admin.py
- TestProjectApplicationViewSetTransferToInstitute
- refresh_prod_users_json
- extract_group_abbrev.py
- PreRegisteredStudentService
- Общая информация
- Command
- TestProjectApplicationCreateDTO
- TagUpdateDTO
- Direction
- MentorGroupsDomain
- TestProjectApplicationListSemesterFilter
- StudentShowcaseViewSet
- _generate_collection.py
- TestMyStudyGroupViewSet
- ApplicationLoggingService
- get_root_department
- TestCoordinationAndDtosService
- TestImportPreRegisteredMentors
- test_institute_access.py
- StudentShowcaseService
- TestMyTeamViewSet
- sync_project_teachers.py
- ProjectService
- .should_require_consultation
- Поддержка multipart/form-data
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- User
- .get_dashboard
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
- ProjectTrackStatisticsDTO
- deploy.sh
- action_types.py
- export_client_sources_to_docx.py
- make_source_docx.py
- .auth
- parse_miit_ief_groups.py
- Command
- test_institute_responsible_viewset.py
- schema.py
- ShowcaseConfig
- student_showcase_service.py
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
- TestProjectApplicationListDTO
- TestStudentBlockedFromStaffApi
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- TestProjectApplicationReadDTO
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
- ApplicationInvolvedUser
- RutMiitClient
- ProjectTrackProjectDetailDTO
- .test_departments_list_allow_any_detail_requires_auth
- .test_registration_request_create_anonymous_allowed
- test_export_import_departments_roundtrip
- MentorGroupListDTO
- TestTagServiceDelete
- ._track_detail_queryset
- TeamSemester
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
- APIClient
- .test_semester_list_is_active_from_settings
- UserRepository
- .test_user_me_institute_code_from_department_institute
- .test_user_roles_list_requires_auth_and_returns
- .validate_update
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
- .get_filtered_queryset
- Command
- StudyGroupRepository
- ProjectApplicationRepository
- Схема БД: студенческий портал
- Справочные эндпоинты
- Парсинг «Проектная деятельность» — РУТ (МИИТ)
- Command
- PasswordChangeSerializer
- django_db
- Department
- TestTagViewSetDelete
- ProjectRepository
- 0017_copy_studygroup_mentors_to_semester.py
- test_team_lobby_viewset.py
- TestProjectApplicationNewFieldsCreateUpdate
- test_application_import.py
- .recalculate_recommended_teams_count
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- StudyGroupSemesterRepository
- Вариант 1: импорт схемы с автообновлением
- TestProjectApplicationViewSetSimple
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
- ProjectApplication.py
- TestSemesterAssignViewSet
- .update_team_member_limits
- ProjectTrack
- InstituteSerializer
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- StudentShowcaseRepository
- .test_password_change_success
- load_users_from_json
- .test_password_change_wrong_current_password
- .test_password_reset_sends_email
- .test_registration_request_approve_allowed_for_cpds_user
- .test_registration_request_approve_creates_user_and_sends_email
- .test_registration_request_approve_forbidden_for_regular_user
- .test_registration_request_approve_mail_failure_returns_400_and_no_user_created
- .add_groups
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
- ProjectTrackGroupListDTO
- ApplicationStatus.py
- ProjectApplicationCreateSerializer
- Command
- PasswordResetSerializer
- test_link_institutes_by_name_simple
- test_application_dashboard_viewset.py
- Валидационные правила
- ._format_external_share_chart
- ProjectTrackAddApplicationsSerializer
- ProjectTrackCreateSerializer
- ._ensure_valid_status_after_department_check
- TagSerializer
- .handle
- 0022_preregistration_generalize.py
- .get_linked_applications
- .remove_application
- .update_recommended_teams_counts
- data/conftest.py
- timetable

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 543 edges
2. `User` - 266 edges
3. `Department` - 151 edges
4. `ProjectApplication` - 151 edges
5. `Semester` - 136 edges
6. `ProjectApplicationService` - 136 edges
7. `StudyGroup` - 133 edges
8. `ProjectApplicationCreateDTO` - 111 edges
9. `PreRegisteredStudent` - 86 edges
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

## Communities (371 total, 118 thin omitted)

### Community 0 - "MentorTeamService"
Cohesion: 0.06
Nodes (39): MentorTeamAddMemberSerializer, MentorTeamCreateSerializer, MentorTeamSetCaptainSerializer, MentorTeamUpdateNameSerializer, Request, Response, PATCH /study-groups/{groupId}/teams/{teamSemesterId}/ — название., DELETE /study-groups/{groupId}/teams/{teamSemesterId}/ — удалить команду. (+31 more)

### Community 1 - "make_user"
Cohesion: 0.04
Nodes (16): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, TestProjectTrackViewSet, Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Admin видит все теги. (+8 more)

### Community 2 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 3 - "Ответственный по институту — API для фронта"
Cohesion: 0.07
Nodes (27): 1. Список активных групп института, 2. Обзор групп института (со счётчиками), 3. Сотрудники института, 4. Группы с назначенными наставниками, 5. Назначить наставника группе, 6. Снять наставника с группы, Значения `semester_id`, Общие query-параметры (+19 more)

### Community 4 - "ProjectTrackService"
Cohesion: 0.12
Nodes (7): Создаёт DTO из словаря., PATCH /api/showcase/project-tracks/{id}/., ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), django_db, TestProjectTrackService

### Community 5 - "accounts/views.py"
Cohesion: 0.08
Nodes (32): RegistrationRequest, Status, ApproveRequestSerializer, DepartmentSerializer, Meta, Сериализатор для подразделений/кафедр., Проверяет email: нормализация, отсутствие пользователя и активной заявки., Сериализатор для ролей пользователей. (+24 more)

### Community 6 - "ApplicationDashboardDomain"
Cohesion: 0.07
Nodes (22): get_department_subtree_ids(), Утилиты для работы с подразделениями., Возвращает id корневого подразделения и всех его потомков., ApplicationDashboardDomain, DashboardFilters, Доменная логика дашборда проектных заявок., Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп. (+14 more)

### Community 7 - "Any"
Cohesion: 0.07
Nodes (17): ProjectTrackApplicationItemDTO, ProjectTrackGroupDetailDTO, ProjectTrackGroupItemDTO, ProjectTrackGroupProjectDTO, Any, Преобразует DTO в словарь для API., DTO заявки в проектном треке., Преобразует DTO в словарь для API. (+9 more)

### Community 8 - "application_import.py"
Cohesion: 0.14
Nodes (19): ApplicationImportRow, build_import_row(), is_data_row(), iter_application_import_rows(), normalize_cell(), parse_customer_type(), parse_institute_codes(), Any (+11 more)

### Community 9 - "TagRepository"
Cohesion: 0.06
Nodes (31): Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., TagRepository, django_db, Unit-тесты для репозитория TagRepository. Проверяем все методы работы с БД:…, get_by_id возвращает общий тег., get_by_id для несуществующего тега вызывает ошибку. (+23 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.06
Nodes (28): ApplicationDashboardService, Оркестрация получения данных дашборда заявок., django_db, Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external., Фильтр по группам статусов., Карточка in_work = total - approved - rejected., Среднее и медиана времени до решения. (+20 more)

### Community 11 - "ApplicationDashboardRepository"
Cohesion: 0.07
Nodes (29): ApplicationDashboardRepository, Q, QuerySet, Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению., Строит карту institute_code -> множество id заявок., ORM-запросы и агрегации для дашборда заявок. (+21 more)

### Community 12 - "_enrollment_with_mentors"
Cohesion: 0.26
Nodes (5): _enrollment_with_mentors(), APIClient, django_db, TestMentorGroupsQueryPerformance, TestMentorGroupsViewSet

### Community 13 - "._collect_group_rows"
Cohesion: 0.18
Nodes (11): GroupImportRow, Строка отчёта, подготовленная к импорту одной учебной группы., Command, BaseCommand, DataFrame, date, Path, Читает отчёт контингента; заголовок колонок — вторая строка. (+3 more)

### Community 14 - "ApplicationStatus"
Cohesion: 0.08
Nodes (18): Command, BaseCommand, Экспорт возможных статусов заявок в Excel., Считывает статусы из базы и сохраняет в Excel., Возвращает статусы, отсортированные по позиции и коду., Command, BaseCommand, ApplicationStatus (+10 more)

### Community 15 - "APIClient"
Cohesion: 0.20
Nodes (9): Any, APIClient, django_db, parametrize, _team_url(), TestMentorTeamAccess, TestMentorTeamMutations, TestMentorTeamProjectEnrollmentBlock (+1 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "MyStudyGroupDTO"
Cohesion: 0.16
Nodes (8): MyStudyGroupDTO, Any, Возвращает наставников: из семестра или fallback на StudyGroup.mentor., Строка списка группы из контингента., Полные данные учебной группы для текущего студента., StudyGroupMemberDTO, Any, Возвращает данные учебной группы текущего студента.

### Community 18 - "TagCreateDTO"
Cohesion: 0.08
Nodes (19): DTO для создания тега., TagCreateDTO, Тесты для метода create репозитория., Создание общего тега (без departments)., Создание тега с подразделением., Создание тега с несуществующим подразделением вызывает ошибку., Нельзя создать тег с таким же именем и таким же набором подразделений., Можно создать тег с таким же именем, но другим набором подразделений. (+11 more)

### Community 19 - "UserManagementService"
Cohesion: 0.06
Nodes (30): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, ViewSet для управления пользователями. (+22 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 22 - "accounts/serializers.py"
Cohesion: 0.10
Nodes (22): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Отправляет администратору письмо о расхождении данных., Публичные операции предрегистрации студентов. (+14 more)

### Community 23 - ".resolve_list_semester_id"
Cohesion: 0.12
Nodes (11): Разбор query-параметра semester_id для GET-списков: id, next, actual., QuerySet, UserType, Список треков по фильтрам., Подгружает подразделение пользователя для проверки институтов., Детали группы с назначенными проектами., Статистика распределения проектов по группам., Проверяет право управления треками. (+3 more)

### Community 24 - "StudyGroupViewSet"
Cohesion: 0.19
Nodes (10): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/my-groups/ — группы наставника в семестре., GET /api/teams/study-groups/{id}/mentor-detail/ — детали группы наставника., GET /api/teams/study-groups/{id}/project-showcase/ — витрина проектов группы., GET /api/teams/study-groups/ — список и просмотр учебных групп. (+2 more)

### Community 25 - "TestStudentShowcaseEnroll"
Cohesion: 0.11
Nodes (8): _create_assembled_team(), django_db, После заполнения последнего слота вторая команда получает 400., Один участник при min_team_members=2., TestStudentShowcaseAccess, TestStudentShowcaseDetail, TestStudentShowcaseEnroll, TestStudentShowcaseList

### Community 26 - "normalize_cell"
Cohesion: 0.13
Nodes (16): build_preregistered_student_import_row(), last_names_match(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки. (+8 more)

### Community 27 - "TeamLobbyService"
Cohesion: 0.05
Nodes (54): PageNumberPagination, ApproveJoinRequestSerializer, CreateInvitationSerializer, CreateTeamSerializer, MyTeamViewSet, action, extend_schema, extend_schema_view (+46 more)

### Community 28 - "TestTeamLobbyViewSet"
Cohesion: 0.14
Nodes (7): _create_captained_team(), django_db, Команда без трека при одном треке у группы → min/max с трека группы., После создания своей команды pending-заявка в чужую → obsolete., При нескольких треках track_id не проставляется; лимиты — effective по трекам., Если группе доступен один трек — он проставляется без track_id в body., TestTeamLobbyViewSet

### Community 29 - "ProjectApplication"
Cohesion: 0.07
Nodes (22): find_existing_imported_application(), Ищет уже импортированную заявку по автору, названию и заказчику., Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., ProjectListDTO, Any, DTO для списка проектов., Возвращает причастное подразделение верхнего уровня (без родителя). ЦПДС… (+14 more)

### Community 30 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "institute_access.py"
Cohesion: 0.07
Nodes (26): ID подразделений для фильтрации; None — без ограничения., ProjectDomain, Доменная логика для списка проектов., Проверяет, может ли пользователь получать список проектов., Коды институтов для фильтрации; None — без ограничения., Правила доступа и фильтрации для списка проектов., Доменная логика для проектных треков., get_accessible_institute_codes() (+18 more)

### Community 33 - "test_project_track_service.py"
Cohesion: 0.07
Nodes (28): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackCreateDTO, ProjectTrackUpdateDTO, DTO для проектных треков., DTO для создания проектного трека., DTO для добавления групп в трек. (+20 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.13
Nodes (22): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+14 more)

### Community 35 - "._get_track_with_access"
Cohesion: 0.11
Nodes (15): ProjectTrackReadDTO, DTO для чтения проектного трека., atomic, Возвращает трек с проверкой доступа., Возвращает детали трека., Создаёт проектный трек., Проставляет лимиты размера команды всем заявкам трека., Обновляет основные поля трека и лимиты команд у заявок. (+7 more)

### Community 36 - "TestTagViewSetCreate"
Cohesion: 0.06
Nodes (19): django_db, Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем. (+11 more)

### Community 37 - "MentorTeamDomain"
Cohesion: 0.06
Nodes (22): MentorTeamDomain, Доменные правила управления командой наставником., Чистая бизнес-логика API команд наставника., Проверяет, что команда принадлежит учебной группе., Запрещает изменения, если команда записана на проект., Проверяет возможность подтверждения состава., Проверяет возможность разутверждения состава., Удаление возможно только при пустом составе. (+14 more)

### Community 38 - "._create_app"
Cohesion: 0.06
Nodes (26): patch, Ошибки валидации института: несуществующий код или отсутствие связанного…, Нет причастности подразделения — матрица запрещает действие, ожидаем…, department_validator: await_department -> approved_department ->…, institute_validator: await_institute -> approved_institute -> await_cpds…, institute_validator может согласовать await_department, подменяя шаг кафедры., cpds: может одобрять заявки в статусе await_cpds (переход в approved разрешен)., Полный цикл: заявка создается, одобряется department_validator, затем… (+18 more)

### Community 39 - "StudentShowcaseDomain"
Cohesion: 0.12
Nodes (19): Правила доступа и записи команды на проект витрины., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI)., StudentShowcaseDomain (+11 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.12
Nodes (17): PreRegisteredStudent, Предрегистрация пользователя (студент или наставник)., Возвращает True, если пользователь прошёл полную регистрацию (не псевдо-user)., MonkeyPatch, Контингент группы с командой студента в семестре (без N+1)., api_client(), pre_registered_student(), Any (+9 more)

### Community 41 - "Tag"
Cohesion: 0.08
Nodes (15): Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, Теги для проектных заявок, Tag, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Создание тега в БД. Args: dto: DTO с данными для создания тега Returns:…, Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, Обновление тега. Обновляет только переданные поля. Args: tag: Тег для… (+7 more)

### Community 42 - ".calculate_initial_status"
Cohesion: 0.10
Nodes (14): Определение начального статуса на основе роли пользователя. Чистая функция -…, Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, Бизнес-операция: подача заявки. Новая логика: 1. Валидация через Domain 2.…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds. (+6 more)

### Community 43 - ".post"
Cohesion: 0.24
Nodes (7): LoginView, extend_schema, Request, Response, Сменяет пароль текущего пользователя после проверки текущего пароля., Получение JWT токена по email и паролю., TokenObtainPairView

### Community 44 - "TestInstituteResponsibleViewSet"
Cohesion: 0.09
Nodes (6): _enrollment_with_mentors(), APIClient, django_db, Создаёт запись группы в семестре с наставниками., TestInstituteResponsibleViewSet, TestMyStudyGroupSemesterMentor

### Community 45 - "Path"
Cohesion: 0.15
Nodes (13): aga_institute(), direction(), Any, django_db, fixture, Path, Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта. (+5 more)

### Community 46 - "Any"
Cohesion: 0.10
Nodes (11): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, Преобразование в DTO - никакой бизнес-логики, Тесты для ProjectApplicationUpdateDTO., Создание DTO для обновления из словаря. (+3 more)

### Community 47 - "CommentService"
Cohesion: 0.08
Nodes (20): ProjectApplicationComment, CommentService, atomic, Сервис для управления комментариями к проектным заявкам. Обеспечивает…, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db (+12 more)

### Community 48 - "prod_users_client.py"
Cohesion: 0.11
Nodes (23): Client, _http_client(), obtain_token(), Клиент prod API для обновления снимка пользователей., Возвращает базовый URL prod API., HTTP-клиент с поддержкой редиректов prod., Получает JWT access token по email и паролю., Возвращает Bearer token из CLI, env или login. (+15 more)

### Community 49 - "test_tag.py"
Cohesion: 0.13
Nodes (11): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Unit-тесты для доменной логики TagDomain. Проверяем все чистые функции бизнес-…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения. (+3 more)

### Community 50 - "TagService"
Cohesion: 0.06
Nodes (41): Разрешает доступ к управлению тегами только для ролей cpds, admin и…, TagManagePermission, Доменная логика для тегов - чистые функции без эффектов., Чистая бизнес-логика для тегов - только функции, никаких эффектов., TagDomain, DTO для работы с тегами., Инициализация из модели Tag., TagReadDTO (+33 more)

### Community 51 - "StudentWithStudyGroupPermission"
Cohesion: 0.22
Nodes (10): _is_staff_or_admin(), APIView, BasePermission, Request, Доступ только студенту с привязанной учебной группой., Чтение — любой аутентифицированный пользователь. Изменение постоянной команды —…, Изменение семестрового контекста — капитан, admin или cpds., StudentWithStudyGroupPermission (+2 more)

### Community 52 - "DirectionService"
Cohesion: 0.06
Nodes (29): DirectionDomain, QuerySet, Фильтрация направлений по роли пользователя., Фильтрует направления: institute_validator — только из групп своего института., DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений. (+21 more)

### Community 53 - "TestTagViewSet"
Cohesion: 0.14
Nodes (8): Тесты для TagViewSet., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level)., Список тегов возвращается без пагинации (все теги сразу)., Эндпоинт доступен без авторизации (AllowAny)., TestTagViewSet

### Community 54 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.09
Nodes (23): build_group_import_row(), build_group_name(), calculate_course_number(), group_ended_by_planned_dates(), parse_direction_level(), parse_permanent_group_code(), parse_planned_end_date(), ParsedPermanentGroup (+15 more)

### Community 55 - "PreRegisteredStudentRepository"
Cohesion: 0.07
Nodes (18): PreRegisteredStudentRepository, QuerySet, Доступ к данным предрегистрации студентов., Привязывает предрегистрацию к пользователю., Возвращает queryset предрегистраций без пользователя., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по табельному номеру., Возвращает предрегистрацию по нормализованному СНИЛС. (+10 more)

### Community 56 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 57 - "ProjectApplicationCreateDTO"
Cohesion: 0.08
Nodes (31): create_test_applications(), Создаем тестовые заявки, ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Явное выражение бизнес-намерений (не технических операций). Этот модуль…, Domain слой - чистая бизнес-логика без побочных эффектов. Этот слой содержит…, build_author_short_name() (+23 more)

### Community 58 - "APIView"
Cohesion: 0.09
Nodes (20): IsAdminOrCpds, IsCpdsUser, IsInstituteValidator, APIView, BasePermission, Request, Проверяет наличие прав у пользователя., Разрешает доступ только сотрудникам, администраторам или роли ЦПДС. (+12 more)

### Community 59 - ".validate_create"
Cohesion: 0.12
Nodes (13): Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Носитель проблемы короче 5 символов вызывает ошибку., Барьер короче 10 символов вызывает ошибку., Имя и фамилия автора короче 2 символов вызывают ошибки., Тесты для валидации при создании заявки., Телефон короче 10 символов вызывает ошибку., Валидный DTO проходит проверку без ошибок., Все ошибки валидации собираются в одном результате. (+5 more)

### Community 60 - "UserSerializer"
Cohesion: 0.17
Nodes (9): Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., UserSerializer, CustomTokenObtainPairSerializer (+1 more)

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.08
Nodes (16): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя., Проверяет, может ли пользователь управлять проектными треками., Коды институтов пользователя; None — без ограничения (admin/cpds). (+8 more)

### Community 62 - "test_mentor_team_viewset.py"
Cohesion: 0.14
Nodes (18): MentorTeamDetailDTO, MentorTeamMemberDTO, Any, Участник команды в карточке наставника., Карточка команды для ответов мутаций наставника., api_client(), _approved_app(), _create_team_url() (+10 more)

### Community 63 - "showcase/admin.py"
Cohesion: 0.11
Nodes (20): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+12 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "TeamLobbyRepository"
Cohesion: 0.04
Nodes (28): QuerySet, Лог событий команды в семестре (новые сверху)., Pending-заявки студента в семестре., Pending-приглашения студента в семестре., Карта team_semester_id → id pending-заявки текущего пользователя., Число команд группы в треке в семестре., True, если студент уже в команде в семестре., Команда в семестре с базовыми связями. (+20 more)

### Community 66 - "Any"
Cohesion: 0.07
Nodes (18): Удаление: капитан, forming, в составе только он., Подтверждение состава: капитан, forming, размер в лимитах трека., ФИО пользователя для лога., LobbyInvitationDTO, LobbyReadDTO, LobbyTeamItemDTO, LobbyTrackDTO, MyTeamInvitationDTO (+10 more)

### Community 67 - "ProjectApplicationService"
Cohesion: 0.04
Nodes (37): ProjectApplicationService, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка. (+29 more)

### Community 68 - "Role"
Cohesion: 0.06
Nodes (22): QuerySet, Доменная логика управления пользователями., Проверяет, что пользователь доступен в отфильтрованном queryset., Правила доступа и валидации для управления пользователями., Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя. (+14 more)

### Community 69 - "Semester"
Cohesion: 0.06
Nodes (36): Идемпотентный импорт строк модели Settings из CSV., Ключ–значение настроек приложения (редактируемые из админки / импортом)., Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Semester, Settings, Репозиторий предрегистрации студентов., Создание псевдо-аккаунтов для незарегистрированных студентов контингента. (+28 more)

### Community 70 - "tests/conftest.py"
Cohesion: 0.20
Nodes (13): departments(), _ensure_preregistration_roles(), institute(), fixture, Возвращает класс модели пользователя для удобства., Роли, необходимые для FK предрегистраций., Создаёт набор ролей, используемых в тестах. Возвращает dict: code -> Role, Создаёт иерархию подразделений: parent -> child. (+5 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.14
Nodes (11): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Тесты для проверки доступа пользователя к заявке., Автор всегда имеет доступ к своей заявке., Админ имеет доступ ко всем заявкам., Модератор имеет доступ ко всем заявкам., CPDS имеет доступ ко всем заявкам., Валидатор подразделения имеет доступ ко всем заявкам., Валидатор института имеет доступ ко всем заявкам. (+3 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.14
Nodes (11): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., Тесты для фильтрации queryset тегов по ролям., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения., institute_validator без подразделения видит только общие теги. (+3 more)

### Community 73 - ".my_department_plan"
Cohesion: 0.17
Nodes (12): DepartmentPlanSerializer, action, extend_schema, Request, Response, Получить словарь планов по подразделениям для указанного семестра., Получить статистику заявок по статусам для каждого подразделения., GET /api/showcase/department-plans/?institute_code=INST&semester_id=1 Получение… (+4 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.10
Nodes (10): ProjectTrackRepository, Создаёт проектный трек., Обновляет поля трека., Возвращает id групп, уже привязанных к треку., Удаляет группу из трека; True если связь была., Возвращает id заявок, уже привязанных к треку., Добавляет заявки в трек; возвращает число созданных связей., Количество групп в треке. (+2 more)

### Community 75 - "PermissionError"
Cohesion: 0.06
Nodes (21): PermissionError, Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации. (+13 more)

### Community 76 - "import_preregistered_mentors.py"
Cohesion: 0.11
Nodes (17): PreRegisteredMentorImportRow, Строка отчёта, подготовленная к импорту одной предрегистрации наставника., Command, DepartmentConflictAction, BaseCommand, DataFrame, Enum, Path (+9 more)

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - ".can_change_status"
Cohesion: 0.08
Nodes (23): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, atomic, Бизнес-операция: отправка заявки на доработку., Бизнес-операция: отзыв заявки автором., Бизнес-операция: одобрение заявки., Бизнес-операция: отклонение заявки., Бизнес-операция: передача заявки в институт. Доступно только для роли cpds для…, Бизнес-операция: получение доступных действий для заявки. Args: application_id:… (+15 more)

### Community 79 - "preregistered_mentor_import.py"
Cohesion: 0.14
Nodes (17): build_preregistered_mentor_import_row(), build_user_name_indexes(), find_user_by_full_name(), normalize_user_name(), AbstractBaseUser, Чистая логика импорта предрегистрации наставников из отчёта 1С., Собирает DTO одной предрегистрации наставника из полей строки отчёта., Нормализует ФИО для сравнения. (+9 more)

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
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, django_db, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения. (+3 more)

### Community 85 - "build_user_indexes"
Cohesion: 0.11
Nodes (26): main(), Сверка преподавателей из Excel со списком пользователей prod API. ..…, Отмечает преподавателей из Excel, которые есть в prod., build_user_indexes(), find_user(), normalize_name(), Сопоставление ФИО преподавателей с пользователями PD., Нормализует ФИО для сравнения. (+18 more)

### Community 86 - ".handle"
Cohesion: 0.18
Nodes (7): Следующий семестр для новых заявок (Settings.next_semester_code)., parse_author_name(), Разбирает строку вида «Фамилия Имя» на фамилию и имя., Command, BaseCommand, Формирует контактные поля автора для DTO из пользователя системы., Создание заявки в БД. Принимает DTO и пользователя, возвращает созданную…

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "Управление командой"
Cohesion: 0.07
Nodes (26): Query-параметры, Query-параметры, Query-параметры, Вернуть состав на редактирование, Витрина проектов, Детали группы наставника, Добавить участника, Карточка команды (+18 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.04
Nodes (37): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы. (+29 more)

### Community 90 - "test_import_preregistered_students.py"
Cohesion: 0.19
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 91 - "TeamSemesterViewSet"
Cohesion: 0.24
Nodes (8): action, Request, Response, POST /api/teams/team-semesters/{id}/members/ — добавить участника., DELETE /api/teams/team-semesters/{id}/members/{member_id}/., CRUD для участия команды в семестре и управления составом., GET /api/teams/team-semesters/my/?semester_id= — команды пользователя., TeamSemesterViewSet

### Community 92 - "serialize_comment_author"
Cohesion: 0.19
Nodes (9): Сериализует автора комментария с role и department. Args: author: User объект…, serialize_comment_author(), Тесты для функции serialize_comment_author., Если author равен None, возвращаются None значения., Сериализация автора с полными данными: имя, фамилия, отчество, роль,…, Сериализация автора без отчества., Сериализация автора без роли и подразделения., Сериализация автора с минимальными данными (только last_name). (+1 more)

### Community 93 - "StudyGroup"
Cohesion: 0.07
Nodes (35): MentorGroupDetailDTO, MentorGroupListItemDTO, MentorGroupTeamDTO, DTO для эндпоинта «Мои группы» наставника., Строка списка групп наставника., Команда группы в семестре для деталей наставника., Детали учебной группы для наставника в семестре., StudyGroup (+27 more)

### Community 94 - "InvolvedManagementService"
Cohesion: 0.12
Nodes (12): InvolvedManagementService, atomic, Добавляет причастное подразделение по его краткому названию. Args: application:…, Добавляет причастное подразделение по его ID. Args: application: Заявка, к…, Добавляет пользователя как причастного к заявке. Args: application: Заявка…, Добавляет подразделение как причастное к заявке. Args: application: Заявка…, Получает всех причастных пользователей заявки. Args: application: Заявка…, Сервис для управления причастными пользователями и подразделениями.… (+4 more)

### Community 95 - "extract.py"
Cohesion: 0.22
Nodes (16): main(), run(), export_marked_xlsx(), export_to_xlsx(), _group_columns(), Any, Экспортирует результаты парсинга с колонками сверки с PD., _collect_events() (+8 more)

### Community 96 - "._resolve_context"
Cohesion: 0.08
Nodes (17): InstituteResponsibleAssignMentorDTO, InstituteResponsibleGroupDTO, InstituteResponsibleGroupMentorsDTO, InstituteResponsibleGroupWithMentorDTO, Any, Компактное представление учебной группы., Учебная группа с ID назначенных наставников в семестре., Ответ: группы с назначениями наставников. (+9 more)

### Community 97 - "InstituteResponsibleService"
Cohesion: 0.15
Nodes (21): delete, AssignMentorSerializer, InstituteResponsiblePermission, InstituteResponsibleViewSet, action, BasePermission, extend_schema, Request (+13 more)

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

### Community 102 - "PreRegisteredStudentService"
Cohesion: 0.13
Nodes (11): PreRegisteredStudentLookupResult, PreRegisteredStudentService, atomic, Сервис предрегистрации и регистрации студентов из контингента., Отправляет администратору письмо о расхождении данных. Raises: ValueError: если…, Отправляет студенту письмо после успешной регистрации., Результат поиска предрегистрации., Сериализует результат для API. (+3 more)

### Community 103 - "Общая информация"
Cohesion: 0.50
Nodes (4): Аутентификация, Базовый URL, Общая информация, Форматы данных

### Community 104 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

### Community 105 - "TestProjectApplicationCreateDTO"
Cohesion: 0.11
Nodes (10): Тесты для ProjectApplicationCreateDTO., Создание DTO из словаря через from_dict., Преобразование DTO в словарь через to_dict., Проверяем значения по умолчанию: пустые строки для title, company_contacts,…, Явно переданное значение needs_consultation сохраняется., По умолчанию is_internal_customer равен False., Явно переданное значение is_internal_customer=True сохраняется., is_internal_customer включается в to_dict. (+2 more)

### Community 106 - "TagUpdateDTO"
Cohesion: 0.14
Nodes (11): DTO для обновления тега., TagUpdateDTO, Тесты для метода update_tag сервиса., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+3 more)

### Community 107 - "Direction"
Cohesion: 0.07
Nodes (23): Доменная логика для направлений подготовки., DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DirectionSerializer, Meta, Сериализатор направления подготовки. (+15 more)

### Community 108 - "MentorGroupsDomain"
Cohesion: 0.09
Nodes (18): MentorGroupsDomain, Проверки для API «Мои группы» наставника., Проверяет, что учебная группа существует., Проверяет, что учебная группа не завершила обучение., Проверяет доступ к группе: наставник или ответственный по институту., Проверяет доступ к группе для списка и деталей., Any, DTO для учебных групп. (+10 more)

### Community 109 - "TestProjectApplicationListSemesterFilter"
Cohesion: 0.09
Nodes (14): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Фильтр ?semester_id= в GET-списке заявок., Автоподстановка семестра при создании заявки., Тесты для проверки наличия поля is_external в ответах API., POST /api/showcase/project-applications/ возвращает is_external в ответе. (+6 more)

### Community 110 - "StudentShowcaseViewSet"
Cohesion: 0.19
Nodes (11): action, extend_schema, extend_schema_view, Request, Response, ViewSet студенческой витрины проектов., Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/. (+3 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 113 - "ApplicationLoggingService"
Cohesion: 0.05
Nodes (37): ApplicationLoggingService, Сервис для логирования изменений в проектных заявках. Обеспечивает полное…, django_db, Unit-тесты для ApplicationLoggingService. Проверяем логирование всех типов…, Первый переход (from_status=None) помечает заявку, если актор не автор., Логирование с указанием предыдущего лога для создания цепочки., Тесты для log_status_change., Если application равен None, выбрасывается ValueError. (+29 more)

### Community 114 - "get_root_department"
Cohesion: 0.12
Nodes (15): get_root_department(), is_cpds_department(), Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, DTO для списка проектов., django_db, Unit-тесты для утилит работы с подразделениями., Тесты для функции get_root_department. (+7 more)

### Community 115 - "TestCoordinationAndDtosService"
Cohesion: 0.11
Nodes (10): django_db, Валидатор получает объединённый список: его причастность пользователя +…, cpds видит все заявки в статусе await_cpds даже без причастности., Преобразователи к DTO возвращают ожидаемые экземпляры., get_external_applications возвращает только заявки с is_external=True., get_external_applications позволяет фильтровать внешние заявки по коду статуса., get_external_applications с несуществующим статусом выбрасывает ValueError., get_external_applications_queryset возвращает QuerySet внешних заявок. (+2 more)

### Community 116 - "TestImportPreRegisteredMentors"
Cohesion: 0.21
Nodes (9): Any, django_db, fixture, Path, Тесты команды import_preregistered_mentors., Создаёт минимальный отчёт преподавателей для тестов., sample_teachers_file(), TestImportPreRegisteredMentors (+1 more)

### Community 117 - "test_institute_access.py"
Cohesion: 0.21
Nodes (11): application_available_for_institute(), application_belongs_to_institutes(), Проверяет доступность заявки институту для проектных треков. Заявка доступна,…, Проверяет принадлежность заявки к институтам по причастным подразделениям.…, _create_approved_app(), django_db, fixture, Тесты institute_access. (+3 more)

### Community 118 - "StudentShowcaseService"
Cohesion: 0.14
Nodes (13): atomic, UserType, Записывает команду капитана на проект., Оркестрация Domain + Repository для студенческой витрины., Резолвит semester_id; по умолчанию actual., Список треков группы студента с проектами и счётчиками записи., Треки группы с проектами и enrolledTeamsCount (без проверки роли)., Детали проекта, доступного группе студента. (+5 more)

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → effective max(min)/min(max)., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "sync_project_teachers.py"
Cohesion: 0.19
Nodes (10): load_project_env(), Загружает переменные из .env в корне проекта., main(), parse_all_groups(), _print_parse_summary(), Path, Парсинг расписания РУТ и сверка преподавателей с пользователями prod PD., Парсит преподавателей «Проектная деятельность» по всем группам. (+2 more)

### Community 121 - "ProjectService"
Cohesion: 0.19
Nodes (6): ProjectService, Оркестрация Domain + Repository для списка проектов., django_db, TestProjectApplicationNewFieldsLists, django_db, TestProjectService

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

### Community 126 - "User"
Cohesion: 0.05
Nodes (24): AbstractBaseUser, User, check_and_fix_user(), Проверяем и исправляем пользователя, PermissionsMixin, Проверяет роль student и наличие учебной группы; возвращает group_id., Получение заявок пользователя, где он является автором. Оптимизированный запрос…, Получение QuerySet заявок пользователя для пагинации. Возвращает QuerySet… (+16 more)

### Community 127 - ".get_dashboard"
Cohesion: 0.17
Nodes (9): ApplicationDashboardDTO, Any, DTO для дашборда проектных заявок., Преобразует DTO в словарь для API., DTO блока KPI-карточек., DTO полного ответа дашборда., Преобразует DTO в словарь для API., SummaryCardsDTO (+1 more)

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
Cohesion: 0.15
Nodes (13): 2. Получение пользователя, 4. Список проектов, Query-параметры, Заголовки, Ошибки, Ошибки, Поведение по ролям, Права доступа (+5 more)

### Community 138 - "ProjectTrackStatisticsDTO"
Cohesion: 0.16
Nodes (9): ProjectTrackAggregatedStatisticsDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackStatisticsDTO, DTO статистики распределения проектов по группам., Преобразует DTO в словарь для API., DTO статистики по одному институту., Преобразует DTO в словарь для API., DTO агрегированной статистики по всем институтам. (+1 more)

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

### Community 146 - "test_institute_responsible_viewset.py"
Cohesion: 0.12
Nodes (20): DTO для API ответственного по институтам., Наставники учебной группы в конкретном семестре., StudyGroupSemester, Репозиторий для StudyGroupSemester и связанных выборок., api_client(), direction(), fixture, Тесты API ответственного по институтам. (+12 more)

### Community 147 - "schema.py"
Cohesion: 0.50
Nodes (3): exclude_auth_api_duplicate(), Хуки и расширения для drf-spectacular., Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*). В…

### Community 149 - "student_showcase_service.py"
Cohesion: 0.11
Nodes (16): Any, DTO студенческой витрины проектов., Результат записи команды на проект., Преобразует DTO в словарь для API., Карточка проекта в списке трека витрины., Преобразует DTO в словарь для API., Трек с вложенными проектами для витрины., Преобразует DTO в словарь для API. (+8 more)

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
Cohesion: 0.36
Nodes (8): _create_approved_app(), _create_track_with_links(), direction(), other_institute(), fixture, Тесты ProjectTrackViewSet., semester(), track_setup()

### Community 164 - "test_study_group_domain.py"
Cohesion: 0.21
Nodes (10): Фильтрация учебных групп по роли пользователя., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., StudyGroupDomain, direction(), other_institute(), fixture, Тесты доменной логики StudyGroupDomain. (+2 more)

### Community 165 - "TestProjectApplicationListDTO"
Cohesion: 0.13
Nodes (9): django_db, Тесты для ProjectApplicationListDTO., Базовые поля DTO для списка заполняются из модели., Если статус None, DTO.status тоже None., to_dict преобразует DTO в словарь с ISO форматированием даты., is_internal_customer включается в ProjectApplicationListDTO., Новые поля трека включаются в ProjectApplicationListDTO., is_internal_customer включается в ProjectApplicationReadDTO. (+1 more)

### Community 166 - "TestStudentBlockedFromStaffApi"
Cohesion: 0.13
Nodes (4): django_db, TestApplicationCommentAccess, TestApplicationDestroyDisabled, TestStudentBlockedFromStaffApi

### Community 170 - "TestProjectApplicationReadDTO"
Cohesion: 0.09
Nodes (13): Exception, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None., target_institutes сериализуется как список словарей с code и name., tags сериализуется как список словарей с id, name и category., involved_users сериализуется с данными пользователя, added_at и added_by. (+5 more)

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
Cohesion: 0.16
Nodes (15): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+7 more)

### Community 193 - "ApplicationInvolvedUser"
Cohesion: 0.17
Nodes (8): ApplicationInvolvedUser, DepartmentPlan, Meta, Причастные пользователи к заявке, План по проектным заявкам для подразделения на семестр, InvolvedManager, atomic, Менеджер для управления причастными пользователями и подразделениями.

### Community 195 - "ProjectTrackProjectDetailDTO"
Cohesion: 0.17
Nodes (7): ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, DTO группы в деталях проекта., Преобразует DTO в словарь для API., DTO деталей проекта с назначенными группами., Преобразует DTO в словарь для API., Детали проекта с назначенными группами.

### Community 198 - "test_export_import_departments_roundtrip"
Cohesion: 0.27
Nodes (10): Any, django_db, Экспорт и последующий импорт институтов восстанавливают данные., Экспорт и последующий импорт подразделений восстанавливают данные., Импорт институтов удаляет те, которых нет в файле., Импорт подразделений удаляет те, которых нет в файле., test_export_import_departments_roundtrip(), test_export_import_institutes_roundtrip() (+2 more)

### Community 199 - "MentorGroupListDTO"
Cohesion: 0.14
Nodes (8): MentorGroupListDTO, MentorGroupStudentDTO, Any, Список групп наставника., Студент контингента для деталей группы наставника., Any, Список групп наставника с количеством студентов и команд., Детали группы: студенты контингента и команды в семестре.

### Community 200 - "TestTagServiceDelete"
Cohesion: 0.10
Nodes (13): django_db, Тесты для метода delete_tag сервиса., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять теги своего подразделения., admin может удалять любые теги., Удаление несуществующего тега вызывает ошибку., Тесты для метода get_tag сервиса. (+5 more)

### Community 201 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 202 - "TeamSemester"
Cohesion: 0.05
Nodes (51): Общие константы приложения showcase., Доменная логика студенческой витрины проектов., Проверяет, что пользователь — капитан команды., Репозиторий студенческой витрины проектов (без N+1)., Доменные правила лобби формирования команд., Заявка должна быть в статусе pending., Приглашение должно быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды». (+43 more)

### Community 203 - "ApplicationDashboard.py"
Cohesion: 0.20
Nodes (7): ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 206 - "API Документация - Проектные заявки"
Cohesion: 0.14
Nodes (12): 1. Создание заявки (авторизованные пользователи), API Документация - Проектные заявки, Заголовки, Пример запроса, ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации (+4 more)

### Community 240 - "APIClient"
Cohesion: 0.30
Nodes (6): _create_assembled_team(), APIClient, django_db, _showcase_url(), TestMentorShowcaseQueryPerformance, TestMentorShowcaseViewSet

### Community 242 - "UserRepository"
Cohesion: 0.16
Nodes (8): QuerySet, Репозиторий для управления пользователями., Доступ к данным пользователей для управления., Базовый queryset без администраторов., Список пользователей с оптимизацией запросов., Возвращает пользователя по ID., Сохраняет изменения пользователя., UserRepository

### Community 245 - ".validate_update"
Cohesion: 0.19
Nodes (8): Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Тесты для валидации при обновлении заявки., Валидные поля при обновлении проходят проверку., Название короче 5 символов вызывает ошибку., Email без символа @ вызывает ошибку., Валидация проверяет только переданные поля (None игнорируются)., Пустые строки вызывают ошибки валидации., TestValidateUpdate

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 277 - ".get_filtered_queryset"
Cohesion: 0.25
Nodes (5): QuerySet, institute_validator — только группы своих институтов., django_db, parametrize, TestStudyGroupGetFilteredQueryset

### Community 278 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 279 - "StudyGroupRepository"
Cohesion: 0.20
Nodes (5): QuerySet, Доступ к данным StudyGroup., Группа с наставником и контингентом без N+1., StudyGroupRepository, _make_preregistered()

### Community 280 - "ProjectApplicationRepository"
Cohesion: 0.03
Nodes (57): ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты…, Получение заявки по ID без дополнительных связанных объектов. Для простых…, Репозиторий - вся работа с БД здесь, Получение заявок для координации по причастному подразделению. Заявки, где…, Получение заявок по статусу. Для административных операций., Получение QuerySet заявок по статусу для пагинации., Получение всех заявок, кроме указанных по статусу. Используется, например, для… (+49 more)

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
Cohesion: 0.26
Nodes (3): Command, BaseCommand, Добавляет причастные подразделения института к заявке.

### Community 293 - "PasswordChangeSerializer"
Cohesion: 0.22
Nodes (5): PasswordChangeSerializer, PasswordResetConfirmSerializer, Any, Возвращает учебную группу пользователя или None., Сериализатор для смены пароля аутентифицированного пользователя.

### Community 294 - "django_db"
Cohesion: 0.22
Nodes (4): django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet

### Community 295 - "Department"
Cohesion: 0.06
Nodes (36): Command, BaseCommand, Department, Генерация тестовых одобренных проектов и учебных групп для института IEF., Импорт проектных заявок из Excel-файла., Command, BaseCommand, ApplicationInvolvedDepartment (+28 more)

### Community 296 - "TestTagViewSetDelete"
Cohesion: 0.20
Nodes (6): Тесты для удаления тегов через API., cpds может удалять общие теги., cpds не может удалять теги с подразделением., admin может удалять любые теги., Остальные роли не могут удалять теги., TestTagViewSetDelete

### Community 297 - "ProjectRepository"
Cohesion: 0.29
Nodes (5): ProjectRepository, QuerySet, Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

### Community 299 - "test_team_lobby_viewset.py"
Cohesion: 0.33
Nodes (9): api_client(), _approved_app(), direction(), lobby_setup(), fixture, Тесты API лобби формирования команд., semester(), study_group() (+1 more)

### Community 301 - "test_application_import.py"
Cohesion: 0.25
Nodes (10): get_or_create_institute_tag(), Возвращает тег направления и флаг, был ли тег создан. Сначала ищет общий…, django_db, Тесты доменной логики импорта заявок из Excel., Повторный импорт находит заявку по автору, названию и заказчику., Если есть базовый тег с таким именем, создавать институтский не нужно., Отсутствующий тег создаётся как институтский и привязывается к подразделению., test_find_existing_imported_application_matches_author_title_company() (+2 more)

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

### Community 307 - "StudyGroupSemesterRepository"
Cohesion: 0.11
Nodes (13): QuerySet, Снимает наставника с группы в семестре; возвращает актуальные mentorIds., Возвращает отсортированные ID наставников группы в семестре., Доступ к данным групп в семестре и сотрудников института., Активные группы института., Активные группы с prefetch наставников в семестре., Возвращает группу по ID или None., Сотрудники института (не студенты, не админы, не staff). (+5 more)

### Community 308 - "Вариант 1: импорт схемы с автообновлением"
Cohesion: 0.33
Nodes (5): Postman и OpenAPI, Вариант 1: импорт схемы с автообновлением, Импорт в Postman, Обновить локальный файл схемы (опционально), Ручная коллекция с ролями

### Community 309 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

### Community 310 - "ProjectApplicationViewSet"
Cohesion: 0.06
Nodes (31): format_validation_errors(), get_error_message(), ProjectApplicationViewSet, action, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, GET /api/project-applications/external/ Получение списка всех внешних заявок…, Возвращает сообщение об ошибке в зависимости от режима DEBUG. Args: exception:… (+23 more)

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

### Community 320 - "ProjectApplication.py"
Cohesion: 0.06
Nodes (32): DenyStudentPermission, ProjectManagementPermission, ProjectTrackPermission, Пользовательские permissions для приложения accounts., Разрешает доступ к проектным трекам для admin, cpds и institute_validator., Разрешает просмотр проектов для admin, cpds и institute_validator., Запрещает доступ пользователям с ролью student., ApplicationStatusViewSet (+24 more)

### Community 321 - "TestSemesterAssignViewSet"
Cohesion: 0.29
Nodes (3): Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, TestSemesterAssignViewSet

### Community 323 - "ProjectTrack"
Cohesion: 0.07
Nodes (32): ProjectTrack, ProjectTrackApplication, ProjectTrackGroup, Проектный трек — контейнер для назначения групп и заявок в рамках семестра., Связь проектного трека с учебной группой., Связь проектного трека с проектной заявкой., Репозиторий для проектных треков., Лимиты размера команды. Приоритет: 1) трек команды; 2) effective по трекам… (+24 more)

### Community 324 - "InstituteSerializer"
Cohesion: 0.67
Nodes (3): InstituteSerializer, Meta, Сериализатор для институтов/академий.

### Community 329 - "StudentShowcaseRepository"
Cohesion: 0.10
Nodes (11): Команда пользователя в семестре с блокировкой строки., Запросы и запись для студенческой витрины проектов., Команда пользователя в семестре (без блокировки)., Связь проект↔трек с проверкой семестра и статуса approved., Треки группы в семестре с одобренными проектами и тегами., Счётчик записанных команд с блокировкой строк TeamSemester проекта., Привязывает проект к команде и пишет лог., Карта (track_id, application_id) → число записанных команд. (+3 more)

### Community 331 - "load_users_from_json"
Cohesion: 0.29
Nodes (7): load_users_from_json(), Any, Path, Загружает список пользователей из JSON-файла., Path, Загружает пользователей из JSON-файла., test_load_users_from_json()

### Community 341 - "ProjectTrackProjectListDTO"
Cohesion: 0.29
Nodes (4): ProjectTrackProjectListDTO, DTO проекта со счётчиком назначенных групп., Преобразует DTO в словарь для API., Список проектов семестра со счётчиком назначенных групп.

### Community 344 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 349 - "ProjectTrackUpdateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackUpdateSerializer, Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

### Community 350 - "ProjectTrackGroupListDTO"
Cohesion: 0.29
Nodes (4): ProjectTrackGroupListDTO, DTO группы со счётчиком назначенных проектов., Преобразует DTO в словарь для API., Список групп института со счётчиком назначенных проектов.

### Community 351 - "ApplicationStatus.py"
Cohesion: 0.40
Nodes (5): ApplicationStatusReadSerializer, ApplicationStatusSerializer, Meta, Сериализатор для статусов заявок, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…

### Community 352 - "ProjectApplicationCreateSerializer"
Cohesion: 0.33
Nodes (4): ProjectApplicationCreateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы…, Проверяет, что min_team_members не больше max_team_members., Преобразование в DTO - никакой бизнес-логики

### Community 353 - "Command"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Сбрасывает счетчик ID для таблицы тегов.

### Community 355 - "test_link_institutes_by_name_simple"
Cohesion: 0.40
Nodes (6): Any, django_db, Простейший сценарий: для каждого института есть одноимённое подразделение., Институты без одноимённого подразделения остаются без связанного подразделения., test_link_institutes_by_name_simple(), test_link_institutes_without_matching_department()

### Community 356 - "test_application_dashboard_viewset.py"
Cohesion: 0.50
Nodes (4): api_client(), fixture, Тесты ApplicationDashboardViewSet., semester()

### Community 357 - "Валидационные правила"
Cohesion: 0.50
Nodes (4): Валидационные правила, Обязательные поля, Обязательные поля:, Типы данных

### Community 359 - "ProjectTrackAddApplicationsSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationsSerializer, Список заявок с рекомендуемым числом команд и лимитами размера., Проверяет отсутствие дубликатов id в одном запросе.

### Community 360 - "ProjectTrackCreateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackCreateSerializer, Сериализатор для создания проектного трека., Проверяет согласованность лимитов размера команды.

### Community 362 - "TagSerializer"
Cohesion: 0.67
Nodes (3): Meta, Сериализатор для тегов., TagSerializer

## Knowledge Gaps
- **272 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+267 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **118 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `MentorTeamService`, `TestCanCreateTag`, `ProjectTrackService`, `accounts/views.py`, `ApplicationDashboardDomain`, `StudyGroupService`, `ApplicationDashboardService`, `MyStudyGroupDTO`, `test_institute_responsible_viewset.py`, `UserManagementService`, `student_showcase_service.py`, `accounts/serializers.py`, `.resolve_list_semester_id`, `.get_filtered_queryset`, `TeamLobbyService`, `ProjectApplication`, `institute_access.py`, `test_project_track_service.py`, `._get_track_with_access`, `test_study_group_domain.py`, `PasswordChangeSerializer`, `StudentShowcaseDomain`, `Tag`, `.calculate_initial_status`, `CommentService`, `test_tag.py`, `TagService`, `StudentWithStudyGroupPermission`, `DirectionService`, `StudyGroupSemesterRepository`, `PreRegisteredStudentRepository`, `ProjectApplicationCreateDTO`, `APIView`, `UserSerializer`, `ProjectTrackDomain`, `test_mentor_team_viewset.py`, `accounts/admin.py`, `ProjectApplication.py`, `ApplicationInvolvedUser`, `ProjectTrackProjectDetailDTO`, `Role`, `Semester`, `Any`, `MentorGroupListDTO`, `.get_filtered_queryset`, `TeamSemester`, `PermissionError`, `import_preregistered_mentors.py`, `.can_change_status`, `TestCanDeleteTag`, `ProjectTrackProjectListDTO`, `.handle`, `ApplicationCapabilities`, `StudyGroup`, `InvolvedManagementService`, `ProjectTrackGroupListDTO`, `._resolve_context`, `PasswordResetSerializer`, `._ensure_valid_status_after_department_check`, `Direction`, `MentorGroupsDomain`, `UserRepository`, `StudentShowcaseService`, `.get_dashboard`?**
  _High betweenness centrality (0.170) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `TestCanCreateTag`, `TestProjectViewSet`, `ProjectTrackService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `StudyGroupService`, `ApplicationDashboardService`, `_enrollment_with_mentors`, `ApplicationStatus`, `APIClient`, `TagCreateDTO`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `TestDepartmentPlanViewSetList`, `test_institute_responsible_viewset.py`, `StudyGroupRepository`, `ProjectApplicationRepository`, `TestStudentShowcaseEnroll`, `.get_filtered_queryset`, `TestProjectApplicationViewSetIsInternalCustomer`, `test_project_track_viewset.py`, `test_project_track_service.py`, `TestTagViewSetCreate`, `TestProjectApplicationListDTO`, `django_db`, `TestStudentBlockedFromStaffApi`, `PreRegisteredStudent`, `TestTagViewSetDelete`, `TestProjectApplicationReadDTO`, `._create_app`, `TestProjectApplicationNewFieldsCreateUpdate`, `test_application_import.py`, `TestInstituteResponsibleViewSet`, `CommentService`, `test_team_lobby_viewset.py`, `test_tag.py`, `TagService`, `StudyGroupSemesterRepository`, `DirectionService`, `ProjectApplicationCreateDTO`, `test_study_group_domain.py`, `ProjectTrackDomain`, `test_mentor_team_viewset.py`, `test_user_me_student.py`, `TestSemesterAssignViewSet`, `ProjectTrack`, `Role`, `ProjectApplicationService`, `tests/conftest.py`, `.get_filtered_queryset`, `TestTagServiceDelete`, `TestApplicationDashboardViewSet`, `preregistered_mentor_import.py`, `TestCanDeleteTag`, `test_import_preregistered_students.py`, `StudyGroup`, `TestProjectApplicationViewSetTransferToInstitute`, `TagUpdateDTO`, `TestProjectApplicationListSemesterFilter`, `APIClient`, `ApplicationLoggingService`, `TestMyStudyGroupViewSet`, `TestCoordinationAndDtosService`, `TestImportPreRegisteredMentors`, `ProjectService`, `User`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `MentorTeamService`, `make_user`, `ProjectTrackService`, `accounts/views.py`, `ApplicationDashboardDomain`, `StudyGroupService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `TestProjectViewSet`, `ApplicationDashboardService`, `_enrollment_with_mentors`, `APIClient`, `test_institute_responsible_viewset.py`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `student_showcase_service.py`, `accounts/serializers.py`, `.resolve_list_semester_id`, `ProjectApplicationRepository`, `Command`, `TestDepartmentPlanViewSetList`, `TeamLobbyService`, `test_project_track_viewset.py`, `institute_access.py`, `test_project_track_service.py`, `Command`, `MentorTeamDomain`, `TestStudentBlockedFromStaffApi`, `Department`, `test_team_lobby_viewset.py`, `TestInstituteResponsibleViewSet`, `ProjectApplicationViewSet`, `test_import_study_groups_from_contingent.py`, `ProjectApplicationCreateDTO`, `test_mentor_team_viewset.py`, `accounts/admin.py`, `ProjectApplication.py`, `TestSemesterAssignViewSet`, `ProjectApplicationService`, `ProjectTrack`, `.my_department_plan`, `TeamSemester`, `AccountsApiTests`, `.handle`, `TeamSemesterViewSet`, `StudyGroup`, `InstituteResponsibleService`, `test_application_dashboard_viewset.py`, `Direction`, `MentorGroupsDomain`, `TestProjectApplicationListSemesterFilter`, `TestMyStudyGroupViewSet`, `test_institute_access.py`, `StudentShowcaseService`, `ProjectService`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 540 inferred relationships involving `make_user()` (e.g. with `.test_find_user_by_full_name()` and `.test_can_list_users_admin()`) actually correct?**
  _`make_user()` has 540 INFERRED edges - model-reasoned connections that need verification._
- **Are the 50 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Are the 79 inferred relationships involving `Department` (e.g. with `resolve_department_by_name()` and `UserManagementDomain`) actually correct?**
  _`Department` has 79 INFERRED edges - model-reasoned connections that need verification._
- **Are the 70 inferred relationships involving `Semester` (e.g. with `Command` and `SemesterSerializer`) actually correct?**
  _`Semester` has 70 INFERRED edges - model-reasoned connections that need verification._