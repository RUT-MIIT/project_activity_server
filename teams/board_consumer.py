import base64
import binascii
import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from teams.board import (
    MAX_BOARD_BODY,
    BoardEditConflict,
    InvalidBoardEdit,
    legacy_changes,
    load_board_state,
    load_legacy_diff,
    persist_board_changes,
)
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
            query = parse_qs(
                self.scope["query_string"].decode("ascii"), max_num_fields=8
            )
        except ValueError:
            query = {}
        tokens = query.get("token", [])
        self.durable = query.get("sync") == ["2"]
        self.edit_buffer = bytearray()
        self.team_id = self.scope["url_route"]["kwargs"]["team_id"]
        if len(tokens) != 1 or not await can_access_board(tokens[0], self.team_id):
            await self.close(code=4403)
            return
        self.legacy_group = f"team_{self.team_id}"
        self.durable_group = f"team_{self.team_id}_durable"
        self.group_name = self.durable_group if self.durable else self.legacy_group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_snapshot()

    async def disconnect(self, code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_snapshot(self, retry=None):
        state = await database_sync_to_async(load_board_state)(self.team_id)
        message = {"type": "snapshot", "clientId": "server", "snapshot": state.snapshot}
        if self.durable:
            message.update(protocol=2, revision=state.revision)
            if retry is not None:
                message["retry"] = retry
        await self.send_json(message)

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
            payload = json.dumps(
                message, allow_nan=False, ensure_ascii=False, separators=(",", ":")
            ).encode()
            if len(payload) > MAX_BOARD_MESSAGE:
                await self.close(code=1009)
                return
        except (ValueError, RecursionError):
            return
        if message.get("type") == "edit-chunk" and self.durable:
            await self.receive_chunk(message)
            return
        self.edit_buffer.clear()
        await self.receive_message(message)

    async def receive_chunk(self, message):
        offset, data, final = (message.get(key) for key in ("offset", "data", "final"))
        try:
            if (
                type(offset) is not int
                or offset != len(self.edit_buffer)
                or type(final) is not bool
            ):
                raise ValueError
            self.edit_buffer.extend(base64.b64decode(data, validate=True))
            if len(self.edit_buffer) > MAX_BOARD_BODY + MAX_BOARD_MESSAGE:
                await self.close(code=1009)
                self.edit_buffer.clear()
                return
            if not final:
                return
            decoded = json.loads(self.edit_buffer.decode("utf-8"))
            if (
                not isinstance(decoded, dict)
                or decoded.get("type") != "edit"
                or decoded.get("clientId") != message["clientId"]
            ):
                raise ValueError
            json.dumps(decoded, allow_nan=False, ensure_ascii=False).encode()
        except (ValueError, TypeError, RecursionError, binascii.Error):
            self.edit_buffer.clear()
            await self.close(code=1007)
            return
        self.edit_buffer.clear()
        await self.receive_message(decoded)

    async def receive_message(self, message):
        if message.get("type") == "hello":
            await self.send_snapshot()
        elif message.get("type") == "edit" and self.durable:
            sequence = message.get("sequence")
            if type(sequence) is int and 0 < sequence < 2**53:
                await self.persist(message, message.get("changes"), sequence)
        elif message.get("type") == "diff" and not self.durable:
            try:
                changes = legacy_changes(message.get("diff"))
            except InvalidBoardEdit:
                return
            await self.persist(message, changes)

    async def persist(self, message, changes, sequence=None):
        try:
            revision = await database_sync_to_async(persist_board_changes)(
                self.team_id, changes
            )
        except BoardEditConflict:
            await self.send_snapshot(retry=sequence)
            return
        except InvalidBoardEdit:
            if self.durable:
                await self.send_json({"type": "edit-rejected", "sequence": sequence})
            return
        if self.durable:
            await self.send_json(
                {"type": "ack", "sequence": sequence, "revision": revision}
            )
        client_id = message["clientId"]
        edit = {
            "type": "edit",
            "clientId": client_id,
            "revision": revision,
            "changes": changes,
        }
        payload = json.dumps(edit, ensure_ascii=False, separators=(",", ":")).encode()
        if len(payload) > MAX_BOARD_MESSAGE:
            payload = json.dumps({"type": "invalidate", "revision": revision}).encode()
        await self.channel_layer.group_send(
            self.durable_group,
            {
                "type": "board.diff",
                "sender": self.channel_name,
                "payload": payload,
            },
        )
        await self.channel_layer.group_send(
            self.legacy_group,
            {
                "type": "board.legacy",
                "sender": self.channel_name,
                "client_id": client_id,
                "record_ids": [
                    *changes["records"],
                    *changes["removed"],
                    *changes["strokes"],
                ],
            },
        )

    async def board_diff(self, event):
        if event["sender"] != self.channel_name:
            await self.send(text_data=event["payload"].decode())

    async def board_legacy(self, event):
        if event["sender"] != self.channel_name:
            diff = await database_sync_to_async(load_legacy_diff)(
                self.team_id, event["record_ids"]
            )
            await self.send_json(
                {"type": "diff", "clientId": event["client_id"], "diff": diff}
            )
