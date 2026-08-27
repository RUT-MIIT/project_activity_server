"""Тесты API «Моя команда»."""

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
    TeamEventLog,
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


@pytest.fixture
def my_team_setup(roles, make_user, semester, study_group, statuses, departments):
    admin = make_user(role_code="admin")
    captain = make_user(role_code="student", email="cap@example.com")
    captain.study_group = study_group
    captain.save(update_fields=["study_group"])
    member = make_user(role_code="student", email="mem@example.com")
    member.study_group = study_group
    member.save(update_fields=["study_group"])
    outsider = make_user(role_code="student", email="out@example.com")
    outsider.study_group = study_group
    outsider.save(update_fields=["study_group"])

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
        min_team_members=2,
        max_team_members=5,
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
        recommended_teams_count=app.recommended_teams_count,
    )
    ProjectTrackGroup.objects.create(project_track=track, study_group=study_group)
    ProjectTrackApplication.objects.create(project_track=track, project_application=app)

    team = Team.objects.create(name="Alpha", home_study_group=study_group)
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
    TeamEventLog.objects.create(
        team=team,
        team_semester=ts,
        user=captain,
        text="Команда создана",
    )
    return {
        "captain": captain,
        "member": member,
        "outsider": outsider,
        "team_semester": ts,
        "track": track,
        "group": study_group,
        "semester": semester,
    }


