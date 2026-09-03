"""Тесты API студенческой витрины проектов."""

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
    Tag,
)
from teams.models import (
    Direction,
    StudyGroup,
    Team,
    TeamEventLog,
    TeamSemester,
    TeamSemesterMember,
)

BASE = "/api/showcase/student-showcase"


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
def other_group(direction, institute):
    return StudyGroup.objects.create(
        name="G2",
        code="g2",
        direction=direction,
        institute=institute,
    )


def _approved_app(
    *,
    semester,
    statuses,
    departments,
    title="Проект",
    teams=3,
    min_members=2,
    max_members=5,
    company="ООО Заказчик",
    company_contacts="secret@example.com",
):
    app = ProjectApplication.objects.create(
        title=title,
        company=company,
        company_contacts=company_contacts,
        author_lastname="Иванов",
        author_firstname="Иван",
        author_email="a@example.com",
        author_phone="+79990000000",
        semester=semester,
        status=statuses["approved"],
        goal="Цель проекта для витрины",
        barrier="Барьер проекта для витрины",
        existing_solutions="Существующие решения",
        context="Контекст проекта",
        stakeholders="Заинтересованные стороны",
        project_level="L1",
        problem_holder="Носитель",
        recommended_teams_count=teams,
        min_team_members=min_members,
        max_team_members=max_members,
    )
    ApplicationInvolvedDepartment.objects.create(
        application=app, department=departments["child"]
    )
    return app


def _track(*, name, semester, department, author, group, applications):
    total = sum(app.recommended_teams_count for app in applications)
    track = ProjectTrack.objects.create(
        name=name,
        description=f"Описание {name}",
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


def _create_assembled_team(
    *,
    group,
    semester,
    track,
    captain,
    name,
    members=None,
):
    team = Team.objects.create(name=name, home_study_group=group)
    ts = TeamSemester.objects.create(
        team=team,
        semester=semester,
        project_track=track,
        captain=captain,
        status=TeamSemester.Status.ASSEMBLED,
    )
    TeamSemesterMember.objects.create(
        team_semester=ts,
        user=captain,
        role=TeamSemesterMember.Role.LEADER,
    )
    for member in members or []:
        TeamSemesterMember.objects.create(
            team_semester=ts,
            user=member,
            role=TeamSemesterMember.Role.MEMBER,
        )
    return ts


@pytest.fixture
def showcase_setup(
    roles, make_user, semester, study_group, other_group, statuses, departments
):
    admin = make_user(role_code="admin")
    captain = make_user(role_code="student", email="cap@example.com")
    captain.study_group = study_group
    captain.save(update_fields=["study_group"])
    member = make_user(role_code="student", email="mem@example.com")
    member.study_group = study_group
    member.save(update_fields=["study_group"])
    other_student = make_user(role_code="student", email="other@example.com")
    other_student.study_group = other_group
    other_student.save(update_fields=["study_group"])

    tag = Tag.objects.create(name="AI", category="Tech")
    app1 = _approved_app(
        semester=semester,
        statuses=statuses,
        departments=departments,
        title="A1",
        teams=2,
    )
    app1.is_continuing = True
    app1.is_competitive_selection = True
    app1.save(update_fields=["is_continuing", "is_competitive_selection"])
    app1.tags.add(tag)
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
    # Трек чужой группы — не должен быть виден студенту G1
    app_foreign = _approved_app(
        semester=semester,
        statuses=statuses,
        departments=departments,
        title="Foreign",
        teams=1,
    )
    _track(
        name="Чужой трек",
        semester=semester,
        department=departments["child"],
        author=admin,
        group=other_group,
        applications=[app_foreign],
    )

    return {
        "admin": admin,
        "captain": captain,
        "member": member,
        "other_student": other_student,
        "group": study_group,
        "other_group": other_group,
        "semester": semester,
        "track1": track1,
        "track2": track2,
        "app1": app1,
        "app2": app2,
        "app3": app3,
        "app_foreign": app_foreign,
        "tag": tag,
    }


@pytest.mark.django_db
class TestStudentShowcaseAccess:
    def test_non_student_forbidden(self, api_client, roles, make_user):
        user = make_user(role_code="admin")
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE}/")
        assert response.status_code == 403

    def test_student_without_group_forbidden(self, api_client, roles, make_user):
        user = make_user(role_code="student", email="nogroup@example.com")
        api_client.force_authenticate(user=user)
        response = api_client.get(f"{BASE}/")
        assert response.status_code == 403


