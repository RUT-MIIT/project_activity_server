"""Тесты API статистики проектов ответственного института."""

from __future__ import annotations

from django.db import connection
from django.test.utils import CaptureQueriesContext
import pytest
from rest_framework.test import APIClient

from accounts.models import Department, Semester
from showcase.models import ApplicationInvolvedDepartment, Institute, ProjectApplication
from teams.models import (
    Direction,
    StudyGroup,
    Team,
    TeamSemester,
    TeamSemesterMember,
)

BASE_URL = "/api/teams/institute-responsible/"


def _create_team_semester(
    *,
    group: StudyGroup,
    semester: Semester,
    captain,
    name: str,
    status: str = TeamSemester.Status.FORMING,
    project: ProjectApplication | None = None,
    members: list | None = None,
    mentors: list | None = None,
) -> TeamSemester:
    team = Team.objects.create(name=name, home_study_group=group)
    team_semester = TeamSemester.objects.create(
        team=team,
        semester=semester,
        captain=captain,
        status=status,
        project_application=project,
        mentor=mentors[0] if mentors else None,
    )
    if mentors:
        team_semester.mentors.set(mentors)
    TeamSemesterMember.objects.create(
        team_semester=team_semester,
        user=captain,
        role=TeamSemesterMember.Role.LEADER,
    )
    for member in members or []:
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=member,
            role=TeamSemesterMember.Role.MEMBER,
        )
    return team_semester


def _create_approved_project(
    *,
    semester: Semester,
    statuses,
    department,
    title: str,
    is_internal_customer: bool = False,
    company: str = "Заказчик",
    author=None,
    **extra,
) -> ProjectApplication:
    application = ProjectApplication.objects.create(
        title=title,
        company=company,
        author=author,
        author_lastname=extra.get("author_lastname", "Иванов"),
        author_firstname=extra.get("author_firstname", "Иван"),
        author_email=extra.get("author_email", "author@example.com"),
        semester=semester,
        status=statuses["approved"],
        is_internal_customer=is_internal_customer,
        recommended_teams_count=extra.get("recommended_teams_count", 3),
        print_number=extra.get("print_number", "П-1"),
        problem_holder=extra.get("problem_holder", "Носитель"),
        goal=extra.get("goal", "Цель проекта"),
        barrier=extra.get("barrier", "Барьер"),
        existing_solutions=extra.get("existing_solutions", "Решения"),
        min_team_members=2,
        max_team_members=5,
    )
    ApplicationInvolvedDepartment.objects.create(
        application=application,
        department=department,
    )
    return application


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def semester(db) -> Semester:
    return Semester.objects.create(code="s1", name="Семестр 1", position=1)


