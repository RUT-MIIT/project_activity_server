from rest_framework.routers import DefaultRouter

from teams.entities.Direction import DirectionViewSet
from teams.entities.StudyGroup import StudyGroupViewSet
from teams.views import TeamViewSet

router = DefaultRouter()
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"directions", DirectionViewSet, basename="direction")
router.register(r"study-groups", StudyGroupViewSet, basename="study-group")

urlpatterns = router.urls