@pytest.mark.django_db
class TestStudentShowcaseList:
    def test_lists_only_own_group_tracks(self, api_client, showcase_setup):
        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.get(f"{BASE}/")
        assert response.status_code == 200
        assert response["Cache-Control"] == "private, max-age=30"
        tracks = {t["id"]: t for t in response.data}
        assert showcase_setup["track1"].id in tracks
        assert showcase_setup["track2"].id in tracks
        assert len(tracks) == 2
        assert tracks[showcase_setup["track1"].id]["name"] == "Трек 1"
        assert tracks[showcase_setup["track1"].id]["description"] == "Описание Трек 1"
        projects = {p["id"]: p for p in tracks[showcase_setup["track1"].id]["projects"]}
        assert projects[showcase_setup["app1"].id]["title"] == "A1"
        assert projects[showcase_setup["app1"].id]["company"] == "ООО Заказчик"
        assert projects[showcase_setup["app1"].id]["maxTeams"] == 2
        assert projects[showcase_setup["app1"].id]["enrolledTeamsCount"] == 0
        assert projects[showcase_setup["app1"].id]["minTeamMembers"] == 2
        assert projects[showcase_setup["app1"].id]["maxTeamMembers"] == 5
        assert projects[showcase_setup["app1"].id]["isContinuing"] is True
        assert projects[showcase_setup["app1"].id]["isCompetitiveSelection"] is True
        assert projects[showcase_setup["app2"].id]["isContinuing"] is False
        assert projects[showcase_setup["app2"].id]["isCompetitiveSelection"] is False
        assert projects[showcase_setup["app1"].id]["tags"] == [
            {"id": showcase_setup["tag"].id, "name": "AI", "category": "Tech"}
        ]

    def test_enrolled_teams_count(self, api_client, showcase_setup):
        _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            name="Alpha",
            members=[showcase_setup["member"]],
        )
        ts = TeamSemester.objects.get(captain=showcase_setup["captain"])
        ts.project_application = showcase_setup["app1"]
        ts.save(update_fields=["project_application"])

        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.get(f"{BASE}/")
        assert response.status_code == 200
        tracks = {t["id"]: t for t in response.data}
        projects = {p["id"]: p for p in tracks[showcase_setup["track1"].id]["projects"]}
        assert projects[showcase_setup["app1"].id]["enrolledTeamsCount"] == 1
        assert projects[showcase_setup["app2"].id]["enrolledTeamsCount"] == 0

    def test_list_query_count_stable(
        self, api_client, showcase_setup, departments, statuses
    ):
        """Число SQL не растёт пропорционально числу проектов."""
        api_client.force_authenticate(user=showcase_setup["captain"])
        with CaptureQueriesContext(connection) as ctx_small:
            response_small = api_client.get(f"{BASE}/")
        assert response_small.status_code == 200
        queries_small = len(ctx_small.captured_queries)

        extra_apps = [
            _approved_app(
                semester=showcase_setup["semester"],
                statuses=statuses,
                departments=departments,
                title=f"Extra{i}",
                teams=1,
            )
            for i in range(5)
        ]
        for app in extra_apps:
            ProjectTrackApplication.objects.create(
                project_track=showcase_setup["track1"],
                project_application=app,
            )

        with CaptureQueriesContext(connection) as ctx_large:
            response_large = api_client.get(f"{BASE}/")
        assert response_large.status_code == 200
        queries_large = len(ctx_large.captured_queries)
        assert queries_large <= queries_small + 1


