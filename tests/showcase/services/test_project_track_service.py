"""Тесты ProjectTrackService."""

import pytest

from showcase.dto.project_track import (
    ProjectTrackAddApplicationItemDTO,
    ProjectTrackAddApplicationsDTO,
    ProjectTrackAddGroupsDTO,
    ProjectTrackCreateDTO,
    ProjectTrackUpdateDTO,
)
from showcase.models import (
    ApplicationInvolvedDepartment,
    Institute,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
)
from showcase.services.project_track_service import ProjectTrackService
from teams.models import Direction, StudyGroup


@pytest.fixture
def semester(db):
    from accounts.models import Department, Semester

    return Semester.objects.create(code="s1", name="S1", position=1)


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def other_institute(departments):
    from accounts.models import Department

    other_dept = Department.objects.create(name="Other Parent", short_name="OP")
    return Institute.objects.create(
        code="OTHER",
        name="Other Institute",
        position=2,
        department=other_dept,
    )


def _create_approved_app(
    *,
    semester,
    statuses,
    involved_department=None,
    title: str = "Проект",
) -> ProjectApplication:
    app = ProjectApplication.objects.create(
        title=title,
        company="ООО Тест",
        author_lastname="Иванов",
        author_firstname="Иван",
        author_email="ivan@example.com",
        semester=semester,
        status=statuses["approved"],
        goal="Длинная цель проекта больше пятидесяти символов для валидации",
        problem_holder="Носитель",
        barrier="Длинный барьер больше пятидесяти символов для валидации",
    )
    if involved_department is not None:
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=involved_department,
        )
    return app


def _create_track_with_links(
    *,
    name: str,
    semester,
    department,
    author,
    group,
    application,
    max_teams: int = 100,
) -> ProjectTrack:
    track = ProjectTrack.objects.create(
        name=name,
        description="Описание",
        department=department,
        semester=semester,
        author=author,
        max_teams=max_teams,
    )
    ProjectTrackGroup.objects.create(project_track=track, study_group=group)
    ProjectTrackApplication.objects.create(
        project_track=track,
        project_application=application,
    )
    return track


@pytest.fixture
def track_data(
    statuses, institute, other_institute, direction, semester, departments, make_user
):
    admin = make_user(role_code="admin")
    own_group = StudyGroup.objects.create(
        name="Группа 1",
        code="g1",
        direction=direction,
        institute=institute,
    )
    other_group = StudyGroup.objects.create(
        name="Группа 2",
        code="g2",
        direction=direction,
        institute=other_institute,
    )
    own_app = _create_approved_app(
        semester=semester,
        statuses=statuses,
        involved_department=departments["child"],
        title="Свой",
    )
    from accounts.models import Department

    other_child = Department.objects.create(
        name="Other Child",
        short_name="OC",
        parent=other_institute.department,
    )
    other_app = _create_approved_app(
        semester=semester,
        statuses=statuses,
        involved_department=other_child,
        title="Чужой",
    )
    track = _create_track_with_links(
        name="Трек 1",
        semester=semester,
        department=departments["child"],
        author=admin,
        group=own_group,
        application=own_app,
    )
    return {
        "admin": admin,
        "own_group": own_group,
        "other_group": other_group,
        "own_app": own_app,
        "other_app": other_app,
        "track": track,
    }


