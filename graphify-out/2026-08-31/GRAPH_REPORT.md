# Graph Report - project_activity_server  (2026-08-29)

## Corpus Check
- 329 files · ~152,092 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5014 nodes · 10060 edges · 329 communities (232 shown, 97 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 990 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9dcb8800`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MentorTeamService
- make_user
- Department
- Ответственный по институту — API для фронта
- ApplicationLoggingService
- accounts/views.py
- action
- Any
- test_institute_responsible_viewset.py
- TagRepository
- ApplicationDashboardService
- QuerySet
- _enrollment_with_mentors
- ._collect_group_rows
- TeamSemester
- test_mentor_team_viewset.py
- prepare_study_groups_xlsx.py
- StudyGroupMemberDTO
- ProjectTrack
- UserManagementService
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- .lookup
- ApplicationDashboardRepository
- StudyGroupViewSet
- test_student_showcase_viewset.py
- preregistered_student_service.py
- Request
- TestTeamLobbyViewSet
- PreRegisteredStudentRepository
- TestProjectApplicationViewSetIsInternalCustomer
- AvailableActionDTO
- TagCreateDTO
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
- Tag
- CommentService
- Path
- dto/institute_responsible.py
- study_group_import.py
- SemesterViewSet
- TestCanUpdateTag
- TagViewSet
- TeamSemesterViewSet
- DirectionService
- TestDepartmentPlanViewSetList
- TestStudyGroupImportDomain
- TestProjectViewSet
- ValidationResult
- TestProjectApplicationReadDTO
- accounts/permissions.py
- PreRegisteredStudentService
- showcase/urls.py
- TestProjectTrackDomain
- TagUpdateDTO
- UserType
- Примеры использования поля is_internal_customer
- Any
- TeamLobbyDomain
- .can_change_status
- UserManagementDomain
- Settings
- mentor_team_service.py
- .can_user_access_application
- .get_filtered_queryset
- DepartmentPlanViewSet
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
- TestInstituteResponsibleViewSet
- test_mentor_group_detail_viewset.py
- .get_filtered_queryset
- TestLogStatusChange
- UserSerializer
- InstituteResponsibleViewSet
- TestCanEditApplication
- TestProjectApplicationViewSetTransferToInstitute
- UserRepository
- extract_group_abbrev.py
- ProjectApplication
- API Документация - Проектные заявки
- Command
- TeamLobbyService
- .get_dashboard
- TestApproveRejectRequest
- ApplicationNotificationService
- TestProjectApplicationListSemesterFilter
- .validate_create
- _generate_collection.py
- TestMyStudyGroupViewSet
- TestGetLogs
- is_cpds_department
- ._resolve_context
- .post
- institute_access.py
- TestProjectApplicationListDTO
- TestMyTeamViewSet
- TeamLobbyViewSet
- StudentShowcaseViewSet
- InstituteResponsibleService
- Поддержка multipart/form-data
- test_import_institutes.py
- build_fgos_napravleniya_csv.py
- StudyGroupDomain
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
- .list_students
- parse_miit_ief_groups.py
- Command
- test_mentor_showcase_viewset.py
- schema.py
- ShowcaseConfig
- fixture
- Command
- 0013_refactor_comments.py
- 0031_refactor_projecttrack.py
- 0033_alter_recommended_teams_count_default.py
- 0036_projecttrack_team_member_limits.py
- 0037_projecttrack_recommended_teams_count.py
- test_import_study_groups_from_contingent.py
- teams/admin.py
- 0011_migrate_team_data.py
- test_import_preregistered_students.py
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- test_study_group_viewset.py
- .get_filtered_queryset
- test_team_lobby_viewset.py
- TeamsConfig
- 0005_studygroup_institute_fk.py
- 0006_direction_code_primary_key.py
- .can_access_track
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
- .submit_application
- test_export_import_departments_roundtrip
- PasswordChangeSerializer
- ._department_to_dict
- InstituteResponsibleGroupMentorsDTO
- InstituteResponsible.py
- .validate_group_institute_codes
- Command
- ProjectApplicationComment
- TagService
- ._track_detail_queryset
- StudyGroup
- ApplicationDashboard.py
- 0021_user_placeholder_preregistered_flag.py
- parse_permanent_group_code
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
- StudyGroupReadDTO
- test_link_institutes_by_name_simple
- test_study_group_domain.py
- format_validation_errors
- Текущий статус реализации
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
- Role
- ProjectTrackAddApplicationItemSerializer
- ProjectApplicationRepository
- Схема БД: студенческий портал
- Справочные эндпоинты
- .get_daily_dynamics
- Command
- TestInstituteResponsibleQueryPerformance
- StudyGroupSemesterRepository
- TeamEventLogPagination
- .handle
- ProjectRepository
- 0017_copy_studygroup_mentors_to_semester.py
- .get_permissions
- .retrieve
- .update
- .recalculate_recommended_teams_count
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- .add_applications
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
- .get_linked_applications
- project_application.md
- project_activity_server
- 0015_team_sem_enroll_lookup_idx.py
- 0038_alter_team_member_limits_default_4_7.py
- TeamSemesterMember
- TeamLobby.py
- 0018_studygroupsemester_mentors_m2m.py

## God Nodes (most connected - your core abstractions)
1. `make_user()` - 527 edges
2. `User` - 253 edges
3. `ProjectApplication` - 148 edges
4. `Department` - 142 edges
5. `ProjectApplicationService` - 136 edges
6. `Semester` - 132 edges
7. `StudyGroup` - 119 edges
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

## Communities (329 total, 97 thin omitted)

### Community 0 - "MentorTeamService"
Cohesion: 0.07
Nodes (36): MentorTeamAddMemberSerializer, MentorTeamSetCaptainSerializer, MentorTeamUpdateNameSerializer, MentorTeamViewSet, Request, Response, DELETE /study-groups/{groupId}/teams/{teamSemesterId}/ — удалить команду., PATCH /study-groups/{groupId}/teams/{teamSemesterId}/captain/. (+28 more)

### Community 1 - "make_user"
Cohesion: 0.04
Nodes (21): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+13 more)

### Community 2 - "Department"
Cohesion: 0.04
Nodes (63): Command, BaseCommand, Department, Semester, Репозиторий для управления пользователями., Сервис управления пользователями., create_test_user(), Создаем тестового пользователя (+55 more)

### Community 3 - "Ответственный по институту — API для фронта"
Cohesion: 0.08
Nodes (24): 1. Список активных групп института, 2. Сотрудники института, 3. Группы с назначенными наставниками, 4. Назначить наставника группе, 5. Снять наставника с группы, Значения `semester_id`, Общие query-параметры, Ответ `200` (+16 more)

### Community 4 - "ApplicationLoggingService"
Cohesion: 0.09
Nodes (19): ProjectApplicationStatusLog, ApplicationLoggingService, atomic, Логирование удаления причастного пользователя. Args: application: Заявка user:…, Логирование добавления причастного подразделения. Args: application: Заявка…, Логирование удаления причастного подразделения. Args: application: Заявка…, Сервис для логирования изменений в проектных заявках. Обеспечивает полное…, Получение всех логов по заявке. Args: application: Заявка Returns:… (+11 more)

### Community 5 - "accounts/views.py"
Cohesion: 0.06
Nodes (38): RegistrationRequest, Status, AcademicYearSerializer, ApproveRequestSerializer, CustomResetPasswordForm, DepartmentSerializer, Meta, PasswordResetConfirmSerializer (+30 more)

### Community 6 - "action"
Cohesion: 0.13
Nodes (8): action, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, POST /api/project-applications/{id}/approve/ Одобрение заявки, POST /api/project-applications/{id}/reject/ Отклонение заявки, POST /api/project-applications/{id}/request_changes/ Запрос изменений (отправка…, POST /api/project-applications/{id}/transfer_to_institute/ Передача заявки в…, POST /api/project-applications/{id}/return_by_author/ Отзыв заявки автором…, GET /api/project-applications/{id}/status_logs/

### Community 7 - "Any"
Cohesion: 0.04
Nodes (35): ProjectTrackApplicationItemDTO, ProjectTrackGroupDetailDTO, ProjectTrackGroupItemDTO, ProjectTrackGroupProjectDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, ProjectTrackProjectListDTO (+27 more)

### Community 8 - "test_institute_responsible_viewset.py"
Cohesion: 0.23
Nodes (10): api_client(), direction(), other_institute(), APIClient, django_db, fixture, Тесты API ответственного по институтам., semester() (+2 more)

### Community 9 - "TagRepository"
Cohesion: 0.05
Nodes (33): Repository слой для изоляции работы с базой данных. Этот слой содержит все…, Репозиторий для работы с тегами в БД. Изолирует всю работу с базой данных от…, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь., TagRepository, django_db, Unit-тесты для репозитория TagRepository. Проверяем все методы работы с БД:… (+25 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.06
Nodes (28): ApplicationDashboardService, Оркестрация получения данных дашборда заявок., django_db, Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external., Фильтр по группам статусов., Карточка in_work = total - approved - rejected., Среднее и медиана времени до решения. (+20 more)

### Community 11 - "QuerySet"
Cohesion: 0.09
Nodes (18): Q, QuerySet, Базовый queryset заявок с учётом всех фильтров., Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению., Строит карту institute_code -> множество id заявок., Строит карту department_id -> множество id заявок (как в DepartmentPlan). (+10 more)

### Community 12 - "_enrollment_with_mentors"
Cohesion: 0.27
Nodes (5): _enrollment_with_mentors(), APIClient, django_db, TestMentorGroupsQueryPerformance, TestMentorGroupsViewSet

### Community 13 - "._collect_group_rows"
Cohesion: 0.19
Nodes (9): Command, BaseCommand, DataFrame, date, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Дедуплицирует строки по коду постоянной группы., Возвращает направление подготовки, создавая при необходимости. (+1 more)

### Community 14 - "TeamSemester"
Cohesion: 0.02
Nodes (49): Проверяет, что пользователь — капитан команды., Проверяет, что команда принадлежит учебной группе., Новый капитан должен быть участником команды., Нельзя удалить текущего капитана без смены капитана., Запрещает изменения состава при подтверждённом составе., Проверяет, что пользователь — капитан команды., Участие команды в конкретном семестре: проект, наставник, капитан., TeamSemester (+41 more)

### Community 15 - "test_mentor_team_viewset.py"
Cohesion: 0.10
Nodes (25): PlaceholderUserService, atomic, Создаёт и возвращает псевдо-user для предрегистрации., Возвращает существующего или создаёт псевдо-user для предрегистрации. Raises:…, Уникальный внутренний email для псевдо-аккаунта., api_client(), _approved_app(), direction() (+17 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroupMemberDTO"
Cohesion: 0.22
Nodes (5): Any, Карточка наставника учебной группы., Строка списка группы из контингента., StudyGroupMemberDTO, StudyGroupMentorDTO

### Community 18 - "ProjectTrack"
Cohesion: 0.06
Nodes (46): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+38 more)

### Community 19 - "UserManagementService"
Cohesion: 0.09
Nodes (21): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, ViewSet для управления пользователями. (+13 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (28): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationCreateSerializer, ProjectApplicationUpdateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы… (+20 more)

### Community 22 - ".lookup"
Cohesion: 0.29
Nodes (4): PreRegisteredStudentLookupResult, Результат поиска предрегистрации., Сериализует результат для API., Ищет предрегистрацию по одному из идентификаторов. Returns: DTO результата или…

### Community 23 - "ApplicationDashboardRepository"
Cohesion: 0.06
Nodes (27): get_department_subtree_ids(), Утилиты для работы с подразделениями., Возвращает id корневого подразделения и всех его потомков., ApplicationDashboardDomain, DashboardFilters, Доменная логика дашборда проектных заявок., Разворачивает группы статусов в набор кодов., Парсит query-параметр status в кортеж групп. (+19 more)

### Community 24 - "StudyGroupViewSet"
Cohesion: 0.19
Nodes (10): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/my-groups/ — группы наставника в семестре., GET /api/teams/study-groups/{id}/mentor-detail/ — детали группы наставника., GET /api/teams/study-groups/{id}/project-showcase/ — витрина проектов группы., GET /api/teams/study-groups/ — список и просмотр учебных групп. (+2 more)

### Community 25 - "test_student_showcase_viewset.py"
Cohesion: 0.08
Nodes (19): api_client(), _approved_app(), _create_assembled_team(), direction(), other_group(), django_db, fixture, Тесты API студенческой витрины проектов. (+11 more)

### Community 26 - "preregistered_student_service.py"
Cohesion: 0.12
Nodes (17): build_preregistered_student_import_row(), last_names_match(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки. (+9 more)

### Community 27 - "Request"
Cohesion: 0.12
Nodes (17): ApproveJoinRequestSerializer, CreateInvitationSerializer, extend_schema, Request, Response, GET /api/teams/my-team/., GET /api/teams/my-team/event-log/ — пагинированный лог (page_size=50)., DELETE /api/teams/my-team/ — удалить свою команду. (+9 more)

### Community 28 - "TestTeamLobbyViewSet"
Cohesion: 0.14
Nodes (7): _create_captained_team(), django_db, Команда без трека при одном треке у группы → min/max с трека группы., После создания своей команды pending-заявка в чужую → obsolete., При нескольких треках track_id не проставляется; лимиты — effective по трекам., Если группе доступен один трек — он проставляется без track_id в body., TestTeamLobbyViewSet

### Community 29 - "PreRegisteredStudentRepository"
Cohesion: 0.09
Nodes (12): PreRegisteredStudentRepository, QuerySet, Репозиторий предрегистрации студентов., Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета., Возвращает предрегистрацию по табельному номеру., Возвращает предрегистрацию по нормализованному СНИЛС., Возвращает предрегистрацию по первичному ключу. (+4 more)

### Community 30 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "TagCreateDTO"
Cohesion: 0.08
Nodes (19): DTO для создания тега., TagCreateDTO, Тесты для метода create репозитория., Создание общего тега (без departments)., Создание тега с подразделением., Создание тега с несуществующим подразделением вызывает ошибку., Нельзя создать тег с таким же именем и таким же набором подразделений., Можно создать тег с таким же именем, но другим набором подразделений. (+11 more)

### Community 33 - "ProjectTrackService"
Cohesion: 0.04
Nodes (46): ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackAggregatedStatisticsDTO, ProjectTrackCreateDTO, ProjectTrackReadDTO, ProjectTrackUpdateDTO, DTO для проектных треков. (+38 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.09
Nodes (30): ProjectTrackAddApplicationsSerializer, ProjectTrackAddGroupsSerializer, ProjectTrackCreateSerializer, ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request (+22 more)

### Community 35 - "TestTagViewSetCreate"
Cohesion: 0.05
Nodes (25): django_db, Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем. (+17 more)

### Community 36 - "TestTagViewSet"
Cohesion: 0.10
Nodes (11): Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Теги отсортированы по категории и названию., GET /api/tags/{id}/ возвращает конкретный тег., GET /api/tags/{id}/ для несуществующего тега возвращает 404 (DRF-level). (+3 more)

### Community 37 - "ProjectService"
Cohesion: 0.12
Nodes (10): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией., ProjectService, Оркестрация Domain + Repository для списка проектов., TestProjectApplicationNewFieldsLists (+2 more)

### Community 38 - "ProjectApplicationService"
Cohesion: 0.03
Nodes (68): ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка., django_db, patch, Ошибки валидации института: несуществующий код или отсутствие связанного…, Нет причастности подразделения — матрица запрещает действие, ожидаем… (+60 more)

### Community 39 - "StudentShowcaseDomain"
Cohesion: 0.06
Nodes (30): Правила доступа и записи команды на проект витрины., Запись на проект доступна только при подтверждённом составе., Запрещает повторную запись / смену проекта., Проект должен принадлежать треку команды., Число участников должно укладываться в лимиты проекта., Жёсткий лимит числа команд на проект., True, если капитан может записать команду на проект (для UI)., StudentShowcaseDomain (+22 more)

### Community 40 - "PreRegisteredStudent"
Cohesion: 0.14
Nodes (15): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., MonkeyPatch, api_client(), pre_registered_student(), Any, APIClient, django_db (+7 more)

### Community 41 - ".update_application"
Cohesion: 0.17
Nodes (8): Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Не-автор и не-ЦПДС не может редактировать заявку., Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult., CPDS может редактировать одобренные заявки., institute_validator-автор: save совпадает с available_actions (подразделение…, TestUpdateApplication

### Community 42 - ".calculate_initial_status"
Cohesion: 0.17
Nodes (9): Определение начального статуса на основе роли пользователя. Чистая функция -…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds., Обычный пользователь создаёт заявки в статусе await_department., Неизвестная роль возвращает статус await_department по умолчанию. (+1 more)

### Community 43 - "Tag"
Cohesion: 0.08
Nodes (15): Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, Теги для проектных заявок, Tag, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален, Создание тега в БД. Args: dto: DTO с данными для создания тега Returns:…, Получение тега по ID с оптимизацией запросов. Args: tag_id: ID тега Returns:…, Обновление тега. Обновляет только переданные поля. Args: tag: Тег для… (+7 more)

### Community 44 - "CommentService"
Cohesion: 0.10
Nodes (17): CommentService, atomic, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db, Пустой текст вызывает ValueError., Тесты для CommentService. (+9 more)

### Community 45 - "Path"
Cohesion: 0.28
Nodes (4): Any, django_db, Path, TestImportStudyGroupsFromContingentCommand

### Community 46 - "dto/institute_responsible.py"
Cohesion: 0.11
Nodes (10): InstituteResponsibleAssignMentorDTO, InstituteResponsibleEmployeeDTO, InstituteResponsibleGroupDTO, InstituteResponsibleMentorDTO, Any, DTO для API ответственного по институтам., Компактное представление учебной группы., Сотрудник института (id + ФИО). (+2 more)

### Community 47 - "study_group_import.py"
Cohesion: 0.17
Nodes (12): build_group_import_row(), build_group_name(), GroupImportRow, parse_direction_level(), Чистая логика импорта учебных групп из отчёта контингента 1С., Собирает отображаемое название группы, например «АМБ-211»., Возвращает код института по полному названию из отчёта 1С. Raises: ValueError:…, Нормализует уровень подготовки из отчёта. Raises: ValueError: если уровень не… (+4 more)

### Community 48 - "SemesterViewSet"
Cohesion: 0.29
Nodes (4): extend_schema, ViewSet для операций над семестрами, связанных с проектными заявками., POST /api/semesters/{id}/assign-empty-applications Присваивает переданный…, SemesterViewSet

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+2 more)

### Community 50 - "TagViewSet"
Cohesion: 0.10
Nodes (22): Разрешает доступ к управлению тегами только для ролей cpds, admin и…, TagManagePermission, Инициализация из модели Tag., TagReadDTO, DepartmentAttachDetachSerializer, action, Request, Response (+14 more)

### Community 51 - "TeamSemesterViewSet"
Cohesion: 0.24
Nodes (8): action, Request, Response, POST /api/teams/team-semesters/{id}/members/ — добавить участника., DELETE /api/teams/team-semesters/{id}/members/{member_id}/., CRUD для участия команды в семестре и управления составом., GET /api/teams/team-semesters/my/?semester_id= — команды пользователя., TeamSemesterViewSet

### Community 52 - "DirectionService"
Cohesion: 0.16
Nodes (10): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений., DirectionService, Оркестрация Domain + Repository для Direction., Список направлений с фильтрацией по роли., Направление по коду с проверкой доступа. (+2 more)

### Community 53 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 54 - "TestStudyGroupImportDomain"
Cohesion: 0.18
Nodes (8): calculate_course_number(), group_ended_by_planned_dates(), parse_planned_end_date(), date, Возвращает True, если у группы есть хотя бы одна дата окончания и все они…, Рассчитывает номер курса на текущий учебный год и семестр., Парсит дату планового окончания из ячейки отчёта 1С., TestStudyGroupImportDomain

### Community 55 - "TestProjectViewSet"
Cohesion: 0.18
Nodes (4): _create_approved_app(), django_db, ЦПДС в причастных не должно подменять основное подразделение проекта., TestProjectViewSet

### Community 56 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 57 - "TestProjectApplicationReadDTO"
Cohesion: 0.09
Nodes (13): Exception, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None., target_institutes сериализуется как список словарей с code и name., tags сериализуется как список словарей с id, name и category., involved_users сериализуется с данными пользователя, added_at и added_by. (+5 more)

### Community 58 - "accounts/permissions.py"
Cohesion: 0.06
Nodes (34): DenyStudentPermission, IsAdminOrCpds, IsCpdsUser, IsInstituteValidator, ProjectManagementPermission, ProjectTrackPermission, APIView, BasePermission (+26 more)

### Community 59 - "PreRegisteredStudentService"
Cohesion: 0.09
Nodes (24): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Отправляет администратору письмо о расхождении данных., Публичные операции предрегистрации студентов. (+16 more)

### Community 60 - "showcase/urls.py"
Cohesion: 0.14
Nodes (13): ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для…, Сериализатор для отображения (чтения) статусов заявок на проекты. Используется…, InstituteSerializer (+5 more)

### Community 61 - "TestProjectTrackDomain"
Cohesion: 0.13
Nodes (7): Код роли пользователя., Проверяет, может ли пользователь управлять проектными треками., Коды институтов пользователя; None — без ограничения (admin/cpds)., True для admin/cpds/staff — статистика без institute_code., Определяет код института: из параметра или по умолчанию для validator., django_db, TestProjectTrackDomain

### Community 62 - "TagUpdateDTO"
Cohesion: 0.14
Nodes (11): DTO для обновления тега., TagUpdateDTO, Тесты для метода update_tag сервиса., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+3 more)

### Community 63 - "UserType"
Cohesion: 0.20
Nodes (10): atomic, UserType, Студент отклоняет приглашение., Возвращает команду капитана или бросает ошибку., Капитан одобряет заявку и назначает роль., Капитан отклоняет заявку., Капитан приглашает одногруппника., Капитан удаляет участника. (+2 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 65 - "Any"
Cohesion: 0.12
Nodes (10): Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Преобразование в словарь., Сериализатор для создания тега., Преобразование в DTO., Сериализатор для обновления тега., Преобразование в DTO. (+2 more)

### Community 66 - "TeamLobbyDomain"
Cohesion: 0.04
Nodes (43): Доменная логика студенческой витрины проектов., Доменные правила лобби формирования команд., Удаление: капитан, forming, в составе только он., Подтверждение состава: капитан, forming, размер в лимитах трека., Заявка должна быть в статусе pending., Приглашение должно быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды»., Лимиты размера команды. Приоритет: 1) трек команды; 2) effective по трекам… (+35 more)

### Community 67 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 68 - "UserManagementDomain"
Cohesion: 0.11
Nodes (12): QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., Правила доступа и валидации для управления пользователями., Проверяет, может ли пользователь просматривать список пользователей., Проверяет, может ли пользователь изменять пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., UserManagementDomain (+4 more)

### Community 69 - "Settings"
Cohesion: 0.09
Nodes (21): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+13 more)

### Community 70 - "mentor_team_service.py"
Cohesion: 0.04
Nodes (42): ViewSet студенческой витрины проектов., Сервис студенческой витрины проектов., Оркестрация Domain + Repository для студенческой витрины., StudentShowcaseService, MentorGroupsDomain, Доменная логика доступа наставника к учебной группе., Проверяет, что учебная группа существует., Проверяет, что учебная группа не завершила обучение. (+34 more)

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
Nodes (12): ProjectTrackRepository, Создаёт проектный трек., Обновляет поля трека., Удаляет группу из трека; True если связь была., Возвращает id заявок, уже привязанных к треку., Удаляет заявку из трека; True если связь была., Количество групп в треке., Доступ к данным проектных треков. (+4 more)

### Community 75 - ".view_application"
Cohesion: 0.25
Nodes (5): Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Автор всегда имеет доступ к просмотру своей заявки., Обычному пользователю чужая заявка недоступна., Список заявок разрешён всем (возвращает True)., TestViewAndList

### Community 76 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

### Community 77 - "TestApplicationDashboardViewSet"
Cohesion: 0.13
Nodes (9): django_db, Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400., Обычный пользователь — 403., Админ получает полную структуру дашборда., API: фильтр department_id включает дочернее подразделение. (+1 more)

### Community 78 - "dto/mentor_team.py"
Cohesion: 0.24
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
Cohesion: 0.08
Nodes (17): Разбор query-параметра semester_id для GET-списков: id, next, actual., ProjectTrackGroupListDTO, DTO группы со счётчиком назначенных проектов., Преобразует DTO в словарь для API., QuerySet, UserType, Список треков по фильтрам., Список групп института со счётчиком назначенных проектов. (+9 more)

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "Управление командой"
Cohesion: 0.08
Nodes (24): Query-параметры, Query-параметры, Query-параметры, Вернуть состав на редактирование, Витрина проектов, Детали группы наставника, Добавить участника, Карточка команды (+16 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.12
Nodes (13): ApplicationCapabilities, Any, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы., Возвращает список доступных действий согласно матрице. (+5 more)

### Community 90 - "User"
Cohesion: 0.03
Nodes (58): AbstractBaseUser, User, QuerySet, Подгружает parent подразделения для корректного resolve институтов., Список пользователей с учётом роли запрашивающего., Возвращает пользователя, если он доступен запрашивающему., Частичное обновление пользователя., check_and_fix_user() (+50 more)

### Community 91 - "dto/student_showcase.py"
Cohesion: 0.07
Nodes (22): Any, DTO студенческой витрины проектов., Результат записи команды на проект., Преобразует DTO в словарь для API., Карточка проекта в списке трека витрины., Преобразует DTO в словарь для API., Трек с вложенными проектами для витрины., Преобразует DTO в словарь для API. (+14 more)

### Community 92 - "TestInstituteResponsibleViewSet"
Cohesion: 0.14
Nodes (3): _enrollment_with_mentors(), Создаёт запись группы в семестре с наставниками., TestInstituteResponsibleViewSet

### Community 93 - "test_mentor_group_detail_viewset.py"
Cohesion: 0.06
Nodes (33): MentorGroupDetailDTO, MentorGroupListDTO, MentorGroupListItemDTO, MentorGroupStudentDTO, MentorGroupTeamDTO, Any, DTO для эндпоинта «Мои группы» наставника., Строка списка групп наставника. (+25 more)

### Community 94 - ".get_filtered_queryset"
Cohesion: 0.15
Nodes (10): DirectionDomain, QuerySet, Фильтрация направлений по роли пользователя., Фильтрует направления: institute_validator — только из групп своего института., django_db, parametrize, Разрешение институтов по подразделению пользователя., Фильтрация queryset направлений по ролям. (+2 more)

### Community 95 - "TestLogStatusChange"
Cohesion: 0.12
Nodes (9): Первый переход (from_status=None) помечает заявку, если актор не автор., Логирование с указанием предыдущего лога для создания цепочки., Тесты для log_status_change., Если application равен None, выбрасывается ValueError., Успешное логирование изменения статуса (не автор — флаг выставляется)., Если to_status равен None, выбрасывается ValueError., Смена статуса автором не помечает заявку для самого автора., Одинаковый from/to статус не помечает заявку как изменённую. (+1 more)

### Community 96 - "UserSerializer"
Cohesion: 0.15
Nodes (11): Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., UserSerializer, CustomTokenObtainPairSerializer (+3 more)

### Community 97 - "InstituteResponsibleViewSet"
Cohesion: 0.26
Nodes (12): delete, InstituteResponsibleViewSet, action, extend_schema, Request, Response, GET /api/teams/institute-responsible/employees/., GET /api/teams/institute-responsible/group-mentors/. (+4 more)

### Community 98 - "TestCanEditApplication"
Cohesion: 0.12
Nodes (9): Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку., Не-автор и не-ЦПДС не может редактировать чужую заявку., Нельзя редактировать заявки со статусом rejected (даже автору и cpds)., Нельзя редактировать одобренные заявки (кроме админов и cpds)., Автор может редактировать заявку в статусе returned_*., institute_validator без причастного подразделения не может сохранить., CPDS может редактировать заявки в статусе rejected_department. (+1 more)

### Community 99 - "TestProjectApplicationViewSetTransferToInstitute"
Cohesion: 0.17
Nodes (8): Тесты для действия передачи заявки в институт по коду института., POST /api/showcase/project-applications/{id}/transfer_to_institute/ с…, Отсутствующий параметр code возвращает 400., Несуществующий код института возвращает 400 от сервиса., Институт без связанного подразделения возвращает 400., GET /api/showcase/project-applications/external/?status=... фильтрует внешние…, GET /api/showcase/project-applications/external/?status=... с несуществующим…, TestProjectApplicationViewSetTransferToInstitute

### Community 100 - "UserRepository"
Cohesion: 0.20
Nodes (7): QuerySet, Доступ к данным пользователей для управления., Базовый queryset без администраторов., Список пользователей с оптимизацией запросов., Возвращает пользователя по ID., Сохраняет изменения пользователя., UserRepository

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - "ProjectApplication"
Cohesion: 0.05
Nodes (33): get_root_department(), Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, ProjectListDTO, Any, DTO для списка проектов., DTO для списка проектов., Возвращает причастное подразделение верхнего уровня (без родителя). ЦПДС…, ApplicationInvolvedUser (+25 more)

### Community 103 - "API Документация - Проектные заявки"
Cohesion: 0.18
Nodes (9): API Документация - Проектные заявки, Аутентификация, Базовый URL, Валидационные правила, Общая информация, Обязательные поля, Обязательные поля:, Типы данных (+1 more)

### Community 104 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

### Community 105 - "TeamLobbyService"
Cohesion: 0.13
Nodes (12): QuerySet, Создаёт команду студента. Если track_id не передан и группе доступен ровно один…, Студент подаёт заявку на вступление., Студент принимает приглашение., Оркестрация Domain + Repository для студенческого лобби., Queryset лога «Моей команды» (новые сверху); 404 если нет команды., Резолвит semester_id; по умолчанию actual., Лимиты команды: свой трек → effective по трекам группы → дефолты. (+4 more)

### Community 106 - ".get_dashboard"
Cohesion: 0.17
Nodes (9): ApplicationDashboardDTO, Any, DTO для дашборда проектных заявок., Преобразует DTO в словарь для API., DTO блока KPI-карточек., DTO полного ответа дашборда., Преобразует DTO в словарь для API., SummaryCardsDTO (+1 more)

### Community 107 - "TestApproveRejectRequest"
Cohesion: 0.27
Nodes (6): parametrize, Матрица прав определяет доступность reject., Для returned_* действует агрегирующее правило returned_(all)., Отзыв доступен только автору и не для финальных approved/rejected., Матрица прав определяет доступность approve для ролей и статусов., TestApproveRejectRequest

### Community 108 - "ApplicationNotificationService"
Cohesion: 0.19
Nodes (8): ApplicationNotificationService, Отправка писем автору при отклонении и отправке на доработку., Email получателя: author_email заявки или email связанного пользователя-автора., Письмо автору: заявка отправлена на доработку., Письмо автору: заявка отклонена., django_db, patch, TestApplicationNotificationService

### Community 109 - "TestProjectApplicationListSemesterFilter"
Cohesion: 0.07
Nodes (17): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, Фильтр ?semester_id= в GET-списке заявок., Автоподстановка семестра при создании заявки. (+9 more)

### Community 110 - ".validate_create"
Cohesion: 0.12
Nodes (13): Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Носитель проблемы короче 5 символов вызывает ошибку., Барьер короче 10 символов вызывает ошибку., Имя и фамилия автора короче 2 символов вызывают ошибки., Тесты для валидации при создании заявки., Телефон короче 10 символов вызывает ошибку., Валидный DTO проходит проверку без ошибок., Все ошибки валидации собираются в одном результате. (+5 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 113 - "TestGetLogs"
Cohesion: 0.06
Nodes (20): django_db, Тесты для логирования причастных пользователей., Логирование добавления причастного пользователя., Проверка валидации при добавлении причастного пользователя., Логирование удаления причастного пользователя., Тесты для получения логов., Получение всех логов по заявке., Если application равен None, выбрасывается ValueError. (+12 more)

### Community 114 - "is_cpds_department"
Cohesion: 0.12
Nodes (12): is_cpds_department(), Проверяет, что подразделение — ЦПДС (координирующее, не основное)., django_db, Unit-тесты для утилит работы с подразделениями., Тесты для функции get_root_department., Подразделение без parent возвращает само себя., Подразделение с одним уровнем parent возвращает корневое., Подразделение с несколькими уровнями parent возвращает корневое. (+4 more)

### Community 115 - "._resolve_context"
Cohesion: 0.17
Nodes (8): Any, Список активных групп института., Список сотрудников института., Группы с ID назначенных наставников в семестре., Назначает наставника группе в семестре., Снимает наставника с группы в семестре., Валидирует доступ и возвращает semester_id, institute_code, accessible_codes., Возвращает группу после проверки доступа.

### Community 116 - ".post"
Cohesion: 0.24
Nodes (7): LoginView, extend_schema, Request, Response, Сменяет пароль текущего пользователя после проверки текущего пароля., Получение JWT токена по email и паролю., TokenObtainPairView

### Community 117 - "institute_access.py"
Cohesion: 0.08
Nodes (31): Доменная логика управления пользователями., ID подразделений для фильтрации; None — без ограничения., Доменная логика для списка проектов., ProjectTrackDomain, Доменная логика для проектных треков., Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., Правила доступа и валидации для проектных треков. (+23 more)

### Community 118 - "TestProjectApplicationListDTO"
Cohesion: 0.13
Nodes (9): django_db, Тесты для ProjectApplicationListDTO., Базовые поля DTO для списка заполняются из модели., Если статус None, DTO.status тоже None., to_dict преобразует DTO в словарь с ISO форматированием даты., is_internal_customer включается в ProjectApplicationListDTO., Новые поля трека включаются в ProjectApplicationListDTO., is_internal_customer включается в ProjectApplicationReadDTO. (+1 more)

### Community 119 - "TestMyTeamViewSet"
Cohesion: 0.12
Nodes (5): django_db, Без трека у команды, но один трек у группы → лимиты с трека группы., Без трека у команды и >1 трека у группы → effective max(min)/min(max)., Число запросов GET /my-team/ не растёт с числом заявок/приглашений., TestMyTeamViewSet

### Community 120 - "TeamLobbyViewSet"
Cohesion: 0.18
Nodes (10): CreateTeamSerializer, action, extend_schema_view, POST /api/teams/lobby/teams/{id}/join-requests/., POST /api/teams/lobby/invitations/{id}/accept/., POST /api/teams/lobby/invitations/{id}/reject/., Создание команды в лобби., Студенческое лобби: треки, команды, заявки, приглашения. (+2 more)

### Community 121 - "StudentShowcaseViewSet"
Cohesion: 0.23
Nodes (10): action, extend_schema, extend_schema_view, Request, Response, Студенческая витрина: треки, детали проекта, запись команды., GET /api/showcase/student-showcase/., GET /api/showcase/student-showcase/projects/{id}/. (+2 more)

### Community 122 - "InstituteResponsibleService"
Cohesion: 0.17
Nodes (8): InstituteResponsibleDomain, Правила доступа и валидации для ответственного по институтам., Проверяет, может ли пользователь работать с API ответственного., Определяет код института из параметра или по умолчанию., ID подразделений института для фильтрации сотрудников., Подгружает parent подразделения для resolve институтов., InstituteResponsibleService, Оркестрация назначения наставников группам по семестрам.

### Community 123 - "Поддержка multipart/form-data"
Cohesion: 0.33
Nodes (6): Допустимые форматы файлов, Заголовки, Загрузка файлов, Максимальный размер файла, Поддержка multipart/form-data, Тело запроса

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
Cohesion: 0.04
Nodes (53): create_test_applications(), Создаем тестовые заявки, Общие константы приложения showcase., ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Определение необходимости консультации на основе данных заявки. Чистая функция… (+45 more)

### Community 133 - "0014_add_intermediate_approved_statuses.py"
Cohesion: 0.33
Nodes (5): add_intermediate_approved_statuses(), Migration, Удаляет промежуточные статусы одобрения из БД., Добавляет промежуточные статусы одобрения в БД., remove_intermediate_approved_statuses()

### Community 134 - "TestDepartmentPlanViewSetMyDepartmentPlan"
Cohesion: 0.13
Nodes (9): django_db, Тесты для GET /api/showcase/department-plans/my-department-plan/ - план…, Успешное получение плана и статистики для подразделения пользователя., Если план отсутствует, возвращается 0, но статистика заявок учитывается., Ошибка: отсутствует semester_id., Ошибка: семестр не найден., Ошибка: у пользователя не указано подразделение., Ошибка: неавторизованный пользователь. (+1 more)

### Community 135 - "StudyGroupService"
Cohesion: 0.19
Nodes (6): Оркестрация Domain + Repository для StudyGroup., StudyGroupService, django_db, TestMyStudyGroupService, django_db, TestStudyGroupService

### Community 136 - "Руководство по ручному развертыванию Project Activity Server"
Cohesion: 0.15
Nodes (12): 10. Проверка и сопровождение, 11. Настройка nginx (backend + SPA), 1. Подготовка окружения, 2. Получение исходного кода, 3. Создание и активация виртуального окружения, 4. Настройка переменных окружения (.env), 5. Настройка PostgreSQL, 6. Миграции и статические файлы (+4 more)

### Community 137 - "4. Список проектов"
Cohesion: 0.29
Nodes (7): 4. Список проектов, Query-параметры, Заголовки, Ошибки, Поведение по ролям, Примеры запросов, Успешный ответ (200)

### Community 138 - "ProjectApplicationViewSet"
Cohesion: 0.11
Nodes (15): get_error_message(), ProjectApplicationViewSet, GET /api/project-applications/external/ Получение списка всех внешних заявок…, Возвращает сообщение об ошибке в зависимости от режима DEBUG. Args: exception:…, Упрощенный ViewSet - только обработка HTTP запросов. Вся бизнес-логика вынесена…, DELETE отключён: заявки не удаляются через API., Выбор сериализатора в зависимости от действия, Возвращает QuerySet для списка заявок. DRF автоматически применит пагинацию. (+7 more)

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

### Community 149 - "fixture"
Cohesion: 0.18
Nodes (10): institute(), fixture, Возвращает класс модели пользователя для удобства., Создаёт набор ролей, используемых в тестах. Возвращает dict: code -> Role, Создаёт все необходимые статусы для сценариев сервисов., Создаёт институт, связанный с родительским подразделением., roles(), statuses() (+2 more)

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

### Community 156 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.24
Nodes (10): aga_institute(), direction(), fixture, Тесты импорта учебных групп из контингента 1С., Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта., Институт АГА для тестового импорта., Создаёт минимальный отчёт контингента для тестов. (+2 more)

### Community 157 - "teams/admin.py"
Cohesion: 0.12
Nodes (17): Репозиторий студенческой витрины проектов (без N+1)., DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin (+9 more)

### Community 159 - "test_import_preregistered_students.py"
Cohesion: 0.19
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 164 - "test_study_group_viewset.py"
Cohesion: 0.47
Nodes (5): direction(), other_institute(), fixture, Тесты StudyGroupViewSet., study_groups()

### Community 165 - ".get_filtered_queryset"
Cohesion: 0.29
Nodes (4): QuerySet, institute_validator — только группы своих институтов., parametrize, TestStudyGroupGetFilteredQueryset

### Community 166 - "test_team_lobby_viewset.py"
Cohesion: 0.33
Nodes (9): api_client(), _approved_app(), direction(), lobby_setup(), fixture, Тесты API лобби формирования команд., semester(), study_group() (+1 more)

### Community 170 - ".can_access_track"
Cohesion: 0.25
Nodes (3): Проверяет доступ к конкретному треку., ID подразделений, доступных пользователю; None — без ограничения., Проверяет доступ к подразделению.

### Community 189 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Возвращает проектную заявку по id или None., Q-фильтр: заявка доступна институту по involved/target institutes., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 190 - "QuerySet"
Cohesion: 0.18
Nodes (6): QuerySet, Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки.

### Community 191 - ".submit_application"
Cohesion: 0.32
Nodes (4): Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, Проверяем, что валидный DTO проходит валидацию без ошибок., Невалидные поля аккумулируют ошибки в ValidationResult., TestSubmitApplication

### Community 192 - "test_export_import_departments_roundtrip"
Cohesion: 0.27
Nodes (10): Any, django_db, Экспорт и последующий импорт институтов восстанавливают данные., Экспорт и последующий импорт подразделений восстанавливают данные., Импорт институтов удаляет те, которых нет в файле., Импорт подразделений удаляет те, которых нет в файле., test_export_import_departments_roundtrip(), test_export_import_institutes_roundtrip() (+2 more)

### Community 193 - "PasswordChangeSerializer"
Cohesion: 0.29
Nodes (4): PasswordChangeSerializer, Any, Возвращает учебную группу пользователя или None., Сериализатор для смены пароля аутентифицированного пользователя.

### Community 194 - "._department_to_dict"
Cohesion: 0.25
Nodes (4): Возвращает кэшированную карту department_id -> institute.code., Строит карту department_id -> institute.code без N+1., Топ самых старых заявок в статусе «В работе»., Преобразует подразделение в JSON-совместимый объект для API.

### Community 195 - "InstituteResponsibleGroupMentorsDTO"
Cohesion: 0.29
Nodes (4): InstituteResponsibleGroupMentorsDTO, InstituteResponsibleGroupWithMentorDTO, Учебная группа с ID назначенных наставников в семестре., Ответ: группы с назначениями наставников.

### Community 196 - "InstituteResponsible.py"
Cohesion: 0.25
Nodes (6): AssignMentorSerializer, InstituteResponsiblePermission, BasePermission, ViewSet API ответственного по институтам., Тело запроса на назначение наставника., Доступ для institute_validator, admin и cpds.

### Community 197 - ".validate_group_institute_codes"
Cohesion: 0.29
Nodes (3): Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет доступ к учебной группе.

### Community 198 - "Command"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Сбрасывает счетчик ID для таблицы тегов.

### Community 199 - "ProjectApplicationComment"
Cohesion: 0.40
Nodes (3): ProjectApplicationComment, Сервис для управления комментариями к проектным заявкам. Обеспечивает…, Unit-тесты для CommentService. Проверяем добавление комментариев, получение…

### Community 200 - "TagService"
Cohesion: 0.06
Nodes (31): Чистая бизнес-логика для тегов - только функции, никаких эффектов., TagDomain, DTO для работы с тегами., DepartmentNestedSerializer, Meta, Вложенный сериализатор для подразделения., Сериализатор для тегов., TagSerializer (+23 more)

### Community 201 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 202 - "StudyGroup"
Cohesion: 0.04
Nodes (57): Доменная логика для учебных групп., DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., MyStudyGroupDTO, DTO для эндпоинта «Моя группа»., Возвращает наставников: из семестра или fallback на StudyGroup.mentor. (+49 more)

### Community 203 - "ApplicationDashboard.py"
Cohesion: 0.20
Nodes (7): ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 205 - "parse_permanent_group_code"
Cohesion: 0.33
Nodes (4): parse_permanent_group_code(), ParsedPermanentGroup, Разбирает код постоянной группы вида «АМБ-2025-11» или «ОММ-2022-11-1». Raises:…, Разобранный код постоянной группы.

### Community 206 - "1. Создание заявки (авторизованные пользователи)"
Cohesion: 0.33
Nodes (6): 1. Создание заявки (авторизованные пользователи), Заголовки, Пример запроса, Тело запроса, Успешный ответ (201), Эндпоинты создания заявок

### Community 240 - "StudyGroupReadDTO"
Cohesion: 0.33
Nodes (3): Any, DTO для чтения учебной группы., StudyGroupReadDTO

### Community 241 - "test_link_institutes_by_name_simple"
Cohesion: 0.40
Nodes (6): Any, django_db, Простейший сценарий: для каждого института есть одноимённое подразделение., Институты без одноимённого подразделения остаются без связанного подразделения., test_link_institutes_by_name_simple(), test_link_institutes_without_matching_department()

### Community 242 - "test_study_group_domain.py"
Cohesion: 0.47
Nodes (5): direction(), other_institute(), fixture, Тесты доменной логики StudyGroupDomain., study_groups()

### Community 243 - "format_validation_errors"
Cohesion: 0.33
Nodes (4): format_validation_errors(), POST /api/project-applications/ Создание заявки - только обработка HTTP, Форматирует ошибки валидации используя стандартные DRF механизмы. Args: errors:…, POST /api/project-applications/simple/ Создание заявки без авторизации

### Community 244 - "Текущий статус реализации"
Cohesion: 0.40
Nodes (5): ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации, 🔧 Требует доработки

### Community 245 - "TestProjectApplicationNewFieldsCreateUpdate"
Cohesion: 0.27
Nodes (4): _base_create_payload(), django_db, TestMyApplicationsNewFields, TestProjectApplicationNewFieldsCreateUpdate

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 278 - "Role"
Cohesion: 0.14
Nodes (8): Command, BaseCommand, Role, UserManager, Создание псевдо-аккаунтов для незарегистрированных студентов контингента., BaseUserManager, Command, BaseCommand

### Community 279 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 280 - "ProjectApplicationRepository"
Cohesion: 0.02
Nodes (59): ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты…, Получение заявки по ID без дополнительных связанных объектов. Для простых…, Получение заявок пользователя, где он является автором. Оптимизированный запрос…, Получение заявок для координации пользователя. Заявки, где пользователь…, Репозиторий - вся работа с БД здесь, Получение заявок для координации по причастному подразделению. Заявки, где…, Получение заявок по статусу. Для административных операций. (+51 more)

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 292 - "Command"
Cohesion: 0.12
Nodes (7): Код текущего активного семестра (Settings.active_semester_code)., Текущий активный семестр (Settings.active_semester_code)., Следующий семестр для новых заявок (Settings.next_semester_code)., Command, BaseCommand, Добавляет причастные подразделения института к заявке., Создание заявки в БД. Принимает DTO и пользователя, возвращает созданную…

### Community 294 - "StudyGroupSemesterRepository"
Cohesion: 0.13
Nodes (12): QuerySet, Снимает наставника с группы в семестре; возвращает актуальные mentorIds., Возвращает отсортированные ID наставников группы в семестре., Доступ к данным групп в семестре и сотрудников института., Активные группы института., Активные группы с prefetch наставников в семестре., Возвращает группу по ID или None., Сотрудники института (не студенты, не админы, не staff). (+4 more)

### Community 295 - "TeamEventLogPagination"
Cohesion: 0.67
Nodes (3): PageNumberPagination, Пагинация ленты событий команды (фиксированный page_size=50)., TeamEventLogPagination

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

### Community 329 - "TeamSemesterMember"
Cohesion: 0.09
Nodes (25): Постоянная команда участников проектной деятельности., Участник команды в конкретном семестре., Role, Team, TeamSemesterMember, Репозиторий управления командой наставником., Репозиторий лобби формирования команд (без N+1)., api_client() (+17 more)

### Community 331 - "TeamLobby.py"
Cohesion: 0.09
Nodes (26): MyTeamViewSet, API лобби формирования команд и «Моей команды»., Раздел «Моя команда» для капитана и участника., _is_staff_or_admin(), APIView, BasePermission, Request, Разрешения для приложения teams. (+18 more)

## Knowledge Gaps
- **263 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+258 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **97 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `MentorTeamService`, `Department`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `ApplicationLoggingService`, `Any`, `StudyGroupService`, `ApplicationDashboardService`, `TeamSemester`, `test_mentor_team_viewset.py`, `StudyGroupMemberDTO`, `UserManagementService`, `ApplicationDashboardRepository`, `ProjectApplicationRepository`, `ProjectTrackService`, `Command`, `.get_filtered_queryset`, `StudyGroupSemesterRepository`, `StudentShowcaseDomain`, `.can_access_track`, `Tag`, `CommentService`, `dto/institute_responsible.py`, `TestCanUpdateTag`, `TagViewSet`, `DirectionService`, `accounts/permissions.py`, `TestProjectTrackDomain`, `PasswordChangeSerializer`, `TeamLobbyDomain`, `UserManagementDomain`, `Settings`, `mentor_team_service.py`, `TagService`, `.get_filtered_queryset`, `StudyGroup`, `TeamLobby.py`, `TestCanCreateTag`, `TestCanDeleteTag`, `.resolve_list_semester_id`, `test_mentor_group_detail_viewset.py`, `.get_filtered_queryset`, `UserSerializer`, `UserRepository`, `ProjectApplication`, `TeamLobbyService`, `.get_dashboard`, `._resolve_context`, `institute_access.py`, `InstituteResponsibleService`, `StudyGroupDomain`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Why does `make_user()` connect `make_user` to `Department`, `ProjectApplicationCreateDTO`, `ApplicationLoggingService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `StudyGroupService`, `test_institute_responsible_viewset.py`, `ApplicationDashboardService`, `_enrollment_with_mentors`, `test_mentor_team_viewset.py`, `ProjectTrack`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `fixture`, `test_mentor_showcase_viewset.py`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `TestProjectApplicationViewSetIsInternalCustomer`, `test_import_preregistered_students.py`, `TagCreateDTO`, `ProjectTrackService`, `TestTagViewSetCreate`, `TestTagViewSet`, `ProjectService`, `ProjectApplicationService`, `TestInstituteResponsibleQueryPerformance`, `PreRegisteredStudent`, `.get_filtered_queryset`, `.can_access_track`, `test_team_lobby_viewset.py`, `CommentService`, `dto/institute_responsible.py`, `TestCanUpdateTag`, `DirectionService`, `TestDepartmentPlanViewSetList`, `TestProjectViewSet`, `TestProjectApplicationReadDTO`, `TestProjectTrackDomain`, `TagUpdateDTO`, `UserManagementDomain`, `.get_filtered_queryset`, `TagService`, `StudyGroup`, `TeamSemesterMember`, `TestApplicationDashboardViewSet`, `TestCanCreateTag`, `TestCanDeleteTag`, `TestInstituteResponsibleViewSet`, `test_mentor_group_detail_viewset.py`, `.get_filtered_queryset`, `TestLogStatusChange`, `TestProjectApplicationViewSetTransferToInstitute`, `ApplicationNotificationService`, `TestProjectApplicationListSemesterFilter`, `TestMyStudyGroupViewSet`, `TestGetLogs`, `TestProjectApplicationNewFieldsCreateUpdate`, `TestProjectApplicationListDTO`, `StudyGroupDomain`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Why does `Semester` connect `Department` to `MentorTeamService`, `make_user`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `StudyGroupService`, `test_institute_responsible_viewset.py`, `ProjectApplicationViewSet`, `ApplicationDashboardService`, `_enrollment_with_mentors`, `test_mentor_team_viewset.py`, `ProjectTrack`, `UserManagementService`, `TestDepartmentPlanViewSetCreate`, `test_mentor_showcase_viewset.py`, `ApplicationDashboardRepository`, `ProjectApplicationRepository`, `test_student_showcase_viewset.py`, `ProjectTrackService`, `Command`, `ProjectService`, `ProjectApplicationService`, `test_team_lobby_viewset.py`, `study_group_import.py`, `TeamSemesterViewSet`, `TestDepartmentPlanViewSetList`, `TestStudyGroupImportDomain`, `TestProjectViewSet`, `TeamLobbyDomain`, `Settings`, `mentor_team_service.py`, `DepartmentPlanViewSet`, `StudyGroup`, `TeamLobby.py`, `TeamSemesterMember`, `AccountsApiTests`, `.resolve_list_semester_id`, `TestInstituteResponsibleViewSet`, `test_mentor_group_detail_viewset.py`, `ProjectApplication`, `TeamLobbyService`, `TestProjectApplicationListSemesterFilter`, `TestMyStudyGroupViewSet`, `institute_access.py`, `TestProjectApplicationNewFieldsCreateUpdate`, `InstituteResponsibleService`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 524 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 524 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 74 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 74 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._