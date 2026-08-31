from django.urls import path
from rest_framework.routers import DefaultRouter

from teams.entities.Direction import DirectionViewSet
from teams.entities.InstituteResponsible import InstituteResponsibleViewSet
from teams.entities.MentorTeam import MentorTeamViewSet
from teams.entities.StudyGroup import StudyGroupViewSet
from teams.entities.TeamLobby import MyTeamViewSet, TeamLobbyViewSet
from teams.views import TeamSemesterViewSet, TeamViewSet

router = DefaultRouter()
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"team-semesters", TeamSemesterViewSet, basename="team-semester")
router.register(r"directions", DirectionViewSet, basename="direction")
router.register(r"study-groups", StudyGroupViewSet, basename="study-group")
router.register(
    r"institute-responsible",
    InstituteResponsibleViewSet,
    basename="institute-responsible",
)
router.register(r"lobby", TeamLobbyViewSet, basename="team-lobby")

my_team = MyTeamViewSet.as_view(
    {
        "get": "list",
        "delete": "delete_team",
    }
)

urlpatterns = [
    path("my-team/", my_team, name="my-team-root"),
    path(
        "my-team/event-log/",
        MyTeamViewSet.as_view({"get": "event_log"}),
        name="my-team-event-log",
    ),
    path(
        "my-team/leave/",
        MyTeamViewSet.as_view({"post": "leave"}),
        name="my-team-leave",
    ),
    path(
        "my-team/confirm-composition/",
        MyTeamViewSet.as_view({"post": "confirm_composition"}),
        name="my-team-confirm",
    ),
    path(
        "my-team/invitations/",
        MyTeamViewSet.as_view({"post": "create_invitation"}),
        name="my-team-invite",
    ),
    path(
        "my-team/join-requests/<int:join_request_id>/approve/",
        MyTeamViewSet.as_view({"post": "approve_join_request"}),
        name="my-team-approve-join",
    ),
    path(
        "my-team/join-requests/<int:join_request_id>/reject/",
        MyTeamViewSet.as_view({"post": "reject_join_request"}),
        name="my-team-reject-join",
    ),
    path(
        "my-team/members/<int:user_id>/",
        MyTeamViewSet.as_view({"delete": "kick_member"}),
        name="my-team-kick",
    ),
    path(
        "study-groups/<int:group_id>/teams/<int:team_semester_id>/",
        MentorTeamViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="mentor-team-detail",
    ),
    path(
        "study-groups/<int:group_id>/teams/<int:team_semester_id>/captain/",
        MentorTeamViewSet.as_view({"patch": "set_captain"}),
        name="mentor-team-captain",
    ),
    path(
        "study-groups/<int:group_id>/teams/<int:team_semester_id>/confirm-composition/",
        MentorTeamViewSet.as_view({"post": "confirm_composition"}),
        name="mentor-team-confirm",
    ),
    path(
        "study-groups/<int:group_id>/teams/<int:team_semester_id>/unconfirm-composition/",
        MentorTeamViewSet.as_view({"post": "unconfirm_composition"}),
        name="mentor-team-unconfirm",
    ),
    path(
        "study-groups/<int:group_id>/teams/<int:team_semester_id>/members/",
        MentorTeamViewSet.as_view({"post": "add_member"}),
        name="mentor-team-add-member",
    ),
    path(
        "study-groups/<int:group_id>/teams/<int:team_semester_id>/members/<int:user_id>/",
        MentorTeamViewSet.as_view({"delete": "remove_member"}),
        name="mentor-team-remove-member",
    ),
] + router.urls
