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
STROKE = {
    "id": "shape:abc",
    "type": "draw",
    "typeName": "shape",
    "props": {"pts": [0, 0, 0.5], "done": False},
}
LIVE_SNAPSHOT = {"document": {"store": {"shape:abc": STROKE}}}


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

    for malformed in (b'{"snapshot":', b'{"snapshot":[]}', b"{}"):
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
                "diff": {"added": {"shape:abc": STROKE}, "removed": {}, "updated": {}},
            }
            await a.send_json_to(diff)
            assert (await b.receive_json_from())["diff"]["updated"] == {
                "shape:abc": [None, STROKE]
            }
            assert await a.receive_nothing()
            assert await c.receive_nothing()
            await a.send_json_to(
                {"type": "snapshot", "clientId": "tab-a", "snapshot": SNAPSHOT}
            )
            await a.send_json_to({"type": "hello", "clientId": "tab-a"})
            assert await a.receive_json_from() == {
                "type": "snapshot",
                "clientId": "server",
                "snapshot": LIVE_SNAPSHOT,
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
    assert client.get(BOARD_URL).json() == {"snapshot": LIVE_SNAPSHOT}
    stale_save = client.put(BOARD_URL, {"snapshot": SNAPSHOT}, format="json")
    assert stale_save.status_code == 200
    assert stale_save.json() == {"snapshot": LIVE_SNAPSHOT}

    async def reconnect():
        connection = socket(room, tokens[1])
        assert (await connection.connect())[0]
        expected = {"type": "snapshot", "clientId": "server", "snapshot": LIVE_SNAPSHOT}
        try:
            assert await connection.receive_json_from() == expected
            await connection.send_json_to({"type": "hello", "clientId": "tab-b"})
            assert await connection.receive_json_from() == expected
        finally:
            await connection.disconnect()

    async_to_sync(reconnect)()


import base64
import json


@pytest.mark.django_db(transaction=True)
def test_edit_ack_stroke_and_oversized_record_survive_reconnect(board_team, settings):
    first, second, _, _, room, _ = board_team
    settings.CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }
    websocket = application.application_mapping["websocket"].application
    socket_app = OriginValidator(websocket, [ORIGIN])

    def socket(user):
        return WebsocketCommunicator(
            socket_app,
            f"/ws/teams/{room.pk}/board/?token={AccessToken.for_user(user)}&sync=2",
            headers=[(b"origin", ORIGIN.encode())],
        )

    async def exercise():
        sender, peer = socket(first), socket(second)
        for connection in (sender, peer):
            assert (await connection.connect())[0]
            initial = await connection.receive_json_from()
            assert initial["protocol"] == 2 and initial["revision"] == 0

        async def edit(sequence, *, records=None, strokes=None):
            message = {
                "type": "edit",
                "clientId": "author",
                "sequence": sequence,
                "changes": {
                    "records": records or {},
                    "removed": [],
                    "strokes": strokes or {},
                },
            }
            await sender.send_json_to(message)

        try:
            await edit(1, records={"shape:abc": STROKE})
            assert await sender.receive_json_from() == {
                "type": "ack",
                "sequence": 1,
                "revision": 1,
            }
            assert (await peer.receive_json_from())["changes"]["records"] == {
                "shape:abc": STROKE
            }
            await edit(
                2,
                strokes={
                    "shape:abc": {"offset": 0, "points": [1, 2, 0.5], "done": True}
                },
            )
            retry = await sender.receive_json_from()
            assert retry["retry"] == 2 and retry["revision"] == 1
            await edit(
                3,
                strokes={
                    "shape:abc": {"offset": 3, "points": [1, 2, 0.5], "done": True}
                },
            )
            assert await sender.receive_json_from() == {
                "type": "ack",
                "sequence": 3,
                "revision": 2,
            }
            remote = await peer.receive_json_from()
            assert remote["revision"] == 2
            assert remote["changes"]["strokes"]["shape:abc"]["points"] == [1, 2, 0.5]

            asset = {"id": "asset:large", "src": "x" * (MAX_BOARD_MESSAGE + 1)}
            large = json.dumps(
                {
                    "type": "edit",
                    "clientId": "author",
                    "sequence": 4,
                    "changes": {
                        "records": {"asset:large": asset},
                        "removed": [],
                        "strokes": {},
                    },
                }
            ).encode()
            step = 64 * 1024
            for offset in range(0, len(large), step):
                data = large[offset : offset + step]
                await sender.send_json_to(
                    {
                        "type": "edit-chunk",
                        "clientId": "author",
                        "offset": offset,
                        "data": base64.b64encode(data).decode(),
                        "final": offset + len(data) == len(large),
                    }
                )
            assert await sender.receive_json_from() == {
                "type": "ack",
                "sequence": 4,
                "revision": 3,
            }
            assert await peer.receive_json_from() == {
                "type": "invalidate",
                "revision": 3,
            }
            await sender.disconnect()
            sender = socket(first)
            assert (await sender.connect())[0]
            restored = await sender.receive_json_from()
            assert restored["revision"] == 3
            records = restored["snapshot"]["document"]["store"]
            assert records["shape:abc"]["props"] == {
                "pts": [0, 0, 0.5, 1, 2, 0.5],
                "done": True,
            }
            assert records["asset:large"] == asset
        finally:
            await sender.disconnect()
            await peer.disconnect()

    async_to_sync(exercise)()
