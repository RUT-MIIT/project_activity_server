"""Тесты новых полей проектных заявок."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Semester
from showcase.admin import ProjectApplicationAdminForm
from showcase.dto.application import ProjectApplicationCreateDTO
from showcase.dto.project import ProjectListDTO
from showcase.models import (
    ApplicationInvolvedDepartment,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
)
from showcase.services.application_service import ProjectApplicationService
from showcase.services.project_service import ProjectService
from teams.models import Direction, StudyGroup


@pytest.fixture
def direction(db):
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def semester(db):
    return Semester.objects.create(code="s1", name="S1", position=1)


def _base_create_payload(**overrides):
    payload = {
        "company": "ООО Тест",
        "title": "Новый проект",
        "company_contacts": "Контакты представителя",
        "existing_solutions": "Описание существующих решений",
        "author_lastname": "Иванов",
        "author_firstname": "Иван",
        "author_email": "ivan@example.com",
        "author_phone": "+79991111111",
        "goal": "Длинная цель проекта, больше 50 символов для консультации",
        "problem_holder": "Носитель проблемы",
        "barrier": "Длинное описание барьера",
        "project_level": "L1",
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
class TestProjectApplicationNewFieldsCreateUpdate:
    @pytest.mark.parametrize("suffix", ["", "simple/"])
    def test_create_case_without_project_description(self, statuses, make_user, suffix):
        client = APIClient()
        if not suffix:
            client.force_authenticate(
                user=make_user(role_code="user", with_department=True)
            )
        payload = _base_create_payload(application_kind="case", case_description="Кейс")
        for field in ("problem_holder", "goal", "barrier", "existing_solutions"):
            payload.pop(field)
        url = f"/api/showcase/project-applications/{suffix}"
        response = client.post(url, payload, format="json")
        assert response.status_code == 201, response.data
        assert response.data["application_kind"] == "case"
        assert response.data["case_description"] == "Кейс"
        assert response.data["goal"] == ""

        response = client.post(
            url, {**payload, "case_description": "  "}, format="json"
        )
        assert response.status_code == 400
        assert "case_description" in response.data["errors"]
        response = client.post(
            url, {**payload, "application_kind": "other"}, format="json"
        )
        assert response.status_code == 400
        assert "application_kind" in response.data["errors"]

    def test_switch_kind_without_erasing_fields(self, statuses, make_user):
        client = APIClient()
        client.force_authenticate(
            user=make_user(role_code="cpds", with_department=True)
        )
        base = "/api/showcase/project-applications/"
        payload = _base_create_payload()
        response = client.post(base, payload, format="json")
        assert response.status_code == 201, response.data
        assert response.data["application_kind"] == "project"
        assert response.data["case_description"] == ""
        application_id = response.data["id"]
        url = f"{base}{application_id}/"

        response = client.patch(
            url, {"application_kind": "case", "case_description": "Кейс"}, format="json"
        )
        assert response.status_code == 200, response.data
        assert response.data["goal"] == payload["goal"]
        assert response.data["application_kind"] == "case"
        response = client.patch(url, {"case_description": ""}, format="json")
        assert response.status_code == 400
        assert "case_description" in response.data["errors"]
        response = client.patch(url, {"application_kind": "other"}, format="json")
        assert response.status_code == 400
        assert "application_kind" in response.data["errors"]

        response = client.put(url, {"application_kind": "project"}, format="json")
        assert response.status_code == 200, response.data
        for field in ("problem_holder", "goal", "barrier", "existing_solutions"):
            assert response.data[field] == payload[field]
        assert response.data["case_description"] == "Кейс"
        assert client.get(url).data["case_description"] == "Кейс"
        response = client.get(base)
        items = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )
        item = next(item for item in items if item["id"] == application_id)
        assert item["application_kind"] == "project"
        assert item["case_description"] == "Кейс"

    def test_case_cannot_switch_to_incomplete_project(self, statuses, make_user):
        client = APIClient()
        user = make_user(role_code="cpds", with_department=True)
        client.force_authenticate(user=user)
        application = ProjectApplication.objects.create(
            author=user,
            status=statuses["approved"],
            application_kind="case",
            case_description="Кейс",
        )
        url = f"/api/showcase/project-applications/{application.id}/"
        response = client.patch(url, {"application_kind": "project"}, format="json")
        assert response.status_code == 400
        assert {"goal", "barrier", "problem_holder", "existing_solutions"} <= set(
            response.data["errors"]
        )
        response = client.patch(url, {"goal": ""}, format="json")
        assert response.status_code == 200, response.data
        assert response.data["application_kind"] == "case"
        assert response.data["case_description"] == "Кейс"

    def test_admin_case_form(self):
        data = {
            "application_kind": "case",
            "author_lastname": "Иванов",
            "author_firstname": "Иван",
            "author_email": "ivan@example.com",
            "author_phone": "+79991111111",
            "company": "Компания",
            "company_contacts": "Контакт",
            "project_level": "L1",
            "recommended_teams_count": 3,
            "min_team_members": 4,
            "max_team_members": 7,
            "application_year": 2026,
            "year_sequence_number": 1,
            "print_number": "2026-1",
        }
        form = ProjectApplicationAdminForm(data={**data, "case_description": "Кейс"})
        assert form.is_valid(), form.errors
        assert form.save().case_description == "Кейс"
        form = ProjectApplicationAdminForm(data={**data, "case_description": "  "})
        assert not form.is_valid()
        assert "case_description" in form.errors

    def test_create_with_new_fields(self, statuses, make_user):
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            "/api/showcase/project-applications/",
            _base_create_payload(
                is_continuing=True,
                track_composer_comment="Нужна команда с ML",
                recommended_teams_count=3,
                min_team_members=2,
                max_team_members=5,
            ),
            format="json",
        )

        assert response.status_code == 201
        assert response.data["is_continuing"] is True
        assert response.data["track_composer_comment"] == "Нужна команда с ML"
        assert response.data["recommended_teams_count"] == 3
        assert response.data["min_team_members"] == 2
        assert response.data["max_team_members"] == 5

        app = ProjectApplication.objects.get(pk=response.data["id"])
        assert app.is_continuing is True
        assert app.track_composer_comment == "Нужна команда с ML"
        assert app.recommended_teams_count == 3
        assert app.min_team_members == 2
        assert app.max_team_members == 5

    def test_create_rejects_zero_recommended_teams_count(self, statuses, make_user):
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            "/api/showcase/project-applications/",
            _base_create_payload(recommended_teams_count=0),
            format="json",
        )

        assert response.status_code == 400
        errors = response.data.get("errors", response.data)
        assert "recommended_teams_count" in errors

    def test_create_rejects_min_greater_than_max(self, statuses, make_user):
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            "/api/showcase/project-applications/",
            _base_create_payload(min_team_members=8, max_team_members=3),
            format="json",
        )

        assert response.status_code == 400
        errors = response.data.get("errors", response.data)
        assert "min_team_members" in errors

    def test_create_rejects_zero_min_team_members(self, statuses, make_user):
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            "/api/showcase/project-applications/",
            _base_create_payload(min_team_members=0),
            format="json",
        )

        assert response.status_code == 400
        errors = response.data.get("errors", response.data)
        assert "min_team_members" in errors

    def test_create_defaults_recommended_teams_count_to_three(
        self, statuses, make_user
    ):
        user = make_user(role_code="user", with_department=True)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            "/api/showcase/project-applications/",
            _base_create_payload(),
            format="json",
        )

        assert response.status_code == 201
        assert response.data["recommended_teams_count"] == 3
        assert response.data["min_team_members"] == 4
        assert response.data["max_team_members"] == 7

    def test_patch_track_composer_comment(self, statuses, make_user):
        author = make_user(role_code="user", with_department=True)
        cpds_user = make_user(role_code="cpds", with_department=True)
        service = ProjectApplicationService()
        application = service.submit_application(
            ProjectApplicationCreateDTO(**_base_create_payload()),
            author,
        )

        client = APIClient()
        client.force_authenticate(user=cpds_user)
        patch_response = client.patch(
            f"/api/showcase/project-applications/{application.id}/",
            {"track_composer_comment": "Обновлённый комментарий"},
            format="json",
        )

        assert patch_response.status_code == 200
        assert (
            patch_response.data["track_composer_comment"] == "Обновлённый комментарий"
        )

    def test_retrieve_returns_is_competitive_selection(self, statuses, make_user):
        author = make_user(role_code="user", with_department=True)
        service = ProjectApplicationService()
        application = service.submit_application(
            ProjectApplicationCreateDTO(**_base_create_payload()),
            author,
        )

        client = APIClient()
        client.force_authenticate(user=author)
        response = client.get(f"/api/showcase/project-applications/{application.id}/")

        assert response.status_code == 200
        assert response.data["is_competitive_selection"] is False

        application.is_competitive_selection = True
        application.save(update_fields=["is_competitive_selection"])

        response = client.get(f"/api/showcase/project-applications/{application.id}/")
        assert response.status_code == 200
        assert response.data["is_competitive_selection"] is True


@pytest.mark.django_db
class TestMyApplicationsNewFields:
    def test_my_applications_returns_new_fields(self, statuses, make_user):
        from accounts.models import Settings

        user = make_user(role_code="user", with_department=True)
        semester = Semester.objects.create(code="next-sem", name="Next", position=1)
        Settings.objects.create(code="next_semester_code", value=semester.code)

        ProjectApplication.objects.create(
            title="Моя заявка",
            company="ООО",
            author=user,
            status=statuses["await_department"],
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="ivan@example.com",
            author_phone="+79990000000",
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
            semester=semester,
            is_continuing=True,
            track_composer_comment="Комментарий",
            recommended_teams_count=2,
            min_team_members=3,
            max_team_members=6,
        )

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(
            "/api/showcase/project-applications/my_applications/?semester_id=next"
        )

        assert response.status_code == 200
        assert len(response.data) == 1
        item = response.data[0]
        assert item["is_continuing"] is True
        assert item["track_composer_comment"] == "Комментарий"
        assert item["recommended_teams_count"] == 2
        assert item["min_team_members"] == 3
        assert item["max_team_members"] == 6


@pytest.mark.django_db
class TestProjectApplicationNewFieldsLists:
    def test_projects_list_returns_is_continuing(
        self, roles, make_user, statuses, institute, departments
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        admin = make_user(role_code="admin")
        app = ProjectApplication.objects.create(
            title="Продолжающийся проект",
            application_kind="case",
            case_description="Описание кейса",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@example.com",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
            is_continuing=True,
            track_composer_comment="Комментарий для трека",
        )
        app.target_institutes.add(institute)
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )

        client = APIClient()
        client.force_authenticate(user=admin)
        response = client.get(
            f"/api/showcase/projects/?semester_id={semester.id}",
        )

        assert response.status_code == 200
        item = next(row for row in response.data if row["id"] == app.id)
        assert item["application_kind"] == "case"
        assert item["case_description"] == "Описание кейса"
        assert item["is_continuing"] is True
        assert item["track_composer_comment"] == "Комментарий для трека"
        assert item["has_track_composer_comment"] is True
        assert item["recommended_teams_count"] == 3
        assert item["min_team_members"] == 4
        assert item["max_team_members"] == 7

    def test_track_projects_list_returns_comment_fields(
        self, roles, make_user, statuses, institute, direction, departments, semester
    ):
        admin = make_user(role_code="admin")
        group = StudyGroup.objects.create(
            name="Группа 1",
            code="g1",
            direction=direction,
            institute=institute,
        )
        app = ProjectApplication.objects.create(
            title="Проект трека",
            application_kind="case",
            case_description="Описание кейса в треке",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="ivan@example.com",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
            track_composer_comment="Комментарий для трека",
            recommended_teams_count=2,
            min_team_members=2,
            max_team_members=7,
        )
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )
        track = ProjectTrack.objects.create(
            name="Трек",
            description="",
            department=departments["child"],
            semester=semester,
            author=admin,
        )
        ProjectTrackGroup.objects.create(project_track=track, study_group=group)
        ProjectTrackApplication.objects.create(
            project_track=track,
            project_application=app,
        )

        client = APIClient()
        client.force_authenticate(user=admin)
        response = client.get(
            f"/api/showcase/project-tracks/projects/"
            f"?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        item = response.data[0]
        assert item["application_kind"] == "case"
        assert item["case_description"] == "Описание кейса в треке"
        assert item["track_composer_comment"] == "Комментарий для трека"
        assert item["has_track_composer_comment"] is True
        assert item["recommended_teams_count"] == 2
        assert item["min_team_members"] == 2
        assert item["max_team_members"] == 7

    def test_project_service_list_includes_is_continuing(
        self, make_user, statuses, institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        admin = make_user(role_code="admin")
        app = ProjectApplication.objects.create(
            title="Проект",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@example.com",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
            is_continuing=True,
        )
        app.target_institutes.add(institute)

        service = ProjectService()
        items = [
            ProjectListDTO(application).to_dict()
            for application in service.list_projects(admin, str(semester.id))
            if application.id == app.id
        ]

        assert items[0]["is_continuing"] is True
