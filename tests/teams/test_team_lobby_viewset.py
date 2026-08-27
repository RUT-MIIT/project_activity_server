"""Тесты API лобби формирования команд."""

from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import CaptureQueriesContext
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
from teams.models import (
    Direction,
    StudyGroup,
    Team,
    TeamInvitation,
    TeamJoinRequest,
    TeamSemester,
    TeamSemesterMember,
)

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def semester(db):
    semester = Semester.objects.create(code="s1", name="S1", position=1)
    Settings.objects.update_or_create(
        code=ACTIVE_SEMESTER_SETTING_CODE,
        defaults={"value": semester.code, "description": ""},
    )
    return semester


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def study_group(direction, institute):
    return StudyGroup.objects.create(
        name="G1",
        code="g1",
        direction=direction,
        institute=institute,
    )


def _approved_app(*, semester, statuses, departments, title="Проект", teams=3):
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
        recommended_teams_count=teams,
    )
    ApplicationInvolvedDepartment.objects.create(
        application=app, department=departments["child"]
    )
    return app


def _track(*, name, semester, department, author, group, applications):
    total = sum(app.recommended_teams_count for app in applications)
    track = ProjectTrack.objects.create(
        name=name,
        department=department,
        semester=semester,
        author=author,
        min_team_members=2,
        max_team_members=5,
        recommended_teams_count=total,
    )
    ProjectTrackGroup.objects.create(project_track=track, study_group=group)
    for app in applications:
        ProjectTrackApplication.objects.create(
            project_track=track, project_application=app
        )
    return track


def _create_captained_team(*, group, semester, track, captain, name):
    team = Team.objects.create(name=name, home_study_group=group)
    ts = TeamSemester.objects.create(
        team=team,
        semester=semester,
        project_track=track,
        captain=captain,
    )
    TeamSemesterMember.objects.create(
        team_semester=ts,
        user=captain,
        role=TeamSemesterMember.Role.LEADER,
    )
    return ts


@pytest.fixture
def lobby_setup(roles, make_user, semester, study_group, statuses, departments):
    admin = make_user(role_code="admin")
    student = make_user(role_code="student", email="st@example.com")
    student.study_group = study_group
    student.save(update_fields=["study_group"])
    classmate = make_user(role_code="student", email="cls@example.com")
    classmate.study_group = study_group
    classmate.save(update_fields=["study_group"])

    app1 = _approved_app(
        semester=semester,
        statuses=statuses,
        departments=departments,
        title="A1",
        teams=2,
    )
    app2 = _approved_app(
        semester=semester,
        statuses=statuses,
        departments=departments,
        title="A2",
        teams=1,
    )
    track1 = _track(
        name="Трек 1",
        semester=semester,
        department=departments["child"],
        author=admin,
        group=study_group,
        applications=[app1, app2],
    )
    app3 = _approved_app(
        semester=semester,
        statuses=statuses,
        departments=departments,
        title="A3",
        teams=4,
    )
    track2 = _track(
        name="Трек 2",
        semester=semester,
        department=departments["child"],
        author=admin,
        group=study_group,
        applications=[app3],
    )
    return {
        "student": student,
        "classmate": classmate,
        "admin": admin,
        "group": study_group,
        "semester": semester,
        "track1": track1,
        "track2": track2,
    }


