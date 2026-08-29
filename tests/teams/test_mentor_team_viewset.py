"""Тесты API управления командой наставником."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

from accounts.models import PreRegisteredStudent, Semester
from accounts.services.placeholder_user_service import PlaceholderUserService
from accounts.services.preregistered_student_service import PreRegisteredStudentService
from showcase.models import (
    ApplicationInvolvedDepartment,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
)
from teams.models import (
    Direction,
    StudyGroup,
    StudyGroupSemester,
    Team,
    TeamSemester,
    TeamSemesterMember,
)

User = get_user_model()


def _team_url(group_id: int, team_semester_id: int, suffix: str = "") -> str:
    base = f"/api/teams/study-groups/{group_id}/teams/{team_semester_id}"
    if not suffix:
        return f"{base}/"
    return f"{base}{suffix}" if suffix.startswith("/") else f"{base}/{suffix}"


def _enrollment_with_mentors(
    group: StudyGroup, semester: Semester, *mentors: User
) -> StudyGroupSemester:
    enrollment = StudyGroupSemester.objects.create(
        study_group=group,
        semester=semester,
    )
    if mentors:
        enrollment.mentors.set(mentors)
    return enrollment


def _approved_app(*, semester, statuses, departments, title="Проект"):
    app = ProjectApplication.objects.create(
        title=title,
        company="ООО",
        author_lastname="Иванов",
        author_firstname="Иван",
        author_email="a@example.com",
        semester=semester,
        status=statuses["approved"],
        goal="Длинная цель проекта больше пятидесяти символов для валидации",
        problem_holder="Носитель",
        barrier="Длинный барьер больше пятидесяти символов для валидации",
        recommended_teams_count=3,
    )
    ApplicationInvolvedDepartment.objects.create(
        application=app, department=departments["child"]
    )
    return app


def _track(*, semester, department, author, group, applications):
    total = sum(app.recommended_teams_count for app in applications)
    track = ProjectTrack.objects.create(
        name="Трек",
        department=department,
        semester=semester,
        author=author,
        min_team_members=1,
        max_team_members=5,
        recommended_teams_count=total,
    )
    ProjectTrackGroup.objects.create(project_track=track, study_group=group)
    for app in applications:
        ProjectTrackApplication.objects.create(
            project_track=track, project_application=app
        )
    return track


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
def study_group(direction, institute) -> StudyGroup:
    return StudyGroup.objects.create(
        name="ИВТ-101",
        code="IVT-101",
        direction=direction,
        institute=institute,
        is_end=False,
    )


@pytest.fixture
def mentor_team_setup(
    roles,
    make_user,
    study_group: StudyGroup,
    semester: Semester,
    departments,
    statuses,
):
    mentor = make_user(role_code="mentor", with_department=True)
    captain = make_user(role_code="student", email="captain@example.com")
    captain.study_group = study_group
    captain.save(update_fields=["study_group"])
    member = make_user(role_code="student", email="member@example.com")
    member.study_group = study_group
    member.save(update_fields=["study_group"])

    _enrollment_with_mentors(study_group, semester, mentor)

    app = _approved_app(semester=semester, statuses=statuses, departments=departments)
    track = _track(
        semester=semester,
        department=departments["child"],
        author=mentor,
        group=study_group,
        applications=[app],
    )

    team = Team.objects.create(name="Alpha", home_study_group=study_group)
    team_semester = TeamSemester.objects.create(
        team=team,
        semester=semester,
        project_track=track,
        captain=captain,
        status=TeamSemester.Status.FORMING,
    )
    TeamSemesterMember.objects.create(
        team_semester=team_semester,
        user=captain,
        semester=semester,
        role=TeamSemesterMember.Role.LEADER,
    )
    TeamSemesterMember.objects.create(
        team_semester=team_semester,
        user=member,
        semester=semester,
        role=TeamSemesterMember.Role.MEMBER,
    )

    return {
        "mentor": mentor,
        "captain": captain,
        "member": member,
        "team_semester": team_semester,
        "track": track,
        "app": app,
        "study_group": study_group,
        "semester": semester,
    }


@pytest.mark.django_db
class TestMentorTeamAccess:
    def test_unauthenticated_returns_401(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        response = api_client.patch(
            f"{_team_url(setup['study_group'].id, setup['team_semester'].id)}"
            f"?semester_id={setup['semester'].id}",
            {"name": "Beta"},
            format="json",
        )
        assert response.status_code == 401

    def test_not_mentor_returns_403(
        self,
        api_client: APIClient,
        roles,
        make_user,
        mentor_team_setup: dict[str, Any],
    ) -> None:
        setup = mentor_team_setup
        viewer = make_user(role_code="user", with_department=True, email="viewer@x.com")
        api_client.force_authenticate(user=viewer)
        response = api_client.patch(
            f"{_team_url(setup['study_group'].id, setup['team_semester'].id)}"
            f"?semester_id={setup['semester'].id}",
            {"name": "Beta"},
            format="json",
        )
        assert response.status_code == 403

    def test_wrong_group_returns_404(
        self,
        api_client: APIClient,
        mentor_team_setup: dict[str, Any],
        direction,
        institute,
        semester: Semester,
    ) -> None:
        setup = mentor_team_setup
        other_group = StudyGroup.objects.create(
            name="OTHER",
            code="OTHER",
            direction=direction,
            institute=institute,
            is_end=False,
        )
        _enrollment_with_mentors(other_group, semester, setup["mentor"])
        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.patch(
            f"{_team_url(other_group.id, setup['team_semester'].id)}"
            f"?semester_id={setup['semester'].id}",
            {"name": "Beta"},
            format="json",
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestMentorTeamMutations:
    def test_update_name(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.patch(
            f"{_team_url(setup['study_group'].id, setup['team_semester'].id)}"
            f"?semester_id={setup['semester'].id}",
            {"name": "Beta"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["name"] == "Beta"
        assert response.data["membersCount"] == 2

    def test_set_captain(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.patch(
            f"{_team_url(setup['study_group'].id, setup['team_semester'].id, '/captain/')}"
            f"?semester_id={setup['semester'].id}",
            {"captainId": setup["member"].id},
            format="json",
        )
        assert response.status_code == 200
        leader = next(
            item for item in response.data["members"] if item["role"] == "leader"
        )
        assert leader["userId"] == setup["member"].id

    def test_confirm_composition_when_assembled_status_allows_mentor_edit_before_confirm(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.post(
            f"{_team_url(setup['study_group'].id, setup['team_semester'].id, '/confirm-composition/')}"
            f"?semester_id={setup['semester'].id}"
        )
        assert response.status_code == 200
        assert response.data["status"] == TeamSemester.Status.ASSEMBLED

    def test_unconfirm_composition(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        team_semester = setup["team_semester"]
        team_semester.status = TeamSemester.Status.ASSEMBLED
        team_semester.save(update_fields=["status"])

        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.post(
            f"{_team_url(setup['study_group'].id, team_semester.id, '/unconfirm-composition/')}"
            f"?semester_id={setup['semester'].id}"
        )
        assert response.status_code == 200
        assert response.data["status"] == TeamSemester.Status.FORMING

    def test_add_registered_member(
        self,
        api_client: APIClient,
        mentor_team_setup: dict[str, Any],
        make_user,
    ) -> None:
        setup = mentor_team_setup
        newcomer = make_user(role_code="student", email="new@example.com")
        newcomer.study_group = setup["study_group"]
        newcomer.save(update_fields=["study_group"])

        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.post(
            f"{_team_url(setup['study_group'].id, setup['team_semester'].id, '/members/')}"
            f"?semester_id={setup['semester'].id}",
            {"userId": newcomer.id},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["membersCount"] == 3
        assert any(item["userId"] == newcomer.id for item in response.data["members"])

    def test_add_preregistered_creates_placeholder(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        pre_registered = PreRegisteredStudent.objects.create(
            last_name="Сидоров",
            first_name="Сидор",
            student_card="25010099",
            snils="33333333333",
            personnel_number="100099",
            group=setup["study_group"],
        )

        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.post(
            f"{_team_url(setup['study_group'].id, setup['team_semester'].id, '/members/')}"
            f"?semester_id={setup['semester'].id}",
            {"preRegisteredStudentId": pre_registered.id},
            format="json",
        )
        assert response.status_code == 200
        pre_registered.refresh_from_db()
        assert pre_registered.has_placeholder_user is True
        assert pre_registered.student.is_placeholder is True
        placeholder_member = next(
            item
            for item in response.data["members"]
            if item["userId"] == pre_registered.student_id
        )
        assert placeholder_member["isPlaceholder"] is True

    def test_remove_member(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        group_id = setup["study_group"].id
        team_id = setup["team_semester"].id
        member_id = setup["member"].id
        semester_id = setup["semester"].id
        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.delete(
            f"{_team_url(group_id, team_id, f'/members/{member_id}/')}"
            f"?semester_id={semester_id}"
        )
        assert response.status_code == 200
        assert response.data["membersCount"] == 1

    def test_cannot_remove_captain(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        group_id = setup["study_group"].id
        team_id = setup["team_semester"].id
        captain_id = setup["captain"].id
        semester_id = setup["semester"].id
        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.delete(
            f"{_team_url(group_id, team_id, f'/members/{captain_id}/')}"
            f"?semester_id={semester_id}"
        )
        assert response.status_code == 400
        assert "капитана" in response.data["error"]

    def test_delete_empty_team(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        team_semester = setup["team_semester"]
        TeamSemesterMember.objects.filter(team_semester=team_semester).delete()

        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.delete(
            f"{_team_url(setup['study_group'].id, team_semester.id)}"
            f"?semester_id={setup['semester'].id}"
        )
        assert response.status_code == 200
        assert response.data["membersCount"] == 0
        assert not TeamSemester.objects.filter(pk=team_semester.id).exists()

    def test_delete_non_empty_team_returns_400(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.delete(
            f"{_team_url(setup['study_group'].id, setup['team_semester'].id)}"
            f"?semester_id={setup['semester'].id}"
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestMentorTeamProjectEnrollmentBlock:
    @pytest.mark.parametrize(
        "method,url_suffix,payload",
        [
            ("patch", "", {"name": "Blocked"}),
            ("patch", "/captain/", {"captainId": 1}),
            ("post", "/confirm-composition/", None),
            ("post", "/unconfirm-composition/", None),
            ("post", "/members/", {"userId": 1}),
            ("delete", "/members/1/", None),
        ],
    )
    def test_enrolled_team_returns_409(
        self,
        api_client: APIClient,
        mentor_team_setup: dict[str, Any],
        method: str,
        url_suffix: str,
        payload: dict[str, Any] | None,
    ) -> None:
        setup = mentor_team_setup
        team_semester = setup["team_semester"]
        team_semester.project_application = setup["app"]
        team_semester.save(update_fields=["project_application"])

        api_client.force_authenticate(user=setup["mentor"])
        url = (
            f"{_team_url(setup['study_group'].id, team_semester.id, url_suffix)}"
            f"?semester_id={setup['semester'].id}"
        )
        if method == "patch":
            response = api_client.patch(url, payload, format="json")
        elif method == "post":
            response = api_client.post(url, payload or {}, format="json")
        else:
            response = api_client.delete(url)

        assert response.status_code == 409
        assert "проект" in response.data["error"].lower()

    def test_delete_enrolled_team_returns_409(
        self, api_client: APIClient, mentor_team_setup: dict[str, Any]
    ) -> None:
        setup = mentor_team_setup
        team_semester = setup["team_semester"]
        team_semester.project_application = setup["app"]
        team_semester.save(update_fields=["project_application"])
        TeamSemesterMember.objects.filter(team_semester=team_semester).delete()

        api_client.force_authenticate(user=setup["mentor"])
        response = api_client.delete(
            f"{_team_url(setup['study_group'].id, team_semester.id)}"
            f"?semester_id={setup['semester'].id}"
        )
        assert response.status_code == 409


@pytest.mark.django_db
class TestPlaceholderUserRegistration:
    def test_register_updates_placeholder_user(
        self,
        roles: dict[str, Any],
        study_group: StudyGroup,
    ) -> None:
        pre_registered = PreRegisteredStudent.objects.create(
            last_name="Иванов",
            first_name="Иван",
            middle_name="Иванович",
            student_card="25011884",
            snils="18457362806",
            personnel_number="1335090",
            group=study_group,
        )
        placeholder = PlaceholderUserService().get_or_create_placeholder(pre_registered)
        assert placeholder.is_placeholder is True

        from django.core import mail
        from django.test import override_settings

        with override_settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
        ):
            result = PreRegisteredStudentService().register(
                pre_registered_id=pre_registered.pk,
                email="student@example.com",
                password="StrongPass123!",
            )

        pre_registered.refresh_from_db()
        placeholder.refresh_from_db()
        assert pre_registered.is_registered is True
        assert pre_registered.has_placeholder_user is False
        assert placeholder.is_placeholder is False
        assert placeholder.email == "student@example.com"
        assert placeholder.pk == result["user"]["id"]
        assert len(mail.outbox) == 1