@pytest.fixture
def direction(db) -> Direction:
    return Direction.objects.create(
        code="09.03.01",
        name="Информатика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def other_institute(departments) -> Institute:
    other_dept = Department.objects.create(name="Other Parent", short_name="OP")
    return Institute.objects.create(
        code="OTHER",
        name="Other Institute",
        position=2,
        department=other_dept,
    )


@pytest.fixture
def study_group(direction, institute) -> StudyGroup:
    return StudyGroup.objects.create(
        name="Группа 1",
        code="g1",
        direction=direction,
        institute=institute,
        course_number=3,
        is_end=False,
    )


@pytest.fixture
def foreign_group(direction, other_institute) -> StudyGroup:
    return StudyGroup.objects.create(
        name="Чужая группа",
        code="g-other",
        direction=direction,
        institute=other_institute,
        course_number=2,
        is_end=False,
    )


@pytest.mark.django_db
class TestProjectsStatsList:
    def test_student_forbidden(self, roles, make_user, api_client, semester):
        user = make_user(role_code="student", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE_URL}projects/?semester_id={semester.id}")
        assert response.status_code == 403

    def test_missing_semester_returns_400(self, roles, make_user, api_client):
        user = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE_URL}projects/")
        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_list_structure_and_types(
        self,
        roles,
        make_user,
        api_client,
        semester,
        statuses,
        departments,
        study_group,
    ):
        author = make_user(role_code="user", email="proj-author@example.com")
        external = _create_approved_project(
            semester=semester,
            statuses=statuses,
            department=departments["parent"],
            title="Внешний проект",
            is_internal_customer=False,
            company="ООО Внешний",
            author=author,
        )
        internal = _create_approved_project(
            semester=semester,
            statuses=statuses,
            department=departments["parent"],
            title="Внутренний проект",
            is_internal_customer=True,
            company="Кафедра",
        )
        captain = make_user(role_code="student", email="cap-list@example.com")
        captain.study_group = study_group
        captain.save(update_fields=["study_group"])
        team_semester = _create_team_semester(
            group=study_group,
            semester=semester,
            captain=captain,
            name="Команда А",
            project=external,
        )

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}projects/?semester_id={semester.id}")

        assert response.status_code == 200
        by_id = {item["id"]: item for item in response.data}
        assert external.id in by_id
        assert internal.id in by_id

        ext_item = by_id[external.id]
        assert ext_item["name"] == "Внешний проект"
        assert ext_item["type"] == "external"
        assert ext_item["customer"] == "ООО Внешний"
        assert ext_item["institute"] == {"id": "INST-1", "name": "Institute 1"}
        assert ext_item["maxTeamsCount"] == 3
        assert len(ext_item["teams"]) == 1
        assert ext_item["teams"][0] == {
            "id": team_semester.id,
            "name": "Команда А",
            "studyGroup": {"id": study_group.id, "name": "Группа 1"},
        }

        int_item = by_id[internal.id]
        assert int_item["type"] == "internal"
        assert int_item["teams"] == []

    def test_validator_does_not_see_foreign_institute_project(
        self,
        roles,
        make_user,
        api_client,
        semester,
        statuses,
        other_institute,
    ):
        _create_approved_project(
            semester=semester,
            statuses=statuses,
            department=other_institute.department,
            title="Чужой проект",
        )
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}projects/?semester_id={semester.id}")

        assert response.status_code == 200
        assert response.data == []

    def test_cpds_sees_projects_from_all_institutes(
        self,
        roles,
        make_user,
        api_client,
        semester,
        statuses,
        departments,
        other_institute,
    ):
        own = _create_approved_project(
            semester=semester,
            statuses=statuses,
            department=departments["parent"],
            title="Свой",
        )
        foreign = _create_approved_project(
            semester=semester,
            statuses=statuses,
            department=other_institute.department,
            title="Чужой",
        )
        cpds = make_user(role_code="cpds", with_department=True)
        api_client.force_authenticate(user=cpds)

        response = api_client.get(f"{BASE_URL}projects/?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert own.id in ids
        assert foreign.id in ids


@pytest.mark.django_db
class TestProjectsStatsDetail:
    def test_detail_with_members_and_mentors(
        self,
        roles,
        make_user,
        api_client,
        semester,
        statuses,
        departments,
        study_group,
    ):
        author = make_user(role_code="user", email="detail-author@example.com")
        author.first_name = "Анна"
        author.last_name = "Автор"
        author.save(update_fields=["first_name", "last_name"])

        application = _create_approved_project(
            semester=semester,
            statuses=statuses,
            department=departments["parent"],
            title="Детальный проект",
            author=author,
            recommended_teams_count=5,
            print_number="42",
            problem_holder="Держатель",
            goal="Большая цель",
            barrier="Сложный барьер",
            existing_solutions="Есть решения",
        )

        mentor = make_user(role_code="mentor", with_department=True, email="m@ex.com")
        mentor.last_name = "Наставников"
        mentor.first_name = "Пётр"
        mentor.save(update_fields=["last_name", "first_name"])

        captain = make_user(role_code="student", email="cap-d@example.com")
        captain.study_group = study_group
        captain.last_name = "Капитанов"
        captain.first_name = "Иван"
        captain.save(update_fields=["study_group", "last_name", "first_name"])

        member = make_user(role_code="student", email="mem-d@example.com")
        member.study_group = study_group
        member.save(update_fields=["study_group"])

        team_semester = _create_team_semester(
            group=study_group,
            semester=semester,
            captain=captain,
            name="Команда Б",
            status=TeamSemester.Status.ASSEMBLED,
            project=application,
            members=[member],
            mentors=[mentor],
        )

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}projects/{application.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        data = response.data
        assert data["id"] == application.id
        assert data["name"] == "Детальный проект"
        assert data["type"] == "external"
        assert data["maxTeamsCount"] == 5
        assert data["currentTeamsCount"] == 1
        assert data["print_number"] == "42"
        assert data["problem_holder"] == "Держатель"
        assert data["goal"] == "Большая цель"
        assert data["barrier"] == "Сложный барьер"
        assert data["existing_solutions"] == "Есть решения"
        assert data["author"] == {
            "id": author.id,
            "fullName": author.get_full_name(),
            "email": author.email,
        }
        assert len(data["teams"]) == 1
        team = data["teams"][0]
        assert team["id"] == team_semester.id
        assert team["status"] == TeamSemester.Status.ASSEMBLED
        assert team["studyGroup"] == {"id": study_group.id, "name": "Группа 1"}
        assert {m["id"] for m in team["members"]} == {captain.id, member.id}
        member_payload = next(m for m in team["members"] if m["id"] == captain.id)
        assert member_payload["fullName"]
        assert member_payload["course"] == 3
        assert member_payload["institute"]["id"] == "INST-1"
        assert team["mentors"] == [
            {"id": str(mentor.id), "fullname": mentor.get_full_name()}
        ]

    def test_detail_not_found_for_foreign_institute(
        self,
        roles,
        make_user,
        api_client,
        semester,
        statuses,
        other_institute,
    ):
        application = _create_approved_project(
            semester=semester,
            statuses=statuses,
            department=other_institute.department,
            title="Чужой detail",
        )
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}projects/{application.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 404

    def test_detail_not_found_for_unknown_id(
        self, roles, make_user, api_client, semester
    ):
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}projects/999999/?semester_id={semester.id}"
        )

        assert response.status_code == 404


