# Graph Report - project_activity_server  (2026-08-29)

## Corpus Check
- 329 files · ~151,788 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5004 nodes · 10018 edges · 321 communities (227 shown, 94 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 987 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dddf38f9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MentorTeamViewSet
- make_user
- showcase/models.py
- Ответственный по институту — API для фронта
- ProjectApplicationStatusLog
- accounts/views.py
- action
- test_project_track_service.py
- test_institute_responsible_viewset.py
- TagRepository
- ApplicationDashboardService
- ProjectApplication
- test_mentor_groups_viewset.py
- import_study_groups_from_contingent.py
- TeamSemester
- Any
- prepare_study_groups_xlsx.py
- StudyGroupMemberDTO
- showcase/admin.py
- UserListDTO
- TestDepartmentPlanViewSetCreate
- Any
- PreRegisteredStudentService
- StudentShowcaseRepository
- StudyGroupViewSet
- test_student_showcase_viewset.py
- normalize_cell
- TeamLobby.py
- test_team_lobby_viewset.py
- PreRegisteredStudentRepository
- TestProjectApplicationViewSetIsInternalCustomer
- AvailableActionDTO
- test_project_track_viewset.py
- ProjectTrackService
- ProjectTrackViewSet
- TestTagViewSetCreate
- TestTagViewSet
- ProjectService
- ProjectApplicationService
- StudentShowcaseDomain
- PreRegisteredStudent
- .update_application
- .calculate_initial_status
- MentorTeamService
- CommentService
- Path
- TestSubmitApplicationService
- study_group_import.py
- SemesterViewSet
- TestCanUpdateTag
- TagViewSet
- TeamSemesterViewSet
- ProjectTrack
- TestDepartmentPlanViewSetList
- test_import_study_groups_from_contingent.py
- TestProjectViewSet
- ValidationResult
- ProjectApplicationReadDTO
- accounts/permissions.py
- PreRegisteredStudentViewSet
- showcase/urls.py
- ProjectTrackDomain
- UserManagementService
- ProjectTrackApplicationItemDTO
- Примеры использования поля is_internal_customer
- Any
- team_lobby_service.py
- .can_change_status
- TestUserManagementDomain
- Settings
- mentor_team_service.py
- .can_user_access_application
- .get_filtered_queryset
- DepartmentPlan.py
- ProjectTrackRepository
- .view_application
- TestProjectApplicationViewSetSimple
- TestApplicationDashboardViewSet
- dto/mentor_team.py
- TestCanCreateTag
- Витрина проектов (студент) — API для фронта
- serialize_comment_author
- API для работы с проектными заявками
- AccountsApiTests
- TestCanDeleteTag
- mark_teachers_in_system.py
- .resolve_list_semester_id
- Command
- Управление командой
- ApplicationCapabilities
- User
- dto/student_showcase.py
- test_mentor_team_viewset.py
- dto/mentor_groups.py
- .get_filtered_queryset
- Command
- UserSerializer
- InstituteResponsibleService
- .can_edit_application
- TestProjectApplicationViewSetTransferToInstitute
- UserRepository
- extract_group_abbrev.py
- InvolvedManagementService
- Общая информация
- Command
- TeamLobbyService
- test_user_me_student.py
- TestApproveRejectRequest
- ApplicationNotificationService
- TestProjectApplicationListSemesterFilter
- ProjectApplicationCreateDTO
- _generate_collection.py
- test_my_study_group_viewset.py
- ApplicationLoggingService
- ProjectListDTO
- ProjectTrackStatisticsDTO
- .post
- institute_access.py
- InvolvedManager
- TestMyTeamViewSet
- django_db
- TestSemesterAssignViewSet
- test_student_staff_access.py
- Поддержка multipart/form-data
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- test_study_group_domain.py
- Command
- Command
- TestInstituteViewSet
- update_prod.sh
- Command
- ProjectApplicationUpdateDTO
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
- .list_students
- parse_miit_ief_groups.py
- Command
- test_mentor_showcase_viewset.py
- schema.py
- ShowcaseConfig
- get_error_message
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- .add_groups
- teams/admin.py
- 0011_migrate_team_data.py
- StudyGroup
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- test_study_group_viewset.py
- ProjectApplicationCreateSerializer
- PlaceholderUserService
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- TestProjectApplicationSemesterAutoAssign
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
- PasswordResetSerializer
- Department
- PasswordChangeSerializer
- UserManager
- Валидационные правила
- .user_in_accessible_queryset
- CustomResetPasswordForm
- .add_applications
- .create
- TagService
- ProjectTrackUpdateSerializer
- teams/models.py
- ApplicationDashboardViewSet
- 0021_user_placeholder_preregistered_flag.py
- ProjectViewSet
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
- StudyGroup.py
- TestProjectApplicationViewSetIsExternalInResponses
- InstituteSerializer
- format_validation_errors
- TagSerializer
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
- Command
- accounts/models.py
- TestHelpers
- ProjectApplicationRepository
- Схема БД: студенческий портал
- Справочные эндпоинты
- .is_registered
- Semester
- StudyGroupSemesterRepository
- TeamLobbyRepository
- repositories/project.py
- 0017_copy_studygroup_mentors_to_semester.py
- .recalculate_recommended_teams_count
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- Вариант 1: импорт схемы с автообновлением
- ProjectApplicationListSerializer
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- 0016_studygroupsemester.py
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- TeamSemesterMember
- teams/views.py
- 0018_studygroupsemester_mentors_m2m.py

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 526 edges
2. `User` - 252 edges
3. `ProjectApplication` - 148 edges
4. `Department` - 142 edges
5. `ProjectApplicationService` - 136 edges
6. `Semester` - 131 edges
7. `StudyGroup` - 119 edges
8. `ProjectApplicationCreateDTO` - 109 edges
9. `PreRegisteredStudent` - 78 edges
10. `Institute` - 74 edges

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

## Communities (321 total, 94 thin omitted)

### Community 0 - "MentorTeamViewSet"
Cohesion: 0.10
Nodes (22): Команда записана на проект — мутации запрещены., TeamEnrolledInProjectError, MentorTeamAddMemberSerializer, MentorTeamSetCaptainSerializer, MentorTeamUpdateNameSerializer, MentorTeamViewSet, Request, Response (+14 more)

### Community 1 - "make_user"
Cohesion: 0.04
Nodes (17): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, TestProjectTrackViewSet, TestStudentBlockedFromStaffApi, django_db, TestDirectionViewSet (+9 more)

### Community 2 - "showcase/models.py"
Cohesion: 0.05
Nodes (44): Общие константы приложения showcase., DTO для работы с проектными заявками., Упрощенный ViewSet для проектных заявок с использованием новой архитектуры.…, Генерация тестовых одобренных проектов и учебных групп для института IEF., ApplicationInvolvedDepartment, ApplicationInvolvedUser, ApplicationStatus, DepartmentPlan (+36 more)

### Community 3 - "Ответственный по институту — API для фронта"
Cohesion: 0.08
Nodes (24): 1. Список активных групп института, 2. Сотрудники института, 3. Группы с назначенными наставниками, 4. Назначить наставника группе, 5. Снять наставника с группы, Значения `semester_id`, Общие query-параметры, Ответ `200` (+16 more)

### Community 4 - "ProjectApplicationStatusLog"
Cohesion: 0.11
Nodes (12): ProjectApplicationStatusLog, atomic, Логирование удаления причастного пользователя. Args: application: Заявка user:…, Логирование добавления причастного подразделения. Args: application: Заявка…, Логирование удаления причастного подразделения. Args: application: Заявка…, Получение всех логов по заявке. Args: application: Заявка Returns:…, Получение последнего лога заявки. Args: application: Заявка Returns:…, Получение логов по типу действия. Args: application: Заявка action_type: Тип… (+4 more)

### Community 5 - "accounts/views.py"
Cohesion: 0.07
Nodes (33): AcademicYearSerializer, ApproveRequestSerializer, DepartmentSerializer, Meta, PasswordResetConfirmSerializer, Сериализатор для подразделений/кафедр., Краткий сериализатор пользователя для отображения в других сущностях., Проверяет email: нормализация, отсутствие пользователя и активной заявки. (+25 more)

### Community 6 - "action"
Cohesion: 0.13
Nodes (8): action, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, POST /api/project-applications/{id}/approve/ Одобрение заявки, POST /api/project-applications/{id}/reject/ Отклонение заявки, POST /api/project-applications/{id}/request_changes/ Запрос изменений (отправка…, POST /api/project-applications/{id}/transfer_to_institute/ Передача заявки в…, POST /api/project-applications/{id}/return_by_author/ Отзыв заявки автором…, GET /api/project-applications/{id}/status_logs/

### Community 7 - "test_project_track_service.py"
Cohesion: 0.06
Nodes (34): ProjectTrackAddGroupsDTO, ProjectTrackAggregatedStatisticsDTO, ProjectTrackCreateDTO, ProjectTrackGroupDetailDTO, ProjectTrackGroupListDTO, ProjectTrackGroupProjectDTO, ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO (+26 more)

### Community 8 - "test_institute_responsible_viewset.py"
Cohesion: 0.19
Nodes (11): api_client(), direction(), other_institute(), APIClient, django_db, fixture, Тесты API ответственного по институтам., semester() (+3 more)

### Community 9 - "TagRepository"
Cohesion: 0.04
Nodes (40): Repository слой для изоляции работы с базой данных. Этот слой содержит все…, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, TagRepository, django_db (+32 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.03
Nodes (59): get_department_subtree_ids(), Утилиты для работы с подразделениями., Возвращает id корневого подразделения и всех его потомков., ApplicationDashboardDomain, DashboardFilters, Доменная логика дашборда проектных заявок., Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп. (+51 more)

### Community 11 - "ProjectApplication"
Cohesion: 0.05
Nodes (42): ProjectApplication, ApplicationDashboardRepository, Q, QuerySet, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению. (+34 more)

### Community 12 - "test_mentor_groups_viewset.py"
Cohesion: 0.16
Nodes (13): Наставники учебной группы в конкретном семестре., StudyGroupSemester, api_client(), direction(), _enrollment_with_mentors(), APIClient, django_db, fixture (+5 more)

### Community 13 - "import_study_groups_from_contingent.py"
Cohesion: 0.16
Nodes (12): GroupImportRow, Строка отчёта, подготовленная к импорту одной учебной группы., Command, BaseCommand, DataFrame, date, Path, Идемпотентный импорт учебных групп из отчёта контингента 1С (.xls/.xlsx). (+4 more)

### Community 14 - "TeamSemester"
Cohesion: 0.04
Nodes (33): MentorTeamDomain, Доменные правила управления командой наставником., Чистая бизнес-логика API команд наставника., Проверяет, что команда принадлежит учебной группе., Запрещает изменения, если команда записана на проект., Проверяет возможность подтверждения состава., Проверяет возможность разутверждения состава., Удаление возможно только при пустом составе. (+25 more)

### Community 15 - "Any"
Cohesion: 0.25
Nodes (8): Any, APIClient, django_db, parametrize, _team_url(), TestMentorTeamAccess, TestMentorTeamMutations, TestMentorTeamProjectEnrollmentBlock

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroupMemberDTO"
Cohesion: 0.18
Nodes (6): Any, Карточка наставника учебной группы., Возвращает наставников: из семестра или fallback на StudyGroup.mentor., Строка списка группы из контингента., StudyGroupMemberDTO, StudyGroupMentorDTO

### Community 18 - "showcase/admin.py"
Cohesion: 0.15
Nodes (17): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+9 more)

### Community 19 - "UserListDTO"
Cohesion: 0.11
Nodes (19): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, ViewSet для управления пользователями. (+11 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "Any"
Cohesion: 0.11
Nodes (10): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationUpdateSerializer, Сериализатор только для валидации HTTP данных при обновлении., Проверяет согласованность min/max, если оба переданы. (+2 more)

### Community 22 - "PreRegisteredStudentService"
Cohesion: 0.14
Nodes (10): PreRegisteredStudentLookupResult, PreRegisteredStudentService, atomic, Отправляет администратору письмо о расхождении данных. Raises: ValueError: если…, Отправляет студенту письмо после успешной регистрации., Результат поиска предрегистрации., Сериализует результат для API., Оркестрация поиска, регистрации и уведомлений по предрегистрации. (+2 more)

### Community 23 - "StudentShowcaseRepository"
Cohesion: 0.10
Nodes (11): Команда пользователя в семестре с блокировкой строки., Запросы и запись для студенческой витрины проектов., Команда пользователя в семестре (без блокировки)., Связь проект↔трек с проверкой семестра и статуса approved., Треки группы в семестре с одобренными проектами и тегами., Счётчик записанных команд с блокировкой строк TeamSemester проекта., Привязывает проект к команде и пишет лог., Карта (track_id, application_id) → число записанных команд. (+3 more)

### Community 24 - "StudyGroupViewSet"
Cohesion: 0.19
Nodes (10): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/my-groups/ — группы наставника в семестре., GET /api/teams/study-groups/{id}/mentor-detail/ — детали группы наставника., GET /api/teams/study-groups/{id}/project-showcase/ — витрина проектов группы., GET /api/teams/study-groups/ — список и просмотр учебных групп. (+2 more)

### Community 25 - "test_student_showcase_viewset.py"
Cohesion: 0.08
Nodes (19): api_client(), _approved_app(), _create_assembled_team(), direction(), other_group(), django_db, fixture, Тесты API студенческой витрины проектов. (+11 more)

### Community 26 - "normalize_cell"
Cohesion: 0.13
Nodes (16): build_preregistered_student_import_row(), last_names_match(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки. (+8 more)

### Community 27 - "TeamLobby.py"
Cohesion: 0.08
Nodes (33): PageNumberPagination, ApproveJoinRequestSerializer, CreateInvitationSerializer, CreateTeamSerializer, MyTeamViewSet, action, extend_schema, extend_schema_view (+25 more)

### Community 28 - "test_team_lobby_viewset.py"
Cohesion: 0.11
Nodes (16): api_client(), _approved_app(), _create_captained_team(), direction(), lobby_setup(), django_db, fixture, Тесты API лобби формирования команд. (+8 more)

### Community 29 - "PreRegisteredStudentRepository"
Cohesion: 0.10
Nodes (11): PreRegisteredStudentRepository, QuerySet, Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по табельному номеру., Возвращает предрегистрацию по нормализованному СНИЛС., Возвращает предрегистрацию по первичному ключу., Удаляет предрегистрации без привязанного пользователя. (+3 more)

### Community 30 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.07
Nodes (25): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+17 more)

### Community 32 - "test_project_track_viewset.py"
Cohesion: 0.16
Nodes (12): _create_approved_app(), _create_track_with_links(), direction(), other_institute(), django_db, fixture, Тесты ProjectTrackViewSet., semester() (+4 more)

### Community 33 - "ProjectTrackService"
Cohesion: 0.04
Nodes (42): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackReadDTO, DTO для чтения проектного трека., Элемент добавления заявки в трек., DTO для добавления заявок в трек., Создаёт DTO из списка элементов API., Список id заявок для валидации и привязки. (+34 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.16
Nodes (19): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+11 more)

### Community 35 - "TestTagViewSetCreate"
Cohesion: 0.05
Nodes (25): django_db, Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем. (+17 more)

### Community 36 - "TestTagViewSet"
Cohesion: 0.10
Nodes (11): Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level). (+3 more)

### Community 37 - "ProjectService"
Cohesion: 0.14
Nodes (11): ProjectDomain, Коды институтов для фильтрации; None — без ограничения., Правила доступа и фильтрации для списка проектов., ProjectService, Сервис для операций со списком проектов., Оркестрация Domain + Repository для списка проектов., other_institute(), django_db (+3 more)

### Community 38 - "ProjectApplicationService"
Cohesion: 0.03
Nodes (57): ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка., django_db, patch, Ошибки валидации института: несуществующий код или отсутствие связанного…, Нет причастности подразделения — матрица запрещает действие, ожидаем… (+49 more)

### Community 39 - "StudentShowcaseDomain"
Cohesion: 0.12
Nodes (19): Правила доступа и записи команды на проект витрины., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI)., StudentShowcaseDomain (+11 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.14
Nodes (15): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., MonkeyPatch, api_client(), pre_registered_student(), Any, APIClient, django_db (+7 more)

### Community 41 - ".update_application"
Cohesion: 0.15
Nodes (9): Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Не-автор и не-ЦПДС не может редактировать заявку., Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult., CPDS может редактировать одобренные заявки., institute_validator-автор: save совпадает с available_actions (подразделение…, institute_validator без причастного подразделения не может сохранить. (+1 more)

### Community 42 - ".calculate_initial_status"
Cohesion: 0.17
Nodes (9): Определение начального статуса на основе роли пользователя. Чистая функция -…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds., Обычный пользователь создаёт заявки в статусе await_department., Неизвестная роль возвращает статус await_department по умолчанию. (+1 more)

### Community 43 - "MentorTeamService"
Cohesion: 0.17
Nodes (15): MentorTeamService, Any, atomic, Назначает нового капитана из состава команды., Подтверждает состав команды (forming → assembled)., Возвращает состав на редактирование (assembled → forming)., Добавляет зарегистрированного или незарегистрированного студента., Операции наставника над командой группы в семестре. (+7 more)

### Community 44 - "CommentService"
Cohesion: 0.10
Nodes (17): CommentService, atomic, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db, Пустой текст вызывает ValueError., Тесты для CommentService. (+9 more)

### Community 45 - "Path"
Cohesion: 0.15
Nodes (13): aga_institute(), direction(), Any, django_db, fixture, Path, Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта. (+5 more)

### Community 46 - "TestSubmitApplicationService"
Cohesion: 0.09
Nodes (12): Если needs_consultation не передан, значение остается False по умолчанию., При создании упрощенной заявки устанавливается is_external=True и статус…, При создании упрощенной заявки добавляется причастное подразделение ЦПДС., При создании обычной заявки is_external=False по умолчанию., Заявка автоматически переходит в await_institute, если в подразделении нет…, Заявка остаётся в await_department, если в подразделении есть…, Успешная подача заявки: создаётся со статусом created, затем переводится в…, Заявка остаётся в await_department, если валидатор есть в родительском… (+4 more)

### Community 47 - "study_group_import.py"
Cohesion: 0.14
Nodes (13): build_group_import_row(), build_group_name(), parse_direction_level(), parse_permanent_group_code(), ParsedPermanentGroup, Чистая логика импорта учебных групп из отчёта контингента 1С., Разбирает код постоянной группы вида «АМБ-2025-11» или «ОММ-2022-11-1». Raises:…, Собирает отображаемое название группы, например «АМБ-211». (+5 more)

### Community 48 - "SemesterViewSet"
Cohesion: 0.29
Nodes (4): extend_schema, ViewSet для операций над семестрами, связанных с проектными заявками., POST /api/semesters/{id}/assign-empty-applications Присваивает переданный…, SemesterViewSet

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+2 more)

### Community 50 - "TagViewSet"
Cohesion: 0.06
Nodes (29): Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Инициализация из модели Tag., Преобразование в словарь., TagReadDTO, DepartmentAttachDetachSerializer, action (+21 more)

### Community 51 - "TeamSemesterViewSet"
Cohesion: 0.18
Nodes (11): action, Request, Response, POST /api/teams/team-semesters/{id}/members/ — добавить участника., DELETE /api/teams/team-semesters/{id}/members/{member_id}/., CRUD для постоянных команд., GET /api/teams/teams/my/?semester_id= — команды пользователя в семестре., CRUD для участия команды в семестре и управления составом. (+3 more)

### Community 52 - "ProjectTrack"
Cohesion: 0.07
Nodes (18): display, Количество групп в треке., Количество заявок в треке., Доменная логика студенческой витрины проектов., ProjectTrack, Проектный трек — контейнер для назначения групп и заявок в рамках семестра., Доменные правила лобби формирования команд., Удаление: капитан, forming, в составе только он. (+10 more)

### Community 53 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 54 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.18
Nodes (9): calculate_course_number(), group_ended_by_planned_dates(), parse_planned_end_date(), date, Возвращает True, если у группы есть хотя бы одна дата окончания и все они…, Рассчитывает номер курса на текущий учебный год и семестр., Парсит дату планового окончания из ячейки отчёта 1С., Тесты импорта учебных групп из контингента 1С. (+1 more)

### Community 55 - "TestProjectViewSet"
Cohesion: 0.18
Nodes (4): _create_approved_app(), django_db, ЦПДС в причастных не должно подменять основное подразделение проекта., TestProjectViewSet

### Community 56 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 57 - "ProjectApplicationReadDTO"
Cohesion: 0.06
Nodes (29): Exception, build_author_short_name(), ProjectApplicationListDTO, ProjectApplicationReadDTO, Формирует короткое имя вида 'Фамилия И.О.' или возвращает None., DTO для чтения заявки - оптимизированный набор полей, DTO для списка заявок - минимальный набор полей, DTO (Data Transfer Object) слой для передачи данных между слоями. Этот слой… (+21 more)

### Community 58 - "accounts/permissions.py"
Cohesion: 0.07
Nodes (27): IsAdminOrCpds, IsCpdsUser, IsInstituteValidator, ProjectManagementPermission, APIView, BasePermission, Request, Пользовательские permissions для приложения accounts. (+19 more)

### Community 59 - "PreRegisteredStudentViewSet"
Cohesion: 0.13
Nodes (18): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Отправляет администратору письмо о расхождении данных., Публичные операции предрегистрации студентов. (+10 more)

### Community 60 - "showcase/urls.py"
Cohesion: 0.18
Nodes (10): ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…, InstituteViewSet (+2 more)

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.06
Nodes (19): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя. (+11 more)

### Community 62 - "UserManagementService"
Cohesion: 0.27
Nodes (5): Оркестрация Domain + Repository для управления пользователями., UserManagementService, django_db, Тесты UserManagementService., TestUserManagementService

### Community 63 - "ProjectTrackApplicationItemDTO"
Cohesion: 0.18
Nodes (6): ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO, Преобразует DTO в словарь для API., DTO заявки в проектном треке., Преобразует DTO в словарь для API., DTO группы в проектном треке.

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "Any"
Cohesion: 0.12
Nodes (9): Any, Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API. (+1 more)

### Community 66 - "team_lobby_service.py"
Cohesion: 0.07
Nodes (23): Подтверждение состава: капитан, forming, размер в лимитах трека., ФИО пользователя для лога., LobbyInvitationDTO, LobbyJoinRequestDTO, LobbyReadDTO, LobbyTeamItemDTO, LobbyTrackDTO, MyTeamEventLogDTO (+15 more)

### Community 67 - ".can_change_status"
Cohesion: 0.05
Nodes (28): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку., Бизнес-операция: отзыв заявки автором. (+20 more)

### Community 68 - "TestUserManagementDomain"
Cohesion: 0.14
Nodes (7): Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., Role, django_db, TestUserManagementDomain

### Community 69 - "Settings"
Cohesion: 0.11
Nodes (19): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+11 more)

### Community 70 - "mentor_team_service.py"
Cohesion: 0.06
Nodes (33): action, extend_schema, extend_schema_view, Request, Response, ViewSet студенческой витрины проектов., Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/. (+25 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.14
Nodes (11): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Тесты для проверки доступа пользователя к заявке., Автор всегда имеет доступ к своей заявке., Админ имеет доступ ко всем заявкам., Модератор имеет доступ ко всем заявкам., CPDS имеет доступ ко всем заявкам., Валидатор подразделения имеет доступ ко всем заявкам., Валидатор института имеет доступ ко всем заявкам. (+3 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.14
Nodes (11): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., Тесты для фильтрации queryset тегов по ролям., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения., institute_validator без подразделения видит только общие теги. (+3 more)

### Community 73 - "DepartmentPlan.py"
Cohesion: 0.12
Nodes (20): DenyStudentPermission, ProjectTrackPermission, Разрешает доступ к проектным трекам для admin, cpds и institute_validator., Запрещает доступ пользователям с ролью student., DepartmentPlanSerializer, DepartmentPlanViewSet, action, extend_schema (+12 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.06
Nodes (16): ProjectTrackRepository, Создаёт проектный трек., Обновляет поля трека., Возвращает id групп, уже привязанных к треку., Добавляет группы в трек; возвращает число созданных связей., Удаляет группу из трека; True если связь была., Возвращает id заявок, уже привязанных к треку., Добавляет заявки в трек; возвращает число созданных связей. (+8 more)

### Community 75 - ".view_application"
Cohesion: 0.15
Nodes (8): Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Автор всегда имеет доступ к просмотру своей заявки., Обычному пользователю чужая заявка недоступна., Список заявок разрешён всем (возвращает True)., TestViewAndList

### Community 76 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - "dto/mentor_team.py"
Cohesion: 0.22
Nodes (6): MentorTeamDetailDTO, MentorTeamMemberDTO, Any, DTO карточки команды для API наставника., Участник команды в карточке наставника., Карточка команды для ответов мутаций наставника.

### Community 79 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 80 - "Витрина проектов (студент) — API для фронта"
Cohesion: 0.14
Nodes (13): 1. Список треков с проектами, 2. Детали проекта, 3. Записать команду на проект, Витрина проектов (студент) — API для фронта, Ответ `200`, Ответ `200`, Ответ `200`, Ошибки (+5 more)

### Community 81 - "serialize_comment_author"
Cohesion: 0.16
Nodes (10): Сериализует автора комментария с role и department. Args: author: User объект…, serialize_comment_author(), GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, Тесты для функции serialize_comment_author., Если author равен None, возвращаются None значения., Сериализация автора с полными данными: имя, фамилия, отчество, роль,…, Сериализация автора без отчества., Сериализация автора без роли и подразделения. (+2 more)

### Community 82 - "API для работы с проектными заявками"
Cohesion: 0.11
Nodes (18): API для работы с проектными заявками, Автоматическая установка статуса, Аутентификация, Дополнительные возможности ViewSet, Минимальный пример запроса, Неавторизованное создание заявок, Необязательные поля:, Объяснение полей (+10 more)

### Community 83 - "AccountsApiTests"
Cohesion: 0.04
Nodes (34): AccountsApiTests, override_settings, Без токена возвращается 401, с токеном — профиль текущего пользователя., GET /api/accounts/user/ возвращает код института, сопоставленного с…, Если для департамента нет института, institute_code должен быть None., Сброс пароля по email отправляет письмо (locmem backend)., Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем., Аутентифицированный пользователь меняет пароль, новый пароль работает. (+26 more)

### Community 84 - "TestCanDeleteTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на удаление тега. Args: user: Пользователь tag:…, django_db, Тесты для проверки прав на удаление тегов., cpds может удалять общие теги., cpds не может удалять теги с подразделением., institute_validator может удалять общие теги., institute_validator может удалять теги своего подразделения., institute_validator не может удалять теги чужого подразделения. (+3 more)

### Community 85 - "mark_teachers_in_system.py"
Cohesion: 0.27
Nodes (11): build_user_indexes(), find_user(), main(), normalize_name(), Сверка преподавателей из Excel со списком пользователей prod API., Нормализует ФИО для сравнения., Ключ из набора слов ФИО (устойчив к перестановке частей)., Строит индексы пользователей по ФИО. (+3 more)

### Community 86 - ".resolve_list_semester_id"
Cohesion: 0.17
Nodes (7): Разбор query-параметра semester_id для GET-списков: id, next, actual., Any, Список треков с проектами для группы наставника в семестре., Any, Возвращает данные учебной группы текущего студента., django_db, TestSemesterResolveListSemesterId

### Community 87 - "Command"
Cohesion: 0.15
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "Управление командой"
Cohesion: 0.08
Nodes (24): Query-параметры, Query-параметры, Query-параметры, Вернуть состав на редактирование, Витрина проектов, Детали группы наставника, Добавить участника, Карточка команды (ответ всех мутаций) (+16 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.16
Nodes (10): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы., Возвращает список доступных действий согласно матрице. (+2 more)

### Community 90 - "User"
Cohesion: 0.03
Nodes (53): AbstractBaseUser, User, QuerySet, Подгружает parent подразделения для корректного resolve институтов., Список пользователей с учётом роли запрашивающего., Возвращает пользователя, если он доступен запрашивающему., Частичное обновление пользователя., check_and_fix_user() (+45 more)

### Community 91 - "dto/student_showcase.py"
Cohesion: 0.07
Nodes (22): Any, DTO студенческой витрины проектов., Результат записи команды на проект., Преобразует DTO в словарь для API., Карточка проекта в списке трека витрины., Преобразует DTO в словарь для API., Трек с вложенными проектами для витрины., Преобразует DTO в словарь для API. (+14 more)

### Community 92 - "test_mentor_team_viewset.py"
Cohesion: 0.33
Nodes (10): api_client(), _approved_app(), direction(), _enrollment_with_mentors(), mentor_team_setup(), fixture, Тесты API управления командой наставником., semester() (+2 more)

### Community 93 - "dto/mentor_groups.py"
Cohesion: 0.09
Nodes (15): MentorGroupDetailDTO, MentorGroupListDTO, MentorGroupListItemDTO, MentorGroupStudentDTO, MentorGroupTeamDTO, Any, DTO для эндпоинта «Мои группы» наставника., Строка списка групп наставника. (+7 more)

### Community 94 - ".get_filtered_queryset"
Cohesion: 0.16
Nodes (8): QuerySet, Фильтрует направления: institute_validator — только из групп своего института., django_db, parametrize, Разрешение институтов по подразделению пользователя., Фильтрация queryset направлений по ролям., TestGetFilteredQueryset, TestGetUserInstituteCodes

### Community 95 - "Command"
Cohesion: 0.24
Nodes (4): Command, BaseCommand, Path, Проверка ссылок для active_* ключей (только предупреждение в stdout).

### Community 96 - "UserSerializer"
Cohesion: 0.15
Nodes (11): Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., UserSerializer, CustomTokenObtainPairSerializer (+3 more)

### Community 97 - "InstituteResponsibleService"
Cohesion: 0.07
Nodes (33): delete, InstituteResponsibleAssignMentorDTO, Ответ после изменения состава наставников., AssignMentorSerializer, InstituteResponsiblePermission, InstituteResponsibleViewSet, action, BasePermission (+25 more)

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

### Community 102 - "InvolvedManagementService"
Cohesion: 0.12
Nodes (12): InvolvedManagementService, atomic, Добавляет причастное подразделение по его краткому названию. Args: application:…, Добавляет причастное подразделение по его ID. Args: application: Заявка, к…, Добавляет пользователя как причастного к заявке. Args: application: Заявка…, Добавляет подразделение как причастное к заявке. Args: application: Заявка…, Получает всех причастных пользователей заявки. Args: application: Заявка…, Сервис для управления причастными пользователями и подразделениями.… (+4 more)

### Community 103 - "Общая информация"
Cohesion: 0.50
Nodes (4): Аутентификация, Базовый URL, Общая информация, Форматы данных

### Community 104 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

### Community 105 - "TeamLobbyService"
Cohesion: 0.11
Nodes (22): atomic, QuerySet, UserType, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент принимает приглашение., Оркестрация Domain + Repository для студенческого лобби., Студент отклоняет приглашение. (+14 more)

### Community 106 - "test_user_me_student.py"
Cohesion: 0.26
Nodes (9): api_client(), Any, APIClient, django_db, fixture, Тесты GET /api/accounts/user/ для роли student., student_user(), study_group() (+1 more)

### Community 107 - "TestApproveRejectRequest"
Cohesion: 0.27
Nodes (6): parametrize, Матрица прав определяет доступность reject., Для returned_* действует агрегирующее правило returned_(all)., Отзыв доступен только автору и не для финальных approved/rejected., Матрица прав определяет доступность approve для ролей и статусов., TestApproveRejectRequest

### Community 108 - "ApplicationNotificationService"
Cohesion: 0.19
Nodes (8): ApplicationNotificationService, Отправка писем автору при отклонении и отправке на доработку., Email получателя: author_email заявки или email связанного пользователя-автора., Письмо автору: заявка отправлена на доработку., Письмо автору: заявка отклонена., django_db, patch, TestApplicationNotificationService

### Community 110 - "ProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (41): create_test_applications(), Создаем тестовые заявки, Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Определение необходимости консультации на основе данных заявки. Чистая функция…, Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, ProjectApplicationCreateDTO, DTO для создания заявки - только данные, никакой логики, Носитель проблемы короче 5 символов вызывает ошибку. (+33 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - "test_my_study_group_viewset.py"
Cohesion: 0.10
Nodes (18): MyStudyGroupDTO, DTO для эндпоинта «Моя группа»., Полные данные учебной группы для текущего студента., QuerySet, Репозиторий для учебных групп., Доступ к данным StudyGroup., Группа с наставником и контингентом без N+1., StudyGroupRepository (+10 more)

### Community 113 - "ApplicationLoggingService"
Cohesion: 0.05
Nodes (38): ApplicationLoggingService, Сервис для логирования изменений в проектных заявках. Обеспечивает отслеживание…, Сервис для логирования изменений в проектных заявках. Обеспечивает полное…, django_db, Unit-тесты для ApplicationLoggingService. Проверяем логирование всех типов…, Первый переход (from_status=None) помечает заявку, если актор не автор., Логирование с указанием предыдущего лога для создания цепочки., Тесты для log_status_change. (+30 more)

### Community 114 - "ProjectListDTO"
Cohesion: 0.09
Nodes (19): get_root_department(), is_cpds_department(), Проверяет, что подразделение — ЦПДС (координирующее, не основное)., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, ProjectListDTO, Any, DTO для списка проектов., DTO для списка проектов. (+11 more)

### Community 115 - "ProjectTrackStatisticsDTO"
Cohesion: 0.18
Nodes (7): ProjectTrackInstituteStatisticsDTO, ProjectTrackStatisticsDTO, DTO статистики распределения проектов по группам., Преобразует DTO в словарь для API., DTO статистики по одному институту., Преобразует DTO в словарь для API., Преобразует DTO в словарь для API.

### Community 116 - ".post"
Cohesion: 0.24
Nodes (7): LoginView, extend_schema, Request, Response, Сменяет пароль текущего пользователя после проверки текущего пароля., Получение JWT токена по email и паролю., TokenObtainPairView

### Community 117 - "institute_access.py"
Cohesion: 0.09
Nodes (27): ID подразделений для фильтрации; None — без ограничения., Доменная логика для списка проектов., Доменная логика для проектных треков., application_available_for_institute(), application_belongs_to_institutes(), get_accessible_institute_codes(), get_department_ids_by_institute_code(), get_department_ids_for_institute_codes() (+19 more)

### Community 118 - "InvolvedManager"
Cohesion: 0.43
Nodes (3): InvolvedManager, atomic, Менеджер для управления причастными пользователями и подразделениями.

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → effective max(min)/min(max)., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "django_db"
Cohesion: 0.29
Nodes (5): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, TestProjectApplicationViewSetExternal

### Community 121 - "TestSemesterAssignViewSet"
Cohesion: 0.29
Nodes (3): Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, TestSemesterAssignViewSet

### Community 122 - "test_student_staff_access.py"
Cohesion: 0.22
Nodes (6): api_client(), django_db, fixture, Ограничения доступа роли student к staff-сущностям., TestApplicationCommentAccess, TestApplicationDestroyDisabled

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

### Community 132 - "ProjectApplicationUpdateDTO"
Cohesion: 0.09
Nodes (23): ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Явное выражение бизнес-намерений (не технических операций). Этот модуль…, Domain слой - чистая бизнес-логика без побочных эффектов. Этот слой содержит…, ProjectApplicationUpdateDTO, DTO для обновления заявки - только изменяемые поля (+15 more)

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

### Community 138 - "ProjectApplicationViewSet"
Cohesion: 0.11
Nodes (11): ProjectApplicationViewSet, Упрощенный ViewSet - только обработка HTTP запросов. Вся бизнес-логика вынесена…, Переопределяем права доступа в зависимости от действия. `simple` — публичное…, DELETE отключён: заявки не удаляются через API., Выбор сериализатора в зависимости от действия, Возвращает QuerySet для списка заявок. DRF автоматически применит пагинацию., GET /api/project-applications/ Получение списка заявок с пагинацией. Query:…, GET /api/project-applications/{id}/ Получение заявки по ID с доступными… (+3 more)

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

### Community 144 - "parse_miit_ief_groups.py"
Cohesion: 0.60
Nodes (4): extract_block(), main(), parse_groups(), Парсинг групп ИЭФ со страницы miit.ru/timetable.

### Community 146 - "test_mentor_showcase_viewset.py"
Cohesion: 0.17
Nodes (16): api_client(), _approved_app(), _create_assembled_team(), direction(), _enrollment_with_mentors(), mentor_showcase_setup(), APIClient, django_db (+8 more)

### Community 147 - "schema.py"
Cohesion: 0.50
Nodes (3): exclude_auth_api_duplicate(), Хуки и расширения для drf-spectacular., Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*). В…

### Community 149 - "get_error_message"
Cohesion: 0.19
Nodes (7): get_error_message(), GET /api/project-applications/external/ Получение списка всех внешних заявок…, Возвращает сообщение об ошибке в зависимости от режима DEBUG. Args: exception:…, PK семестра из ?semester_id= (id | next | actual) или None, если параметра нет., GET /api/project-applications/by_status/?status=created Получение заявок по…, GET /api/project-applications/recent/ Получение последних заявок (только для…, GET /api/project-applications/coordination/ Заявки для координации: где…

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

### Community 156 - ".add_groups"
Cohesion: 0.33
Nodes (4): Создаёт DTO из словаря., ProjectTrackAddGroupsSerializer, Сериализатор для добавления групп в трек., POST /api/showcase/project-tracks/{id}/groups/.

### Community 157 - "teams/admin.py"
Cohesion: 0.27
Nodes (11): DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin, TeamSemesterAdmin (+3 more)

### Community 159 - "StudyGroup"
Cohesion: 0.11
Nodes (24): StudyGroup, aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов. (+16 more)

### Community 164 - "test_study_group_viewset.py"
Cohesion: 0.47
Nodes (5): direction(), other_institute(), fixture, Тесты StudyGroupViewSet., study_groups()

### Community 165 - "ProjectApplicationCreateSerializer"
Cohesion: 0.33
Nodes (4): ProjectApplicationCreateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы…, Проверяет, что min_team_members не больше max_team_members., Преобразование в DTO - никакой бизнес-логики

### Community 166 - "PlaceholderUserService"
Cohesion: 0.24
Nodes (6): PlaceholderUserService, atomic, Создаёт и возвращает псевдо-user для предрегистрации., Возвращает существующего или создаёт псевдо-user для предрегистрации. Raises:…, Уникальный внутренний email для псевдо-аккаунта., TestPlaceholderUserRegistration

### Community 189 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 190 - "QuerySet"
Cohesion: 0.12
Nodes (9): QuerySet, Возвращает трек по id или None., Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки., Queryset трека с prefetch связей. (+1 more)

### Community 192 - "Department"
Cohesion: 0.07
Nodes (28): Command, BaseCommand, Department, Command, BaseCommand, Сбрасывает счетчик ID для таблицы тегов., Command, Any (+20 more)

### Community 193 - "PasswordChangeSerializer"
Cohesion: 0.33
Nodes (4): PasswordChangeSerializer, Any, Возвращает учебную группу пользователя или None., Сериализатор для смены пароля аутентифицированного пользователя.

### Community 195 - "Валидационные правила"
Cohesion: 0.50
Nodes (4): Валидационные правила, Обязательные поля, Обязательные поля:, Типы данных

### Community 198 - ".add_applications"
Cohesion: 0.33
Nodes (4): ProjectTrackAddApplicationsSerializer, Список заявок с рекомендуемым числом команд и лимитами размера., Проверяет отсутствие дубликатов id в одном запросе., POST /api/showcase/project-tracks/{id}/applications/.

### Community 199 - ".create"
Cohesion: 0.25
Nodes (5): Создаёт DTO из словаря., ProjectTrackCreateSerializer, POST /api/showcase/project-tracks/ — создание трека., Сериализатор для создания проектного трека., Проверяет согласованность лимитов размера команды.

### Community 200 - "TagService"
Cohesion: 0.03
Nodes (67): Доменная логика для тегов - чистые функции без эффектов., Чистая бизнес-логика для тегов - только функции, никаких эффектов., Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, TagDomain, DTO для работы с тегами., DTO для обновления тега., DTO для создания тега. (+59 more)

### Community 201 - "ProjectTrackUpdateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackUpdateSerializer, Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

### Community 202 - "teams/models.py"
Cohesion: 0.05
Nodes (43): DirectionDomain, Доменная логика для направлений подготовки., Фильтрация направлений по роли пользователя., DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DirectionSerializer (+35 more)

### Community 203 - "ApplicationDashboardViewSet"
Cohesion: 0.25
Nodes (6): ApplicationDashboardViewSet, extend_schema, Request, Response, API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 205 - "ProjectViewSet"
Cohesion: 0.25
Nodes (5): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией.

### Community 206 - "API Документация - Проектные заявки"
Cohesion: 0.14
Nodes (12): 1. Создание заявки (авторизованные пользователи), API Документация - Проектные заявки, Заголовки, Пример запроса, ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации (+4 more)

### Community 240 - "StudyGroup.py"
Cohesion: 0.19
Nodes (10): Any, DTO для учебных групп., DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, Компактная выдача для списка учебных групп. (+2 more)

### Community 241 - "TestProjectApplicationViewSetIsExternalInResponses"
Cohesion: 0.25
Nodes (5): Тесты для проверки наличия поля is_external в ответах API., POST /api/showcase/project-applications/ возвращает is_external в ответе., GET /api/showcase/project-applications/{id}/ возвращает is_external в ответе., GET /api/showcase/project-applications/ возвращает is_external в списке., TestProjectApplicationViewSetIsExternalInResponses

### Community 242 - "InstituteSerializer"
Cohesion: 0.67
Nodes (3): InstituteSerializer, Meta, Сериализатор для институтов/академий.

### Community 243 - "format_validation_errors"
Cohesion: 0.33
Nodes (4): format_validation_errors(), POST /api/project-applications/ Создание заявки - только обработка HTTP, Форматирует ошибки валидации используя стандартные DRF механизмы. Args: errors:…, POST /api/project-applications/simple/ Создание заявки без авторизации

### Community 244 - "TagSerializer"
Cohesion: 0.67
Nodes (3): Meta, Сериализатор для тегов., TagSerializer

### Community 245 - "TestProjectApplicationNewFieldsCreateUpdate"
Cohesion: 0.18
Nodes (5): _base_create_payload(), django_db, TestMyApplicationsNewFields, TestProjectApplicationNewFieldsCreateUpdate, TestProjectApplicationNewFieldsLists

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 278 - "accounts/models.py"
Cohesion: 0.08
Nodes (26): Доменная логика управления пользователями., Правила доступа и валидации для управления пользователями., UserManagementDomain, Command, BaseCommand, Role, Репозиторий предрегистрации студентов., Создание псевдо-аккаунтов для незарегистрированных студентов контингента. (+18 more)

### Community 280 - "ProjectApplicationRepository"
Cohesion: 0.03
Nodes (54): ProjectApplicationRepository, Репозиторий - вся работа с БД здесь, Получение QuerySet заявок по статусу для пагинации., Обновление заявки. Обновляет только переданные поля., Создание заявки в БД. Принимает DTO и пользователя, возвращает созданную…, Проверка существования заявки. Быстрая проверка без загрузки объекта., Подсчет заявок по статусу. Для аналитики и отчетов., Присваивает семестр всем заявкам без установленного семестра. Args:… (+46 more)

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 292 - "Semester"
Cohesion: 0.11
Nodes (11): Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Следующий семестр для новых заявок (Settings.next_semester_code)., Semester, Command, BaseCommand, Добавляет причастные подразделения института к заявке., api_client() (+3 more)

### Community 294 - "StudyGroupSemesterRepository"
Cohesion: 0.11
Nodes (13): QuerySet, Репозиторий для StudyGroupSemester и связанных выборок., Снимает наставника с группы в семестре; возвращает актуальные mentorIds., Возвращает отсортированные ID наставников группы в семестре., Доступ к данным групп в семестре и сотрудников института., Активные группы института., Активные группы с prefetch наставников в семестре., Возвращает группу по ID или None. (+5 more)

### Community 295 - "TeamLobbyRepository"
Cohesion: 0.03
Nodes (36): Заявка должна быть в статусе pending., Приглашение должно быть в статусе pending., Заявка студента на вступление в команду в семестре., Приглашение капитана студенту вступить в команду., Status, TeamInvitation, TeamJoinRequest, QuerySet (+28 more)

### Community 297 - "repositories/project.py"
Cohesion: 0.25
Nodes (6): ProjectRepository, QuerySet, Репозиторий для списка проектов., Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

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

### Community 310 - "ProjectApplicationListSerializer"
Cohesion: 0.67
Nodes (3): Meta, ProjectApplicationListSerializer, Простой сериализатор для списка заявок

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

### Community 329 - "TeamSemesterMember"
Cohesion: 0.08
Nodes (29): Репозиторий студенческой витрины проектов (без N+1)., Meta, Постоянная команда участников проектной деятельности., Участник команды в конкретном семестре., Лог действий по команде., Role, Team, TeamEventLog (+21 more)

### Community 331 - "teams/views.py"
Cohesion: 0.12
Nodes (20): _is_staff_or_admin(), APIView, BasePermission, Request, Разрешения для приложения teams., Доступ только студенту с привязанной учебной группой., Чтение — любой аутентифицированный пользователь. Изменение постоянной команды —…, Изменение семестрового контекста — капитан, admin или cpds. (+12 more)

## Knowledge Gaps
- **263 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+258 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **94 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `showcase/models.py`, `ProjectApplicationStatusLog`, `accounts/views.py`, `test_project_track_service.py`, `StudyGroupService`, `ApplicationDashboardService`, `StudyGroupMemberDTO`, `UserListDTO`, `accounts/models.py`, `ProjectApplicationRepository`, `AvailableActionDTO`, `ProjectTrackService`, `ProjectService`, `PlaceholderUserService`, `StudentShowcaseDomain`, `StudyGroupSemesterRepository`, `TeamLobbyRepository`, `MentorTeamService`, `CommentService`, `TestCanUpdateTag`, `ProjectTrack`, `accounts/permissions.py`, `ProjectTrackDomain`, `PasswordResetSerializer`, `PasswordChangeSerializer`, `team_lobby_service.py`, `.can_change_status`, `.user_in_accessible_queryset`, `TestUserManagementDomain`, `Settings`, `mentor_team_service.py`, `TagService`, `DepartmentPlan.py`, `.get_filtered_queryset`, `.view_application`, `teams/models.py`, `teams/views.py`, `TestCanCreateTag`, `TestCanDeleteTag`, `.resolve_list_semester_id`, `test_mentor_team_viewset.py`, `dto/mentor_groups.py`, `.get_filtered_queryset`, `UserSerializer`, `InstituteResponsibleService`, `UserRepository`, `InvolvedManagementService`, `TeamLobbyService`, `ProjectApplicationCreateDTO`, `test_my_study_group_viewset.py`, `institute_access.py`, `InvolvedManager`, `test_study_group_domain.py`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `make_user`, `showcase/models.py`, `accounts/views.py`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `test_project_track_service.py`, `StudyGroupService`, `test_institute_responsible_viewset.py`, `ProjectApplicationViewSet`, `ApplicationDashboardService`, `test_mentor_groups_viewset.py`, `Any`, `test_mentor_showcase_viewset.py`, `TestDepartmentPlanViewSetCreate`, `accounts/models.py`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `test_team_lobby_viewset.py`, `StudyGroup`, `test_project_track_viewset.py`, `ProjectTrackService`, `ProjectService`, `ProjectApplicationService`, `TestProjectApplicationSemesterAutoAssign`, `MentorTeamService`, `study_group_import.py`, `TeamSemesterViewSet`, `TestDepartmentPlanViewSetList`, `test_import_study_groups_from_contingent.py`, `TestProjectViewSet`, `UserManagementService`, `Department`, `team_lobby_service.py`, `Settings`, `mentor_team_service.py`, `DepartmentPlan.py`, `TeamSemesterMember`, `teams/views.py`, `AccountsApiTests`, `.resolve_list_semester_id`, `test_mentor_team_viewset.py`, `Command`, `InstituteResponsibleService`, `TeamLobbyService`, `TestProjectApplicationListSemesterFilter`, `test_my_study_group_viewset.py`, `TestProjectApplicationNewFieldsCreateUpdate`, `institute_access.py`, `TestSemesterAssignViewSet`, `test_student_staff_access.py`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `TestDepartmentPlanViewSetMyDepartmentPlan`, `test_project_track_service.py`, `test_institute_responsible_viewset.py`, `StudyGroupService`, `ApplicationDashboardService`, `test_mentor_groups_viewset.py`, `Any`, `test_mentor_showcase_viewset.py`, `TestDepartmentPlanViewSetCreate`, `accounts/models.py`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `test_team_lobby_viewset.py`, `TestProjectApplicationViewSetIsInternalCustomer`, `StudyGroup`, `test_project_track_viewset.py`, `ProjectTrackService`, `TestTagViewSetCreate`, `TestTagViewSet`, `ProjectService`, `ProjectApplicationService`, `PreRegisteredStudent`, `TestProjectApplicationSemesterAutoAssign`, `CommentService`, `TestSubmitApplicationService`, `TestCanUpdateTag`, `TestDepartmentPlanViewSetList`, `TestProjectViewSet`, `ProjectApplicationReadDTO`, `ProjectTrackDomain`, `UserManagementService`, `TestUserManagementDomain`, `.get_filtered_queryset`, `TagService`, `teams/models.py`, `TeamSemesterMember`, `TestApplicationDashboardViewSet`, `TestCanCreateTag`, `TestCanDeleteTag`, `User`, `test_mentor_team_viewset.py`, `.get_filtered_queryset`, `TestProjectApplicationViewSetTransferToInstitute`, `test_user_me_student.py`, `ApplicationNotificationService`, `TestProjectApplicationListSemesterFilter`, `test_my_study_group_viewset.py`, `TestProjectApplicationViewSetIsExternalInResponses`, `ApplicationLoggingService`, `TestProjectApplicationNewFieldsCreateUpdate`, `django_db`, `TestSemesterAssignViewSet`, `test_student_staff_access.py`, `test_study_group_domain.py`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Are the 523 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 523 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 74 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 74 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._