@pytest.mark.django_db
class TestMyTeamViewSet:
    def test_captain_sees_pending_without_event_log(self, api_client, my_team_setup):
        ts = my_team_setup["team_semester"]
        TeamJoinRequest.objects.create(
            team_semester=ts,
            user=my_team_setup["outsider"],
            status=TeamJoinRequest.Status.PENDING,
        )
        api_client.force_authenticate(user=my_team_setup["captain"])
        response = api_client.get("/api/teams/my-team/")
        assert response.status_code == 200
        assert response.data["isCaptain"] is True
        assert len(response.data["joinRequests"]) == 1
        assert "eventLog" not in response.data
        assert response.data["minTeamMembers"] == 2
        assert response.data["maxTeamMembers"] == 5

    def test_event_log_paginated(self, api_client, my_team_setup):
        ts = my_team_setup["team_semester"]
        captain = my_team_setup["captain"]
        TeamEventLog.objects.filter(team_semester=ts).delete()
        for i in range(55):
            TeamEventLog.objects.create(
                user=captain,
                team=ts.team,
                team_semester=ts,
                text=f"Событие {i}",
            )
        api_client.force_authenticate(user=captain)
        page1 = api_client.get("/api/teams/my-team/event-log/")
        assert page1.status_code == 200
        assert page1.data["count"] == 55
        assert len(page1.data["results"]) == 50
        assert page1.data["next"] is not None
        assert "user_id" in page1.data["results"][0]
        assert "text" in page1.data["results"][0]
        assert "created_at" in page1.data["results"][0]

        page2 = api_client.get("/api/teams/my-team/event-log/?page=2")
        assert page2.status_code == 200
        assert len(page2.data["results"]) == 5
        assert page2.data["previous"] is not None

    def test_event_log_404_without_team(self, api_client, my_team_setup):
        outsider = my_team_setup["outsider"]
        api_client.force_authenticate(user=outsider)
        response = api_client.get("/api/teams/my-team/event-log/")
        assert response.status_code == 404

    def test_approve_join_request_with_role(self, api_client, my_team_setup):
        ts = my_team_setup["team_semester"]
        applicant = my_team_setup["outsider"]
        join = TeamJoinRequest.objects.create(
            team_semester=ts,
            user=applicant,
            status=TeamJoinRequest.Status.PENDING,
        )
        # вторая pending-заявка того же студента в другой команде
        other_cap = User.objects.create_user(
            email="oc2@example.com",
            password="pass",
            first_name="O",
            last_name="C",
            role=applicant.role,
            study_group=my_team_setup["group"],
        )
        other_team = Team.objects.create(
            name="Other", home_study_group=my_team_setup["group"]
        )
        other_ts = TeamSemester.objects.create(
            team=other_team,
            semester=my_team_setup["semester"],
            project_track=my_team_setup["track"],
            captain=other_cap,
        )
        TeamSemesterMember.objects.create(
            team_semester=other_ts,
            user=other_cap,
            role=TeamSemesterMember.Role.LEADER,
        )
        other_join = TeamJoinRequest.objects.create(
            team_semester=other_ts,
            user=applicant,
            status=TeamJoinRequest.Status.PENDING,
        )

        api_client.force_authenticate(user=my_team_setup["captain"])
        response = api_client.post(
            f"/api/teams/my-team/join-requests/{join.id}/approve/",
            {"role": "member"},
            format="json",
        )
        assert response.status_code == 200
        assert any(m["id"] == applicant.id for m in response.data["members"])
        join.refresh_from_db()
        other_join.refresh_from_db()
        assert join.status == TeamJoinRequest.Status.APPROVED
        assert other_join.status == TeamJoinRequest.Status.OBSOLETE
        texts = list(
            TeamEventLog.objects.filter(team_semester=ts).values_list("text", flat=True)
        )
        assert any("Одобрена заявка" in t for t in texts)

    def test_reject_join_and_invitation_write_event_log(
        self, api_client, my_team_setup
    ):
        ts = my_team_setup["team_semester"]
        captain = my_team_setup["captain"]
        outsider = my_team_setup["outsider"]
        member = my_team_setup["member"]

        join = TeamJoinRequest.objects.create(
            team_semester=ts,
            user=outsider,
            status=TeamJoinRequest.Status.PENDING,
        )
        api_client.force_authenticate(user=captain)
        reject_join = api_client.post(
            f"/api/teams/my-team/join-requests/{join.id}/reject/"
        )
        assert reject_join.status_code == 200
        assert TeamEventLog.objects.filter(
            team_semester=ts, text__contains="Отклонена заявка"
        ).exists()

        invite = api_client.post(
            "/api/teams/my-team/invitations/",
            {"user_id": member.id, "role": "member"},
            format="json",
        )
        assert invite.status_code == 201
        invitation_id = invite.data["id"]

        api_client.force_authenticate(user=member)
        reject_inv = api_client.post(
            f"/api/teams/lobby/invitations/{invitation_id}/reject/"
        )
        assert reject_inv.status_code == 200
        assert TeamEventLog.objects.filter(
            team_semester=ts, text__contains="Отклонено приглашение"
        ).exists()

        # повторное приглашение и принятие
        api_client.force_authenticate(user=captain)
        invite2 = api_client.post(
            "/api/teams/my-team/invitations/",
            {"user_id": member.id, "role": "member"},
            format="json",
        )
        assert invite2.status_code == 201
        api_client.force_authenticate(user=member)
        accept = api_client.post(
            f"/api/teams/lobby/invitations/{invite2.data['id']}/accept/"
        )
        assert accept.status_code == 200
        assert TeamEventLog.objects.filter(
            team_semester=ts, text__contains="Принято приглашение"
        ).exists()

    def test_invite_kick_leave_confirm_delete(self, api_client, my_team_setup):
        captain = my_team_setup["captain"]
        member = my_team_setup["member"]
        api_client.force_authenticate(user=captain)

        inv = api_client.post(
            "/api/teams/my-team/invitations/",
            {"user_id": member.id, "role": "member"},
            format="json",
        )
        assert inv.status_code == 201

        api_client.force_authenticate(user=member)
        accept = api_client.post(
            f"/api/teams/lobby/invitations/{inv.data['id']}/accept/"
        )
        assert accept.status_code == 200

        api_client.force_authenticate(user=captain)
        kick = api_client.delete(f"/api/teams/my-team/members/{member.id}/")
        assert kick.status_code == 200
        assert all(m["id"] != member.id for m in kick.data["members"])

        # снова принять через заявку
        TeamJoinRequest.objects.create(
            team_semester=my_team_setup["team_semester"],
            user=member,
            status=TeamJoinRequest.Status.PENDING,
        )
        join = TeamJoinRequest.objects.filter(
            team_semester=my_team_setup["team_semester"],
            user=member,
            status=TeamJoinRequest.Status.PENDING,
        ).first()
        api_client.post(
            f"/api/teams/my-team/join-requests/{join.id}/approve/",
            {"role": "member"},
            format="json",
        )

        api_client.force_authenticate(user=member)
        leave = api_client.post("/api/teams/my-team/leave/")
        assert leave.status_code == 204

        # снова добавить для confirm
        TeamJoinRequest.objects.create(
            team_semester=my_team_setup["team_semester"],
            user=member,
            status=TeamJoinRequest.Status.PENDING,
        )
        join2 = TeamJoinRequest.objects.filter(
            team_semester=my_team_setup["team_semester"],
            user=member,
            status="pending",
        ).first()
        api_client.force_authenticate(user=captain)
        api_client.post(
            f"/api/teams/my-team/join-requests/{join2.id}/approve/",
            {"role": "member"},
            format="json",
        )

        confirm = api_client.post("/api/teams/my-team/confirm-composition/")
        assert confirm.status_code == 200
        assert confirm.data["status"] == "assembled"

        # после assembled нельзя кикать
        kick2 = api_client.delete(f"/api/teams/my-team/members/{member.id}/")
        assert kick2.status_code == 400

        api_client.force_authenticate(user=member)
        leave2 = api_client.post("/api/teams/my-team/leave/")
        assert leave2.status_code == 400

    def test_delete_team_requires_empty_roster(self, api_client, my_team_setup):
        captain = my_team_setup["captain"]
        member = my_team_setup["member"]
        ts = my_team_setup["team_semester"]
        TeamSemesterMember.objects.create(
            team_semester=ts,
            user=member,
            role=TeamSemesterMember.Role.MEMBER,
        )
        api_client.force_authenticate(user=captain)
        response = api_client.delete("/api/teams/my-team/")
        assert response.status_code == 400

        api_client.delete(f"/api/teams/my-team/members/{member.id}/")
        response = api_client.delete("/api/teams/my-team/")
        assert response.status_code == 204
        assert not TeamSemester.objects.filter(pk=ts.id).exists()

    def test_member_view_can_leave(self, api_client, my_team_setup):
        ts = my_team_setup["team_semester"]
        member = my_team_setup["member"]
        TeamSemesterMember.objects.create(
            team_semester=ts,
            user=member,
            role=TeamSemesterMember.Role.MEMBER,
        )
        api_client.force_authenticate(user=member)
        response = api_client.get("/api/teams/my-team/")
        assert response.status_code == 200
        assert response.data["isCaptain"] is False
        assert response.data["canLeave"] is True
        assert "joinRequests" not in response.data

    def test_limits_from_sole_group_track_when_team_has_no_track(
        self, api_client, my_team_setup
    ):
        """Без трека у команды, но один трек у группы → лимиты с трека группы."""
        ts = my_team_setup["team_semester"]
        track = my_team_setup["track"]
        track.min_team_members = 3
        track.max_team_members = 6
        track.save(update_fields=["min_team_members", "max_team_members"])
        ts.project_track = None
        ts.save(update_fields=["project_track"])

        api_client.force_authenticate(user=my_team_setup["captain"])
        response = api_client.get("/api/teams/my-team/")
        assert response.status_code == 200
        assert ts.project_track_id is None
        assert response.data["minTeamMembers"] == 3
        assert response.data["maxTeamMembers"] == 6

    def test_limits_default_when_group_has_multiple_tracks(
        self, api_client, my_team_setup, departments
    ):
        """Без трека у команды и >1 трека у группы → дефолты 4/7."""
        ts = my_team_setup["team_semester"]
        admin = my_team_setup["track"].author
        second = ProjectTrack.objects.create(
            name="Второй трек",
            department=departments["child"],
            semester=my_team_setup["semester"],
            author=admin,
            min_team_members=2,
            max_team_members=5,
            recommended_teams_count=3,
        )
        ProjectTrackGroup.objects.create(
            project_track=second, study_group=my_team_setup["group"]
        )
        ts.project_track = None
        ts.save(update_fields=["project_track"])

        api_client.force_authenticate(user=my_team_setup["captain"])
        response = api_client.get("/api/teams/my-team/")
        assert response.status_code == 200
        assert response.data["minTeamMembers"] == 4
        assert response.data["maxTeamMembers"] == 7

    def test_my_team_no_n_plus_one(self, api_client, my_team_setup):
        """Число запросов GET /my-team/ не растёт с числом заявок/приглашений."""
        ts = my_team_setup["team_semester"]
        captain = my_team_setup["captain"]
        role = captain.role
        group = my_team_setup["group"]

        def _outsider(email: str):
            return User.objects.create_user(
                email=email,
                password="pass",
                first_name="O",
                last_name="U",
                role=role,
                study_group=group,
            )

        for i in range(3):
            TeamJoinRequest.objects.create(
                team_semester=ts,
                user=_outsider(f"jr{i}@example.com"),
                status=TeamJoinRequest.Status.PENDING,
            )

        api_client.force_authenticate(user=captain)
        with CaptureQueriesContext(connection) as ctx_small:
            small = api_client.get("/api/teams/my-team/")
        assert small.status_code == 200
        assert len(small.data["joinRequests"]) == 3
        small_q = len(ctx_small.captured_queries)

        for i in range(5):
            TeamJoinRequest.objects.create(
                team_semester=ts,
                user=_outsider(f"jr_more{i}@example.com"),
                status=TeamJoinRequest.Status.PENDING,
            )

        with CaptureQueriesContext(connection) as ctx_large:
            large = api_client.get("/api/teams/my-team/")
        assert large.status_code == 200
        assert len(large.data["joinRequests"]) == 8
        assert len(ctx_large.captured_queries) <= small_q + 1
        assert len(ctx_large.captured_queries) <= 15
