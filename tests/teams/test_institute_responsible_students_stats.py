"""Тесты API статистики студентов ответственного института."""

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
    """Создаёт запись группы в семестре с наставниками."""
    enrollment = StudyGroupSemester.objects.create(
        study_group=group,
        semester=semester,
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
    project: ProjectApplication | None = None,
) -> TeamSemester:
    team = Team.objects.create(name=name, home_study_group=group)
    team_semester = TeamSemester.objects.create(
        team=team,
        semester=semester,
        captain=captain,
        status=TeamSemester.Status.FORMING,
        project_application=project,
    )
    TeamSemesterMember.objects.create(
        team_semester=team_semester,
        user=captain,
        role=TeamSemesterMember.Role.LEADER,
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
class TestStudentsStatsList:
    def test_student_forbidden(self, roles, make_user, api_client, semester):
        user = make_user(role_code="student", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(
            f"{BASE_URL}students-stats/?semester_id={semester.id}"
        )
        assert response.status_code == 403

    def test_missing_semester_returns_400(self, roles, make_user, api_client):
        user = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE_URL}students-stats/")
        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_list_shape_team_project_mentors_and_without_team(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        statuses,
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        mentor.first_name = "Mentor"
        mentor.last_name = "One"
        mentor.save(update_fields=["first_name", "last_name"])
        _enrollment_with_mentors(study_group, semester, mentor)

        without_team = PreRegisteredStudent.objects.create(
            last_name="Безкомандный",
            first_name="Студент",
            middle_name="И",
            role_id="student",
            group=study_group,
            personnel_number="pn-bare-1",
        )
        captain = make_user(role_code="student", email="cap-stats@example.com")
        captain.first_name = "Капитан"
        captain.last_name = "Командный"
        captain.study_group = study_group
        captain.save(update_fields=["first_name", "last_name", "study_group"])
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

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}students-stats/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        by_id = {item["id"]: item for item in response.data}
        assert without_team.id in by_id
        assert captain.id in by_id

        bare = by_id[without_team.id]
        assert bare["fullName"] == "Безкомандный Студент И"
        assert bare["institute"] == {"id": "INST-1", "name": "Institute 1"}
        assert bare["studyGroup"] == {"id": study_group.id, "name": "Группа 1"}
        assert bare["course"] == 3
        assert bare["isRegistered"] is False
        assert bare["team"] is None
        assert bare["project"] is None
        assert bare["mentors"] == [{"id": mentor.id, "fullName": mentor.get_full_name()}]

        with_team = by_id[captain.id]
        assert with_team["fullName"] == "Командный Капитан"
        assert with_team["isRegistered"] is True
        assert with_team["team"] == {"id": team_semester.id, "name": "Команда А"}
        assert with_team["project"] == {"id": project.id, "name": "Проект А"}
        assert with_team["mentors"] == [
            {"id": mentor.id, "fullName": mentor.get_full_name()}
        ]

    def test_validator_does_not_see_foreign_institute_students(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        foreign_group,
    ):
        PreRegisteredStudent.objects.create(
            last_name="Свой",
            first_name="Студент",
            role_id="student",
            group=study_group,
            personnel_number="pn-own-1",
        )
        foreign = PreRegisteredStudent.objects.create(
            last_name="Чужой",
            first_name="Студент",
            role_id="student",
            group=foreign_group,
            personnel_number="pn-foreign-1",
        )

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(
            f"{BASE_URL}students-stats/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert foreign.id not in ids
        assert any(item["fullName"].startswith("Свой") for item in response.data)

    def test_cpds_sees_students_from_all_institutes(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
        foreign_group,
    ):
        own = PreRegisteredStudent.objects.create(
            last_name="Свой",
            first_name="Студент",
            role_id="student",
            group=study_group,
            personnel_number="pn-own-2",
        )
        foreign = PreRegisteredStudent.objects.create(
            last_name="Чужой",
            first_name="Студент",
            role_id="student",
            group=foreign_group,
            personnel_number="pn-foreign-2",
        )

        cpds = make_user(role_code="cpds", with_department=True)
        api_client.force_authenticate(user=cpds)

        response = api_client.get(
            f"{BASE_URL}students-stats/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert own.id in ids
        assert foreign.id in ids

    def test_list_query_count_does_not_scale_with_students(
        self,
        roles,
        make_user,
        api_client,
        semester,
        direction,
        institute,
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        for index in range(5):
            group = StudyGroup.objects.create(
                name=f"Группа {index}",
                code=f"g-{index}",
                direction=direction,
                institute=institute,
                course_number=2,
                is_end=False,
            )
            _enrollment_with_mentors(group, semester, mentor)
            for student_index in range(3):
                PreRegisteredStudent.objects.create(
                    last_name=f"Студент{index}",
                    first_name=f"Имя{student_index}",
                    role_id="student",
                    group=group,
                    personnel_number=f"pn-q-{index}-{student_index}",
                )

        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        url = f"{BASE_URL}students-stats/?semester_id={semester.id}"
        # Прогрев кэша/соединений
        api_client.get(url)

        with CaptureQueriesContext(connection) as ctx:
            response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 15
        # Число запросов не должно расти с числом студентов (константный батч)
        assert len(ctx) < 25

    def test_operational_students_endpoint_unchanged(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_group,
    ):
        PreRegisteredStudent.objects.create(
            last_name="Иванов",
            first_name="Иван",
            middle_name="Иванович",
            role_id="student",
            group=study_group,
            personnel_number="pn-ops-1",
        )
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}students/?semester_id={semester.id}")

        assert response.status_code == 200
        assert len(response.data) == 1
        item = response.data[0]
        assert "lastName" in item
        assert "firstName" in item
        assert "teamName" in item
        assert "fullName" not in item
        assert "course" not in item
