"""Тесты GET /api/teams/study-groups/my/."""

from __future__ import annotations

from typing import Any

import pytest
from rest_framework.test import APIClient

from accounts.models import (
    ACTIVE_SEMESTER_SETTING_CODE,
    PreRegisteredStudent,
    Semester,
    Settings,
)
from teams.dto.my_study_group import MyStudyGroupDTO
from teams.models import Direction, StudyGroup, Team, TeamSemester, TeamSemesterMember
from teams.repositories.study_group import StudyGroupRepository
from teams.services.study_group_service import StudyGroupService

MY_GROUP_URL = "/api/teams/study-groups/my/"


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def direction(db: Any) -> Direction:
    return Direction.objects.create(
        code="25.03.03",
        name="Аэронавигация",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def study_group(direction: Direction, institute) -> StudyGroup:
    return StudyGroup.objects.create(
        name="АМБ-211",
        code="АМБ-2025-11",
        enrollment_year=2025,
        course_number=2,
        profile="Организация бизнес-процессов",
        form="Очная",
        direction=direction,
        institute=institute,
    )


def _make_preregistered(
    group: StudyGroup,
    *,
    last_name: str,
    first_name: str,
    student_card: str,
    personnel_number: str,
    snils: str,
    student=None,
    middle_name: str = "",
) -> PreRegisteredStudent:
    return PreRegisteredStudent.objects.create(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        student_card=student_card,
        snils=snils,
        personnel_number=personnel_number,
        group=group,
        student=student,
    )


@pytest.mark.django_db
class TestMyStudyGroupViewSet:
    def test_unauthenticated_returns_401(self, api_client: APIClient) -> None:
        response = api_client.get(MY_GROUP_URL)
        assert response.status_code == 401

    def test_admin_returns_403(self, api_client: APIClient, roles, make_user) -> None:
        user = make_user(role_code="admin")
        api_client.force_authenticate(user=user)

        response = api_client.get(MY_GROUP_URL)

        assert response.status_code == 403

    def test_student_without_group_returns_404(
        self, api_client: APIClient, roles, make_user
    ) -> None:
        user = make_user(role_code="student")
        api_client.force_authenticate(user=user)

        response = api_client.get(MY_GROUP_URL)

        assert response.status_code == 404

    def test_student_without_mentor_returns_null_mentor(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
    ) -> None:
        user = make_user(role_code="student", email="student@example.com")
        user.study_group = study_group
        user.save(update_fields=["study_group"])
        api_client.force_authenticate(user=user)

        response = api_client.get(MY_GROUP_URL)

        assert response.status_code == 200
        assert response.data["id"] == study_group.id
        assert response.data["name"] == "АМБ-211"
        assert response.data["mentor"] is None
        assert response.data["members"] == []
        assert response.data["students_count"] == 0
        assert response.data["registered_students_count"] == 0

    def test_student_with_mentor_and_members(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
    ) -> None:
        mentor = make_user(role_code="mentor", email="mentor@example.com")
        mentor.last_name = "Сидоров"
        mentor.first_name = "Сидор"
        mentor.middle_name = "Сидорович"
        mentor.position = "Старший преподаватель"
        mentor.academic_degree = "к.т.н."
        mentor.academic_title = "доцент"
        mentor.save()
        study_group.mentor = mentor
        study_group.save(update_fields=["mentor"])

        registered = make_user(role_code="student", email="ivan@example.com")
        registered.study_group = study_group
        registered.save(update_fields=["study_group"])
        _make_preregistered(
            study_group,
            last_name="Иванов",
            first_name="Иван",
            middle_name="Иванович",
            student_card="25010001",
            personnel_number="100001",
            snils="11111111111",
            student=registered,
        )
        _make_preregistered(
            study_group,
            last_name="Петров",
            first_name="Пётр",
            student_card="25010002",
            personnel_number="100002",
            snils="22222222222",
        )

        current = make_user(role_code="student", email="me@example.com")
        current.study_group = study_group
        current.save(update_fields=["study_group"])
        api_client.force_authenticate(user=current)

        response = api_client.get(MY_GROUP_URL)

        assert response.status_code == 200
        assert response.data["direction"]["code"] == "25.03.03"
        assert response.data["institute"]["code"] == study_group.institute_id
        assert response.data["mentor"] == {
            "id": mentor.id,
            "last_name": "Сидоров",
            "first_name": "Сидор",
            "middle_name": "Сидорович",
            "email": "mentor@example.com",
            "position": "Старший преподаватель",
            "academic_degree": "к.т.н.",
            "academic_title": "доцент",
        }
        assert response.data["students_count"] == 2
        assert response.data["registered_students_count"] == 1
        members = response.data["members"]
        assert [item["last_name"] for item in members] == ["Иванов", "Петров"]
        assert members[0]["is_registered"] is True
        assert members[0]["user_id"] == registered.id
        assert members[0]["email"] == "ivan@example.com"
        assert members[1]["is_registered"] is False
        assert members[1]["user_id"] is None
        assert members[1]["email"] is None
        assert "team" not in members[0]

    def test_invalid_semester_id_returns_400(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
    ) -> None:
        user = make_user(role_code="student")
        user.study_group = study_group
        user.save(update_fields=["study_group"])
        api_client.force_authenticate(user=user)

        response = api_client.get(MY_GROUP_URL, {"semester_id": "invalid"})

        assert response.status_code == 400

    def test_semester_id_adds_teammate_team(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
    ) -> None:
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        Settings.objects.update_or_create(
            code=ACTIVE_SEMESTER_SETTING_CODE,
            defaults={"value": semester.code, "description": ""},
        )
        registered = make_user(role_code="student", email="ivan@example.com")
        registered.study_group = study_group
        registered.save(update_fields=["study_group"])
        _make_preregistered(
            study_group,
            last_name="Иванов",
            first_name="Иван",
            student_card="25010001",
            personnel_number="100001",
            snils="11111111111",
            student=registered,
        )
        _make_preregistered(
            study_group,
            last_name="Петров",
            first_name="Пётр",
            student_card="25010002",
            personnel_number="100002",
            snils="22222222222",
        )
        team = Team.objects.create(name="Команда Альфа", home_study_group=study_group)
        team_semester = TeamSemester.objects.create(
            team=team, semester=semester, captain=registered
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=registered,
            role=TeamSemesterMember.Role.LEADER,
        )

        current = make_user(role_code="student", email="me@example.com")
        current.study_group = study_group
        current.save(update_fields=["study_group"])
        api_client.force_authenticate(user=current)

        response = api_client.get(MY_GROUP_URL, {"semester_id": "actual"})

        assert response.status_code == 200
        members = response.data["members"]
        assert members[0]["team"] == {
            "id": team.id,
            "name": "Команда Альфа",
            "role": "leader",
        }
        assert members[1]["team"] is None


@pytest.mark.django_db
class TestMyStudyGroupService:
    def test_get_my_study_group_success(
        self, roles, make_user, study_group: StudyGroup
    ) -> None:
        user = make_user(role_code="student")
        user.study_group = study_group
        user.save(update_fields=["study_group"])
        service = StudyGroupService()

        data = service.get_my_study_group(user)

        assert data["id"] == study_group.id
        assert data["mentor"] is None

    def test_get_my_study_group_forbidden_for_admin(self, roles, make_user) -> None:
        user = make_user(role_code="admin")
        service = StudyGroupService()
        with pytest.raises(PermissionError, match="студентов"):
            service.get_my_study_group(user)

    def test_get_my_study_group_not_found_without_group(self, roles, make_user) -> None:
        user = make_user(role_code="student")
        service = StudyGroupService()
        with pytest.raises(LookupError, match="не назначена"):
            service.get_my_study_group(user)

    def test_serialize_my_group_has_no_n_plus_one(
        self,
        roles,
        make_user,
        study_group: StudyGroup,
        django_assert_num_queries,
    ) -> None:
        mentor = make_user(role_code="mentor", email="mentor@example.com")
        mentor.position = "Преподаватель"
        mentor.save(update_fields=["position"])
        study_group.mentor = mentor
        study_group.save(update_fields=["mentor"])

        registered = make_user(role_code="student", email="st1@example.com")
        for index in range(5):
            student = registered if index == 0 else None
            _make_preregistered(
                study_group,
                last_name=f"Студент{index:02d}",
                first_name="Имя",
                student_card=f"2501000{index}",
                personnel_number=f"10000{index}",
                snils=f"1111111111{index}",
                student=student,
            )

        group = StudyGroupRepository().get_my_group_detail(study_group.id)

        with django_assert_num_queries(0):
            data = MyStudyGroupDTO(group).to_dict()

        assert data["mentor"]["id"] == mentor.id
        assert data["students_count"] == 5
        assert data["registered_students_count"] == 1
        assert len(data["members"]) == 5
        assert "team" not in data["members"][0]

    def test_serialize_my_group_with_semester_has_no_n_plus_one(
        self,
        roles,
        make_user,
        study_group: StudyGroup,
        django_assert_num_queries,
    ) -> None:
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        registered = make_user(role_code="student", email="st1@example.com")
        team = Team.objects.create(name="Alpha")
        team_semester = TeamSemester.objects.create(
            team=team, semester=semester, captain=registered
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=registered,
            role=TeamSemesterMember.Role.LEADER,
        )
        for index in range(5):
            student = registered if index == 0 else None
            _make_preregistered(
                study_group,
                last_name=f"Студент{index:02d}",
                first_name="Имя",
                student_card=f"2501001{index}",
                personnel_number=f"20000{index}",
                snils=f"3333333333{index}",
                student=student,
            )

        group = StudyGroupRepository().get_my_group_detail(
            study_group.id, semester_id=semester.pk
        )

        with django_assert_num_queries(0):
            data = MyStudyGroupDTO(group, include_team=True).to_dict()

        assert data["members"][0]["team"]["id"] == team.id
        assert data["members"][0]["team"]["name"] == "Alpha"
        assert all("team" in item for item in data["members"])