@pytest.mark.django_db
class TestTeamLobbyViewSet:
    def test_lobby_lists_tracks_and_slot_sum(self, api_client, lobby_setup):
        api_client.force_authenticate(user=lobby_setup["student"])
        response = api_client.get("/api/teams/lobby/")
        assert response.status_code == 200
        assert response.data["myTeam"] is None
        tracks = {t["id"]: t for t in response.data["tracks"]}
        assert tracks[lobby_setup["track1"].id]["recommendedTeamsCount"] == 3
        assert tracks[lobby_setup["track2"].id]["recommendedTeamsCount"] == 4
        assert tracks[lobby_setup["track1"].id]["canCreateTeam"] is True
        assert tracks[lobby_setup["track1"].id]["minTeamMembers"] == 2
        assert tracks[lobby_setup["track1"].id]["maxTeamMembers"] == 5
        assert response.data["canCreateTeam"] is True

    def test_lobby_team_limits_from_sole_group_track(self, api_client, lobby_setup):
        """Команда без трека при одном треке у группы → min/max с трека группы."""
        ProjectTrackGroup.objects.filter(project_track=lobby_setup["track2"]).delete()
        track = lobby_setup["track1"]
        track.min_team_members = 5
        track.max_team_members = 8
        track.save(update_fields=["min_team_members", "max_team_members"])

        captain = lobby_setup["student"]
        ts = _create_captained_team(
            group=lobby_setup["group"],
            semester=lobby_setup["semester"],
            track=None,
            captain=captain,
            name="NoTrack",
        )
        assert ts.project_track_id is None

        api_client.force_authenticate(user=captain)
        response = api_client.get("/api/teams/lobby/")
        assert response.status_code == 200
        team = next(t for t in response.data["teams"] if t["id"] == ts.id)
        assert team["minTeamMembers"] == 5
        assert team["maxTeamMembers"] == 8
        assert response.data["myTeam"]["minTeamMembers"] == 5
        assert response.data["myTeam"]["maxTeamMembers"] == 8
        assert response.data["tracks"][0]["minTeamMembers"] == 5
        assert response.data["tracks"][0]["maxTeamMembers"] == 8

    def test_create_team_and_join_request_flow(self, api_client, lobby_setup):
        captain = lobby_setup["student"]
        classmate = lobby_setup["classmate"]
        api_client.force_authenticate(user=captain)
        create = api_client.post(
            "/api/teams/lobby/teams/",
            {"track_id": lobby_setup["track1"].id, "name": "Alpha"},
            format="json",
        )
        assert create.status_code == 201
        team_id = create.data["id"]
        assert create.data["status"] == "forming"
        assert create.data["isCaptain"] is True

        api_client.force_authenticate(user=classmate)
        join = api_client.post(
            f"/api/teams/lobby/teams/{team_id}/join-requests/",
            format="json",
        )
        assert join.status_code == 201
        req_id = join.data["id"]

        lobby = api_client.get("/api/teams/lobby/")
        assert lobby.status_code == 200
        assert len(lobby.data["joinRequests"]) == 1
        assert lobby.data["joinRequests"][0]["id"] == req_id

    def test_create_own_team_marks_pending_join_obsolete(self, api_client, lobby_setup):
        """После создания своей команды pending-заявка в чужую → obsolete."""
        captain = lobby_setup["student"]
        classmate = lobby_setup["classmate"]
        api_client.force_authenticate(user=captain)
        created = api_client.post(
            "/api/teams/lobby/teams/",
            {"track_id": lobby_setup["track1"].id, "name": "Alpha"},
            format="json",
        )
        assert created.status_code == 201
        team_id = created.data["id"]

        api_client.force_authenticate(user=classmate)
        join = api_client.post(
            f"/api/teams/lobby/teams/{team_id}/join-requests/",
            format="json",
        )
        assert join.status_code == 201
        req_id = join.data["id"]

        own = api_client.post(
            "/api/teams/lobby/teams/",
            {"track_id": lobby_setup["track2"].id, "name": "My Team"},
            format="json",
        )
        assert own.status_code == 201
        join_req = TeamJoinRequest.objects.get(pk=req_id)
        assert join_req.status == TeamJoinRequest.Status.OBSOLETE

        lobby = api_client.get("/api/teams/lobby/")
        assert lobby.status_code == 200
        assert lobby.data["joinRequests"] == []
        assert lobby.data["myTeam"]["id"] == own.data["id"]

    def test_create_team_without_track(self, api_client, lobby_setup):
        """При нескольких треках track_id не проставляется; лимиты — effective по трекам."""
        captain = lobby_setup["student"]
        api_client.force_authenticate(user=captain)
        create = api_client.post(
            "/api/teams/lobby/teams/",
            {"name": "No Track Team"},
            format="json",
        )
        assert create.status_code == 201
        team_semester = TeamSemester.objects.get(pk=create.data["id"])
        assert team_semester.project_track_id is None

        lobby = api_client.get("/api/teams/lobby/")
        assert lobby.status_code == 200
        my_team = lobby.data["myTeam"]
        assert my_team is not None
        assert my_team["id"] == create.data["id"]
        assert my_team["track_id"] is None
        assert len(my_team["members"]) == 1
        member = my_team["members"][0]
        assert member["id"] == captain.id
        assert member["role"] == "leader"
        assert "full_name" in member
        assert member["full_name"]
        assert any(t["id"] == create.data["id"] for t in lobby.data["teams"])
        assert any(
            t["id"] == create.data["id"] and t["track_id"] is None
            for t in lobby.data["teams"]
        )
        # оба трека в fixture: min=2, max=5 → effective 2/5
        assert create.data["minTeamMembers"] == 2
        assert create.data["maxTeamMembers"] == 5
        assert my_team["minTeamMembers"] == 2
        assert my_team["maxTeamMembers"] == 5
        team_card = next(t for t in lobby.data["teams"] if t["id"] == create.data["id"])
        assert team_card["minTeamMembers"] == 2
        assert team_card["maxTeamMembers"] == 5
        # без трека команда не дублируется внутри tracks[].teams
        assert all(
            t["id"] != create.data["id"]
            for track in lobby.data["tracks"]
            for t in track["teams"]
        )

    def test_create_team_auto_assigns_single_track(self, api_client, lobby_setup):
        """Если группе доступен один трек — он проставляется без track_id в body."""
        ProjectTrackGroup.objects.filter(project_track=lobby_setup["track2"]).delete()
        captain = lobby_setup["student"]
        api_client.force_authenticate(user=captain)
        create = api_client.post(
            "/api/teams/lobby/teams/",
            {"name": "Auto Track"},
            format="json",
        )
        assert create.status_code == 201
        team_semester = TeamSemester.objects.get(pk=create.data["id"])
        assert team_semester.project_track_id == lobby_setup["track1"].id
        assert create.data["minTeamMembers"] == lobby_setup["track1"].min_team_members
        assert create.data["maxTeamMembers"] == lobby_setup["track1"].max_team_members

    def test_lobby_my_team_members_no_n_plus_one(self, api_client, lobby_setup):
        captain = lobby_setup["student"]
        classmate = lobby_setup["classmate"]
        role = captain.role
        group = lobby_setup["group"]
        api_client.force_authenticate(user=captain)
        create = api_client.post(
            "/api/teams/lobby/teams/",
            {"name": "Members Team"},
            format="json",
        )
        assert create.status_code == 201
        ts = TeamSemester.objects.get(pk=create.data["id"])
        TeamSemesterMember.objects.create(
            team_semester=ts,
            user=classmate,
            role=TeamSemesterMember.Role.MEMBER,
        )

        with CaptureQueriesContext(connection) as ctx_small:
            response_small = api_client.get("/api/teams/lobby/")
        assert response_small.status_code == 200
        assert len(response_small.data["myTeam"]["members"]) == 2
        queries_small = len(ctx_small.captured_queries)

        for i in range(3):
            extra = User.objects.create_user(
                email=f"extra{i}@example.com",
                password="pass",
                first_name="E",
                last_name=f"X{i}",
                role=role,
                study_group=group,
            )
            TeamSemesterMember.objects.create(
                team_semester=ts,
                user=extra,
                role=TeamSemesterMember.Role.MEMBER,
            )

        with CaptureQueriesContext(connection) as ctx_large:
            response_large = api_client.get("/api/teams/lobby/")
        assert response_large.status_code == 200
        assert len(response_large.data["myTeam"]["members"]) == 5
        queries_large = len(ctx_large.captured_queries)
        # Состав растёт, число SQL-запросов не должно расти пропорционально
        assert queries_large <= queries_small + 1

    def test_cannot_create_when_slots_full(self, api_client, lobby_setup):
        track = lobby_setup["track1"]
        role = lobby_setup["student"].role
        group = lobby_setup["group"]
        semester = lobby_setup["semester"]
        for i in range(3):
            cap = User.objects.create_user(
                email=f"full{i}@example.com",
                password="pass",
                first_name="C",
                last_name="C",
                role=role,
                study_group=group,
            )
            _create_captained_team(
                group=group,
                semester=semester,
                track=track,
                captain=cap,
                name=f"Full{i}",
            )

        free = User.objects.create_user(
            email="free@example.com",
            password="pass",
            first_name="F",
            last_name="F",
            role=role,
            study_group=group,
        )
        api_client.force_authenticate(user=free)
        response = api_client.post(
            "/api/teams/lobby/teams/",
            {"track_id": track.id, "name": "Overflow"},
            format="json",
        )
        assert response.status_code == 400

    def test_accept_invitation_marks_others_obsolete(self, api_client, lobby_setup):
        captain = lobby_setup["student"]
        invitee = lobby_setup["classmate"]
        api_client.force_authenticate(user=captain)
        created = api_client.post(
            "/api/teams/lobby/teams/",
            {"track_id": lobby_setup["track1"].id, "name": "Beta"},
            format="json",
        )
        assert created.status_code == 201

        other_cap = User.objects.create_user(
            email="oc@example.com",
            password="pass",
            first_name="O",
            last_name="C",
            role=captain.role,
            study_group=lobby_setup["group"],
        )
        other_ts = _create_captained_team(
            group=lobby_setup["group"],
            semester=lobby_setup["semester"],
            track=lobby_setup["track1"],
            captain=other_cap,
            name="Other",
        )
        join = TeamJoinRequest.objects.create(
            team_semester=other_ts,
            user=invitee,
            status=TeamJoinRequest.Status.PENDING,
        )

        inv = api_client.post(
            "/api/teams/my-team/invitations/",
            {"user_id": invitee.id, "role": "member"},
            format="json",
        )
        assert inv.status_code == 201
        invitation_id = inv.data["id"]

        api_client.force_authenticate(user=invitee)
        accept = api_client.post(
            f"/api/teams/lobby/invitations/{invitation_id}/accept/"
        )
        assert accept.status_code == 200
        join.refresh_from_db()
        assert join.status == TeamJoinRequest.Status.OBSOLETE
        invitation = TeamInvitation.objects.get(pk=invitation_id)
        assert invitation.status == TeamInvitation.Status.ACCEPTED

    def test_lobby_n_plus_one_budget(self, api_client, lobby_setup):
        for track in (lobby_setup["track1"], lobby_setup["track2"]):
            for i in range(2):
                cap = User.objects.create_user(
                    email=f"n{track.id}_{i}@example.com",
                    password="pass",
                    first_name="N",
                    last_name="N",
                    role=lobby_setup["student"].role,
                    study_group=lobby_setup["group"],
                )
                _create_captained_team(
                    group=lobby_setup["group"],
                    semester=lobby_setup["semester"],
                    track=track,
                    captain=cap,
                    name=f"N{track.id}-{i}",
                )

        api_client.force_authenticate(user=lobby_setup["student"])
        with CaptureQueriesContext(connection) as ctx:
            response = api_client.get("/api/teams/lobby/")
        assert response.status_code == 200
        assert len(response.data["tracks"]) == 2
        assert len(response.data["teams"]) == 4
        assert sum(len(t["teams"]) for t in response.data["tracks"]) == 4
        assert len(ctx.captured_queries) <= 20
