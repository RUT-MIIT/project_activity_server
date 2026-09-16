"""Тесты домена и сервиса сборки смешанной команды в admin."""

from django.contrib.auth import get_user_model
import pytest

from accounts.models import (
    ACTIVE_SEMESTER_SETTING_CODE,
    Semester,
    Settings,
)
from showcase.models import Institute, ProjectTrack
from teams.domain.admin_mixed_team import AdminMixedTeamDomain
from teams.models import (
    Direction,
    StudyGroup,
    TeamEventLog,
    TeamSemester,
    TeamSemesterMember,
)
from teams.services.admin_mixed_team_service import AdminMixedTeamService

User = get_user_model()


@pytest.fixture
def semester(db):
    semester = Semester.objects.create(code="s-mixed", name="S Mixed", position=1)
    Settings.objects.update_or_create(
        code=ACTIVE_SEMESTER_SETTING_CODE,
        defaults={"value": semester.code, "description": ""},
    )
    return semester


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="23.03.01",
        name="Технология транспортных процессов",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def institutes(db, departments):
    imtk = Institute.objects.create(
        code="IMTK",
        name="ИМТК",
        department=departments["parent"],
        is_active=True,
        position=1,
    )
    ief = Institute.objects.create(
        code="IEF2",
        name="ИЭФ-тест",
        department=departments["child"],
        is_active=True,
        position=2,
    )
    return {"imtk": imtk, "ief": ief}


@pytest.fixture
def mixed_setup(roles, make_user, semester, direction, institutes, departments):
    group_a = StudyGroup.objects.create(
        name="ОМНк-212",
        code="omnk212",
        direction=direction,
        institute=institutes["imtk"],
    )
    group_b = StudyGroup.objects.create(
        name="УЭБ-241",
        code="ueb241",
        direction=direction,
        institute=institutes["ief"],
    )
    author = make_user(role_code="admin", email="track-author@example.com")
    track = ProjectTrack.objects.create(
        name="Международная логистика",
        semester=semester,
        department=departments["parent"],
        author=author,
        min_team_members=4,
        max_team_members=7,
    )
    # Трек только для group_a — group_b намеренно вне трека.
    track.group_links.create(study_group=group_a)

    captain = make_user(role_code="student", email="maslov@example.com")
    captain.last_name = "Маслов"
    captain.first_name = "Алексей"
    captain.study_group = group_a
    captain.save(update_fields=["last_name", "first_name", "study_group"])

    members = []
    for idx, (email, last_name, group) in enumerate(
        [
            ("maximov@example.com", "Максимов", group_a),
            ("kiselev@example.com", "Киселев", group_a),
            ("belavina@example.com", "Белавина", group_b),
            ("yaseneva@example.com", "Ясенева", group_b),
            ("mironova@example.com", "Миронова", group_b),
        ],
        start=1,
    ):
        user = make_user(role_code="student", email=email)
        user.last_name = last_name
        user.first_name = f"Имя{idx}"
        user.study_group = group
        user.save(update_fields=["last_name", "first_name", "study_group"])
        members.append(user)

    mentor = make_user(role_code="mentor", email="kurzina@example.com")
    mentor.last_name = "Курзина"
    mentor.first_name = "Ангелина"
    mentor.save(update_fields=["last_name", "first_name"])

    return {
        "semester": semester,
        "group_a": group_a,
        "group_b": group_b,
        "track": track,
        "captain": captain,
        "members": members,
        "mentor": mentor,
    }


class TestAdminMixedTeamDomain:
    def test_merge_captain_into_members_dedupes(self):
        assert AdminMixedTeamDomain.merge_captain_into_members(
            captain_id=1,
            member_ids=[2, 1, 3, 2],
        ) == [1, 2, 3]

    def test_ensure_status_member_count_assembled_too_few(self):
        with pytest.raises(ValueError, match="не меньше"):
            AdminMixedTeamDomain.ensure_status_member_count(
                status=TeamSemester.Status.ASSEMBLED,
                members_count=3,
                min_team_members=4,
                max_team_members=7,
            )


@pytest.mark.django_db
class TestAdminMixedTeamService:
    def test_creates_team_across_institutes_without_shared_track(
        self, mixed_setup, make_user
    ):
        setup = mixed_setup
        actor = make_user(role_code="admin", email="admin-mixed@example.com")

        result = AdminMixedTeamService().create_mixed_team(
            name="Компас ЮВА",
            semester=setup["semester"],
            captain=setup["captain"],
            members=setup["members"],
            actor_id=actor.id,
            project_track=setup["track"],
            mentor=setup["mentor"],
            status=TeamSemester.Status.ASSEMBLED,
        )

        assert result.members_count == 6
        assert result.team.home_study_group_id == setup["group_a"].id
        assert result.team_semester.status == TeamSemester.Status.ASSEMBLED
        assert result.team_semester.project_track_id == setup["track"].id
        assert result.team_semester.captain_id == setup["captain"].id
        assert result.team_semester.mentor_id == setup["mentor"].id
        assert set(result.team_semester.mentors.values_list("id", flat=True)) == {
            setup["mentor"].id
        }

        members = list(
            TeamSemesterMember.objects.filter(
                team_semester=result.team_semester
            ).select_related("user")
        )
        assert len(members) == 6
        leader = next(m for m in members if m.user_id == setup["captain"].id)
        assert leader.role == TeamSemesterMember.Role.LEADER
        other_roles = {m.role for m in members if m.user_id != setup["captain"].id}
        assert other_roles == {TeamSemesterMember.Role.MEMBER}

        # Участники из группы вне трека тоже в составе.
        ueb_ids = {
            m.id for m in setup["members"] if m.study_group_id == setup["group_b"].id
        }
        member_user_ids = {m.user_id for m in members}
        assert ueb_ids.issubset(member_user_ids)

        assert TeamEventLog.objects.filter(
            team_id=result.team.id,
            text__contains="собрана вручную в admin",
        ).exists()

    def test_assigns_multiple_mentors(self, mixed_setup, make_user):
        setup = mixed_setup
        mentor2 = make_user(role_code="mentor", email="sheshel@example.com")
        mentor2.last_name = "Шешель"
        mentor2.first_name = "Артем"
        mentor2.save(update_fields=["last_name", "first_name"])

        result = AdminMixedTeamService().create_mixed_team(
            name="Компас ЮВА",
            semester=setup["semester"],
            captain=setup["captain"],
            members=setup["members"],
            mentors=[setup["mentor"], mentor2],
            status=TeamSemester.Status.ASSEMBLED,
        )

        mentor_ids = set(result.team_semester.mentors.values_list("id", flat=True))
        assert mentor_ids == {setup["mentor"].id, mentor2.id}
        assert result.team_semester.mentor_id == min(setup["mentor"].id, mentor2.id)

    def test_rejects_student_already_in_team(self, mixed_setup):
        setup = mixed_setup
        AdminMixedTeamService().create_mixed_team(
            name="Первая",
            semester=setup["semester"],
            captain=setup["captain"],
            members=setup["members"][:3],
            status=TeamSemester.Status.FORMING,
        )

        with pytest.raises(ValueError, match="Уже состоят в команде"):
            AdminMixedTeamService().create_mixed_team(
                name="Вторая",
                semester=setup["semester"],
                captain=setup["members"][0],
                members=[setup["members"][1]],
                status=TeamSemester.Status.FORMING,
            )
