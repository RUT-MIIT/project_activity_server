"""Тесты API ответственного по институтам."""

from __future__ import annotations

from django.db import connection
from django.test.utils import CaptureQueriesContext
import pytest
from rest_framework.test import APIClient

from accounts.models import Department, Semester
from showcase.models import Institute
from teams.dto.institute_responsible import InstituteResponsibleGroupMentorsDTO
from teams.models import Direction, StudyGroup, StudyGroupSemester
from teams.repositories.study_group_semester import StudyGroupSemesterRepository
from teams.services.institute_responsible_service import InstituteResponsibleService
from teams.services.study_group_service import StudyGroupService

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
def study_groups(direction, institute, other_institute) -> dict[str, StudyGroup]:
    active = StudyGroup.objects.create(
        name="Группа 1",
        code="g1",
        direction=direction,
        institute=institute,
        course_number=3,
        is_end=False,
    )
    ended = StudyGroup.objects.create(
        name="Группа ended",
        code="g-end",
        direction=direction,
        institute=institute,
        is_end=True,
    )
    foreign = StudyGroup.objects.create(
        name="Чужая группа",
        code="g-other",
        direction=direction,
        institute=other_institute,
        is_end=False,
    )
    return {"active": active, "ended": ended, "foreign": foreign}


@pytest.mark.django_db
class TestInstituteResponsibleViewSet:
    def test_unauthenticated_returns_401(self, api_client, semester, study_groups):
        response = api_client.get(f"{BASE_URL}groups/?semester_id={semester.id}")
        assert response.status_code == 401

    def test_student_forbidden(
        self, roles, make_user, api_client, semester, study_groups
    ):
        user = make_user(role_code="student", with_department=True)
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE_URL}groups/?semester_id={semester.id}")
        assert response.status_code == 403

    def test_list_groups_only_active(
        self, roles, make_user, api_client, semester, study_groups
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=user)

        response = api_client.get(f"{BASE_URL}groups/?semester_id={semester.id}")

        assert response.status_code == 200
        assert len(response.data) == 1
        item = response.data[0]
        assert item["id"] == study_groups["active"].id
        assert item["name"] == "Группа 1"
        assert item["courseNumber"] == 3
        assert item["directionCode"] == "09.03.01"

    def test_list_groups_missing_semester_returns_400(
        self, roles, make_user, api_client, study_groups
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=user)

        response = api_client.get(f"{BASE_URL}groups/")

        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_list_groups_overview_returns_all_institute_groups_with_counts(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_groups,
        direction,
        institute,
    ):
        from accounts.models import PreRegisteredStudent
        from teams.models import Team, TeamSemester

        user = make_user(role_code="institute_validator", with_department=True)
        captain = make_user(role_code="student", email="overview-captain@example.com")
        captain.study_group = study_groups["active"]
        captain.save(update_fields=["study_group"])
        api_client.force_authenticate(user=user)

        extra_group = StudyGroup.objects.create(
            name="Группа 2",
            code="g2",
            direction=direction,
            institute=institute,
            is_end=False,
        )
        for index in range(2):
            PreRegisteredStudent.objects.create(
                last_name=f"Фамилия{index}",
                first_name=f"Имя{index}",
                student_card=f"SC{index}",
                snils=f"1234567890{index}",
                personnel_number=f"PN{index}",
                group=study_groups["active"],
            )
        team = Team.objects.create(
            name="Alpha",
            home_study_group=study_groups["active"],
        )
        TeamSemester.objects.create(team=team, semester=semester, captain=captain)

        response = api_client.get(
            f"{BASE_URL}groups-overview/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        by_id = {item["id"]: item for item in response.data}
        assert set(by_id) == {study_groups["active"].id, extra_group.id}
        active_item = by_id[study_groups["active"].id]
        assert active_item["name"] == "Группа 1"
        assert active_item["studentsCount"] == 2
        assert active_item["teamsCount"] == 1
        assert by_id[extra_group.id]["studentsCount"] == 0
        assert by_id[extra_group.id]["teamsCount"] == 0

    def test_list_groups_overview_excludes_foreign_institute(
        self,
        roles,
        make_user,
        api_client,
        semester,
        study_groups,
        other_institute,
        direction,
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=user)

        response = api_client.get(
            f"{BASE_URL}groups-overview/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert study_groups["foreign"].id not in ids
        assert study_groups["active"].id in ids

    def test_list_groups_overview_missing_semester_returns_400(
        self, roles, make_user, api_client, study_groups
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=user)

        response = api_client.get(f"{BASE_URL}groups-overview/")

        assert response.status_code == 400
        assert "semester_id" in response.data["error"]

    def test_list_employees_excludes_students(
        self, roles, make_user, api_client, study_groups
    ):
        validator = make_user(role_code="institute_validator", with_department=True)
        mentor = make_user(role_code="mentor", with_department=True)
        mentor.last_name = "Петров"
        mentor.first_name = "Пётр"
        mentor.save(update_fields=["last_name", "first_name"])
        student = make_user(role_code="student", with_department=True)

        api_client.force_authenticate(user=validator)
        response = api_client.get(f"{BASE_URL}employees/")

        assert response.status_code == 200
        ids = {item["id"] for item in response.data}
        assert mentor.id in ids
        assert student.id not in ids
        mentor_item = next(item for item in response.data if item["id"] == mentor.id)
        assert mentor_item["fullName"] == mentor.get_full_name()

    def test_list_group_mentors_structure(
        self, roles, make_user, api_client, semester, study_groups
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        _enrollment_with_mentors(study_groups["active"], semester, mentor)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}group-mentors/?semester_id={semester.id}")

        assert response.status_code == 200
        assert len(response.data) == 1
        item = response.data[0]
        assert item["id"] == study_groups["active"].id
        assert item["mentorIds"] == [mentor.id]
        assert set(item.keys()) == {
            "id",
            "name",
            "courseNumber",
            "directionCode",
            "mentorIds",
        }

    def test_list_group_mentors_multiple_mentors(
        self, roles, make_user, api_client, semester, study_groups
    ):
        mentor1 = make_user(role_code="mentor", with_department=True, email="m1@x.com")
        mentor2 = make_user(role_code="mentor", with_department=True, email="m2@x.com")
        _enrollment_with_mentors(study_groups["active"], semester, mentor1, mentor2)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.get(f"{BASE_URL}group-mentors/?semester_id={semester.id}")

        assert response.status_code == 200
        assert response.data[0]["mentorIds"] == [mentor1.id, mentor2.id]

    def test_assign_mentor_success(
        self, roles, make_user, api_client, semester, study_groups
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.post(
            f"{BASE_URL}groups/{study_groups['active'].id}/mentor/"
            f"?semester_id={semester.id}",
            {"mentorId": mentor.id},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["groupId"] == study_groups["active"].id
        assert response.data["semesterId"] == semester.id
        assert response.data["mentorIds"] == [mentor.id]

        enrollment = StudyGroupSemester.objects.get(
            study_group=study_groups["active"],
            semester=semester,
        )
        assert list(enrollment.mentors.values_list("id", flat=True)) == [mentor.id]

    def test_assign_mentor_adds_second_without_removing_first(
        self, roles, make_user, api_client, semester, study_groups
    ):
        mentor1 = make_user(role_code="mentor", with_department=True, email="m1@x.com")
        mentor2 = make_user(role_code="mentor", with_department=True, email="m2@x.com")
        _enrollment_with_mentors(study_groups["active"], semester, mentor1)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.post(
            f"{BASE_URL}groups/{study_groups['active'].id}/mentor/"
            f"?semester_id={semester.id}",
            {"mentorId": mentor2.id},
            format="json",
        )

        assert response.status_code == 200
        assert set(response.data["mentorIds"]) == {mentor1.id, mentor2.id}

    def test_assign_mentor_non_mentor_employee_allowed(
        self, roles, make_user, api_client, semester, study_groups
    ):
        employee = make_user(role_code="user", with_department=True)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.post(
            f"{BASE_URL}groups/{study_groups['active'].id}/mentor/"
            f"?semester_id={semester.id}",
            {"mentorId": employee.id},
            format="json",
        )

        assert response.status_code == 200
        assert employee.id in response.data["mentorIds"]

    def test_assign_mentor_foreign_group_rejected(
        self, roles, make_user, api_client, semester, study_groups
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.post(
            f"{BASE_URL}groups/{study_groups['foreign'].id}/mentor/"
            f"?semester_id={semester.id}",
            {"mentorId": mentor.id},
            format="json",
        )

        assert response.status_code == 400

    def test_remove_mentor_success(
        self, roles, make_user, api_client, semester, study_groups
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        mentor2 = make_user(role_code="mentor", with_department=True, email="m2@x.com")
        _enrollment_with_mentors(study_groups["active"], semester, mentor, mentor2)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.delete(
            f"{BASE_URL}groups/{study_groups['active'].id}/mentor/"
            f"?semester_id={semester.id}&mentor_id={mentor.id}"
        )

        assert response.status_code == 200
        assert response.data["mentorIds"] == [mentor2.id]
        enrollment = StudyGroupSemester.objects.get(
            study_group=study_groups["active"],
            semester=semester,
        )
        assert list(enrollment.mentors.values_list("id", flat=True)) == [mentor2.id]

    def test_remove_mentor_idempotent(
        self, roles, make_user, api_client, semester, study_groups
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.delete(
            f"{BASE_URL}groups/{study_groups['active'].id}/mentor/"
            f"?semester_id={semester.id}&mentor_id={mentor.id}"
        )

        assert response.status_code == 200
        assert response.data["mentorIds"] == []

    def test_remove_mentor_requires_mentor_id(
        self, roles, make_user, api_client, semester, study_groups
    ):
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        response = api_client.delete(
            f"{BASE_URL}groups/{study_groups['active'].id}/mentor/"
            f"?semester_id={semester.id}"
        )

        assert response.status_code == 400
        assert "mentor_id" in response.data["error"]


@pytest.mark.django_db
class TestMyStudyGroupSemesterMentor:
    def test_my_group_uses_semester_mentor(
        self, roles, make_user, api_client, semester, direction, institute
    ):
        group = StudyGroup.objects.create(
            name="АМБ-211",
            code="amb",
            direction=direction,
            institute=institute,
        )
        global_mentor = make_user(role_code="mentor", email="global@x.com")
        semester_mentor = make_user(role_code="mentor", email="sem@x.com")
        group.mentor = global_mentor
        group.save(update_fields=["mentor"])
        _enrollment_with_mentors(group, semester, semester_mentor)

        student = make_user(role_code="student", with_department=True)
        student.study_group = group
        student.save(update_fields=["study_group"])

        api_client = APIClient()
        api_client.force_authenticate(user=student)
        response = api_client.get(
            f"/api/teams/study-groups/my/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert response.data["mentors"][0]["id"] == semester_mentor.id

    def test_my_group_without_semester_falls_back_to_group_mentor(
        self, roles, make_user, direction, institute
    ):
        group = StudyGroup.objects.create(
            name="АМБ-212",
            code="amb2",
            direction=direction,
            institute=institute,
        )
        global_mentor = make_user(role_code="mentor", email="global2@x.com")
        group.mentor = global_mentor
        group.save(update_fields=["mentor"])

        student = make_user(role_code="student", with_department=True)
        student.study_group = group
        student.save(update_fields=["study_group"])

        service = StudyGroupService()
        data = service.get_my_study_group(student, semester_id_raw=None)

        assert data["mentors"][0]["id"] == global_mentor.id


@pytest.mark.django_db
class TestInstituteResponsibleQueryPerformance:
    def _create_groups(
        self,
        direction: Direction,
        institute: Institute,
        count: int,
        *,
        prefix: str,
    ) -> list[StudyGroup]:
        return [
            StudyGroup.objects.create(
                name=f"{prefix}-{index}",
                code=f"{prefix}-{index}",
                direction=direction,
                institute=institute,
                is_end=False,
            )
            for index in range(count)
        ]

    def test_group_mentors_dto_serialization_has_no_extra_queries(
        self,
        roles,
        make_user,
        semester,
        direction,
        institute,
        django_assert_num_queries,
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        groups = self._create_groups(direction, institute, 8, prefix="perf")
        for group in groups:
            _enrollment_with_mentors(group, semester, mentor)

        repository = StudyGroupSemesterRepository()
        loaded = list(
            repository.list_active_groups_with_mentors(institute.code, semester.id)
        )

        with django_assert_num_queries(0):
            payload = InstituteResponsibleGroupMentorsDTO(loaded).to_list()

        assert len(payload) == 8
        assert all("mentorIds" in item for item in payload)

    def test_list_group_mentors_query_count_does_not_scale_with_groups(
        self,
        roles,
        make_user,
        api_client,
        semester,
        direction,
        institute,
    ):
        mentor = make_user(role_code="mentor", with_department=True)
        validator = make_user(role_code="institute_validator", with_department=True)
        api_client.force_authenticate(user=validator)

        small_groups = self._create_groups(direction, institute, 3, prefix="small")
        for group in small_groups:
            _enrollment_with_mentors(group, semester, mentor)

        with CaptureQueriesContext(connection) as small_ctx:
            response = api_client.get(
                f"{BASE_URL}group-mentors/?semester_id={semester.id}"
            )
        assert response.status_code == 200
        small_count = len(small_ctx.captured_queries)

        large_groups = self._create_groups(direction, institute, 12, prefix="large")
        for group in large_groups:
            _enrollment_with_mentors(group, semester, mentor)

        with CaptureQueriesContext(connection) as large_ctx:
            response = api_client.get(
                f"{BASE_URL}group-mentors/?semester_id={semester.id}"
            )
        assert response.status_code == 200
        assert len(response.data) == 15

        assert len(large_ctx.captured_queries) == small_count

    def test_list_employees_dto_serialization_has_no_extra_queries(
        self,
        roles,
        make_user,
        institute,
        departments,
        django_assert_num_queries,
    ):
        from teams.dto.institute_responsible import InstituteResponsibleEmployeeDTO

        for index in range(6):
            make_user(
                role_code="mentor",
                with_department=True,
                email=f"mentor-dto-{index}@example.com",
            )

        repository = StudyGroupSemesterRepository()
        department_ids = {departments["parent"].id, departments["child"].id}
        employees = list(repository.list_employees(department_ids))

        with django_assert_num_queries(0):
            payload = [
                InstituteResponsibleEmployeeDTO(employee).to_dict()
                for employee in employees
            ]

        assert len(payload) >= 6
