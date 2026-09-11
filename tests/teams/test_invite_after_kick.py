"""Репро: после кика человек должен снова находиться в invite-candidates."""

from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

from accounts.models import ACTIVE_SEMESTER_SETTING_CODE, Semester, Settings
from showcase.models import (
    ApplicationInvolvedDepartment,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
)
from teams.models import Direction, StudyGroup, Team, TeamSemester, TeamSemesterMember

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_kicked_member_appears_in_invite_candidates(
    api_client, roles, make_user, institute, statuses, departments
):
    semester = Semester.objects.create(code="kick-s", name="S", position=1)
    Settings.objects.update_or_create(
        code=ACTIVE_SEMESTER_SETTING_CODE,
        defaults={"value": semester.code, "description": ""},
    )
    direction = Direction.objects.create(
        code="01.03.01",
        name="Math",
        level=Direction.Level.BAKALAVRIAT,
    )
    group = StudyGroup.objects.create(
        name="G", code="g", direction=direction, institute=institute
    )
    admin = make_user(role_code="admin")
    captain = make_user(role_code="student", email="cap-kick@example.com")
    captain.study_group = group
    captain.save(update_fields=["study_group"])
    member = make_user(role_code="student", email="mem-kick@example.com")
    member.last_name = "Кикнутая"
    member.first_name = "Анна"
    member.study_group = group
    member.save(update_fields=["last_name", "first_name", "study_group"])

    app = ProjectApplication.objects.create(
        title="P",
        company="ООО",
        author_lastname="И",
        author_firstname="И",
        author_email="p@example.com",
        semester=semester,
        status=statuses["approved"],
        goal="Длинная цель проекта больше пятидесяти символов для валидации",
        problem_holder="Носитель",
        barrier="Длинный барьер больше пятидесяти символов для валидации",
        recommended_teams_count=5,
    )
    ApplicationInvolvedDepartment.objects.create(
        application=app, department=departments["child"]
    )
    track = ProjectTrack.objects.create(
        name="Трек",
        department=departments["child"],
        semester=semester,
        author=admin,
        min_team_members=2,
        max_team_members=5,
        recommended_teams_count=5,
    )
    ProjectTrackGroup.objects.create(project_track=track, study_group=group)
    ProjectTrackApplication.objects.create(project_track=track, project_application=app)

    team = Team.objects.create(name="Alpha", home_study_group=group)
    ts = TeamSemester.objects.create(
        team=team,
        semester=semester,
        project_track=track,
        captain=captain,
        status=TeamSemester.Status.FORMING,
    )
    TeamSemesterMember.objects.create(
        team_semester=ts,
        user=captain,
        role=TeamSemesterMember.Role.LEADER,
    )

    api_client.force_authenticate(user=captain)
    inv = api_client.post(
        "/api/teams/my-team/invitations/",
        {"user_id": member.id, "role": "member"},
        format="json",
    )
    assert inv.status_code == 201, inv.data

    api_client.force_authenticate(user=member)
    accept = api_client.post(f"/api/teams/lobby/invitations/{inv.data['id']}/accept/")
    assert accept.status_code == 200, accept.data

    api_client.force_authenticate(user=captain)
    kick = api_client.delete(f"/api/teams/my-team/members/{member.id}/")
    assert kick.status_code == 200, kick.data

    search = api_client.get(
        "/api/teams/my-team/invite-candidates/",
        {"q": "Кикн"},
    )
    assert search.status_code == 200, search.data
    by_user = {
        item["user_id"]: item
        for item in search.data["results"]
        if item["user_id"] is not None
    }
    assert member.id in by_user, search.data
    assert by_user[member.id]["inTeam"] is False
    assert by_user[member.id]["canInvite"] is True

    inv2 = api_client.post(
        "/api/teams/my-team/invitations/",
        {"user_id": member.id, "role": "member"},
        format="json",
    )
    assert inv2.status_code == 201, inv2.data
