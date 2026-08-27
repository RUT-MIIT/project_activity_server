# Graph Report - project_activity_server  (2026-08-26)

## Corpus Check
- 289 files · ~132,676 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4238 nodes · 8257 edges · 299 communities (195 shown, 104 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 826 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b9ad2288`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ProjectApplicationRepository
- make_user
- Department
- ProjectApplication
- TestSubmitApplicationService
- RegistrationRequestViewSet
- ProjectApplicationViewSet
- ProjectTrack
- teams/models.py
- TagRepository
- ApplicationDashboardService
- ApplicationDashboardRepository
- is_cpds_department
- PreRegisteredStudentService
- PasswordChangeSerializer
- StudyGroupDomain
- prepare_study_groups_xlsx.py
- StudyGroup
- test_project_track_viewset.py
- TagService
- TestDepartmentPlanViewSetCreate
- TestProjectApplicationCreateDTO
- Semester
- .validate_create
- ValidationResult
- test_export_import_departments_roundtrip
- test_import_study_groups_from_contingent.py
- TeamLobbyService
- Role
- domain/project_track.py
- TestProjectApplicationReadDTO
- AvailableActionDTO
- RegistrationRequestCreateSerializer
- Any
- ProjectTrackViewSet
- institute_access.py
- ProjectService
- StudyGroupViewSet
- ProjectApplicationService
- normalize_cell
- UserManagementDomain
- test_project_track_service.py
- User
- TagCreateDTO
- CommentService
- TestTagViewSetCreate
- test_team_lobby_viewset.py
- .approve_application
- TeamLobby.py
- TestCanUpdateTag
- Tag.py
- ProjectTrackService
- dto/team_lobby.py
- TestDepartmentPlanViewSetList
- UserManagementService
- ._track_detail_queryset
- APIClient
- StudyGroupService
- test_preregistered_student_viewset.py
- accounts/serializers.py
- test_study_group_viewset.py
- ProjectTrackDomain
- Tag
- .can_change_status
- Примеры использования поля is_internal_customer
- PasswordResetSerializer
- ApplicationNotificationService
- TestProjectApplicationListSemesterFilter
- TestUserManagementDomain
- PreRegisteredStudent
- .update_application
- .can_user_access_application
- .get_filtered_queryset
- showcase/urls.py
- ProjectTrackRepository
- DirectionService
- Текущий статус реализации
- test_application_dashboard_viewset.py
- TestTagViewSet
- TestCanCreateTag
- TestCoordinationAndDtosService
- .recalculate_recommended_teams_count
- API для работы с проектными заявками
- AccountsApiTests
- TestCanDeleteTag
- Path
- .add_applications
- Command
- TeamSemester
- ApplicationCapabilities
- test_import_preregistered_students.py
- TestProjectViewSet
- .calculate_initial_status
- .get_existing_group_ids
- .get_filtered_queryset
- import_study_groups_from_contingent.py
- Any
- TestProjectApplicationViewSetIsInternalCustomer
- TestProjectApplicationNewFieldsCreateUpdate
- TestProjectApplicationViewSetTransferToInstitute
- .update
- extract_group_abbrev.py
- .get_dashboard
- StudyGroup.py
- accounts/admin.py
- Command
- ._application_institute_access_q
- .auth
- .update_team_member_limits
- ProjectApplicationCreateDTO
- _generate_collection.py
- QuerySet
- ApplicationLoggingService
- .submit_application
- accounts/views.py
- test_institute_access.py
- accounts/permissions.py
- TestMyTeamViewSet
- StudyGroupMemberDTO
- TestSemesterAssignViewSet
- TestProjectApplicationListDTO
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
- deploy.sh
- action_types.py
- export_client_sources_to_docx.py
- make_source_docx.py
- parse_miit_ief_groups.py
- Command
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
- 0011_migrate_team_data.py
- AccountsConfig
- 0016_semester_code.py
- enable_db_access_for_all_tests
- main
- Command
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
- .test_departments_list_allow_any_detail_requires_auth
- .test_password_change_success
- .test_password_change_wrong_current_password
- .test_password_reset_sends_email
- .test_registration_request_approve_allowed_for_cpds_user
- .test_registration_request_approve_creates_user_and_sends_email
- .test_registration_request_approve_forbidden_for_regular_user
- .test_registration_request_approve_mail_failure_returns_400_and_no_user_created
- .test_registration_request_create_anonymous_allowed
- .test_registration_request_list_requires_privileged_user
- .test_registration_request_race_condition_integrity_error
- .test_registration_request_reject_forbidden_for_regular_user
- .test_semester_create_allowed_for_admin_and_cpds
- .test_semester_list_is_active_from_settings
- .test_semester_list_requires_auth
- .test_user_me_institute_code_from_department_institute
- .test_user_me_institute_code_none_if_no_institute
- .test_user_roles_list_requires_auth_and_returns
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
- Command
- UserSerializer
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
- TestApproveRejectRequest
- Схема БД: студенческий портал
- Справочные эндпоинты
- ProjectViewSet
- ProjectRepository
- TestProjectApplicationViewSetSimple
- Endpoints
- 6. Маппинг разделов UI → сущности БД
- 1. Список пользователей
- 3. Изменение пользователя
- Поддержка multipart/form-data
- Вариант 1: импорт схемы с автообновлением
- 4. State machine статусов команды и блокировки
- 5. Вычисляемые лимиты размера команды (effective_min / effective_max)
- Обработка ошибок
- 1. Введение и scope
- 2. As-is: текущее состояние
- 3.5. Изменения `Team` и семестровый контекст (`teams`)
- 8. Сводка: новые vs изменённые сущности
- РАСПОРЯЖЕНИЕ
- API Документация - Проектные заявки
- ProjectTrackAddApplicationItemSerializer
- ProjectTrackUpdateSerializer
- project_application.md
- project_activity_server
- .handle

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

## Communities (299 total, 104 thin omitted)

### Community 0 - "ProjectApplicationRepository"
Cohesion: 0.02
Nodes (60): ProjectApplicationRepository, Получение заявки по ID с оптимизацией запросов. Включает все связанные объекты…, Получение заявки по ID без дополнительных связанных объектов. Для простых…, Получение заявок пользователя, где он является автором. Оптимизированный запрос…, Получение заявок для координации пользователя. Заявки, где пользователь…, Репозиторий - вся работа с БД здесь, Получение заявок для координации по причастному подразделению. Заявки, где…, Получение заявок по статусу. Для административных операций. (+52 more)

### Community 1 - "make_user"
Cohesion: 0.04
Nodes (21): django_db, TestUserManagementViewSet, make_user(), Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.…, django_db, TestProjectTrackGroupsViewSet, TestProjectTrackProjectsViewSet, TestProjectTrackStatisticsViewSet (+13 more)

### Community 2 - "Department"
Cohesion: 0.04
Nodes (53): Command, BaseCommand, Department, Генерация тестовых одобренных проектов и учебных групп для института IEF., Command, BaseCommand, ApplicationInvolvedDepartment, ApplicationInvolvedUser (+45 more)

### Community 3 - "ProjectApplication"
Cohesion: 0.05
Nodes (34): Репозиторий для управления пользователями., ProjectListDTO, Any, DTO для списка проектов., DTO для списка проектов., Возвращает причастное подразделение верхнего уровня (без родителя). ЦПДС…, ProjectApplication, InvolvedManager (+26 more)

### Community 4 - "TestSubmitApplicationService"
Cohesion: 0.08
Nodes (13): django_db, Если needs_consultation не передан, значение остается False по умолчанию., При создании упрощенной заявки устанавливается is_external=True и статус…, При создании упрощенной заявки добавляется причастное подразделение ЦПДС., При создании обычной заявки is_external=False по умолчанию., Заявка автоматически переходит в await_institute, если в подразделении нет…, Заявка остаётся в await_department, если в подразделении есть…, Успешная подача заявки: создаётся со статусом created, затем переводится в… (+5 more)

### Community 5 - "RegistrationRequestViewSet"
Cohesion: 0.14
Nodes (12): RegistrationRequest, Status, ApproveRequestSerializer, Сериализатор для ролей пользователей., RegistrationRequestSerializer, RejectRequestSerializer, RoleSerializer, action (+4 more)

### Community 6 - "ProjectApplicationViewSet"
Cohesion: 0.05
Nodes (33): format_validation_errors(), get_error_message(), ProjectApplicationViewSet, action, extend_schema, POST /api/project-applications/{id}/add_comment/ Добавление комментария к…, GET /api/project-applications/{id}/comments/ Получение всех комментариев к…, GET /api/project-applications/external/ Получение списка всех внешних заявок… (+25 more)

### Community 7 - "ProjectTrack"
Cohesion: 0.10
Nodes (14): ProjectTrackAdmin, display, Админка проектных треков., Количество групп в треке., Количество заявок в треке., Оптимизирует список треков., ProjectTrackApplicationItemDTO, ProjectTrackGroupItemDTO (+6 more)

### Community 8 - "teams/models.py"
Cohesion: 0.05
Nodes (42): DirectionDomain, Доменная логика для направлений подготовки., Фильтрация направлений по роли пользователя., DirectionReadDTO, Any, DTO для направлений подготовки., DTO для чтения направления., DirectionSerializer (+34 more)

### Community 9 - "TagRepository"
Cohesion: 0.05
Nodes (37): DTO для работы с тегами., DTO для обновления тега., TagUpdateDTO, Repository слой для изоляции работы с базой данных. Этот слой содержит все…, Репозиторий для работы с тегами в БД. Изолирует всю работу с базой данных от…, Получение всех тегов с оптимизацией запросов. Returns: QuerySet всех тегов с…, Проверка существования тега. Быстрая проверка без загрузки объекта. Args:…, Репозиторий - вся работа с БД здесь. (+29 more)

### Community 10 - "ApplicationDashboardService"
Cohesion: 0.06
Nodes (33): ApplicationDashboardService, Оркестрация получения данных дашборда заявок., _create_app(), django_db, fixture, Тесты ApplicationDashboardService., Заявка дочернего подразделения видна при фильтре по родителю., Фильтр application_type=external. (+25 more)

### Community 11 - "ApplicationDashboardRepository"
Cohesion: 0.07
Nodes (29): ApplicationDashboardRepository, Q, QuerySet, Сводные KPI: total, approved, rejected, resolution times., Агрегирует заявки по измерению (institute/department) и группе статуса., Считает долю внешних заявок (is_internal_customer=False) по каждому измерению., Цвет столбца по порогам доли внешних заявок., Строит карту institute_code -> множество id заявок. (+21 more)

### Community 12 - "is_cpds_department"
Cohesion: 0.12
Nodes (12): is_cpds_department(), Проверяет, что подразделение — ЦПДС (координирующее, не основное)., django_db, Unit-тесты для утилит работы с подразделениями., Тесты для функции get_root_department., Подразделение без parent возвращает само себя., Подразделение с одним уровнем parent возвращает корневое., Подразделение с несколькими уровнями parent возвращает корневое. (+4 more)

### Community 13 - "PreRegisteredStudentService"
Cohesion: 0.14
Nodes (10): PreRegisteredStudentLookupResult, PreRegisteredStudentService, atomic, Отправляет администратору письмо о расхождении данных. Raises: ValueError: если…, Отправляет студенту письмо после успешной регистрации., Результат поиска предрегистрации., Сериализует результат для API., Оркестрация поиска, регистрации и уведомлений по предрегистрации. (+2 more)

### Community 14 - "PasswordChangeSerializer"
Cohesion: 0.22
Nodes (5): PasswordChangeSerializer, PasswordResetConfirmSerializer, Any, Возвращает учебную группу пользователя или None., Сериализатор для смены пароля аутентифицированного пользователя.

### Community 15 - "StudyGroupDomain"
Cohesion: 0.15
Nodes (10): QuerySet, Фильтрация учебных групп по роли пользователя., institute_validator — только группы своих институтов., Возвращает True, если пользователь — аутентифицированный студент., Студент с привязанной учебной группой может открыть «Мою группу»., StudyGroupDomain, django_db, parametrize (+2 more)

### Community 16 - "prepare_study_groups_xlsx.py"
Cohesion: 0.08
Nodes (46): build_parser(), _cell_str(), _extract_group_abbrev_from_text(), _find_header_row(), _fio_from_row(), _looks_like_student_id(), main(), _normalize_header() (+38 more)

### Community 17 - "StudyGroup"
Cohesion: 0.07
Nodes (33): Доменная логика для учебных групп., MyStudyGroupDTO, DTO для эндпоинта «Моя группа»., Карточка наставника учебной группы., Полные данные учебной группы для текущего студента., StudyGroupMentorDTO, StudyGroup, QuerySet (+25 more)

### Community 18 - "test_project_track_viewset.py"
Cohesion: 0.08
Nodes (30): ApplicationInvolvedDepartmentInline, ApplicationInvolvedUserInline, ApplicationStatusAdmin, DepartmentPlanAdmin, InstituteAdmin, ProjectApplicationAdmin, ProjectApplicationCommentAdmin, ProjectApplicationStatusLogAdmin (+22 more)

### Community 19 - "TagService"
Cohesion: 0.06
Nodes (31): Бизнес-операция: получение списка тегов с фильтрацией по ролям. Для…, Сервис - оркестрация всех операций с тегами. Координирует Domain, Repository и…, TagService, django_db, Unit-тесты для сервиса TagService. Проверяем все методы работы с тегами:…, Тесты для метода update_tag сервиса., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением. (+23 more)

### Community 20 - "TestDepartmentPlanViewSetCreate"
Cohesion: 0.06
Nodes (17): Создание плана с большим значением., Ошибка: неавторизованный пользователь., Ошибка: подразделение не найдено., Ошибка: семестр не найден., Ошибка: отрицательное значение plan., Ошибка: отсутствует department_id., Тесты для POST /api/showcase/department-plans/ - установка плана., Ошибка: отсутствует semester_id. (+9 more)

### Community 21 - "TestProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (28): Any, Преобразование в словарь, Преобразование в словарь, исключая None значения, Преобразование в словарь для JSON, Преобразование в словарь для JSON, ProjectApplicationCreateSerializer, ProjectApplicationUpdateSerializer, Сериализатор для технической валидации HTTP данных. ОТВЕТСТВЕННОСТЬ: - Типы… (+20 more)

### Community 22 - "Semester"
Cohesion: 0.05
Nodes (34): Command, BaseCommand, Path, Идемпотентный импорт строк модели Settings из CSV., Проверка ссылок для active_* ключей (только предупреждение в stdout)., Идемпотентный импорт предрегистрации студентов из отчёта контингента 1С., AcademicYear, Meta (+26 more)

### Community 23 - ".validate_create"
Cohesion: 0.12
Nodes (13): Валидация бизнес-правил для создания заявки. Чистая функция - принимает данные,…, Носитель проблемы короче 5 символов вызывает ошибку., Барьер короче 10 символов вызывает ошибку., Имя и фамилия автора короче 2 символов вызывают ошибки., Тесты для валидации при создании заявки., Телефон короче 10 символов вызывает ошибку., Валидный DTO проходит проверку без ошибок., Все ошибки валидации собираются в одном результате. (+5 more)

### Community 24 - "ValidationResult"
Cohesion: 0.06
Nodes (23): Проверка, что валидация прошла успешно, Добавление ошибки валидации, Добавление нескольких ошибок, Получение списка ошибок для отображения, Результат валидации данных, ValidationResult, Unit-тесты для ValidationResult showcase.dto.validation. Проверяем добавление…, Тесты для ValidationResult. (+15 more)

### Community 25 - "test_export_import_departments_roundtrip"
Cohesion: 0.27
Nodes (10): Any, django_db, Экспорт и последующий импорт институтов восстанавливают данные., Экспорт и последующий импорт подразделений восстанавливают данные., Импорт институтов удаляет те, которых нет в файле., Импорт подразделений удаляет те, которых нет в файле., test_export_import_departments_roundtrip(), test_export_import_institutes_roundtrip() (+2 more)

### Community 26 - "test_import_study_groups_from_contingent.py"
Cohesion: 0.13
Nodes (17): build_group_import_row(), build_group_name(), calculate_course_number(), parse_direction_level(), parse_permanent_group_code(), ParsedPermanentGroup, Чистая логика импорта учебных групп из отчёта контингента 1С., Рассчитывает номер курса на текущий учебный год и семестр. (+9 more)

### Community 27 - "TeamLobbyService"
Cohesion: 0.05
Nodes (53): PageNumberPagination, MyTeamReadDTO, ApproveJoinRequestSerializer, CreateInvitationSerializer, CreateTeamSerializer, MyTeamViewSet, action, extend_schema (+45 more)

### Community 28 - "Role"
Cohesion: 0.11
Nodes (12): Command, BaseCommand, Role, UserManager, Сериализатор частичного обновления пользователя., Проверяет уникальность email с учётом обновляемого пользователя., UserUpdateSerializer, BaseUserManager (+4 more)

### Community 29 - "domain/project_track.py"
Cohesion: 0.15
Nodes (11): Проверяет, может ли пользователь изменять пользователей., ProjectDomain, Доменная логика для списка проектов., Проверяет, может ли пользователь получать список проектов., Коды институтов для фильтрации; None — без ограничения., Правила доступа и фильтрации для списка проектов., Доменная логика для проектных треков., get_accessible_institute_codes() (+3 more)

### Community 30 - "TestProjectApplicationReadDTO"
Cohesion: 0.09
Nodes (13): Exception, Тесты для ProjectApplicationReadDTO., Базовые поля DTO заполняются из модели заявки., Если статус заявки None, DTO.status тоже None., Если автор заявки None, DTO.author тоже None., target_institutes сериализуется как список словарей с code и name., tags сериализуется как список словарей с id, name и category., involved_users сериализуется с данными пользователя, added_at и added_by. (+5 more)

### Community 31 - "AvailableActionDTO"
Cohesion: 0.08
Nodes (24): AvailableActionDTO, AvailableActionsDTO, Any, DTO для представления доступных действий с заявками., Преобразование в словарь для JSON ответа., DTO для представления списка доступных действий., Преобразование в словарь для JSON ответа., Создание DTO из списка действий. Args: actions_list: Список действий в формате… (+16 more)

### Community 32 - "RegistrationRequestCreateSerializer"
Cohesion: 0.14
Nodes (10): AcademicYearSerializer, Meta, Краткий сериализатор пользователя для отображения в других сущностях., Проверяет email: нормализация, отсутствие пользователя и активной заявки., Валидация подразделения., Сериализатор учебного года (краткий)., Сериализатор для семестров., RegistrationRequestCreateSerializer (+2 more)

### Community 33 - "Any"
Cohesion: 0.06
Nodes (21): ProjectTrackGroupListDTO, ProjectTrackInstituteStatisticsDTO, ProjectTrackProjectListDTO, ProjectTrackStatisticsDTO, Any, Преобразует DTO в словарь для API., Преобразует DTO в словарь для API., Создаёт DTO из словаря. (+13 more)

### Community 34 - "ProjectTrackViewSet"
Cohesion: 0.13
Nodes (22): ProjectTrackViewSet, action, extend_schema, extend_schema_view, Request, Response, API для проектных треков: CRUD и управление составом., Извлекает institute_code и semester_id из query-параметров. (+14 more)

### Community 35 - "institute_access.py"
Cohesion: 0.06
Nodes (29): get_department_subtree_ids(), get_root_department(), Утилиты для работы с подразделениями., Находит корневое подразделение в иерархии. Поднимается по цепочке parent до тех…, Возвращает id корневого подразделения и всех его потомков., ApplicationDashboardDomain, DashboardFilters, Доменная логика дашборда проектных заявок. (+21 more)

### Community 36 - "ProjectService"
Cohesion: 0.21
Nodes (5): ProjectService, Оркестрация Domain + Repository для списка проектов., TestProjectApplicationNewFieldsLists, django_db, TestProjectService

### Community 37 - "StudyGroupViewSet"
Cohesion: 0.22
Nodes (7): action, Request, Response, GET /api/teams/study-groups/my/ — группа текущего студента., GET /api/teams/study-groups/ — список и просмотр учебных групп., Парсит query-параметр is_end; None — фильтр не применяется., StudyGroupViewSet

### Community 38 - "ProjectApplicationService"
Cohesion: 0.03
Nodes (54): ViewSet для операций над семестрами, связанных с проектными заявками., SemesterViewSet, ProjectApplicationService, Сервис - оркестрация всех операций. Координирует Domain, Repository и…, Преобразование модели в DTO для чтения., Преобразование модели в DTO для списка., Бизнес-операция: получение заявок по статусу., Бизнес-операция: получение последних заявок. (+46 more)

### Community 39 - "normalize_cell"
Cohesion: 0.17
Nodes (13): build_preregistered_student_import_row(), normalize_snils(), parse_full_name(), PreRegisteredStudentImportRow, Чистая логика импорта предрегистрации студентов из отчёта контингента 1С., Строка отчёта, подготовленная к импорту одной предрегистрации., Нормализует СНИЛС до 11 цифр или пустой строки., Разбирает ФИО из отчёта контингента. Returns: Кортеж (фамилия, имя, отчество). (+5 more)

### Community 40 - "UserManagementDomain"
Cohesion: 0.21
Nodes (8): Доменная логика управления пользователями., Правила доступа и валидации для управления пользователями., ID подразделений для фильтрации; None — без ограничения., UserManagementDomain, Сервис управления пользователями., get_user_institute_codes(), Коды активных институтов, связанных с подразделением пользователя., Тесты UserManagementDomain.

### Community 41 - "test_project_track_service.py"
Cohesion: 0.06
Nodes (32): ProjectTrackPermission, Разрешает доступ к проектным трекам для admin, cpds и institute_validator., ProjectTrackAddApplicationItemDTO, ProjectTrackAddApplicationsDTO, ProjectTrackAddGroupsDTO, ProjectTrackAggregatedStatisticsDTO, ProjectTrackCreateDTO, ProjectTrackUpdateDTO (+24 more)

### Community 42 - "User"
Cohesion: 0.05
Nodes (34): AbstractBaseUser, QuerySet, Проверяет, что пользователь доступен в отфильтрованном queryset., User, check_and_fix_user(), Проверяем и исправляем пользователя, PermissionsMixin, ProjectTrackReadDTO (+26 more)

### Community 43 - "TagCreateDTO"
Cohesion: 0.08
Nodes (20): DTO для создания тега., TagCreateDTO, Создание тега в БД. Args: dto: DTO с данными для создания тега Returns:…, Тесты для метода create репозитория., Создание общего тега (без departments)., Создание тега с подразделением., Создание тега с несуществующим подразделением вызывает ошибку., Нельзя создать тег с таким же именем и таким же набором подразделений. (+12 more)

### Community 44 - "CommentService"
Cohesion: 0.08
Nodes (20): ProjectApplicationComment, CommentService, atomic, Сервис для управления комментариями к проектным заявкам. Обеспечивает…, Сервис для управления комментариями к заявкам. Обеспечивает добавление и…, Добавляет комментарий к заявке. Args: application_id: ID заявки field: Поле, к…, Получает все комментарии к заявке. Args: application_id: ID заявки Returns:…, django_db (+12 more)

### Community 45 - "TestTagViewSetCreate"
Cohesion: 0.12
Nodes (9): Тесты для создания тегов через API., cpds может создавать общие теги., cpds не может создавать теги с подразделением., institute_validator автоматически устанавливает свое подразделение., admin может создавать любые теги., Остальные роли не могут создавать теги., Нельзя создать тег для подразделения, если уже есть общий тег с таким именем., Нельзя создать общий тег, если имя уже используется (общим или departmental… (+1 more)

### Community 46 - "test_team_lobby_viewset.py"
Cohesion: 0.33
Nodes (9): api_client(), _approved_app(), direction(), lobby_setup(), fixture, Тесты API лобби формирования команд., semester(), study_group() (+1 more)

### Community 47 - ".approve_application"
Cohesion: 0.09
Nodes (18): Any, Возвращает список доступных действий согласно матрице., atomic, Определяет статус для доработки в зависимости от роли пользователя. Args:…, Определяет статус для отклонения в зависимости от роли пользователя. Args:…, Определяет промежуточный статус для одобрения в зависимости от роли…, Определяет следующий статус после промежуточного одобрения. Args:…, Бизнес-операция: отправка заявки на доработку. (+10 more)

### Community 48 - "TeamLobby.py"
Cohesion: 0.07
Nodes (34): API лобби формирования команд и «Моей команды»., Постоянная команда участников проектной деятельности., Team, _is_staff_or_admin(), APIView, BasePermission, Request, Разрешения для приложения teams. (+26 more)

### Community 49 - "TestCanUpdateTag"
Cohesion: 0.15
Nodes (10): Проверяет права пользователя на обновление тега. Args: user: Пользователь tag:…, Тесты для проверки прав на обновление тегов., cpds может обновлять общие теги., cpds не может обновлять теги с подразделением., institute_validator может обновлять общие теги., institute_validator может обновлять теги своего подразделения., institute_validator не может обновлять теги чужого подразделения., admin может обновлять любые теги. (+2 more)

### Community 50 - "Tag.py"
Cohesion: 0.08
Nodes (28): Инициализация из модели Tag., TagReadDTO, DepartmentAttachDetachSerializer, DepartmentNestedSerializer, Meta, action, Request, Response (+20 more)

### Community 51 - "ProjectTrackService"
Cohesion: 0.12
Nodes (7): Создаёт DTO из словаря., PATCH /api/showcase/project-tracks/{id}/., ProjectTrackService, Оркестрация Domain + Repository для проектных треков., _create_approved_app(), django_db, TestProjectTrackService

### Community 52 - "dto/team_lobby.py"
Cohesion: 0.04
Nodes (34): Доменные правила лобби формирования команд., Заявка должна быть в статусе pending., Чистая бизнес-логика лобби и «Моей команды»., Проверяет роль student и наличие учебной группы; возвращает group_id., True, если студент без команды и есть свободный слот., Запрещает изменения состава при подтверждённом составе., Проверяет, что пользователь — капитан команды., Приглашение не может назначать роль leader. (+26 more)

### Community 53 - "TestDepartmentPlanViewSetList"
Cohesion: 0.06
Nodes (18): Тесты для GET /api/showcase/department-plans/ - получение планов., Успешное получение планов дочерних подразделений по коду института., Успешное получение планов верхнеуровневых подразделений., Пустой список дочерних подразделений., Если план отсутствует, возвращается 0., Проверка статистики заявок по статусам., Подразделение без заявок - пустая статистика., Ошибка: неавторизованный пользователь. (+10 more)

### Community 54 - "UserManagementService"
Cohesion: 0.06
Nodes (29): Any, DTO для списка пользователей., DTO для элемента списка пользователей., UserListDTO, extend_schema_view, Request, Response, API управления пользователями: список, деталь, частичное обновление. (+21 more)

### Community 55 - "._track_detail_queryset"
Cohesion: 0.33
Nodes (3): Возвращает трек по id или None., Queryset трека с prefetch связей., Список треков по фильтрам.

### Community 56 - "APIClient"
Cohesion: 0.19
Nodes (8): MonkeyPatch, Any, APIClient, django_db, override_settings, TestPreRegisteredStudentLookup, TestPreRegisteredStudentMismatch, TestPreRegisteredStudentRegister

### Community 57 - "StudyGroupService"
Cohesion: 0.22
Nodes (4): Оркестрация Domain + Repository для StudyGroup., StudyGroupService, django_db, TestStudyGroupService

### Community 58 - "test_preregistered_student_viewset.py"
Cohesion: 0.47
Nodes (5): api_client(), pre_registered_student(), fixture, Тесты API предрегистрации студентов., study_group()

### Community 59 - "accounts/serializers.py"
Cohesion: 0.11
Nodes (21): PreRegisteredStudentViewSet, action, extend_schema_view, Request, Response, API предрегистрации студентов из контингента., Публичные операции предрегистрации студентов., Ищет предрегистрацию по студбилету, табельному номеру или СНИЛС. (+13 more)

### Community 60 - "test_study_group_viewset.py"
Cohesion: 0.47
Nodes (5): direction(), other_institute(), fixture, Тесты StudyGroupViewSet., study_groups()

### Community 61 - "ProjectTrackDomain"
Cohesion: 0.07
Nodes (17): ProjectTrackDomain, Проверяет, что все группы доступны пользователю., Проверяет, что группу можно добавить в трек., Проверяет, что заявка доступна пользователю по институтам., Проверяет, что заявку можно добавить в трек., Проверяет доступ к конкретному треку., Правила доступа и валидации для проектных треков., Код роли пользователя. (+9 more)

### Community 62 - "Tag"
Cohesion: 0.08
Nodes (18): Доменная логика для тегов - чистые функции без эффектов., Чистая бизнес-логика для тегов - только функции, никаких эффектов., Проверяет права пользователя на присоединение подразделения к тегу. Args: user:…, Проверяет права пользователя на отцепление подразделения от тега. Args: user:…, TagDomain, Теги для проектных заявок, Tag, Удаление тега. Args: tag: Тег для удаления Returns: True если тег был удален (+10 more)

### Community 63 - ".can_change_status"
Cohesion: 0.13
Nodes (12): Проверка возможности изменения статуса. Чистая функция - принимает параметры,…, parametrize, Тесты для проверки возможности изменения статуса., Разрешённый переход возвращает True., Институт может согласовать заявку на шаге кафедры., Институт может отклонить заявку на шаге кафедры., Запрещённый переход возвращает False с сообщением об ошибке., Переход в approved из await_cpds разрешён для всех ролей (проверка матрицы в… (+4 more)

### Community 64 - "Примеры использования поля is_internal_customer"
Cohesion: 0.11
Nodes (18): 1. Создание заявки с внутренним заказчиком, 2. Создание заявки с внешним заказчиком, 3. Создание заявки без указания типа заказчика (по умолчанию false), Endpoint, Возможные ошибки, Использование в Python коде, Обновление только поля is_internal_customer, Обновление через DTO (+10 more)

### Community 66 - "ApplicationNotificationService"
Cohesion: 0.19
Nodes (8): ApplicationNotificationService, Отправка писем автору при отклонении и отправке на доработку., Email получателя: author_email заявки или email связанного пользователя-автора., Письмо автору: заявка отправлена на доработку., Письмо автору: заявка отклонена., django_db, patch, TestApplicationNotificationService

### Community 67 - "TestProjectApplicationListSemesterFilter"
Cohesion: 0.09
Nodes (14): django_db, Тесты для получения списка внешних заявок (external endpoint)., GET /api/showcase/project-applications/external/ требует авторизации., GET /api/showcase/project-applications/external/ возвращает только внешние…, Фильтр ?semester_id= в GET-списке заявок., Автоподстановка семестра при создании заявки., Тесты для проверки наличия поля is_external в ответах API., POST /api/showcase/project-applications/ возвращает is_external в ответе. (+6 more)

### Community 68 - "TestUserManagementDomain"
Cohesion: 0.17
Nodes (6): Проверяет, может ли пользователь просматривать список пользователей., Проверяет, что пользователь защищён от изменений (админ/staff)., Валидирует частичное обновление пользователя., Role, django_db, TestUserManagementDomain

### Community 69 - "PreRegisteredStudent"
Cohesion: 0.10
Nodes (15): PreRegisteredStudent, Предрегистрация студента из отчёта контингента 1С., Возвращает True, если предрегистрация уже привязана к User., PreRegisteredStudentRepository, QuerySet, Репозиторий предрегистрации студентов., Доступ к данным предрегистрации студентов., Возвращает предрегистрацию по номеру студенческого билета. (+7 more)

### Community 70 - ".update_application"
Cohesion: 0.15
Nodes (9): Бизнес-операция: обновление заявки. Чистая функция - проверяет возможность…, Автор с ролью user в статусе await_department не может редактировать заявку., Сотрудник ЦПДС может редактировать любую заявку (кроме rejected)., Не-автор и не-ЦПДС не может редактировать заявку., Нет доступа и запрещённые статусы добавляют ошибки в ValidationResult., CPDS может редактировать одобренные заявки., institute_validator-автор: save совпадает с available_actions (подразделение…, institute_validator без причастного подразделения не может сохранить. (+1 more)

### Community 71 - ".can_user_access_application"
Cohesion: 0.06
Nodes (23): Проверка доступа пользователя к заявке. Чистая функция - принимает параметры,…, Бизнес-операция: просмотр заявки. Чистая функция - проверяет возможность…, Бизнес-операция: получение списка заявок. Чистая функция - проверяет…, Бизнес-операция: получение заявки., Получение логов заявки; для автора сбрасывает has_unseen_changes., Сбрасывает флаг непросмотренных изменений, если заявку открыл автор., Бизнес-операция: получение заявок пользователя., Бизнес-операция: получение QuerySet заявок пользователя для пагинации. (+15 more)

### Community 72 - ".get_filtered_queryset"
Cohesion: 0.14
Nodes (11): QuerySet, Фильтрует queryset тегов в зависимости от роли пользователя. Чистая функция -…, Остальные роли без подразделения видят только общие теги., Неавторизованный пользователь видит только общие теги., Тесты для фильтрации queryset тегов по ролям., cpds видит только общие теги (без departments)., institute_validator видит общие теги + теги своего подразделения., institute_validator без подразделения видит только общие теги. (+3 more)

### Community 73 - "showcase/urls.py"
Cohesion: 0.07
Nodes (31): DenyStudentPermission, Запрещает доступ пользователям с ролью student., ApplicationStatusReadSerializer, ApplicationStatusSerializer, ApplicationStatusViewSet, Meta, Сериализатор для статусов заявок, ViewSet только для чтения статусов заявок на проекты. Доступен только для… (+23 more)

### Community 74 - "ProjectTrackRepository"
Cohesion: 0.09
Nodes (12): ProjectTrackRepository, Создаёт проектный трек., Добавляет группы в трек; возвращает число созданных связей., Удаляет группу из трека; True если связь была., Возвращает id заявок, уже привязанных к треку., Удаляет заявку из трека; True если связь была., Доступ к данным проектных треков., Количество групп в треке. (+4 more)

### Community 75 - "DirectionService"
Cohesion: 0.16
Nodes (10): DirectionViewSet, Request, Response, GET /api/teams/directions/ — список и просмотр направлений., DirectionService, Оркестрация Domain + Repository для Direction., Список направлений с фильтрацией по роли., Направление по коду с проверкой доступа. (+2 more)

### Community 76 - "Текущий статус реализации"
Cohesion: 0.40
Nodes (5): ⚠️ Проблемные функции, ✅ Работающие функции, 📊 Статистика тестирования, Текущий статус реализации, 🔧 Требует доработки

### Community 77 - "test_application_dashboard_viewset.py"
Cohesion: 0.11
Nodes (13): api_client(), django_db, fixture, Тесты ApplicationDashboardViewSet., Неизвестная группа статусов — 400., HTTP-тесты дашборда заявок., Без авторизации — 401., Без semester_id — 400. (+5 more)

### Community 78 - "TestTagViewSet"
Cohesion: 0.04
Nodes (27): django_db, Список тегов фильтруется для роли cpds (только общие теги)., Список тегов фильтруется для роли institute_validator (общие + своего…, Тесты для TagViewSet., Admin видит все теги., GET /api/tags/ возвращает все теги без пагинации., Тесты для обновления тегов через API., cpds может обновлять общие теги. (+19 more)

### Community 79 - "TestCanCreateTag"
Cohesion: 0.14
Nodes (11): Проверяет права пользователя на создание тега. Args: user: Пользователь…, Тесты для проверки прав на создание тегов., cpds может создавать только общие теги., cpds не может создавать теги с подразделением., institute_validator может создавать общие теги., institute_validator может создавать теги для своего подразделения., institute_validator не может создавать теги для чужого подразделения., admin может создавать любые теги. (+3 more)

### Community 80 - "TestCoordinationAndDtosService"
Cohesion: 0.11
Nodes (9): Валидатор получает объединённый список: его причастность пользователя +…, cpds видит все заявки в статусе await_cpds даже без причастности., Преобразователи к DTO возвращают ожидаемые экземпляры., get_external_applications возвращает только заявки с is_external=True., get_external_applications позволяет фильтровать внешние заявки по коду статуса., get_external_applications с несуществующим статусом выбрасывает ValueError., get_external_applications_queryset возвращает QuerySet внешних заявок., get_external_applications требует авторизации. (+1 more)

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
Cohesion: 0.16
Nodes (13): aga_institute(), direction(), Any, django_db, fixture, Path, Временный файл контингента для интеграционных тестов., Направление подготовки для тестов импорта. (+5 more)

### Community 87 - "Command"
Cohesion: 0.16
Nodes (10): Command, Any, BaseCommand, Экспортирует все институты в Excel., Команда для импорта/экспорта подразделений и институтов в Excel., Импортирует подразделения из Excel с обновлением и удалением лишних., Импортирует институты из Excel с обновлением и удалением лишних., Добавляет аргументы командной строки. (+2 more)

### Community 88 - "TeamSemester"
Cohesion: 0.03
Nodes (62): DirectionAdmin, register, StudyGroupAdmin, TeamAdmin, TeamEventLogAdmin, TeamInvitationAdmin, TeamJoinRequestAdmin, TeamSemesterAdmin (+54 more)

### Community 89 - "ApplicationCapabilities"
Cohesion: 0.08
Nodes (19): ApplicationCapabilities, Бизнес-операция: запрос изменений. Чистая функция - проверяет возможность…, Явное выражение бизнес-намерений. Вместо технических операций типа "create",…, Бизнес-операция: одобрение заявки. Чистая функция - проверяет возможность…, Возвращает список ключей матрицы, подходящих под статус. Сначала точное…, Проверка права на конкретное действие на основе статической матрицы., УСТАРЕВШЕ: прокси к новой матрице. Считаем, что "управление" означает…, Проверка права на редактирование заявки. Бизнес-правило: редактировать может… (+11 more)

### Community 90 - "test_import_preregistered_students.py"
Cohesion: 0.20
Nodes (11): aga_institute(), Any, django_db, fixture, Path, Тесты команды import_preregistered_students., Создаёт минимальный отчёт контингента для тестов., sample_contingent_file() (+3 more)

### Community 91 - "TestProjectViewSet"
Cohesion: 0.18
Nodes (4): _create_approved_app(), django_db, ЦПДС в причастных не должно подменять основное подразделение проекта., TestProjectViewSet

### Community 92 - ".calculate_initial_status"
Cohesion: 0.17
Nodes (9): Определение начального статуса на основе роли пользователя. Чистая функция -…, Тесты для определения начального статуса по роли., Админ создаёт заявки со статусом approved., CPDS создаёт заявки со статусом approved., Валидатор подразделения создаёт заявки в статусе await_institute., Валидатор института создаёт заявки в статусе await_cpds., Обычный пользователь создаёт заявки в статусе await_department., Неизвестная роль возвращает статус await_department по умолчанию. (+1 more)

### Community 94 - ".get_filtered_queryset"
Cohesion: 0.10
Nodes (11): QuerySet, Фильтрует направления: institute_validator — только из групп своего института., django_db, parametrize, Разрешение институтов по подразделению пользователя., Фильтрация queryset направлений по ролям., TestGetFilteredQueryset, TestGetUserInstituteCodes (+3 more)

### Community 95 - "import_study_groups_from_contingent.py"
Cohesion: 0.17
Nodes (11): GroupImportRow, Строка отчёта, подготовленная к импорту одной учебной группы., Command, BaseCommand, DataFrame, Path, Идемпотентный импорт учебных групп из отчёта контингента 1С (.xls/.xlsx)., Читает отчёт контингента; заголовок колонок — вторая строка. (+3 more)

### Community 96 - "Any"
Cohesion: 0.15
Nodes (6): Any, Преобразование в словарь., Преобразование в словарь, исключая None значения., Преобразование в словарь., Преобразование в DTO., Преобразование в DTO.

### Community 97 - "TestProjectApplicationViewSetIsInternalCustomer"
Cohesion: 0.12
Nodes (10): django_db, Тесты для проверки поля is_internal_customer при создании заявки., PATCH /api/showcase/project-applications/{id}/ обновляет is_internal_customer., POST /api/showcase/project-applications/ создает заявку с…, PATCH /api/showcase/project-applications/{id}/ автор может обновить…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, PATCH /api/showcase/project-applications/{id}/ без поля is_internal_customer…, POST /api/showcase/project-applications/ создает заявку с… (+2 more)

### Community 98 - "TestProjectApplicationNewFieldsCreateUpdate"
Cohesion: 0.27
Nodes (4): _base_create_payload(), django_db, TestMyApplicationsNewFields, TestProjectApplicationNewFieldsCreateUpdate

### Community 99 - "TestProjectApplicationViewSetTransferToInstitute"
Cohesion: 0.17
Nodes (8): Тесты для действия передачи заявки в институт по коду института., POST /api/showcase/project-applications/{id}/transfer_to_institute/ с…, Отсутствующий параметр code возвращает 400., Несуществующий код института возвращает 400 от сервиса., Институт без связанного подразделения возвращает 400., GET /api/showcase/project-applications/external/?status=... фильтрует внешние…, GET /api/showcase/project-applications/external/?status=... с несуществующим…, TestProjectApplicationViewSetTransferToInstitute

### Community 101 - "extract_group_abbrev.py"
Cohesion: 0.23
Nodes (13): add_abbrev_column_to_students(), build_parser(), extract_abbrev_column(), _extract_group_abbrev_from_text(), _looks_like_student_id(), main(), _normalize_header(), Any (+5 more)

### Community 102 - ".get_dashboard"
Cohesion: 0.17
Nodes (9): ApplicationDashboardDTO, Any, DTO для дашборда проектных заявок., Преобразует DTO в словарь для API., DTO блока KPI-карточек., DTO полного ответа дашборда., Преобразует DTO в словарь для API., SummaryCardsDTO (+1 more)

### Community 103 - "StudyGroup.py"
Cohesion: 0.19
Nodes (10): Any, DTO для учебных групп., DTO для чтения учебной группы., StudyGroupReadDTO, DirectionNestedSerializer, InstituteNestedSerializer, Meta, Компактная выдача для списка учебных групп. (+2 more)

### Community 104 - "accounts/admin.py"
Cohesion: 0.24
Nodes (11): AcademicYearAdmin, DepartmentAdmin, PreRegisteredStudentAdmin, display, register, RegistrationRequestAdmin, RoleAdmin, SemesterAdmin (+3 more)

### Community 105 - "Command"
Cohesion: 0.26
Nodes (3): Command, BaseCommand, Добавляет причастные подразделения института к заявке.

### Community 106 - "._application_institute_access_q"
Cohesion: 0.19
Nodes (7): Q, Q-фильтр: заявка относится к институту по причастным подразделениям., Список одобренных проектов семестра со счётчиком назначенных групп., Q-фильтр: заявка доступна институту по involved/target institutes., Возвращает проектную заявку по id или None., Агрегированная статистика распределения проектов по группам., Статистика по каждому активному институту.

### Community 107 - ".auth"
Cohesion: 0.17
Nodes (6): Без токена возвращается 401, с токеном — профиль текущего пользователя., Админ отклоняет заявку: статус становится REJECTED и уходит письмо., Пользователь ЦПДС может отклонять заявки (IsCpdsUser)., Если отправка письма при reject падает, возвращаем 200 и оставляем статус…, Детальный просмотр роли по коду (lookup_field=code) требует авторизации., Логинится и проставляет Bearer-токен в заголовках клиента.

### Community 110 - "ProjectApplicationCreateDTO"
Cohesion: 0.04
Nodes (58): create_test_applications(), Создаем тестовые заявки, ProjectApplicationDomain, Доменная логика для проектных заявок - чистые функции без эффектов., Чистая бизнес-логика - только функции, никаких эффектов, Валидация бизнес-правил для обновления заявки. Чистая функция - проверяет…, Определение необходимости консультации на основе данных заявки. Чистая функция…, Явное выражение бизнес-намерений (не технических операций). Этот модуль… (+50 more)

### Community 111 - "_generate_collection.py"
Cohesion: 0.24
Nodes (7): env_file(), main(), make_env_values(), Генератор Postman collection + environments для Project Activity API., Собрать объект url Postman из raw URL с {{baseUrl}}., req(), url()

### Community 112 - "QuerySet"
Cohesion: 0.18
Nodes (6): QuerySet, Возвращает группы по списку id., Возвращает заявки по списку id., Список активных групп института со счётчиком назначенных проектов., Одобренные заявки, назначенные группе через общие треки в семестре., Активные группы института, назначенные на проект через общие треки.

### Community 113 - "ApplicationLoggingService"
Cohesion: 0.04
Nodes (46): ApplicationLoggingService, atomic, Логирование удаления причастного пользователя. Args: application: Заявка user:…, Логирование добавления причастного подразделения. Args: application: Заявка…, Логирование удаления причастного подразделения. Args: application: Заявка…, Сервис для логирования изменений в проектных заявках. Обеспечивает полное…, Получение всех логов по заявке. Args: application: Заявка Returns:…, Получение последнего лога заявки. Args: application: Заявка Returns:… (+38 more)

### Community 115 - ".submit_application"
Cohesion: 0.16
Nodes (7): Бизнес-операция: подача заявки. Чистая функция - проверяет возможность подачи…, Бизнес-операция: подача заявки. Новая логика: 1. Валидация через Domain 2.…, Проверяет наличие пользователя с ролью department_validator в причастных…, Проверяет и корректирует статус заявки при необходимости. Если целевой статус -…, Проверяем, что валидный DTO проходит валидацию без ошибок., Невалидные поля аккумулируют ошибки в ValidationResult., TestSubmitApplication

### Community 116 - "accounts/views.py"
Cohesion: 0.11
Nodes (21): DepartmentSerializer, Сериализатор для подразделений/кафедр., DepartmentViewSet, LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView, APIView (+13 more)

### Community 117 - "test_institute_access.py"
Cohesion: 0.21
Nodes (11): application_available_for_institute(), application_belongs_to_institutes(), Проверяет доступность заявки институту для проектных треков. Заявка доступна,…, Проверяет принадлежность заявки к институтам по причастным подразделениям.…, _create_approved_app(), django_db, fixture, Тесты institute_access. (+3 more)

### Community 118 - "accounts/permissions.py"
Cohesion: 0.07
Nodes (29): ViewSet для управления пользователями., IsAdminOrCpds, IsCpdsUser, IsInstituteValidator, ProjectManagementPermission, APIView, BasePermission, Request (+21 more)

### Community 120 - "StudyGroupMemberDTO"
Cohesion: 0.32
Nodes (3): Any, Строка списка группы из контингента., StudyGroupMemberDTO

### Community 121 - "TestSemesterAssignViewSet"
Cohesion: 0.29
Nodes (3): Тесты для ручки массового назначения семестра., GET /api/showcase/project-applications/external/ включает поле is_external в…, TestSemesterAssignViewSet

### Community 123 - "TestProjectApplicationListDTO"
Cohesion: 0.13
Nodes (9): django_db, Тесты для ProjectApplicationListDTO., Базовые поля DTO для списка заполняются из модели., Если статус None, DTO.status тоже None., to_dict преобразует DTO в словарь с ISO форматированием даты., is_internal_customer включается в ProjectApplicationListDTO., Новые поля трека включаются в ProjectApplicationListDTO., is_internal_customer включается в ProjectApplicationReadDTO. (+1 more)

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

### Community 170 - "ProjectTrackProjectDetailDTO"
Cohesion: 0.17
Nodes (7): ProjectTrackProjectDetailDTO, ProjectTrackProjectGroupDTO, DTO группы в деталях проекта., Преобразует DTO в словарь для API., DTO деталей проекта с назначенными группами., Преобразует DTO в словарь для API., Детали проекта с назначенными группами.

### Community 243 - "Command"
Cohesion: 0.29
Nodes (6): Command, BaseCommand, DataFrame, Path, Читает отчёт контингента; заголовок колонок — вторая строка., Строит карту кодов постоянных групп из файла к объектам StudyGroup.

### Community 244 - "UserSerializer"
Cohesion: 0.18
Nodes (9): Проверяет, что у пользователя роль student., Возвращает предрегистрацию пользователя, если она есть., Возвращает код института пользователя. Приоритет: институт подразделения, затем…, Возвращает номер студенческого билета для роли student., Возвращает табельный номер для роли student., Возвращает СНИЛС для роли student., UserSerializer, CustomTokenObtainPairSerializer (+1 more)

### Community 247 - "3. To-be: изменения и новые сущности"
Cohesion: 0.20
Nodes (10): 3.1. ER-диаграмма (целевая), 3.2. Изменения `User` (`accounts`) — данные наставника, 3.3. Изменения `StudyGroup` (`teams`), 3.4. Изменения `ProjectTrack` (`showcase`), 3.6. `TeamJoinRequest` (новая, `teams`, миграция `0013`), 3.6a. `TeamInvitation` (новая, `teams`, миграция `0013`), 3.7. `TeamEventLog` (новая, `teams`, миграция `0013`), 3.8. Один студент — одна команда в семестре (+2 more)

### Community 277 - "ApplicationDashboard.py"
Cohesion: 0.20
Nodes (7): ApplicationDashboardViewSet, extend_schema, Request, Response, ViewSet дашборда проектных заявок., API дашборда проектных заявок., GET /api/showcase/project-applications/dashboard/

### Community 278 - "TestApproveRejectRequest"
Cohesion: 0.27
Nodes (6): parametrize, Матрица прав определяет доступность reject., Для returned_* действует агрегирующее правило returned_(all)., Отзыв доступен только автору и не для финальных approved/rejected., Матрица прав определяет доступность approve для ролей и статусов., TestApproveRejectRequest

### Community 281 - "Схема БД: студенческий портал"
Cohesion: 0.22
Nodes (8): 10. Файлы для будущей реализации (не сейчас), 7.1. Data migration для существующих `Team` (шаг 4), 7.2. Индексы (рекомендуемые), 7. Порядок миграций, 9. Открытые вопросы (вне схемы или follow-up), Приложение A. Черновик TextChoices (для реализации), Приложение B. Связь с разделами backlog, Схема БД: студенческий портал

### Community 288 - "Справочные эндпоинты"
Cohesion: 0.22
Nodes (9): 1. Статусы заявок, 2. Институты/Академии, 3. Роли пользователей, 4. Подразделения/Кафедры, Справочные эндпоинты, Успешный ответ (200), Успешный ответ (200), Успешный ответ (200) (+1 more)

### Community 296 - "ProjectViewSet"
Cohesion: 0.25
Nodes (5): ProjectViewSet, extend_schema_view, Request, Response, GET /api/showcase/projects/ — список проектов с role-based фильтрацией.

### Community 297 - "ProjectRepository"
Cohesion: 0.29
Nodes (5): ProjectRepository, QuerySet, Доступ к данным для списка проектов., Список заявок с фильтрацией по институту и семестру., Одобренные проекты семестра для указанных институтов (legacy).

### Community 298 - "TestProjectApplicationViewSetSimple"
Cohesion: 0.25
Nodes (5): Тесты для упрощенного создания заявок (simple endpoint)., POST /api/showcase/project-applications/simple/ устанавливает is_external=True…, POST /api/showcase/project-applications/simple/ возвращает is_external в ответе., POST /api/showcase/project-applications/simple/ добавляет причастное…, TestProjectApplicationViewSetSimple

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

### Community 320 - "API Документация - Проектные заявки"
Cohesion: 0.18
Nodes (9): API Документация - Проектные заявки, Аутентификация, Базовый URL, Валидационные правила, Общая информация, Обязательные поля, Обязательные поля:, Типы данных (+1 more)

### Community 322 - "ProjectTrackAddApplicationItemSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackAddApplicationItemSerializer, Элемент списка заявок для добавления в трек., Проверяет, что minTeamMembers не больше maxTeamMembers.

### Community 323 - "ProjectTrackUpdateSerializer"
Cohesion: 0.50
Nodes (3): ProjectTrackUpdateSerializer, Сериализатор для обновления проектного трека., Проверяет согласованность лимитов размера команды.

## Knowledge Gaps
- **214 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+209 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **104 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `make_user()` connect `make_user` to `ProjectApplicationRepository`, `Department`, `TestSubmitApplicationService`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `ApplicationDashboardService`, `StudyGroupDomain`, `StudyGroup`, `test_project_track_viewset.py`, `TagService`, `TestDepartmentPlanViewSetCreate`, `Semester`, `domain/project_track.py`, `TestProjectApplicationReadDTO`, `ProjectService`, `ProjectApplicationService`, `test_project_track_service.py`, `TagCreateDTO`, `CommentService`, `TestTagViewSetCreate`, `test_team_lobby_viewset.py`, `TestCanUpdateTag`, `ProjectTrackService`, `TestDepartmentPlanViewSetList`, `UserManagementService`, `APIClient`, `StudyGroupService`, `ProjectTrackDomain`, `ApplicationNotificationService`, `TestProjectApplicationListSemesterFilter`, `TestUserManagementDomain`, `.get_filtered_queryset`, `DirectionService`, `test_application_dashboard_viewset.py`, `TestTagViewSet`, `TestCanCreateTag`, `TestCoordinationAndDtosService`, `TestCanDeleteTag`, `test_import_preregistered_students.py`, `TestProjectViewSet`, `.get_filtered_queryset`, `TestProjectApplicationViewSetIsInternalCustomer`, `TestProjectApplicationNewFieldsCreateUpdate`, `TestProjectApplicationViewSetTransferToInstitute`, `ProjectApplicationCreateDTO`, `ApplicationLoggingService`, `TestSemesterAssignViewSet`, `TestProjectApplicationListDTO`?**
  _High betweenness centrality (0.174) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `ProjectApplicationRepository`, `Department`, `ProjectApplication`, `teams/models.py`, `ApplicationDashboardService`, `PasswordChangeSerializer`, `StudyGroupDomain`, `StudyGroup`, `TagService`, `Semester`, `TeamLobbyService`, `Role`, `domain/project_track.py`, `RegistrationRequestCreateSerializer`, `Any`, `institute_access.py`, `ProjectApplicationService`, `UserManagementDomain`, `test_project_track_service.py`, `ProjectTrackProjectDetailDTO`, `CommentService`, `.approve_application`, `TeamLobby.py`, `TestCanUpdateTag`, `ProjectTrackService`, `dto/team_lobby.py`, `UserManagementService`, `StudyGroupService`, `accounts/serializers.py`, `ProjectTrackDomain`, `Tag`, `PasswordResetSerializer`, `TestUserManagementDomain`, `.can_user_access_application`, `.get_filtered_queryset`, `showcase/urls.py`, `DirectionService`, `TestCanCreateTag`, `TestCanDeleteTag`, `TeamSemester`, `.get_filtered_queryset`, `.get_dashboard`, `accounts/admin.py`, `ProjectApplicationCreateDTO`, `ApplicationLoggingService`, `.submit_application`, `UserSerializer`, `accounts/views.py`, `accounts/permissions.py`, `StudyGroupMemberDTO`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `Semester` connect `Semester` to `ProjectApplicationRepository`, `make_user`, `Department`, `ProjectApplication`, `ProjectApplicationViewSet`, `TestDepartmentPlanViewSetMyDepartmentPlan`, `ApplicationDashboardService`, `StudyGroup`, `test_project_track_viewset.py`, `TestDepartmentPlanViewSetCreate`, `test_import_study_groups_from_contingent.py`, `TeamLobbyService`, `RegistrationRequestCreateSerializer`, `institute_access.py`, `ProjectService`, `ProjectApplicationService`, `test_project_track_service.py`, `test_team_lobby_viewset.py`, `TeamLobby.py`, `ProjectTrackService`, `dto/team_lobby.py`, `TestDepartmentPlanViewSetList`, `UserManagementService`, `StudyGroupService`, `accounts/serializers.py`, `TestProjectApplicationListSemesterFilter`, `showcase/urls.py`, `test_application_dashboard_viewset.py`, `AccountsApiTests`, `TeamSemester`, `TestProjectViewSet`, `TestProjectApplicationNewFieldsCreateUpdate`, `accounts/admin.py`, `Command`, `ProjectApplicationCreateDTO`, `accounts/views.py`, `test_institute_access.py`, `TestSemesterAssignViewSet`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 478 inferred relationships involving `make_user()` (e.g. with `.test_can_list_users_admin()` and `.test_can_list_users_denied_for_regular_user()`) actually correct?**
  _`make_user()` has 478 INFERRED edges - model-reasoned connections that need verification._
- **Are the 42 inferred relationships involving `User` (e.g. with `UserManagementDomain` and `UserListDTO`) actually correct?**
  _`User` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `Department` (e.g. with `UserManagementDomain` and `Command`) actually correct?**
  _`Department` has 72 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `ProjectApplicationService` (e.g. with `ProjectApplicationViewSet` and `SemesterViewSet`) actually correct?**
  _`ProjectApplicationService` has 20 INFERRED edges - model-reasoned connections that need verification._