@pytest.mark.django_db
class TestStudentShowcaseDetail:
    def test_detail_fields_without_contacts(self, api_client, showcase_setup):
        api_client.force_authenticate(user=showcase_setup["captain"])
        app = showcase_setup["app1"]
        response = api_client.get(f"{BASE}/projects/{app.id}/")
        assert response.status_code == 200
        assert response["Cache-Control"] == "private, max-age=30"
        data = response.data
        assert data["title"] == "A1"
        assert data["company"] == "ООО Заказчик"
        assert data["goal"] == "Цель проекта для витрины"
        assert data["barrier"] == "Барьер проекта для витрины"
        assert data["existing_solutions"] == "Существующие решения"
        assert data["context"] == "Контекст проекта"
        assert data["stakeholders"] == "Заинтересованные стороны"
        assert data["project_level"] == "L1"
        assert data["track_id"] == showcase_setup["track1"].id
        assert data["recommended_teams_count"] == 2
        assert data["enrolled_teams_count"] == 0
        assert data["is_continuing"] is True
        assert data["is_competitive_selection"] is True
        assert "company_contacts" not in data
        assert "companyContacts" not in data
        assert "author_email" not in data
        assert "authorEmail" not in data
        assert "author_phone" not in data

    def test_foreign_project_not_found(self, api_client, showcase_setup):
        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.get(
            f"{BASE}/projects/{showcase_setup['app_foreign'].id}/"
        )
        assert response.status_code == 404

    def test_can_enroll_true_for_assembled_captain(self, api_client, showcase_setup):
        _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            name="Alpha",
            members=[showcase_setup["member"]],
        )
        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.get(f"{BASE}/projects/{showcase_setup['app1'].id}/")
        assert response.status_code == 200
        assert response.data["can_enroll"] is True


