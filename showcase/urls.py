from django.urls import path, include
from rest_framework.routers import DefaultRouter
from showcase.entities.ProjectApplication import ProjectApplicationViewSet
from showcase.entities.ApplicationStatus import ApplicationStatusViewSet

router = DefaultRouter()
router.register(
    r'project-applications',
    ProjectApplicationViewSet,
    basename='project-application'
)
router.register(
    r'application-statuses',
    ApplicationStatusViewSet,
    basename='application-status'
)

urlpatterns = [
    path('', include(router.urls)),
]
