"""Тесты GET /api/teams/study-groups/my/."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
import pytest
from rest_framework.test import APIClient

from accounts.models import (
    ACTIVE_SEMESTER_SETTING_CODE,
    PreRegisteredStudent,
    Semester,
    Settings,
)
from showcase.models import InstituteSemesterSettings, ProjectApplication
from teams.dto.my_study_group import MyStudyGroupDTO
from teams.models import Direction, StudyGroup, Team, TeamSemester, TeamSemesterMember
from teams.repositories.institute_responsible import InstituteResponsibleRepository
from teams.repositories.study_group import StudyGroupRepository
from teams.repositories.team_lobby import TeamLobbyRepository
from teams.services.study_group_service import StudyGroupService

MY_GROUP_URL = "/api/teams/study-groups/my/"


def _activate_semester() -> Semester:
    semester = Semester.objects.create(code="s1", name="S1", position=1)
    Settings.objects.update_or_create(
        code=ACTIVE_SEMESTER_SETTING_CODE,
        defaults={"value": semester.code, "description": ""},
    )
    return semester


def _open_registration(institute, semester: Semester) -> InstituteSemesterSettings:
    return InstituteSemesterSettings.objects.create(
        institute=institute,
        semester=semester,
        registration_opens_at=timezone.now() - timedelta(days=1),
        closed_by_decision=False,
    )


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
    user=None,
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
        user=user,
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

    def test_student_without_mentor_returns_empty_mentors(
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
        assert response.data["mentors"] == []
        assert response.data["students_count"] == 1
        assert response.data["registered_students_count"] == 1
        assert len(response.data["members"]) == 1
        assert response.data["members"][0]["user_id"] == user.id
        assert response.data["members"][0]["is_registered"] is True

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
            user=registered,
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
        assert response.data["mentors"] == [
            {
                "id": mentor.id,
                "last_name": "Сидоров",
                "first_name": "Сидор",
                "middle_name": "Сидорович",
                "email": "mentor@example.com",
                "position": "Старший преподаватель",
                "academic_degree": "к.т.н.",
                "academic_title": "доцент",
            }
        ]
        assert response.data["students_count"] == 3
        assert response.data["registered_students_count"] == 2
        members = response.data["members"]
        by_name = {item["last_name"]: item for item in members}
        assert set(by_name) == {"Иванов", "Петров", current.last_name}
        assert by_name["Иванов"]["is_registered"] is True
        assert by_name["Иванов"]["user_id"] == registered.id
        assert "email" not in by_name["Иванов"]
        assert by_name["Петров"]["is_registered"] is False
        assert by_name["Петров"]["user_id"] is None
        assert by_name[current.last_name]["user_id"] == current.id
        assert by_name[current.last_name]["is_registered"] is True
        assert "team" not in by_name["Иванов"]

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
        semester = _activate_semester()
        _open_registration(study_group.institute, semester)
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
            user=registered,
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
        members = {item["last_name"]: item for item in response.data["members"]}
        assert members["Иванов"]["team"] == {
            "id": team.id,
            "name": "Команда Альфа",
            "role": "leader",
        }
        assert members["Петров"]["team"] is None
        assert members[current.last_name]["team"] is None
        assert members[current.last_name]["user_id"] == current.id
        assert response.data["my_team"] is None
        assert response.data["registration"]["is_open"] is True
        assert response.data["registration"]["opens_at"] is not None
        assert response.data["registration"]["closed_by_decision"] is False

    def test_semester_id_returns_my_team_and_registration(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
        statuses,
    ) -> None:
        semester = _activate_semester()
        settings = _open_registration(study_group.institute, semester)
        captain = make_user(role_code="student", email="cap@example.com")
        captain.last_name = "Капитанов"
        captain.first_name = "Кап"
        captain.study_group = study_group
        captain.save()
        member = make_user(role_code="student", email="mem@example.com")
        member.last_name = "Участников"
        member.first_name = "Уч"
        member.study_group = study_group
        member.save()

        project = ProjectApplication.objects.create(
            title="Проект Альфа",
            status=statuses["approved"],
            semester=semester,
        )
        team = Team.objects.create(name="Моя команда", home_study_group=study_group)
        team_semester = TeamSemester.objects.create(
            team=team,
            semester=semester,
            captain=captain,
            status=TeamSemester.Status.ASSEMBLED,
            project_application=project,
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=captain,
            role=TeamSemesterMember.Role.LEADER,
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=member,
            role=TeamSemesterMember.Role.MEMBER,
        )

        api_client.force_authenticate(user=captain)
        response = api_client.get(MY_GROUP_URL, {"semester_id": "actual"})

        assert response.status_code == 200
        my_team = response.data["my_team"]
        assert my_team["id"] == team_semester.id
        assert my_team["name"] == "Моя команда"
        assert my_team["status"] == TeamSemester.Status.ASSEMBLED
        assert my_team["is_captain"] is True
        assert my_team["has_project"] is True
        assert my_team["project"] == {"id": project.id, "title": "Проект Альфа"}
        assert {m["id"] for m in my_team["members"]} == {captain.id, member.id}
        assert response.data["registration"] == {
            "is_open": True,
            "opens_at": settings.registration_opens_at.isoformat(),
            "closed_by_decision": False,
        }

        api_client.force_authenticate(user=member)
        member_response = api_client.get(MY_GROUP_URL, {"semester_id": "actual"})
        assert member_response.status_code == 200
        assert member_response.data["my_team"]["is_captain"] is False
        assert member_response.data["my_team"]["has_project"] is True

    def test_without_semester_id_omits_my_team_and_registration(
        self,
        api_client: APIClient,
        roles,
        make_user,
        study_group: StudyGroup,
    ) -> None:
        user = make_user(role_code="student", email="me@example.com")
        user.study_group = study_group
        user.save(update_fields=["study_group"])
        api_client.force_authenticate(user=user)

        response = api_client.get(MY_GROUP_URL)

        assert response.status_code == 200
        assert "my_team" not in response.data
        assert "registration" not in response.data
        assert "team" not in response.data["members"][0]


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
        assert data["mentors"] == []

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
                user=student,
            )

        group = StudyGroupRepository().get_my_group_detail(study_group.id)
        members = StudyGroupRepository().list_group_contingent(study_group.id)

        with django_assert_num_queries(0):
            data = MyStudyGroupDTO(group, members).to_dict()

        assert data["mentors"][0]["id"] == mentor.id
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
        statuses,
    ) -> None:
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        settings = _open_registration(study_group.institute, semester)
        registered = make_user(role_code="student", email="st1@example.com")
        project = ProjectApplication.objects.create(
            title="P1",
            status=statuses["approved"],
            semester=semester,
        )
        team = Team.objects.create(name="Alpha")
        team_semester = TeamSemester.objects.create(
            team=team,
            semester=semester,
            captain=registered,
            project_application=project,
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
                user=student,
            )

        group = StudyGroupRepository().get_my_group_detail(
            study_group.id, semester_id=semester.pk
        )
        members = StudyGroupRepository().list_group_contingent(
            study_group.id, semester_id=semester.pk
        )
        my_team = TeamLobbyRepository().get_user_team_semester_snapshot(
            user_id=registered.id, semester_id=semester.pk
        )
        registration_settings = InstituteResponsibleRepository().get_settings(
            institute_code=study_group.institute_id,
            semester_id=semester.pk,
        )

        with django_assert_num_queries(0):
            data = MyStudyGroupDTO(
                group,
                members,
                include_team=True,
                semester_id=semester.pk,
                viewer_id=registered.id,
                my_team=my_team,
                registration_settings=registration_settings,
                include_semester_context=True,
            ).to_dict()

        assert data["members"][0]["team"]["id"] == team.id
        assert data["members"][0]["team"]["name"] == "Alpha"
        assert all("team" in item for item in data["members"])
        assert data["my_team"]["id"] == team_semester.id
        assert data["my_team"]["is_captain"] is True
        assert data["my_team"]["has_project"] is True
        assert data["my_team"]["project"]["id"] == project.id
        assert data["registration"]["is_open"] is True
        assert (
            data["registration"]["opens_at"]
            == settings.registration_opens_at.isoformat()
        )

    def test_get_my_study_group_query_count_stable_with_more_team_members(
        self,
        roles,
        make_user,
        study_group: StudyGroup,
    ) -> None:
        """Число SQL не растёт с числом участников команды."""
        semester = _activate_semester()
        _open_registration(study_group.institute, semester)
        captain = make_user(role_code="student", email="cap@example.com")
        captain.study_group = study_group
        captain.save(update_fields=["study_group"])

        team = Team.objects.create(name="T1", home_study_group=study_group)
        team_semester = TeamSemester.objects.create(
            team=team,
            semester=semester,
            captain=captain,
            status=TeamSemester.Status.FORMING,
        )
        TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=captain,
            role=TeamSemesterMember.Role.LEADER,
        )

        service = StudyGroupService()
        with CaptureQueriesContext(connection) as ctx_small:
            baseline = service.get_my_study_group(captain, semester_id_raw="actual")
        assert baseline["my_team"] is not None
        queries_small = len(ctx_small.captured_queries)

        for index in range(4):
            member = make_user(role_code="student", email=f"extra{index}@example.com")
            member.study_group = study_group
            member.save(update_fields=["study_group"])
            TeamSemesterMember.objects.create(
                team_semester=team_semester,
                user=member,
                role=TeamSemesterMember.Role.MEMBER,
            )

        with CaptureQueriesContext(connection) as ctx_large:
            enlarged = service.get_my_study_group(captain, semester_id_raw="actual")
        queries_large = len(ctx_large.captured_queries)

        assert len(enlarged["my_team"]["members"]) == 5
        assert enlarged["registration"]["is_open"] is True
        assert queries_large <= queries_small
