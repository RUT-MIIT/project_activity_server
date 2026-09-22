"""Тесты API статистики наставников ответственного института."""

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
    StudyGroupSemester,
    Team,
    TeamSemester,
    TeamSemesterMember,
)

BASE_URL = "/api/teams/institute-responsible/"


def _enrollment_with_mentors(
    group: StudyGroup, semester: Semester, *mentors
) -> StudyGroupSemester:
    enrollment = StudyGroupSemester.objects.create(
        study_group=group, semester=semester
    )
    if mentors:
        enrollment.mentors.set(mentors)
    return enrollment


def _create_team_semester(
    *,
    group: StudyGroup,
    semester: Semester,
    captain,
    name: str,
    status: str = TeamSemester.Status.FORMING,
    project: ProjectApplication | None = None,
    members: list | None = None,
) -> TeamSemester:
    team = Team.objects.create(name=name, home_study_group=group)
    team_semester = TeamSemester.objects.create(
        team=team,
        semester=semester,
        captain=captain,
        status=status,
        project_application=project,
    )
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
class TestMentorsStatsList:
    def test_student_forbidden(self, roles, make_user, api_client, semester):
        user = make_user(role_code="student", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE_URL}mentors/?semester_id={semester.id}")
        assert response.status_code == 403

    def test_missing_semester_returns_400(self, roles, make_user, api_client):
        user = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE_URL}mentors/")
        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_mentor_without_groups_in_list(
        self, roles, make_user, api_client, semester, institute
    ):
        mentor = make_user(
            role_code="mentor",
            with_department=True,
            email="lonely-mentor@example.com",
        )
        mentor.last_name = "Одиноков"
        mentor.first_name = "Пётр"
        mentor.save(update_fields=["last_name", "first_name"])
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}mentors/?semester_id={semester.id}")

        assert response.status_code == 200
        by_id = {item["id"]: item for item in response.data}
        assert mentor.id in by_id
        item = by_id[mentor.id]
        assert item["fullName"] == mentor.get_full_name()
        assert item["institute"] == {"id": "INST-1", "name": "Institute 1"}
        assert item["groups"] == []
        assert item["teamsCount"] == 0
        assert "loadStatus" not in item

    def test_validator_sees_only_own_institute_mentors(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        foreign_group,
        other_institute,
        departments,
    ):
        own_mentor = make_user(
            role_code="mentor",
            with_department=True,
            email="own-mentor@example.com",
        )
        foreign_mentor = make_user(
            role_code="mentor",
            with_department=False,
            email="foreign-mentor@example.com",
        )
        foreign_mentor.department = other_institute.department
        foreign_mentor.save(update_fields=["department"])
        _enrollment_with_mentors(foreign_group, semester, foreign_mentor)

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}mentors/?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert own_mentor.id in ids
        assert foreign_mentor.id not in ids

    def test_cpds_sees_mentors_from_all_institutes(
        self,
        roles,
        make_user,
        api_client,
        semester,
        institute,
        foreign_group,
        other_institute,
    ):
        own_mentor = make_user(
            role_code="mentor",
            with_department=True,
            email="cpds-own@example.com",
        )
        foreign_mentor = make_user(
            role_code="mentor",
            with_department=False,
            email="cpds-foreign@example.com",
        )
        foreign_mentor.department = other_institute.department
        foreign_mentor.save(update_fields=["department"])

        cpds = make_user(role_code="cpds", with_department=True)
        api_client.force_authenticate(user=cpds)

        response = api_client.get(f"{BASE_URL}mentors/?semester_id={semester.id}")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert own_mentor.id in ids
        assert foreign_mentor.id in ids

    def test_list_includes_groups_and_teams_count(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        statuses,
    ):
        mentor = make_user(
            role_code="mentor",
            with_department=True,
            email="loaded-mentor@example.com",
        )
        _enrollment_with_mentors(study_group, semester, mentor)
        PreRegisteredStudent.objects.create(
            last_name="Студентов",
            first_name="Алексей",
            role_id="student",
            group=study_group,
        )
        captain = make_user(role_code="student", email="cap-list@example.com")
        captain.study_group = study_group
        captain.save(update_fields=["study_group"])
        _create_team_semester(
            group=study_group,
            semester=semester,
            captain=captain,
            name="Команда 1",
        )
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}mentors/?semester_id={semester.id}")

        assert response.status_code == 200
        item = next(row for row in response.data if row["id"] == mentor.id)
        assert len(item["groups"]) == 1
        assert item["groups"][0]["id"] == study_group.id
        assert item["groups"][0]["name"] == "Группа 1"
        assert item["groups"][0]["studentsCount"] == 2
        assert item["teamsCount"] == 1

    def test_m2m_group_appears_for_both_mentors(
        self, roles, make_user, api_client, semester, study_group
    ):
        mentor_a = make_user(
            role_code="mentor", with_department=True, email="m2m-a@example.com"
        )
        mentor_b = make_user(
            role_code="mentor", with_department=True, email="m2m-b@example.com"
        )
        _enrollment_with_mentors(study_group, semester, mentor_a, mentor_b)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}mentors/?semester_id={semester.id}")

        by_id = {item["id"]: item for item in response.data}
        assert by_id[mentor_a.id]["groups"][0]["id"] == study_group.id
        assert by_id[mentor_b.id]["groups"][0]["id"] == study_group.id


