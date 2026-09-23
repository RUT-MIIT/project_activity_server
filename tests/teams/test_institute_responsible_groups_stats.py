"""Тесты API статистики учебных групп ответственного института."""

from __future__ import annotations

from django.db import connection
from django.test.utils import CaptureQueriesContext
import pytest
from rest_framework.test import APIClient

from accounts.models import Department, PreRegisteredStudent, Semester
from showcase.models import Institute, ProjectApplication
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
class TestGroupsStatsList:
    def test_student_forbidden(self, roles, make_user, api_client, semester):
        user = make_user(role_code="student", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE_URL}groups-stats/?semester_id={semester.id}")
        assert response.status_code == 403

    def test_missing_semester_returns_400(self, roles, make_user, api_client):
        user = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE_URL}groups-stats/")
        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_list_structure_counts_and_empty_teams(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        statuses,
    ):
        PreRegisteredStudent.objects.create(
            last_name="Безкомандный",
            first_name="Студент",
            role_id="student",
            group=study_group,
        )
        captain = make_user(role_code="student", email="cap-list@example.com")
        captain.study_group = study_group
        captain.save(update_fields=["study_group"])
        project = ProjectApplication.objects.create(
            title="Проект А",
            company="ООО",
            author_lastname="И",
            author_firstname="А",
            author_email="a@example.com",
            semester=semester,
            status=statuses["approved"],
            min_team_members=2,
            max_team_members=5,
        )
        team_semester = _create_team_semester(
            group=study_group,
            semester=semester,
            captain=captain,
            name="Команда А",
            project=project,
        )

        empty_group = StudyGroup.objects.create(
            name="Группа без команд",
            code="g-empty",
            direction=study_group.direction,
            institute=study_group.institute,
            course_number=2,
            is_end=False,
        )

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}groups-stats/?semester_id={semester.id}")

        assert response.status_code == 200
        by_id = {item["id"]: item for item in response.data}
        assert study_group.id in by_id
        assert empty_group.id in by_id

        item = by_id[study_group.id]
        assert item["name"] == "Группа 1"
        assert item["institute"] == {"id": "INST-1", "name": "Institute 1"}
        assert item["course"] == 3
        assert item["studentsCount"] == 2
        assert item["studentsInTeamCount"] == 1
        assert len(item["teams"]) == 1
        assert item["teams"][0] == {
            "id": team_semester.id,
            "name": "Команда А",
            "studentsCount": 1,
        }

        empty_item = by_id[empty_group.id]
        assert empty_item["teams"] == []
        assert empty_item["studentsInTeamCount"] == 0
        assert empty_item["course"] == 2

    def test_validator_does_not_see_foreign_institute_group(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        foreign_group,
    ):
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}groups-stats/?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert study_group.id in ids
        assert foreign_group.id not in ids

    def test_cpds_sees_groups_from_all_institutes(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        foreign_group,
    ):
        cpds = make_user(role_code="cpds", with_department=True)
        api_client.force_authenticate(user=cpds)

        response = api_client.get(f"{BASE_URL}groups-stats/?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert study_group.id in ids
        assert foreign_group.id in ids

    def test_list_query_count_does_not_scale_with_groups(
        self,
        roles,
        make_user,
        api_client,
        semester,
        direction,
        institute,
    ):
        for index in range(5):
            StudyGroup.objects.create(
                name=f"Группа {index}",
                code=f"g-{index}",
                direction=direction,
                institute=institute,
                course_number=2,
                is_end=False,
            )

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        with CaptureQueriesContext(connection) as ctx_small:
            response_small = api_client.get(
                f"{BASE_URL}groups-stats/?semester_id={semester.id}"
            )
        assert response_small.status_code == 200
        small_count = len(ctx_small)

        for index in range(5, 15):
            StudyGroup.objects.create(
                name=f"Группа {index}",
                code=f"g-{index}",
                direction=direction,
                institute=institute,
                course_number=2,
                is_end=False,
            )

        with CaptureQueriesContext(connection) as ctx_large:
            response_large = api_client.get(
                f"{BASE_URL}groups-stats/?semester_id={semester.id}"
            )
        assert response_large.status_code == 200
        large_count = len(ctx_large)

        assert large_count <= small_count + 2


@pytest.mark.django_db
class TestGroupsStatsDetail:
    def test_detail_with_students_teams_members_mentors(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        statuses,
    ):
        PreRegisteredStudent.objects.create(
            last_name="Предрег",
            first_name="Алексей",
            role_id="student",
            group=study_group,
        )
        mentor = make_user(
            role_code="mentor",
            with_department=True,
            email="group-mentor@example.com",
        )
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

        project = ProjectApplication.objects.create(
            title="Проект Б",
            company="ООО",
            author_lastname="И",
            author_firstname="А",
            author_email="a@example.com",
            semester=semester,
            status=statuses["approved"],
            min_team_members=2,
            max_team_members=5,
        )
        team_semester = _create_team_semester(
            group=study_group,
            semester=semester,
            captain=captain,
            name="Команда Б",
            status=TeamSemester.Status.ASSEMBLED,
            project=project,
            members=[member],
            mentors=[mentor],
        )

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}groups-stats/{study_group.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        data = response.data
        assert data["id"] == study_group.id
        assert data["name"] == "Группа 1"
        assert data["institute"] == {"id": "INST-1", "name": "Institute 1"}
        assert data["course"] == 3
        assert len(data["students"]) == 3
        student_names = {row["fullName"] for row in data["students"]}
        assert "Предрег Алексей" in student_names
        assert data["students"][0]["course"] == 3
        assert data["students"][0]["institute"]["id"] == "INST-1"

        assert len(data["teams"]) == 1
        team = data["teams"][0]
        assert team["id"] == team_semester.id
        assert team["name"] == "Команда Б"
        assert team["status"] == TeamSemester.Status.ASSEMBLED
        assert {m["id"] for m in team["members"]} == {captain.id, member.id}
        leader = next(m for m in team["members"] if m["id"] == captain.id)
        assert leader["role"] == TeamSemesterMember.Role.LEADER
        assert leader["fullName"]
        assert leader["course"] == 3
        assert team["mentors"] == [
            {"id": mentor.id, "fullName": mentor.get_full_name()}
        ]

    def test_detail_not_found_for_foreign_institute(
        self,
        roles,
        make_user,
        api_client,
        semester,
        foreign_group,
    ):
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}groups-stats/{foreign_group.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 404

    def test_detail_not_found_for_ended_group(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
    ):
        study_group.is_end = True
        study_group.save(update_fields=["is_end"])

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}groups-stats/{study_group.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 404

    def test_detail_empty_teams(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
    ):
        PreRegisteredStudent.objects.create(
            last_name="Студентов",
            first_name="Безкоманды",
            role_id="student",
            group=study_group,
        )
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}groups-stats/{study_group.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert response.data["teams"] == []
        assert len(response.data["students"]) == 1

    def test_operational_groups_unchanged(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
    ):
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}groups/?semester_id={semester.id}")

        assert response.status_code == 200
        assert response.data
        item = response.data[0]
        assert "courseNumber" in item
        assert "directionCode" in item
        assert "studentsInTeamCount" not in item
        assert "teams" not in item
