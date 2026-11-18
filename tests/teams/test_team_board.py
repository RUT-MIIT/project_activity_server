from asgiref.sync import async_to_sync
from channels.security.websocket import OriginValidator
from channels.testing import WebsocketCommunicator
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from accounts.models import ACTIVE_SEMESTER_SETTING_CODE, Semester, Settings
from config.asgi import application
from teams.board_consumer import MAX_BOARD_MESSAGE
from teams.models import Direction, StudyGroup, Team, TeamSemester, TeamSemesterMember

BOARD_URL = "/api/teams/my-team/board/"
ORIGIN = "https://board.example.test"
EMPTY = {"document": {"store": {}}}
SNAPSHOT = {"document": {"store": {"shape:abc": {"opaque": [1, "рисунок"]}}}}


@pytest.fixture
def board_team(db, institute, make_user):
    semester = Semester.objects.create(code="boards", name="Boards", position=1)
    Settings.objects.update_or_create(
        code=ACTIVE_SEMESTER_SETTING_CODE, defaults={"value": semester.code}
    )
    direction = Direction.objects.create(
        code="38.03.01", name="Direction", level=Direction.Level.BAKALAVRIAT
    )
    group = StudyGroup.objects.create(
        name="Group", code="board-group", direction=direction, institute=institute
    )
    users = []
    for index in range(4):
        user = make_user(role_code="student", email=f"board{index}@example.test")
        user.study_group = group
        user.save(update_fields=["study_group"])
        users.append(user)
    first, second, other, outsider = users
    room = TeamSemester.objects.create(
        team=Team.objects.create(name="First", home_study_group=group),
        semester=semester,
        captain=first,
    )
    other_room = TeamSemester.objects.create(
        team=Team.objects.create(name="Other", home_study_group=group),
        semester=semester,
        captain=other,
    )
    for user, team in [(first, room), (second, room), (other, other_room)]:
        TeamSemesterMember.objects.create(
            team_semester=team, user=user, semester=semester
        )
    return first, second, other, outsider, room, other_room


def client_for(user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(user)}")
    return client


def test_rest_snapshot(board_team):
    first, second, other, outsider, room, _ = board_team
    client = client_for(first)
    assert client.get(BOARD_URL).json() == {"snapshot": EMPTY}
    assert (
        client.put(BOARD_URL, {"snapshot": SNAPSHOT}, format="json").status_code == 200
    )
    peer = client_for(second)
    assert peer.get(BOARD_URL).json() == {"snapshot": SNAPSHOT}
    assert peer.put(BOARD_URL, {"snapshot": {}}, format="json").json() == {
        "snapshot": {}
    }
    assert client.get(BOARD_URL).json() == {"snapshot": {}}
    assert client_for(other).get(BOARD_URL).json() == {"snapshot": EMPTY}
    assert client_for(outsider).get(BOARD_URL).status_code == 403
    assert (
        client_for(outsider).put(BOARD_URL, {"snapshot": {}}, format="json").status_code
        == 403
    )
    assert APIClient().get(BOARD_URL).status_code == 401

    next_semester = Semester.objects.create(code="boards-next", name="Next", position=2)
    assert client.get(BOARD_URL, {"semester_id": next_semester.pk}).status_code == 403
    next_room = TeamSemester.objects.create(
        team=room.team, semester=next_semester, captain=first
    )
    TeamSemesterMember.objects.create(
        team_semester=next_room, user=first, semester=next_semester
    )
    assert client.get(BOARD_URL, {"semester_id": next_semester.pk}).json() == {
        "snapshot": EMPTY
    }

    for malformed in (b'{"snapshot":', b'{"snapshot":[]}', b'{}'):
        assert (
            client.put(
                BOARD_URL, malformed, content_type="application/json"
            ).status_code
            == 400
        )
    oversized = b'{"snapshot":{}}' + b" " * (8 * 1024 * 1024)
    assert (
        client.put(BOARD_URL, oversized, content_type="application/json").status_code
        == 413
    )
    assert client.get(BOARD_URL).json() == {"snapshot": {}}


@pytest.mark.django_db(transaction=True)
def test_websocket_room_and_rest_reconnect(board_team, settings):
    first, second, other, _, room, other_room = board_team
    settings.CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }
    # Build the OriginValidator with the test origin without reloading Django.
    websocket = application.application_mapping["websocket"].application
    socket_app = OriginValidator(websocket, [ORIGIN])
    tokens = [str(AccessToken.for_user(user)) for user in (first, second, other)]
    refresh = str(RefreshToken.for_user(first))

    def socket(team, token, origin=ORIGIN):
        return WebsocketCommunicator(
            socket_app,
            f"/ws/teams/{team.pk}/board/?token={token}",
            headers=[(b"origin", origin.encode())],
        )

    async def exchange():
        rejected = [
            socket(room, tokens[2]),
            socket(room, "invalid"),
            socket(room, refresh),
            socket(room, tokens[0], "https://untrusted.example.test"),
        ]
        for connection in rejected:
            assert not (await connection.connect())[0]
            await connection.disconnect()
        a, b, c = (
            socket(room, tokens[0]),
            socket(room, tokens[1]),
            socket(other_room, tokens[2]),
        )
        for connection in (a, b, c):
            assert (await connection.connect())[0]
            assert (await connection.receive_json_from())["snapshot"] == EMPTY
        try:
            diff = {
                "type": "diff",
                "clientId": "tab-a",
                "diff": {"added": {"shape:abc": {}}, "removed": {}, "updated": {}},
            }
            await a.send_json_to(diff)
            assert await b.receive_json_from() == diff
            assert await a.receive_nothing()
            assert await c.receive_nothing()
            await a.send_json_to(
                {"type": "snapshot", "clientId": "tab-a", "snapshot": SNAPSHOT}
            )
            await a.send_json_to({"type": "hello", "clientId": "tab-a"})
            assert await a.receive_json_from() == {
                "type": "snapshot",
                "clientId": "server",
                "snapshot": EMPTY,
            }
            assert await b.receive_nothing()
            await a.send_to(text_data=" " * (MAX_BOARD_MESSAGE + 1))
            assert await a.receive_output() == {"type": "websocket.close", "code": 1009}
            assert await b.receive_nothing()
        finally:
            for connection in (a, b, c):
                await connection.disconnect()

    async_to_sync(exchange)()
    client = client_for(first)
    assert client.get(BOARD_URL).json() == {"snapshot": EMPTY}
    assert (
        client.put(BOARD_URL, {"snapshot": SNAPSHOT}, format="json").status_code == 200
    )

    async def reconnect():
        connection = socket(room, tokens[1])
        assert (await connection.connect())[0]
        expected = {"type": "snapshot", "clientId": "server", "snapshot": SNAPSHOT}
        try:
            assert await connection.receive_json_from() == expected
            await connection.send_json_to({"type": "hello", "clientId": "tab-b"})
            assert await connection.receive_json_from() == expected
        finally:
            await connection.disconnect()

    async_to_sync(reconnect)()