@pytest.mark.django_db
class TestMentorsStatsDetail:
    def test_detail_full_shape(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        statuses,
    ):
        mentor = make_user(
            role_code="mentor",
            with_department=True,
            email="detail-mentor@example.com",
        )
        _enrollment_with_mentors(study_group, semester, mentor)
        captain = make_user(role_code="student", email="detail-cap@example.com")
        captain.study_group = study_group
        captain.last_name = "Капитанов"
        captain.first_name = "Иван"
        captain.save(update_fields=["study_group", "last_name", "first_name"])
        member = make_user(role_code="student", email="detail-mem@example.com")
        member.study_group = study_group
        member.save(update_fields=["study_group"])
        project = ProjectApplication.objects.create(
            title="Проект Б",
            status=statuses["approved"],
            semester=semester,
        )
        team_semester = _create_team_semester(
            group=study_group,
            semester=semester,
            captain=captain,
            name="Команда Б",
            status=TeamSemester.Status.ASSEMBLED,
            project=project,
            members=[member],
        )
        PreRegisteredStudent.objects.create(
            last_name="Безкомандный",
            first_name="Студент",
            role_id="student",
            group=study_group,
        )
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}mentors/{mentor.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        data = response.data
        assert data["id"] == mentor.id
        assert data["institute"]["id"] == "INST-1"
        assert data["teamsCount"] == 1
        assert len(data["groups"]) == 1
        group = data["groups"][0]
        assert group["id"] == study_group.id
        assert len(group["students"]) == 3
        student_names = {row["fullName"] for row in group["students"]}
        assert any("Безкомандный" in name for name in student_names)
        assert group["students"][0]["course"] == 3
        assert group["students"][0]["institute"]["id"] == "INST-1"
        assert len(group["teams"]) == 1
        team = group["teams"][0]
        assert team["id"] == team_semester.id
        assert team["status"] == "assembled"
        assert team["project"] == {"id": project.id, "name": "Проект Б"}
        assert team["membersCount"] == 2
        assert len(team["members"]) == 2
        assert team["members"][0]["team"]["id"] == team_semester.id

    def test_detail_foreign_mentor_returns_404(
        self,
        roles,
        make_user,
        api_client,
        semester,
        other_institute,
    ):
        foreign_mentor = make_user(
            role_code="mentor",
            with_department=False,
            email="detail-foreign@example.com",
        )
        foreign_mentor.department = other_institute.department
        foreign_mentor.save(update_fields=["department"])
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}mentors/{foreign_mentor.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 404

    def test_detail_mentor_without_groups(
        self, roles, make_user, api_client, semester, institute
    ):
        mentor = make_user(
            role_code="mentor",
            with_department=True,
            email="detail-empty@example.com",
        )
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}mentors/{mentor.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert response.data["groups"] == []
        assert response.data["teamsCount"] == 0

    def test_detail_not_mentor_returns_404(
        self, roles, make_user, api_client, semester
    ):
        student = make_user(role_code="student", with_department=True)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}mentors/{student.id}/?semester_id={semester.id}"
        )

        assert response.status_code == 404


@pytest.mark.django_db
class TestMentorsStatsQueries:
    def test_list_query_count_does_not_scale_with_mentors(
        self, roles, make_user, api_client, semester, study_group
    ):
        mentors = [
            make_user(
                role_code="mentor",
                with_department=True,
                email=f"q-mentor-{index}@example.com",
            )
            for index in range(5)
        ]
        _enrollment_with_mentors(study_group, semester, *mentors)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        with CaptureQueriesContext(connection) as ctx:
            response = api_client.get(f"{BASE_URL}mentors/?semester_id={semester.id}")

        assert response.status_code == 200
        assert len(response.data) >= 5
        assert len(ctx.captured_queries) < 25
