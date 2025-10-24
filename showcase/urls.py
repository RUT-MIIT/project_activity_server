from django.urls import path, include
from rest_framework.routers import DefaultRouter
from showcase.entities.ProjectApplication import ProjectApplicationViewSet
from showcase.entities.Institute import InstituteViewSet
from showcase.entities.ApplicationStatus import ApplicationStatusViewSet

# Создаем основной роутер
router = DefaultRouter()

# Регистрируем все ViewSet'ы
router.register(
    r'project-applications',
    ProjectApplicationViewSet,
    basename='project-application'
)

router.register(
    r'institutes',
    InstituteViewSet,
    basename='institute'
)

router.register(
    r'application-statuses',
    ApplicationStatusViewSet,
    basename='application-status'
)

urlpatterns = router.urls
