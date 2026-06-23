"""Тесты ProjectTrackService."""

import pytest

from accounts.models import Department, Semester
from showcase.dto.project_track import ProjectTrackAssignDTO, ProjectTrackDeleteDTO
from showcase.models import (
    ApplicationInvolvedDepartment,
    Institute,
    ProjectApplication,
    ProjectTrack,
)
from showcase.services.project_track_service import ProjectTrackService
from teams.models import Direction, StudyGroup


@pytest.fixture
def semester(db):
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
    other_dept = Department.objects.create(name="Other Parent", short_name="OP")
    return Institute.objects.create(
        code="OTHER",
        name="Other Institute",
        position=2,
        department=other_dept,
    )


def _create_approved_app(
    *,
    semester: Semester,
    statuses: dict,
    involved_department: Department | None = None,
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


@pytest.fixture
def track_data(statuses, institute, other_institute, direction, semester, departments):
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
    track = ProjectTrack.objects.create(
        semester=semester,
        study_group=own_group,
        project_application=own_app,
    )
    return {
        "own_group": own_group,
        "other_group": other_group,
        "own_app": own_app,
        "other_app": other_app,
        "track": track,
    }


@pytest.mark.django_db
class TestProjectTrackService:
    def test_list_tracks_admin(self, roles, make_user, institute, semester, track_data):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        tracks = service.list_tracks(user, institute.code, str(semester.id))
        assert tracks.count() == 1
        assert tracks.first().id == track_data["track"].id

    def test_list_tracks_validator_filtered(
        self, roles, make_user, institute, semester, track_data
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        tracks = service.list_tracks(user, institute.code, str(semester.id))
        assert tracks.count() == 1

    def test_list_tracks_validator_other_institute_denied(
        self, roles, make_user, other_institute, semester, track_data
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        with pytest.raises(PermissionError):
            service.list_tracks(user, other_institute.code, str(semester.id))

    def test_bulk_assign_creates_tracks(
        self, roles, make_user, institute, semester, track_data
    ):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackAssignDTO(
            semester_id=semester.id,
            group_ids=[track_data["own_group"].id],
            project_application_ids=[track_data["own_app"].id],
        )
        result = service.bulk_assign(user, dto)
        assert result.created == 0
        assert result.skipped == 1
        assert result.total_requested == 1

    def test_bulk_assign_new_tracks(
        self, roles, make_user, institute, semester, direction, statuses, departments
    ):
        group = StudyGroup.objects.create(
            name="Г3",
            code="g3",
            direction=direction,
            institute=institute,
        )
        app = _create_approved_app(
            semester=semester,
            statuses=statuses,
            involved_department=departments["child"],
        )
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackAssignDTO(
            semester_id=semester.id,
            group_ids=[group.id],
            project_application_ids=[app.id],
        )
        result = service.bulk_assign(user, dto)
        assert result.created == 1
        assert result.skipped == 0
        assert ProjectTrack.objects.count() == 1

    def test_bulk_assign_validator_cannot_use_other_group(
        self, roles, make_user, institute, semester, track_data
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        dto = ProjectTrackAssignDTO(
            semester_id=semester.id,
            group_ids=[track_data["other_group"].id],
            project_application_ids=[track_data["own_app"].id],
        )
        with pytest.raises(PermissionError):
            service.bulk_assign(user, dto)

    def test_bulk_assign_validator_with_involved_department_no_targets(
        self,
        roles,
        make_user,
        institute,
        semester,
        direction,
        statuses,
        departments,
    ):
        from showcase.models import ApplicationInvolvedDepartment

        group = StudyGroup.objects.create(
            name="Г5",
            code="g5",
            direction=direction,
            institute=institute,
        )
        app = ProjectApplication.objects.create(
            title="Без институтов",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@b.c",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        dto = ProjectTrackAssignDTO(
            semester_id=semester.id,
            group_ids=[group.id],
            project_application_ids=[app.id],
        )
        result = service.bulk_assign(user, dto)
        assert result.created == 1

    def test_bulk_assign_validator_with_target_institutes_only(
        self,
        roles,
        make_user,
        institute,
        semester,
        direction,
        statuses,
    ):
        group = StudyGroup.objects.create(
            name="Г6",
            code="g6",
            direction=direction,
            institute=institute,
        )
        app = ProjectApplication.objects.create(
            title="Только target",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@b.c",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        app.target_institutes.add(institute)
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        dto = ProjectTrackAssignDTO(
            semester_id=semester.id,
            group_ids=[group.id],
            project_application_ids=[app.id],
        )
        result = service.bulk_assign(user, dto)
        assert result.created == 1

    def test_bulk_assign_rejects_non_approved(
        self, roles, make_user, institute, semester, direction, statuses
    ):
        group = StudyGroup.objects.create(
            name="Г4",
            code="g4",
            direction=direction,
            institute=institute,
        )
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
        dto = ProjectTrackAssignDTO(
            semester_id=semester.id,
            group_ids=[group.id],
            project_application_ids=[app.id],
        )
        with pytest.raises(ValueError, match="не одобрена"):
            service.bulk_assign(user, dto)

    def test_delete_track_admin(self, roles, make_user, track_data, semester):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        dto = ProjectTrackDeleteDTO(
            semester_id=semester.id,
            group_id=track_data["own_group"].id,
            project_application_id=track_data["own_app"].id,
        )
        service.delete_track(user, dto)
        assert not ProjectTrack.objects.filter(pk=track_data["track"].id).exists()

    def test_delete_track_validator_other_denied(
        self, roles, make_user, semester, statuses, other_institute, direction
    ):
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
        track = ProjectTrack.objects.create(
            semester=semester,
            study_group=other_group,
            project_application=other_app,
        )
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        dto = ProjectTrackDeleteDTO(
            semester_id=semester.id,
            group_id=other_group.id,
            project_application_id=other_app.id,
        )
        with pytest.raises(PermissionError):
            service.delete_track(user, dto)

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
        assert by_id[track_data["own_group"].id]["direction"]["name"] == "Экономика"

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
        assert detail["projects"][0]["author_name"] == "Иванов Иван"

    def test_get_group_detail_wrong_institute(
        self, roles, make_user, institute, semester, track_data
    ):
        user = make_user(role_code="admin")
        service = ProjectTrackService()
        with pytest.raises(ValueError, match="не принадлежит институту"):
            service.get_group_detail(
                user,
                track_data["other_group"].id,
                institute.code,
                str(semester.id),
            )

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
        assert stats["average_projects_per_group"] == 0.5
        assert stats["groups_without_projects"] == 1

    def test_list_groups_validator_without_institute_code_service(
        self, roles, make_user, institute, semester, track_data
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        groups = service.list_groups(user, None, str(semester.id))
        assert len(groups) == 1

    def test_get_group_detail_without_institute_code(
        self, roles, make_user, institute, semester, track_data
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        detail = service.get_group_detail(
            user,
            track_data["own_group"].id,
            None,
            str(semester.id),
        )
        assert detail["id"] == track_data["own_group"].id
        assert len(detail["projects"]) == 1

    def test_list_groups_validator_other_institute_denied(
        self, roles, make_user, other_institute, semester, track_data
    ):
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectTrackService()
        with pytest.raises(PermissionError):
            service.list_groups(user, other_institute.code, str(semester.id))
