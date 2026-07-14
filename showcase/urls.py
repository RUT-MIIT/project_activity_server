from django.urls import include, path
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

router.register(r"project-tracks", ProjectTrackViewSet, basename="project-track")

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
    path("", include(router.urls)),
]
