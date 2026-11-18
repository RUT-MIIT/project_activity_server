import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from teams.board import load_board_snapshot
from teams.models import TeamSemesterMember

MAX_BOARD_MESSAGE = 512 * 1024


@database_sync_to_async
def can_access_board(token: str, team_id: int) -> bool:
    authentication = JWTAuthentication()
    try:
        user = authentication.get_user(authentication.get_validated_token(token))
    except (AuthenticationFailed, TokenError):
        return False
    return bool(
        user.role
        and user.role.code == "student"
        and user.study_group_id
        and TeamSemesterMember.objects.filter(
            team_semester_id=team_id, user_id=user.pk
        ).exists()
    )


class TeamBoardConsumer(AsyncJsonWebsocketConsumer):
    group_name = None

    async def connect(self):
        try:
            tokens = parse_qs(
                self.scope["query_string"].decode("ascii"), max_num_fields=8
            ).get("token", [])
        except ValueError:
            tokens = []
        self.team_id = self.scope["url_route"]["kwargs"]["team_id"]
        if len(tokens) != 1 or not await can_access_board(tokens[0], self.team_id):
            await self.close(code=4403)
            return
        self.group_name = f"team_{self.team_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_snapshot()

    async def disconnect(self, code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_snapshot(self):
        snapshot = await database_sync_to_async(load_board_snapshot)(self.team_id)
        await self.send_json(
            {"type": "snapshot", "clientId": "server", "snapshot": snapshot}
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data is None:
            await self.close(code=1003)
            return
        if len(text_data.encode("utf-8")) > MAX_BOARD_MESSAGE:
            await self.close(code=1009)
            return
        try:
            message = json.loads(text_data)
            if not isinstance(message, dict) or not isinstance(
                message.get("clientId"), str
            ):
                return
            # Validate JSON encodability before sending it to the channel layer.
            payload = json.dumps(message, allow_nan=False, ensure_ascii=False).encode()
            if len(payload) > MAX_BOARD_MESSAGE:
                await self.close(code=1009)
                return
        except (ValueError, RecursionError):
            return
        if message.get("type") == "hello":
            await self.send_snapshot()
        elif message.get("type") == "diff":
            diff = message.get("diff")
            if isinstance(diff, dict) and all(
                isinstance(diff.get(key), dict)
                for key in ("added", "removed", "updated")
            ):
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "board.diff",
                        "sender": self.channel_name,
                        "payload": payload,
                    },
                )

    async def board_diff(self, event):
        if event["sender"] != self.channel_name:
            await self.send(text_data=event["payload"].decode())
