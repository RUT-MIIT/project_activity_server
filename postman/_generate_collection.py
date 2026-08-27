"""Генератор Postman collection + environments для Project Activity API."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

LOGIN_TEST = """\
const json = pm.response.json();
if (json.access && json.user && json.user.role) {
    const role = json.user.role;
    const key = 'token_' + role;
    pm.environment.set(key, json.access);
    pm.environment.set('token', json.access);
    console.log('Saved access to ' + key + ' and token');
}
"""

USE_TOKEN_PRE = """\
const role = pm.variables.get('roleToUse');
const key = 'token_' + role;
const value = pm.environment.get(key);
if (!value) {
    throw new Error('Environment variable ' + key + ' is empty. Login as ' + role + ' first.');
}
pm.environment.set('token', value);
console.log('Active token set from ' + key);
"""


def bearer_inherit() -> dict:
    return {
        "type": "bearer",
        "bearer": [{"key": "token", "value": "{{token}}", "type": "string"}],
    }


def noauth() -> dict:
    return {"type": "noauth"}


def url(raw: str, query: list[dict] | None = None) -> dict:
    """Собрать объект url Postman из raw URL с {{baseUrl}}."""
    path_part = raw.replace("{{baseUrl}}", "").lstrip("/")
    clean_path = path_part.split("?")[0]
    segments = [s for s in clean_path.split("/") if s]
    # DRF uses trailing slash; append empty string to mirror "/resource/"
    path_segments = segments + [""] if segments else [""]

    result: dict = {
        "raw": raw if "?" in raw or not query else raw,
        "host": ["{{baseUrl}}"],
        "path": path_segments,
    }

    if query is not None:
        result["query"] = query
        # rebuild raw with query
        enabled = [q for q in query if not q.get("disabled")]
        if enabled:
            qs = "&".join(f"{q['key']}={q['value']}" for q in enabled)
            base = "{{baseUrl}}/" + "/".join(segments) + "/"
            result["raw"] = f"{base}?{qs}"
        else:
            result["raw"] = "{{baseUrl}}/" + "/".join(segments) + "/"
    elif "?" in raw:
        # parse query from raw
        result["raw"] = raw
        result["query"] = []
        _, qs = raw.split("?", 1)
        for pair in qs.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                result["query"].append({"key": k, "value": v})
    else:
        result["raw"] = "{{baseUrl}}/" + "/".join(segments) + "/"

    return result


def req(
    name: str,
    method: str,
    path: str,
    *,
    description: str = "",
    body: str | None = None,
    query: list[dict] | None = None,
    auth: dict | None = None,
    test: str | None = None,
    prerequest: str | None = None,
) -> dict:
    raw = f"{{{{baseUrl}}}}{path}"
    headers = []
    request: dict = {
        "method": method,
        "header": headers,
        "url": url(raw, query=query),
        "description": description,
    }
    if body is not None:
        headers.append({"key": "Content-Type", "value": "application/json"})
        request["body"] = {"mode": "raw", "raw": body}
    if auth is not None:
        request["auth"] = auth

    item: dict = {"name": name, "request": request}
    events = []
    if prerequest:
        events.append(
            {
                "listen": "prerequest",
                "script": {"type": "text/javascript", "exec": prerequest.split("\n")},
            }
        )
    if test:
        events.append(
            {
                "listen": "test",
                "script": {"type": "text/javascript", "exec": test.split("\n")},
            }
        )
    if events:
        item["event"] = events
    return item


def folder(name: str, items: list, description: str = "") -> dict:
    f: dict = {"name": name, "item": items}
    if description:
        f["description"] = description
    return f


def env_file(name: str, env_id: str, values: list[dict]) -> dict:
    return {
        "id": env_id,
        "name": name,
        "values": [
            {
                "key": v["key"],
                "value": v.get("value", ""),
                "type": "default",
                "enabled": True,
            }
            for v in values
        ],
        "_postman_variable_scope": "environment",
    }


# --- Auth ---
auth_folder = folder(
    "Auth",
    [
        req(
            "Login (admin)",
            "POST",
            "/api/accounts/login/",
            description=(
                "JWT login. Ответ: {access, refresh, user}.\n"
                "Test-script сохраняет access в token_admin и token.\n"
                "Body: email, password (credentials admin)."
            ),
            body='{\n  "email": "{{adminEmail}}",\n  "password": "{{adminPassword}}"\n}',
            auth=noauth(),
            test=LOGIN_TEST,
        ),
        req(
            "Login (cpds)",
            "POST",
            "/api/accounts/login/",
            description="Login под ролью cpds → token_cpds + token.",
            body='{\n  "email": "{{cpdsEmail}}",\n  "password": "{{cpdsPassword}}"\n}',
            auth=noauth(),
            test=LOGIN_TEST,
        ),
        req(
            "Login (institute_validator)",
            "POST",
            "/api/accounts/login/",
            description="Login под ролью institute_validator → token_institute_validator + token.",
            body='{\n  "email": "{{validatorEmail}}",\n  "password": "{{validatorPassword}}"\n}',
            auth=noauth(),
            test=LOGIN_TEST,
        ),
        req(
            "Use token: admin",
            "GET",
            "/api/accounts/user/",
            description="Копирует token_admin → token и проверяет /user/.",
            prerequest="pm.variables.set('roleToUse', 'admin');\n" + USE_TOKEN_PRE,
        ),
        req(
            "Use token: cpds",
            "GET",
            "/api/accounts/user/",
            description="Копирует token_cpds → token и проверяет /user/.",
            prerequest="pm.variables.set('roleToUse', 'cpds');\n" + USE_TOKEN_PRE,
        ),
        req(
            "Use token: institute_validator",
            "GET",
            "/api/accounts/user/",
            description="Копирует token_institute_validator → token и проверяет /user/.",
            prerequest=(
                "pm.variables.set('roleToUse', 'institute_validator');\n"
                + USE_TOKEN_PRE
            ),
        ),
        req(
            "User me",
            "GET",
            "/api/accounts/user/",
            description="Текущий пользователь. Auth: JWT. Response: UserSerializer.",
        ),
        req(
            "Password reset",
            "POST",
            "/api/accounts/password/reset/",
            description="Публичный. Body: {email}.",
            body='{\n  "email": "{{adminEmail}}"\n}',
            auth=noauth(),
        ),
        req(
            "Password reset confirm",
            "POST",
            "/api/accounts/password/reset/confirm/",
            description="Публичный. Body: {uid, token, new_password}.",
            body='{\n  "uid": "",\n  "token": "",\n  "new_password": ""\n}',
            auth=noauth(),
        ),
        req(
            "Password change",
            "POST",
            "/api/accounts/password/change/",
            description="Auth: JWT. Body: {current_password, new_password}.",
            body='{\n  "current_password": "",\n  "new_password": ""\n}',
        ),
    ],
    description="Логин JWT и переключение активного Bearer {{token}}.",
)

# --- Accounts ---
accounts_folder = folder(
    "Accounts",
    [
        folder(
            "Departments",
            [
                req(
                    "List departments",
                    "GET",
                    "/api/accounts/departments/",
                    description="Список подразделений. Публичный (AllowAny).",
                    auth=noauth(),
                ),
                req(
                    "Get department",
                    "GET",
                    "/api/accounts/departments/{{departmentId}}/",
                    description="Детали подразделения. Auth: JWT.",
                ),
            ],
        ),
        folder(
            "Roles",
            [
                req(
                    "List roles",
                    "GET",
                    "/api/accounts/roles/",
                    description="Активные роли. Auth: JWT. {code, name, requires_department, is_active}.",
                ),
                req(
                    "Get role",
                    "GET",
                    "/api/accounts/roles/{{roleCode}}/",
                    description="Роль по code. Auth: JWT.",
                ),
            ],
        ),
        folder(
            "Semesters",
            [
                req(
                    "List semesters",
                    "GET",
                    "/api/accounts/semesters/",
                    description="Список семестров. Auth: JWT (любая роль).",
                ),
                req(
                    "Get semester",
                    "GET",
                    "/api/accounts/semesters/{{semesterId}}/",
                    description="Детали семестра.",
                ),
                req(
                    "Create semester",
                    "POST",
                    "/api/accounts/semesters/",
                    description="Создание. Роли: admin/cpds/staff. Body: {code, name, position, academic_year_id?}",
                    body='{\n  "code": "2026-1",\n  "name": "Весна 2026",\n  "position": 1\n}',
                ),
                req(
                    "Update semester (PATCH)",
                    "PATCH",
                    "/api/accounts/semesters/{{semesterId}}/",
                    description="Частичное обновление. Роли: admin/cpds/staff.",
                    body='{\n  "name": "Обновлённый семестр",\n  "position": 2\n}',
                ),
                req(
                    "Delete semester",
                    "DELETE",
                    "/api/accounts/semesters/{{semesterId}}/",
                    description="Удаление. Роли: admin/cpds/staff.",
                ),
            ],
        ),
        folder(
            "Users",
            [
                req(
                    "List users",
                    "GET",
                    "/api/accounts/users/",
                    description=(
                        "Роли: admin, cpds, institute_validator (+ staff).\n"
                        "Query: include_authored_projects=true.\n"
                        "institute_validator — только свой институт; admin/cpds — все кроме admin/staff."
                    ),
                    query=[
                        {
                            "key": "include_authored_projects",
                            "value": "true",
                            "disabled": True,
                            "description": "Добавить authored_projects[]",
                        }
                    ],
                ),
                req(
                    "Get user",
                    "GET",
                    "/api/accounts/users/{{userId}}/",
                    description="Детали пользователя. Scope как у list.",
                    query=[
                        {
                            "key": "include_authored_projects",
                            "value": "true",
                            "disabled": True,
                        }
                    ],
                ),
                req(
                    "Update user (PATCH)",
                    "PATCH",
                    "/api/accounts/users/{{userId}}/",
                    description=(
                        "Только admin/cpds. Поля: role (код), department_id, email, phone.\n"
                        "Нельзя назначить role=admin. institute_validator → 403."
                    ),
                    body='{\n  "role": "department_validator",\n  "department_id": {{departmentId}}\n}',
                ),
            ],
        ),
        folder(
            "Registration requests",
            [
                req(
                    "Create registration request",
                    "POST",
                    "/api/accounts/registration-requests/",
                    description="Публичная заявка на регистрацию.",
                    body=(
                        '{\n  "last_name": "Иванов",\n  "first_name": "Иван",\n'
                        '  "middle_name": "Иванович",\n  "department": {{departmentId}},\n'
                        '  "email": "new.user@example.com",\n  "phone": "+79001234567",\n'
                        '  "comment": ""\n}'
                    ),
                    auth=noauth(),
                ),
                req(
                    "List registration requests",
                    "GET",
                    "/api/accounts/registration-requests/",
                    description="Manage: admin/cpds/staff. Query: status=submitted|approved|rejected.",
                    query=[
                        {
                            "key": "status",
                            "value": "submitted",
                            "disabled": True,
                        }
                    ],
                ),
                req(
                    "Get registration request",
                    "GET",
                    "/api/accounts/registration-requests/{{registrationId}}/",
                    description="Детали заявки. Manage: admin/cpds/staff.",
                ),
                req(
                    "Approve registration",
                    "POST",
                    "/api/accounts/registration-requests/{{registrationId}}/approve/",
                    description="AdminUser или cpds. Body: {role_id, department_id?}",
                    body='{\n  "role_id": "user",\n  "department_id": {{departmentId}}\n}',
                ),
                req(
                    "Reject registration",
                    "POST",
                    "/api/accounts/registration-requests/{{registrationId}}/reject/",
                    description="AdminUser или cpds. Body: {reason?}",
                    body='{\n  "reason": "Недостаточно данных"\n}',
                ),
            ],
        ),
    ],
)

# --- Teams ---
teams_folder = folder(
    "Teams",
    [
        folder(
            "Teams CRUD",
            [
                req(
                    "List teams",
                    "GET",
                    "/api/teams/teams/",
                    description="Список постоянных команд. Auth: JWT.",
                ),
                req(
                    "My teams",
                    "GET",
                    "/api/teams/teams/my/",
                    description="Команды текущего пользователя в семестре. Обязателен semester_id (id | actual | next).",
                    query=[
                        {
                            "key": "semester_id",
                            "value": "actual",
                            "disabled": False,
                        }
                    ],
                ),
                req(
                    "Create team",
                    "POST",
                    "/api/teams/teams/",
                    description="Body: {name, description?, home_study_group_id?}",
                    body='{\n  "name": "Команда Alpha",\n  "description": "Описание",\n  "home_study_group_id": {{groupId}}\n}',
                ),
                req(
                    "Get team",
                    "GET",
                    "/api/teams/teams/{{teamId}}/",
                    description="Постоянные поля команды.",
                ),
                req(
                    "Update team (PATCH)",
                    "PATCH",
                    "/api/teams/teams/{{teamId}}/",
                    description="Write: капитан любого семестра / admin / cpds / staff.",
                    body='{\n  "name": "Команда Beta",\n  "description": "Обновлено"\n}',
                ),
                req(
                    "Delete team",
                    "DELETE",
                    "/api/teams/teams/{{teamId}}/",
                    description="Write: капитан / admin / cpds / staff.",
                ),
            ],
        ),
        folder(
            "Team semesters",
            [
                req(
                    "List team semesters",
                    "GET",
                    "/api/teams/team-semesters/",
                    description="Query: semester_id=id|actual|next (опционально).",
                    query=[
                        {
                            "key": "semester_id",
                            "value": "actual",
                            "disabled": True,
                        }
                    ],
                ),
                req(
                    "My team semesters",
                    "GET",
                    "/api/teams/team-semesters/my/",
                    description="Обязателен semester_id.",
                    query=[
                        {
                            "key": "semester_id",
                            "value": "actual",
                            "disabled": False,
                        }
                    ],
                ),
                req(
                    "Create team semester",
                    "POST",
                    "/api/teams/team-semesters/",
                    description="Body: {team_id, semester_id, captain_id?, mentor_id?, project_application_id?}",
                    body='{\n  "team_id": {{teamId}},\n  "semester_id": {{semesterId}}\n}',
                ),
                req(
                    "Get team semester",
                    "GET",
                    "/api/teams/team-semesters/{{teamSemesterId}}/",
                    description="Детали с members[].",
                ),
                req(
                    "Add member",
                    "POST",
                    "/api/teams/team-semesters/{{teamSemesterId}}/members/",
                    description='Body: {user_id, role?: "leader"|"member"}. Write: капитан / admin / cpds.',
                    body='{\n  "user_id": {{userId}},\n  "role": "member"\n}',
                ),
                req(
                    "Remove member",
                    "DELETE",
                    "/api/teams/team-semesters/{{teamSemesterId}}/members/{{memberId}}/",
                    description="Нельзя удалить leader.",
                ),
            ],
        ),
        folder(
            "Directions",
            [
                req(
                    "List directions",
                    "GET",
                    "/api/teams/directions/",
                    description="Auth: JWT. institute_validator — фильтр по своим институтам.",
                ),
                req(
                    "Get direction",
                    "GET",
                    "/api/teams/directions/{{directionCode}}/",
                    description="lookup по code. {code, level, name}.",
                ),
            ],
        ),
        folder(
            "Lobby (student)",
            [
                req(
                    "Get lobby",
                    "GET",
                    "/api/teams/lobby/",
                    description=(
                        "Лобби формирования команд. Семестр: actual по умолчанию. "
                        "teams — все команды учебной группы (без фильтра по треку); "
                        "tracks — треки + команды с привязкой к треку; "
                        "myTeam включает members (id, full_name, role); "
                        "заявки/приглашения — если студент без команды."
                    ),
                    query=[
                        {
                            "key": "semester_id",
                            "value": "actual",
                            "disabled": False,
                        }
                    ],
                ),
                req(
                    "Create team in lobby",
                    "POST",
                    "/api/teams/lobby/teams/",
                    description=(
                        "Body: {name, track_id?}. track_id можно не указывать; "
                        "если группе доступен ровно один трек — он проставится сам."
                    ),
                    body='{\n  "name": "Команда Alpha",\n  "track_id": {{trackId}}\n}',
                ),
                req(
                    "Create join request",
                    "POST",
                    "/api/teams/lobby/teams/{{teamSemesterId}}/join-requests/",
                    description="Заявка на вступление в команду (team semester id).",
                ),
                req(
                    "Accept invitation",
                    "POST",
                    "/api/teams/lobby/invitations/{{invitationId}}/accept/",
                    description="Принять приглашение; остальные заявки/приглашения → obsolete.",
                ),
                req(
                    "Reject invitation",
                    "POST",
                    "/api/teams/lobby/invitations/{{invitationId}}/reject/",
                    description="Отклонить приглашение.",
                ),
            ],
        ),
        folder(
            "My team (student)",
            [
                req(
                    "Get my team",
                    "GET",
                    "/api/teams/my-team/",
                    description="Моя команда: состав; у капитана — заявки и приглашения. Лог — отдельно.",
                    query=[
                        {
                            "key": "semester_id",
                            "value": "actual",
                            "disabled": True,
                        }
                    ],
                ),
                req(
                    "Get my team event log",
                    "GET",
                    "/api/teams/my-team/event-log/",
                    description="Пагинированный лог событий (page_size=50). Query: semester_id, page.",
                    query=[
                        {
                            "key": "semester_id",
                            "value": "actual",
                            "disabled": True,
                        },
                        {
                            "key": "page",
                            "value": "1",
                            "disabled": True,
                        },
                    ],
                ),
                req(
                    "Approve join request",
                    "POST",
                    "/api/teams/my-team/join-requests/{{joinRequestId}}/approve/",
                    description='Капитан. Body: {role: "member"}.',
                    body='{\n  "role": "member"\n}',
                ),
                req(
                    "Reject join request",
                    "POST",
                    "/api/teams/my-team/join-requests/{{joinRequestId}}/reject/",
                    description="Капитан отклоняет заявку.",
                ),
                req(
                    "Invite classmate",
                    "POST",
                    "/api/teams/my-team/invitations/",
                    description='Капитан. Body: {user_id, role: "member"}.',
                    body='{\n  "user_id": {{userId}},\n  "role": "member"\n}',
                ),
                req(
                    "Kick member",
                    "DELETE",
                    "/api/teams/my-team/members/{{userId}}/",
                    description="Капитан исключает участника (не себя).",
                ),
                req(
                    "Leave team",
                    "POST",
                    "/api/teams/my-team/leave/",
                    description="Участник покидает команду (не капитан).",
                ),
                req(
                    "Confirm composition",
                    "POST",
                    "/api/teams/my-team/confirm-composition/",
                    description="Капитан: forming → assembled. Состав в min..max трека.",
                ),
                req(
                    "Delete my team",
                    "DELETE",
                    "/api/teams/my-team/",
                    description="Капитан удаляет команду (в составе только он).",
                ),
            ],
        ),
        folder(
            "Study groups",
            [
                req(
                    "List study groups",
                    "GET",
                    "/api/teams/study-groups/",
                    description="Query: is_end=true|false. institute_validator — свой институт.",
                    query=[
                        {
                            "key": "is_end",
                            "value": "false",
                            "disabled": True,
                        }
                    ],
                ),
                req(
                    "Get study group",
                    "GET",
                    "/api/teams/study-groups/{{groupId}}/",
                    description="Детали с direction, institute и mentor.",
                ),
                req(
                    "My study group",
                    "GET",
                    "/api/teams/study-groups/my/",
                    description=(
                        "Группа текущего студента: данные группы, наставник, "
                        "список контингента с is_registered. "
                        "Опционально semester_id — команда одногруппника в members[].team. "
                        "Роль: student."
                    ),
                    query=[
                        {
                            "key": "semester_id",
                            "value": "actual",
                            "disabled": True,
                        }
                    ],
                ),
            ],
        ),
    ],
)

# --- Showcase: Project Tracks (from existing collection) ---
tracks_crud = folder(
    "CRUD",
    [
        req(
            "List tracks",
            "GET",
            "/api/showcase/project-tracks/",
            description=(
                "Список треков. Обязателен semester_id (id | actual | next).\n"
                "Роли: admin, cpds, institute_validator, staff."
            ),
            query=[
                {
                    "key": "semester_id",
                    "value": "{{semesterId}}",
                    "description": "Обязательный. ID или actual/next",
                },
                {
                    "key": "department_id",
                    "value": "{{departmentId}}",
                    "disabled": True,
                    "description": "Опционально",
                },
                {
                    "key": "institute_code",
                    "value": "{{instituteCode}}",
                    "disabled": True,
                    "description": "Опционально",
                },
            ],
        ),
        req(
            "Create track",
            "POST",
            "/api/showcase/project-tracks/",
            description=(
                "Создание. Поля: name*, department_id*, semester_id*, description?, "
                "minTeamMembers?, maxTeamMembers?\n"
                "author_id из текущего пользователя. Лимиты по умолчанию: 4 / 7."
            ),
            body=(
                '{\n  "name": "Трек ИЭУ",\n  "description": "Описание трека",\n'
                '  "department_id": {{departmentId}},\n  "semester_id": {{semesterId}},\n'
                '  "minTeamMembers": 4,\n  "maxTeamMembers": 7\n}'
            ),
        ),
        req(
            "Get track",
            "GET",
            "/api/showcase/project-tracks/{{trackId}}/",
            description=(
                "Детали с groups[], applications[], minTeamMembers, maxTeamMembers."
            ),
        ),
        req(
            "Update track (PATCH)",
            "PATCH",
            "/api/showcase/project-tracks/{{trackId}}/",
            description=(
                "Опциональные поля: name, description, department_id, semester_id, "
                "minTeamMembers, maxTeamMembers. Лимиты сохраняются на треке и "
                "применяются ко всем заявкам трека."
            ),
            body='{\n  "name": "Обновлённый трек",\n  "description": "Новое описание",\n  "minTeamMembers": 2,\n  "maxTeamMembers": 5\n}',
        ),
        req(
            "Delete track",
            "DELETE",
            "/api/showcase/project-tracks/{{trackId}}/",
            description="Каскадно удаляет связи. Ответ 204.",
        ),
    ],
)

tracks_groups = folder(
    "Groups in track",
    [
        req(
            "Add groups to track",
            "POST",
            "/api/showcase/project-tracks/{{trackId}}/groups/",
            description="Body: {group_ids}. Дубликаты пропускаются. Ответ — полный трек.",
            body='{\n  "group_ids": [1, 2]\n}',
        ),
        req(
            "Remove group from track",
            "DELETE",
            "/api/showcase/project-tracks/{{trackId}}/groups/{{groupId}}/",
            description="Удалить группу из трека. Ответ — полный трек.",
        ),
    ],
)

tracks_apps = folder(
    "Applications in track",
    [
        req(
            "Add applications to track",
            "POST",
            "/api/showcase/project-tracks/{{trackId}}/applications/",
            description="Только approved заявки, semester совпадает. Body: {application_ids}.",
            body='{\n  "application_ids": [1, 2]\n}',
        ),
        req(
            "Remove application from track",
            "DELETE",
            "/api/showcase/project-tracks/{{trackId}}/applications/{{applicationId}}/",
            description="Удалить заявку из трека. Ответ — полный трек.",
        ),
    ],
)

tracks_aux = folder(
    "Auxiliary (groups / projects / statistics)",
    [
        req(
            "List study groups (via tracks)",
            "GET",
            "/api/showcase/project-tracks/groups/",
            description="Группы с assigned_projects_count. semester_id обязателен.",
            query=[
                {"key": "semester_id", "value": "{{semesterId}}"},
                {"key": "institute_code", "value": "{{instituteCode}}"},
            ],
        ),
        req(
            "Get study group detail (via tracks)",
            "GET",
            "/api/showcase/project-tracks/groups/{{groupId}}/",
            description="Группа + projects[].",
            query=[
                {"key": "semester_id", "value": "{{semesterId}}"},
                {
                    "key": "institute_code",
                    "value": "{{instituteCode}}",
                    "disabled": True,
                },
            ],
        ),
        req(
            "List projects (via tracks)",
            "GET",
            "/api/showcase/project-tracks/projects/",
            description="Одобренные заявки с assigned_groups_count.",
            query=[
                {"key": "semester_id", "value": "{{semesterId}}"},
                {"key": "institute_code", "value": "{{instituteCode}}"},
            ],
        ),
        req(
            "Get project detail (via tracks)",
            "GET",
            "/api/showcase/project-tracks/projects/{{applicationId}}/",
            description="Заявка + groups[].",
            query=[
                {"key": "semester_id", "value": "{{semesterId}}"},
                {"key": "institute_code", "value": "{{instituteCode}}"},
            ],
        ),
        req(
            "Statistics",
            "GET",
            "/api/showcase/project-tracks/statistics/",
            description=(
                "Статистика распределения. Без institute_code (admin/cpds): "
                "{overall, by_institute}."
            ),
            query=[
                {"key": "semester_id", "value": "{{semesterId}}"},
                {
                    "key": "institute_code",
                    "value": "{{instituteCode}}",
                    "description": "Без параметра — агрегат (admin/cpds)",
                },
            ],
        ),
    ],
)

tracks_folder = folder(
    "Project Tracks",
    [tracks_crud, tracks_groups, tracks_apps, tracks_aux],
    description="CRUD треков. Роли: admin, cpds, institute_validator, staff.",
)

# --- Project Applications ---
app_create_body = """\
{
  "title": "Система управления проектными заявками",
  "company": "ООО Тестовая компания",
  "company_contacts": "ivan@example.com, +79001234567",
  "problem_holder": "Кафедра ИТ",
  "goal": "Автоматизировать процесс согласования",
  "barrier": "Нет единой системы",
  "existing_solutions": "Таблицы Excel",
  "description": "Описание проекта",
  "target_institutes": ["{{instituteCode}}"],
  "tags": [],
  "needs_consultation": false,
  "is_internal_customer": false,
  "semester_id": {{semesterId}},
  "main_department_id": {{departmentId}}
}"""

applications_folder = folder(
    "Project Applications",
    [
        folder(
            "CRUD",
            [
                req(
                    "List my applications (list)",
                    "GET",
                    "/api/showcase/project-applications/",
                    description="Пагинация (20). Query: semester_id?, page?. Заявки текущего пользователя.",
                    query=[
                        {
                            "key": "semester_id",
                            "value": "{{semesterId}}",
                            "disabled": True,
                        },
                        {"key": "page", "value": "1", "disabled": True},
                    ],
                ),
                req(
                    "Create application",
                    "POST",
                    "/api/showcase/project-applications/",
                    description=(
                        "Обязательные: title, company, company_contacts, problem_holder, "
                        "goal, barrier, existing_solutions. Auth: JWT. 201."
                    ),
                    body=app_create_body,
                ),
                req(
                    "Get application",
                    "GET",
                    "/api/showcase/project-applications/{{applicationId}}/",
                    description="Полная заявка + available_actions[].",
                ),
                req(
                    "Update application (PATCH)",
                    "PATCH",
                    "/api/showcase/project-applications/{{applicationId}}/",
                    description="Все поля опциональны.",
                    body='{\n  "title": "Обновлённое название",\n  "goal": "Новая цель"\n}',
                ),
                req(
                    "Delete application",
                    "DELETE",
                    "/api/showcase/project-applications/{{applicationId}}/",
                    description="Удаление заявки (ModelViewSet destroy).",
                ),
                req(
                    "Create simple (public)",
                    "POST",
                    "/api/showcase/project-applications/simple/",
                    description="Без авторизации. is_external=true. Те же обязательные поля.",
                    body=app_create_body,
                    auth=noauth(),
                ),
            ],
        ),
        folder(
            "Workflow",
            [
                req(
                    "Approve",
                    "POST",
                    "/api/showcase/project-applications/{{applicationId}}/approve/",
                    description="Одобрение. Права по ApplicationCapabilities (роль + статус).",
                ),
                req(
                    "Reject",
                    "POST",
                    "/api/showcase/project-applications/{{applicationId}}/reject/",
                    description="Отклонение. Body: {reason?} optional.",
                    body='{\n  "reason": "Не соответствует требованиям"\n}',
                ),
                req(
                    "Request changes",
                    "POST",
                    "/api/showcase/project-applications/{{applicationId}}/request_changes/",
                    description="Отправка на доработку.",
                ),
                req(
                    "Transfer to institute",
                    "POST",
                    "/api/showcase/project-applications/{{applicationId}}/transfer_to_institute/",
                    description='Body: {"code": "INST_CODE"} обязателен.',
                    body='{\n  "code": "{{instituteCode}}"\n}',
                ),
                req(
                    "Return by author",
                    "POST",
                    "/api/showcase/project-applications/{{applicationId}}/return_by_author/",
                    description="Отзыв автором → returned_author.",
                ),
            ],
        ),
        folder(
            "Lists",
            [
                req(
                    "By status",
                    "GET",
                    "/api/showcase/project-applications/by_status/",
                    description="Только admin/moderator. Query: status*, semester_id?",
                    query=[
                        {"key": "status", "value": "created"},
                        {
                            "key": "semester_id",
                            "value": "{{semesterId}}",
                            "disabled": True,
                        },
                    ],
                ),
                req(
                    "Recent",
                    "GET",
                    "/api/showcase/project-applications/recent/",
                    description="Только admin/moderator. Query: limit? (default 10), semester_id?",
                    query=[
                        {"key": "limit", "value": "10", "disabled": True},
                        {
                            "key": "semester_id",
                            "value": "{{semesterId}}",
                            "disabled": True,
                        },
                    ],
                ),
                req(
                    "My applications",
                    "GET",
                    "/api/showcase/project-applications/my_applications/",
                    description="Заявки текущего пользователя.",
                    query=[
                        {
                            "key": "semester_id",
                            "value": "{{semesterId}}",
                            "disabled": True,
                        }
                    ],
                ),
                req(
                    "Coordination",
                    "GET",
                    "/api/showcase/project-applications/coordination/",
                    description="Заявки для координации (причастные, не approved/rejected).",
                    query=[
                        {
                            "key": "semester_id",
                            "value": "{{semesterId}}",
                            "disabled": True,
                        }
                    ],
                ),
                req(
                    "External",
                    "GET",
                    "/api/showcase/project-applications/external/",
                    description="Внешние заявки (is_external=true). Auth: JWT.",
                    query=[
                        {"key": "status", "value": "created", "disabled": True},
                        {
                            "key": "semester_id",
                            "value": "{{semesterId}}",
                            "disabled": True,
                        },
                    ],
                ),
            ],
        ),
        folder(
            "Comments & logs",
            [
                req(
                    "Status logs",
                    "GET",
                    "/api/showcase/project-applications/{{applicationId}}/status_logs/",
                    description="История смены статусов.",
                ),
                req(
                    "List comments",
                    "GET",
                    "/api/showcase/project-applications/{{applicationId}}/comments/",
                    description="Все комментарии к заявке.",
                ),
                req(
                    "Add comment",
                    "POST",
                    "/api/showcase/project-applications/{{applicationId}}/add_comment/",
                    description='Body: {"field": "goal", "text": "..."}.',
                    body='{\n  "field": "goal",\n  "text": "Уточните формулировку цели"\n}',
                ),
            ],
        ),
    ],
)

dashboard_folder = folder(
    "Application Dashboard",
    [
        req(
            "Get dashboard",
            "GET",
            "/api/showcase/project-applications/dashboard/",
            description=(
                "Дашборд заявок. Роли: admin, cpds, institute_validator, staff.\n"
                "Query: semester_id*, institute_code?, department_id?, status?, "
                "application_type? (all|external|internal), days? (default 30, max 366)."
            ),
            query=[
                {"key": "semester_id", "value": "{{semesterId}}"},
                {
                    "key": "institute_code",
                    "value": "{{instituteCode}}",
                    "disabled": True,
                },
                {
                    "key": "department_id",
                    "value": "{{departmentId}}",
                    "disabled": True,
                },
                {
                    "key": "status",
                    "value": "pending",
                    "disabled": True,
                    "description": "approved,rejected,pending,in_progress (через запятую)",
                },
                {
                    "key": "application_type",
                    "value": "all",
                    "disabled": True,
                },
                {"key": "days", "value": "30", "disabled": True},
            ],
        ),
    ],
)

tags_folder = folder(
    "Tags",
    [
        req(
            "List tags",
            "GET",
            "/api/showcase/tags/",
            description="Публичный. {id, name, category, is_base}.",
            auth=noauth(),
        ),
        req(
            "Get tag",
            "GET",
            "/api/showcase/tags/{{tagId}}/",
            description="Публичный. TagReadDTO с departments[].",
            auth=noauth(),
        ),
        req(
            "Create tag",
            "POST",
            "/api/showcase/tags/",
            description="Manage: admin/cpds/institute_validator/staff.",
            body='{\n  "name": "ИИ",\n  "category": "tech",\n  "department_id": {{departmentId}}\n}',
        ),
        req(
            "Update tag (PATCH)",
            "PATCH",
            "/api/showcase/tags/{{tagId}}/",
            description="Manage roles.",
            body='{\n  "name": "Искусственный интеллект"\n}',
        ),
        req(
            "Delete tag",
            "DELETE",
            "/api/showcase/tags/{{tagId}}/",
            description="Manage roles. 204.",
        ),
        req(
            "Attach department",
            "POST",
            "/api/showcase/tags/{{tagId}}/attach-department/",
            description="Body: {department_id}.",
            body='{\n  "department_id": {{departmentId}}\n}',
        ),
        req(
            "Detach department",
            "POST",
            "/api/showcase/tags/{{tagId}}/detach-department/",
            description="Body: {department_id}.",
            body='{\n  "department_id": {{departmentId}}\n}',
        ),
    ],
)

institutes_folder = folder(
    "Institutes",
    [
        req(
            "List institutes",
            "GET",
            "/api/showcase/institutes/",
            description="Публичный. Активные институты {code, name, department_id}.",
            auth=noauth(),
        ),
        req(
            "Get institute",
            "GET",
            "/api/showcase/institutes/{{instituteCode}}/",
            description="lookup по code. Публичный.",
            auth=noauth(),
        ),
    ],
)

statuses_folder = folder(
    "Application statuses",
    [
        req(
            "List statuses",
            "GET",
            "/api/showcase/application-statuses/",
            description="Auth: JWT. [{code, name}].",
        ),
        req(
            "Get status",
            "GET",
            "/api/showcase/application-statuses/{{statusCode}}/",
            description="lookup по code.",
        ),
    ],
)

dept_plans_folder = folder(
    "Department plans",
    [
        req(
            "Create / upsert plan",
            "POST",
            "/api/showcase/department-plans/",
            description="Body: {department_id, semester_id, plan}. Auth: JWT.",
            body='{\n  "department_id": {{departmentId}},\n  "semester_id": {{semesterId}},\n  "plan": 10\n}',
        ),
        req(
            "List plans",
            "GET",
            "/api/showcase/department-plans/",
            description="Query: semester_id*, institute_code?. Статистика по подразделениям.",
            query=[
                {"key": "semester_id", "value": "{{semesterId}}"},
                {
                    "key": "institute_code",
                    "value": "{{instituteCode}}",
                    "disabled": True,
                },
            ],
        ),
        req(
            "My department plan",
            "GET",
            "/api/showcase/department-plans/my-department-plan/",
            description="План подразделения текущего пользователя. Query: semester_id*.",
            query=[{"key": "semester_id", "value": "{{semesterId}}"}],
        ),
    ],
)

projects_folder = folder(
    "Projects",
    [
        req(
            "List approved projects",
            "GET",
            "/api/showcase/projects/",
            description=(
                "Одобренные заявки. Роли: admin, cpds, institute_validator, staff.\n"
                "Query: semester_id? (id|actual|next)."
            ),
            query=[
                {
                    "key": "semester_id",
                    "value": "{{semesterId}}",
                    "disabled": True,
                }
            ],
        ),
    ],
)

showcase_semesters = folder(
    "Semesters (showcase)",
    [
        req(
            "Assign empty applications to semester",
            "POST",
            "/api/showcase/semesters/{{semesterId}}/assign-empty-applications/",
            description="Назначить семестр всем заявкам без semester_id. Роли: admin, cpds. 204.",
        ),
    ],
)

showcase_folder = folder(
    "Showcase",
    [
        tracks_folder,
        applications_folder,
        dashboard_folder,
        tags_folder,
        institutes_folder,
        statuses_folder,
        dept_plans_folder,
        projects_folder,
        showcase_semesters,
    ],
    description="API витрины: треки, заявки, справочники, дашборд.",
)

collection = {
    "info": {
        "name": "Project Activity API",
        "description": (
            "Полный API: accounts + teams + showcase.\n\n"
            "## Environments\n"
            "- **local**: baseUrl = http://localhost:8000\n"
            "- **prod**: baseUrl = https://pd.emiit.ru\n\n"
            "## Авторизация\n"
            "Collection-level: `Authorization: Bearer {{token}}`.\n\n"
            "Переменные ролей: `token_admin`, `token_cpds`, `token_institute_validator`.\n"
            "1. Выполните Login (admin/cpds/institute_validator) — test-script сохранит access.\n"
            "2. Или Use token: … — скопирует нужный token_* → token.\n"
            "3. Публичные запросы помечены noauth.\n\n"
            "## Префиксы\n"
            "- `/api/accounts/` — auth, users, roles, semesters\n"
            "- `/api/teams/` — teams, directions, study-groups\n"
            "- `/api/showcase/` — applications, tracks, tags, projects"
        ),
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "auth": bearer_inherit(),
    "variable": [
        {"key": "roleCode", "value": "user"},
        {"key": "statusCode", "value": "created"},
        {"key": "directionCode", "value": "09.03.01"},
        {"key": "tagId", "value": "1"},
        {"key": "memberId", "value": "1"},
        {"key": "registrationId", "value": "1"},
    ],
    "item": [auth_folder, accounts_folder, teams_folder, showcase_folder],
}

ENV_KEYS = [
    ("baseUrl",),
    ("token",),
    ("token_admin",),
    ("token_cpds",),
    ("token_institute_validator",),
    ("adminEmail",),
    ("adminPassword",),
    ("cpdsEmail",),
    ("cpdsPassword",),
    ("validatorEmail",),
    ("validatorPassword",),
    ("trackId",),
    ("groupId",),
    ("applicationId",),
    ("semesterId",),
    ("departmentId",),
    ("instituteCode",),
    ("userId",),
    ("teamId",),
    ("tagId",),
    ("memberId",),
    ("registrationId",),
    ("roleCode",),
    ("statusCode",),
    ("directionCode",),
]

local_defaults = {
    "baseUrl": "http://localhost:8000",
    "trackId": "1",
    "groupId": "1",
    "applicationId": "1",
    "semesterId": "1",
    "departmentId": "1",
    "instituteCode": "IEF",
    "userId": "1",
    "teamId": "1",
    "tagId": "1",
    "memberId": "1",
    "registrationId": "1",
    "roleCode": "user",
    "statusCode": "created",
    "directionCode": "09.03.01",
    "adminEmail": "admin@example.com",
    "adminPassword": "",
    "cpdsEmail": "cpds@example.com",
    "cpdsPassword": "",
    "validatorEmail": "validator@example.com",
    "validatorPassword": "",
}

prod_defaults = {
    "baseUrl": "https://pd.emiit.ru",
    "instituteCode": "IEF",
    "roleCode": "user",
    "statusCode": "created",
}


def make_env_values(defaults: dict) -> list[dict]:
    values = []
    for (key,) in ENV_KEYS:
        values.append({"key": key, "value": defaults.get(key, "")})
    return values


def main() -> None:
    coll_path = OUT / "Project_Activity_API.postman_collection.json"
    local_path = OUT / "local.postman_environment.json"
    prod_path = OUT / "prod.postman_environment.json"

    coll_path.write_text(
        json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    local_path.write_text(
        json.dumps(
            env_file(
                "Project Activity — local",
                "project-activity-local",
                make_env_values(local_defaults),
            ),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    prod_path.write_text(
        json.dumps(
            env_file(
                "Project Activity — prod",
                "project-activity-prod",
                make_env_values(prod_defaults),
            ),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # count requests
    def count_req(items: list) -> int:
        n = 0
        for it in items:
            if "request" in it:
                n += 1
            elif "item" in it:
                n += count_req(it["item"])
        return n

    print(f"Collection: {coll_path}")
    print(f"Requests: {count_req(collection['item'])}")
    print(f"Local env: {local_path}")
    print(f"Prod env: {prod_path}")


if __name__ == "__main__":
    main()
