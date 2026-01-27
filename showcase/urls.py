from rest_framework.routers import DefaultRouter

from showcase.entities.ApplicationStatus import ApplicationStatusViewSet
from showcase.entities.DepartmentPlan import DepartmentPlanViewSet
from showcase.entities.Institute import InstituteViewSet
from showcase.entities.ProjectApplication import (
    ProjectApplicationViewSet,
    SemesterViewSet,
)
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

urlpatterns = router.urls