@pytest.mark.django_db
class TestProjectsStatsQueries:
    def test_list_query_count_stable_with_more_projects(
        self,
        roles,
        make_user,
        api_client,
        semester,
        statuses,
        departments,
        study_group,
    ):
        counter = {"n": 0}

        def seed(count: int) -> None:
            for _ in range(count):
                index = counter["n"]
                counter["n"] += 1
                application = _create_approved_project(
                    semester=semester,
                    statuses=statuses,
                    department=departments["parent"],
                    title=f"Проект {index}",
                    print_number=f"P-{index}",
                )
                captain = make_user(
                    role_code="student",
                    email=f"q-cap-{index}@example.com",
                )
                captain.study_group = study_group
                captain.save(update_fields=["study_group"])
                _create_team_semester(
                    group=study_group,
                    semester=semester,
                    captain=captain,
                    name=f"Команда {index}",
                    project=application,
                )

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        seed(2)
        with CaptureQueriesContext(connection) as ctx_small:
            response_small = api_client.get(
                f"{BASE_URL}projects/?semester_id={semester.id}"
            )
        assert response_small.status_code == 200
        small_count = len(ctx_small)

        ProjectApplication.objects.filter(semester=semester).delete()
        seed(8)
        with CaptureQueriesContext(connection) as ctx_large:
            response_large = api_client.get(
                f"{BASE_URL}projects/?semester_id={semester.id}"
            )
        assert response_large.status_code == 200
        large_count = len(ctx_large)

        assert large_count <= small_count + 2
