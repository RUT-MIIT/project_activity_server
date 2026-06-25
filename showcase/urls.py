from django.urls import path
from rest_framework.routers import DefaultRouter

from showcase.entities.ApplicationDashboard import ApplicationDashboardViewSet
from showcase.entities.ApplicationStatus import ApplicationStatusViewSet
from showcase.entities.DepartmentPlan import DepartmentPlanViewSet
from showcase.entities.Institute import InstituteViewSet
from showcase.entities.Project import ProjectViewSet
from showcase.entities.ProjectApplication import (
    ProjectApplicationViewSet,
    SemesterViewSet,
)
from showcase.entities.ProjectTrack import ProjectTrackViewSet
from showcase.entities.Tag import TagViewSet

# Создаем основной роутер
router = DefaultRouter()

# Регистрируем все ViewSet'ы
router.register(
    r"project-applications", ProjectApplicationViewSet, basename="project-application"
)

router.register(r"institutes", InstituteViewSet, basename="institute")

router.register(r"tags", TagViewSet, basename="tag")

router.register(
    r"application-statuses", ApplicationStatusViewSet, basename="application-status"
)

router.register(r"semesters", SemesterViewSet, basename="semester")

router.register(r"department-plans", DepartmentPlanViewSet, basename="department-plan")

router.register(r"projects", ProjectViewSet, basename="project")

project_track_list = ProjectTrackViewSet.as_view(
    {
        "get": "list",
        "post": "create",
        "delete": "remove",
    }
)

project_track_groups_list = ProjectTrackViewSet.as_view(
    {
        "get": "list_groups",
    }
)

project_track_group_detail = ProjectTrackViewSet.as_view(
    {
        "get": "retrieve_group",
    }
)

project_track_statistics = ProjectTrackViewSet.as_view(
    {
        "get": "statistics",
    }
)

application_dashboard = ApplicationDashboardViewSet.as_view(
    {
        "get": "retrieve",
    }
)

urlpatterns = [
    path(
        "project-applications/dashboard/",
        application_dashboard,
        name="project-application-dashboard",
    ),
    path(
        "project-tracks/groups/",
        project_track_groups_list,
        name="project-track-groups-list",
    ),
    path(
        "project-tracks/groups/<int:group_id>/",
        project_track_group_detail,
        name="project-track-group-detail",
    ),
    path(
        "project-tracks/statistics/",
        project_track_statistics,
        name="project-track-statistics",
    ),
    path("project-tracks/", project_track_list, name="project-track-list"),
    *router.urls,
]