@pytest.mark.django_db
class TestProjectTrackService:
    def test_create_track(self, roles, make_user, semester, departments):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackCreateDTO(
            name="Новый трек",
            department_id=departments["child"].id,
            semester_id=semester.id,
            max_teams=50,
        )
        result = service.create_track(user, dto)
        assert result["name"] == "Новый трек"
        assert result["max_teams"] == 50
        assert result["author_id"] == user.id

    def test_list_tracks_admin(self, roles, make_user, semester, track_data):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        tracks = service.list_tracks(user, str(semester.id))
        assert tracks.count() == 1
        assert tracks.first().id == track_data["track"].id

    def test_list_tracks_includes_groups_and_applications(
        self, roles, make_user, semester, track_data
    ):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        tracks = service.list_tracks(user, str(semester.id))
        items = service.serialize_list(tracks)
        assert len(items) == 1
        assert len(items[0]["groups"]) == 1
        assert len(items[0]["applications"]) == 1
        assert items[0]["groups"][0]["id"] == track_data["own_group"].id
        assert items[0]["applications"][0]["id"] == track_data["own_app"].id

    def test_list_tracks_no_n_plus_one(
        self, roles, make_user, semester, track_data, django_assert_num_queries
    ):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        tracks = list(service.list_tracks(user, str(semester.id)))

        with django_assert_num_queries(0):
            items = service.serialize_list(tracks)

        assert len(items[0]["groups"]) == 1
        assert len(items[0]["applications"]) == 1

    def test_list_tracks_filter_by_institute(
        self, roles, make_user, institute, semester, track_data
    ):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        tracks = service.list_tracks(
            user, str(semester.id), institute_code=institute.code
        )
        assert tracks.count() == 1

    def test_get_track(self, roles, make_user, track_data):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        detail = service.get_track(user, track_data["track"].id)
        assert detail["id"] == track_data["track"].id
        assert len(detail["groups"]) == 1
        assert len(detail["applications"]) == 1

    def test_update_track(self, roles, make_user, track_data):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackUpdateDTO(name="Обновлённый")
        result = service.update_track(user, track_data["track"].id, dto)
        assert result["name"] == "Обновлённый"

    def test_delete_track(self, roles, make_user, track_data):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        service.delete_track(user, track_data["track"].id)
        assert not ProjectTrack.objects.filter(pk=track_data["track"].id).exists()

    def test_add_groups_to_track(
        self, roles, make_user, institute, semester, direction, track_data
    ):
        group = StudyGroup.objects.create(
            name="Г3",
            code="g3",
            direction=direction,
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackAddGroupsDTO(group_ids=[group.id])
        result = service.add_groups_to_track(user, track_data["track"].id, dto)
        assert len(result["groups"]) == 2

    def test_add_groups_exceeds_max_teams(
        self, roles, make_user, institute, semester, direction, track_data, departments
    ):
        track = ProjectTrack.objects.create(
            name="Малый",
            department=departments["child"],
            semester=semester,
            author=track_data["admin"],
            max_teams=1,
        )
        ProjectTrackGroup.objects.create(
            project_track=track,
            study_group=track_data["own_group"],
        )
        group = StudyGroup.objects.create(
            name="Г3",
            code="g3",
            direction=direction,
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackAddGroupsDTO(group_ids=[group.id])
        with pytest.raises(ValueError, match="max_teams"):
            service.add_groups_to_track(user, track.id, dto)

    def test_remove_group_from_track(self, roles, make_user, track_data):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        result = service.remove_group_from_track(
            user, track_data["track"].id, track_data["own_group"].id
        )
        assert result["groups"] == []

    def test_add_applications_to_track(
        self, roles, make_user, semester, statuses, departments, track_data
    ):
        app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=departments["child"],
            title="Второй",
        )
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackAddApplicationsDTO(
            items=[
                ProjectTrackAddApplicationItemDTO(
                    application_id=app.id,
                    teams_count=5,
                )
            ]
        )
        result = service.add_applications_to_track(user, track_data["track"].id, dto)
        assert len(result["applications"]) == 2
        app.refresh_from_db()
        assert app.recommended_teams_count == 5

    def test_add_applications_rejects_non_approved(
        self, roles, make_user, semester, statuses, institute, track_data
    ):
        app = ProjectApplication.objects.create(
            title="Не одобрен",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@b.c",
            semester=semester,
            status=statuses["await_institute"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        app.target_institutes.add(institute)
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackAddApplicationsDTO(
            items=[
                ProjectTrackAddApplicationItemDTO(
                    application_id=app.id,
                    teams_count=3,
                )
            ]
        )
        with pytest.raises(ValueError, match="не одобрена"):
            service.add_applications_to_track(user, track_data["track"].id, dto)

    def test_add_groups_validator_cannot_use_other_group(
        self, roles, make_user, track_data
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        dto = ProjectTrackAddGroupsDTO(group_ids=[track_data["other_group"].id])
        with pytest.raises(ValueError, match="групп"):
            service.add_groups_to_track(user, track_data["track"].id, dto)

    def test_delete_track_validator_other_denied(
        self,
        roles,
        make_user,
        semester,
        statuses,
        other_institute,
        direction,
        departments,
    ):
        from accounts.models import Department

        admin = make_user(role_code="admin")
        other_child = Department.objects.create(
            name="Other Child",
            short_name="OC",
            parent=other_institute.department,
        )
        other_group = StudyGroup.objects.create(
            name="Чужая",
            code="og",
            direction=direction,
            institute=other_institute,
        )
        other_app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=other_child,
        )
        track = _create_track_with_links(
            name="Чужой трек",
            semester=semester,
            department=other_child,
            author=admin,
            group=other_group,
            application=other_app,
        )
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        with pytest.raises(PermissionError):
            service.delete_track(user, track.id)

    def test_list_groups_with_counts(
        self, roles, make_user, institute, semester, direction, track_data
    ):
        StudyGroup.objects.create(
            name="Пустая",
            code="empty",
            direction=direction,
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        groups = service.list_groups(user, institute.code, str(semester.id))
        assert len(groups) == 2
        by_id = {g["id"]: g for g in groups}
        assert by_id[track_data["own_group"].id]["assigned_projects_count"] == 1

    def test_get_group_detail(self, roles, make_user, institute, semester, track_data):
        track_data["own_app"].print_number = "25-00042"
        track_data["own_app"].save(update_fields=["print_number"])
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        detail = service.get_group_detail(
            user,
            track_data["own_group"].id,
            institute.code,
            str(semester.id),
        )
        assert detail["id"] == track_data["own_group"].id
        assert len(detail["projects"]) == 1
        assert detail["projects"][0]["print_number"] == "25-00042"

    def test_list_projects_with_counts(
        self, roles, make_user, institute, semester, statuses, departments, track_data
    ):
        _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=departments["child"],
            title="Второй проект",
        )
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        projects = service.list_projects(user, institute.code, str(semester.id))
        assert len(projects) == 2
        by_id = {p["id"]: p for p in projects}
        assert by_id[track_data["own_app"].id]["assigned_groups_count"] == 1

    def test_get_project_detail(
        self, roles, make_user, institute, semester, track_data
    ):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        detail = service.get_project_detail(
            user,
            track_data["own_app"].id,
            institute.code,
            str(semester.id),
        )
        assert detail["id"] == track_data["own_app"].id
        assert len(detail["groups"]) == 1

    def test_get_statistics(
        self,
        roles,
        make_user,
        institute,
        semester,
        direction,
        statuses,
        departments,
        track_data,
    ):
        StudyGroup.objects.create(
            name="Пустая",
            code="empty",
            direction=direction,
            institute=institute,
        )
        _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=departments["child"],
            title="Нераспределённый",
        )
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        stats = service.get_statistics(user, institute.code, str(semester.id))
        assert stats["total_projects"] == 2
        assert stats["distributed_projects"] == 1
        assert stats["groups_without_projects"] == 1

    def test_get_statistics_without_institute_code_aggregated(
        self,
        roles,
        make_user,
        institute,
        other_institute,
        semester,
        track_data,
    ):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        stats = service.get_statistics(user, None, str(semester.id))
        assert "overall" in stats
        assert "by_institute" in stats
        assert stats["overall"]["distributed_projects"] == 1
