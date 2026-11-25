import pytest
from rest_framework.test import APIClient

from showcase.models import ProjectApplication
from showcase.repositories.application_dashboard import ApplicationDashboardRepository
from showcase.dto.student_showcase import StudentShowcaseProjectListItemDTO
from showcase.domain.application_dashboard import DashboardFilters
from accounts.models import Semester
from teams.dto.institute_responsible_projects_stats import _project_type


@pytest.fixture
def payload():
    return {
        "company": "Company", "title": "Project", "company_contacts": "Contacts",
        "existing_solutions": "Solutions", "author_lastname": "Иванов",
        "author_firstname": "Иван", "author_email": "test@example.com",
        "author_phone": "+79990000000", "goal": "Длинная цель проекта для тестирования заявки",
        "problem_holder": "Носитель проблемы", "barrier": "Длинное описание барьера", "project_level": "L1",
    }


@pytest.mark.django_db
@pytest.mark.parametrize("customer_type", ["internal", "external", "representative"])
@pytest.mark.parametrize("simple", [True, False])
def test_create_customer_type(statuses, make_user, payload, customer_type, simple):
    client = APIClient()
    if not simple:
        client.force_authenticate(user=make_user(role_code="user"))
    path = "/api/showcase/project-applications/" + ("simple/" if simple else "")
    response = client.post(path, {**payload, "customer_type": customer_type}, format="json")
    assert response.status_code == 201, response.data
    assert response.data["customer_type"] == customer_type
    assert response.data["is_internal_customer"] == (customer_type == "internal")
    assert response.data["is_external"] == simple


@pytest.mark.django_db
def test_conflict_and_invalid(statuses, payload):
    client = APIClient()
    url = "/api/showcase/project-applications/simple/"
    for extra in ({"customer_type": "representative", "is_internal_customer": True},
                  {"customer_type": "unknown"}):
        assert client.post(url, {**payload, **extra}, format="json").status_code == 400


@pytest.mark.django_db
def test_patch_preserves_and_changes_customer_type(statuses, make_user, payload):
    author = make_user(role_code="user", with_department=True)
    client = APIClient()
    client.force_authenticate(user=author)
    response = client.post("/api/showcase/project-applications/", {**payload, "customer_type": "representative"}, format="json")
    assert response.status_code == 201, response.data
    url = f"/api/showcase/project-applications/{response.data['id']}/"
    client.force_authenticate(user=make_user(role_code="cpds", with_department=True))
    response = client.patch(url, {"title": "Новое название"}, format="json")
    assert response.status_code == 200, response.data
    assert response.data["customer_type"] == "representative"
    response = client.patch(url, {"is_internal_customer": False}, format="json")
    assert response.status_code == 200, response.data
    assert response.data["customer_type"] == "external"


@pytest.mark.django_db
def test_distribution_and_share():
    for value in ("internal", "external", "representative"):
        ProjectApplication.objects.create(customer_type=value)
    repo = ApplicationDashboardRepository()
    qs = ProjectApplication.objects.all()
    segments = repo.get_application_type_distribution(qs)["segments"]
    assert {s["group"]: s["count"] for s in segments} == {
        "internal": 1, "external": 1, "representative": 1,
    }
    share = repo._aggregate_external_share(qs, {"all": set(qs.values_list("id", flat=True))})
    assert share["all"] == {"external_count": 2, "percent": 66.7}


@pytest.mark.django_db
def test_student_showcase_preserves_customer_type():
    app = ProjectApplication.objects.create(customer_type="representative")
    item = StudentShowcaseProjectListItemDTO(app, enrolled_teams_count=0).to_dict()
    assert item["customerType"] == "representative"


@pytest.mark.parametrize("value", ["internal", "external", "representative"])
def test_project_stats_type(value):
    assert _project_type(ProjectApplication(customer_type=value)) == value


@pytest.mark.django_db
def test_dashboard_filters_types_exactly(statuses):
    semester = Semester.objects.create(code="customer-types", name="Семестр", position=1)
    for value in ("internal", "external", "representative"):
        ProjectApplication.objects.create(customer_type=value, semester=semester, status=statuses["created"])
    repo = ApplicationDashboardRepository()
    for value in ("internal", "external", "representative"):
        filters = DashboardFilters(semester_id=semester.id, institute_code=None, department_id=None,
                                   status_groups=("in_progress",), application_type=value,
                                   days=30, accessible_institute_codes=None)
        assert list(repo.get_filtered_queryset(filters).values_list("customer_type", flat=True)) == [value]
