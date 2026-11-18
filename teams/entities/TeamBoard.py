import json

from rest_framework import status
from rest_framework.exceptions import ParseError, PermissionDenied, UnsupportedMediaType
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils.json import loads
from rest_framework.views import APIView

from accounts.models import Semester
from teams.board import load_board_snapshot
from teams.models import TeamBoard, TeamSemester
from teams.permissions import StudentWithStudyGroupPermission

MAX_BOARD_BODY = 8 * 1024 * 1024


class TeamBoardView(APIView):
    permission_classes = [IsAuthenticated, StudentWithStudyGroupPermission]
    renderer_classes = [JSONRenderer]

    def get_team_id(self, request):
        try:
            semester_id = Semester.resolve_list_semester_id(
                request.query_params.get("semester_id") or "actual"
            )
        except ValueError as exc:
            raise ParseError(str(exc)) from exc
        team_id = (
            TeamSemester.objects.filter(
                semester_id=semester_id, members__user_id=request.user.pk
            )
            .values_list("pk", flat=True)
            .first()
        )
        if team_id is None:
            raise PermissionDenied("You are not a member of a team in this semester.")
        return team_id

    def get(self, request):
        return Response({"snapshot": load_board_snapshot(self.get_team_id(request))})

    def put(self, request):
        team_id = self.get_team_id(request)
        body = request.read(MAX_BOARD_BODY + 1)
        if len(body) > MAX_BOARD_BODY:
            return Response(status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        if request.content_type.split(";", 1)[0].strip().lower() != "application/json":
            raise UnsupportedMediaType(request.content_type)
        try:
            data = loads(body)
            # Verify values can also round-trip through a database JSON field.
            json.dumps(data, allow_nan=False, ensure_ascii=False).encode()
        except (ValueError, RecursionError) as exc:
            raise ParseError("Expected valid JSON.") from exc
        snapshot = data.get("snapshot") if isinstance(data, dict) else None
        if not isinstance(snapshot, dict):
            raise ParseError("snapshot must be a JSON object.")
        TeamBoard.objects.update_or_create(
            team_id=team_id, defaults={"snapshot": snapshot}
        )
        return Response({"snapshot": snapshot})