@pytest.mark.django_db
class TestStudentShowcaseEnroll:
    def test_enroll_success(self, api_client, showcase_setup):
        ts = _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            name="Alpha",
            members=[showcase_setup["member"]],
        )
        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.post(
            f"{BASE}/projects/{showcase_setup['app1'].id}/enroll/"
        )
        assert response.status_code == 200
        assert response.data["teamSemesterId"] == ts.id
        assert response.data["projectId"] == showcase_setup["app1"].id
        assert response.data["projectTitle"] == "A1"

        ts.refresh_from_db()
        assert ts.project_application_id == showcase_setup["app1"].id
        assert TeamEventLog.objects.filter(
            team_semester=ts,
            text__contains="A1",
        ).exists()

    def test_enroll_forbidden_for_member(self, api_client, showcase_setup):
        _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            name="Alpha",
            members=[showcase_setup["member"]],
        )
        api_client.force_authenticate(user=showcase_setup["member"])
        response = api_client.post(
            f"{BASE}/projects/{showcase_setup['app1'].id}/enroll/"
        )
        assert response.status_code == 403

    def test_enroll_rejected_when_forming(self, api_client, showcase_setup):
        team = Team.objects.create(
            name="Forming", home_study_group=showcase_setup["group"]
        )
        ts = TeamSemester.objects.create(
            team=team,
            semester=showcase_setup["semester"],
            project_track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            status=TeamSemester.Status.FORMING,
        )
        TeamSemesterMember.objects.create(
            team_semester=ts,
            user=showcase_setup["captain"],
            role=TeamSemesterMember.Role.LEADER,
        )
        TeamSemesterMember.objects.create(
            team_semester=ts,
            user=showcase_setup["member"],
            role=TeamSemesterMember.Role.MEMBER,
        )
        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.post(
            f"{BASE}/projects/{showcase_setup['app1'].id}/enroll/"
        )
        assert response.status_code == 400
        assert "подтверждения состава" in response.data["error"]

    def test_enroll_rejected_when_already_enrolled(self, api_client, showcase_setup):
        ts = _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            name="Alpha",
            members=[showcase_setup["member"]],
        )
        ts.project_application = showcase_setup["app1"]
        ts.save(update_fields=["project_application"])

        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.post(
            f"{BASE}/projects/{showcase_setup['app2'].id}/enroll/"
        )
        assert response.status_code == 400
        assert "уже записана" in response.data["error"]

    def test_enroll_rejected_when_quota_full(
        self, api_client, showcase_setup, make_user
    ):
        # app2: maxTeams=1
        other_cap = make_user(role_code="student", email="oc@example.com")
        other_cap.study_group = showcase_setup["group"]
        other_cap.save(update_fields=["study_group"])
        other_mem = make_user(role_code="student", email="om@example.com")
        other_mem.study_group = showcase_setup["group"]
        other_mem.save(update_fields=["study_group"])

        first = _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=other_cap,
            name="First",
            members=[other_mem],
        )
        first.project_application = showcase_setup["app2"]
        first.save(update_fields=["project_application"])

        _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            name="Second",
            members=[showcase_setup["member"]],
        )
        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.post(
            f"{BASE}/projects/{showcase_setup['app2'].id}/enroll/"
        )
        assert response.status_code == 400
        assert "максимальное число команд" in response.data["error"]

    def test_enroll_rejected_project_not_in_team_track(
        self, api_client, showcase_setup
    ):
        _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            name="Alpha",
            members=[showcase_setup["member"]],
        )
        api_client.force_authenticate(user=showcase_setup["captain"])
        # app3 в track2, команда в track1
        response = api_client.post(
            f"{BASE}/projects/{showcase_setup['app3'].id}/enroll/"
        )
        assert response.status_code == 400

    def test_enroll_last_slot_second_team_fails(
        self, api_client, showcase_setup, make_user
    ):
        """После заполнения последнего слота вторая команда получает 400."""
        # app2: maxTeams=1 — первый успех, второй отказ
        cap1 = showcase_setup["captain"]
        mem1 = showcase_setup["member"]
        cap2 = make_user(role_code="student", email="cap2@example.com")
        cap2.study_group = showcase_setup["group"]
        cap2.save(update_fields=["study_group"])
        mem2 = make_user(role_code="student", email="mem2@example.com")
        mem2.study_group = showcase_setup["group"]
        mem2.save(update_fields=["study_group"])

        _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=cap1,
            name="T1",
            members=[mem1],
        )
        _create_assembled_team(
            group=showcase_setup["group"],
            semester=showcase_setup["semester"],
            track=showcase_setup["track1"],
            captain=cap2,
            name="T2",
            members=[mem2],
        )

        api_client.force_authenticate(user=cap1)
        first = api_client.post(f"{BASE}/projects/{showcase_setup['app2'].id}/enroll/")
        assert first.status_code == 200

        api_client.force_authenticate(user=cap2)
        second = api_client.post(f"{BASE}/projects/{showcase_setup['app2'].id}/enroll/")
        assert second.status_code == 400
        assert (
            TeamSemester.objects.filter(
                project_application=showcase_setup["app2"]
            ).count()
            == 1
        )

    def test_enroll_without_team(self, api_client, showcase_setup):
        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.post(
            f"{BASE}/projects/{showcase_setup['app1'].id}/enroll/"
        )
        assert response.status_code == 400
        assert "не состоите в команде" in response.data["error"]

    def test_enroll_rejects_members_out_of_range(self, api_client, showcase_setup):
        """Один участник при min_team_members=2."""
        team = Team.objects.create(
            name="Solo", home_study_group=showcase_setup["group"]
        )
        ts = TeamSemester.objects.create(
            team=team,
            semester=showcase_setup["semester"],
            project_track=showcase_setup["track1"],
            captain=showcase_setup["captain"],
            status=TeamSemester.Status.ASSEMBLED,
        )
        TeamSemesterMember.objects.create(
            team_semester=ts,
            user=showcase_setup["captain"],
            role=TeamSemesterMember.Role.LEADER,
        )
        api_client.force_authenticate(user=showcase_setup["captain"])
        response = api_client.post(
            f"{BASE}/projects/{showcase_setup['app1'].id}/enroll/"
        )
        assert response.status_code == 400
        assert "пределах" in response.data["error"]
