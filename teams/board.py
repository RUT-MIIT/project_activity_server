import json
from dataclasses import dataclass

from django.db import transaction

from teams.models import TeamBoard, TeamSemester

MAX_BOARD_BODY = 8 * 1024 * 1024


class InvalidBoardEdit(ValueError):
    pass


class BoardEditConflict(ValueError):
    pass


@dataclass
class BoardState:
    snapshot: dict
    revision: int


def empty_snapshot() -> dict:
    return {"document": {"store": {}}}


def load_board_state(team_id: int) -> BoardState:
    row = (
        TeamBoard.objects.filter(team_id=team_id)
        .values_list("snapshot", "revision")
        .first()
    )
    return BoardState(*row) if row is not None else BoardState(empty_snapshot(), 0)


def load_board_snapshot(team_id: int) -> dict:
    return load_board_state(team_id).snapshot


def board_records(snapshot: dict) -> dict:
    document = snapshot.get("document")
    records = document.get("store") if isinstance(document, dict) else None
    return records if isinstance(records, dict) else {}


def lock_board(team_id: int) -> TeamBoard:
    # The team row also serializes the first write, before a board row exists.
    TeamSemester.objects.select_for_update().only("id").get(pk=team_id)
    board, _ = TeamBoard.objects.get_or_create(
        team_id=team_id, defaults={"snapshot": empty_snapshot()}
    )
    return board


@transaction.atomic
def save_board_snapshot(team_id: int, snapshot: dict) -> dict:
    board = lock_board(team_id)
    if board.revision == 0:
        board.snapshot = snapshot
        board.save(update_fields=["snapshot"])
    return board.snapshot


def legacy_changes(diff: dict) -> dict:
    if not isinstance(diff, dict) or not all(
        isinstance(diff.get(key), dict) for key in ("added", "removed", "updated")
    ):
        raise InvalidBoardEdit("invalid diff")
    records = dict(diff["added"])
    for key, pair in diff["updated"].items():
        if not isinstance(pair, list) or len(pair) != 2:
            raise InvalidBoardEdit("invalid update")
        records[key] = pair[1]
    return {"records": records, "removed": list(diff["removed"]), "strokes": {}}


def validate_changes(changes: dict) -> None:
    if not isinstance(changes, dict):
        raise InvalidBoardEdit("invalid changes")
    records, removed, strokes = (
        changes.get(key) for key in ("records", "removed", "strokes")
    )
    if (
        not isinstance(records, dict)
        or not isinstance(removed, list)
        or not isinstance(strokes, dict)
    ):
        raise InvalidBoardEdit("invalid changes")
    ids = [*records, *removed, *strokes]
    if any(
        not isinstance(key, str)
        or not key
        or key in {"__proto__", "prototype", "constructor"}
        for key in ids
    ) or len(set(ids)) != len(ids):
        raise InvalidBoardEdit("invalid record ids")
    for key, record in records.items():
        if not isinstance(record, dict) or record.get("id") != key:
            raise InvalidBoardEdit("invalid record")
    for stroke in strokes.values():
        if not isinstance(stroke, dict):
            raise InvalidBoardEdit("invalid stroke")
        offset, points, done = (stroke.get(key) for key in ("offset", "points", "done"))
        if (
            type(offset) is not int
            or offset < 0
            or offset % 3
            or not isinstance(points, list)
            or len(points) % 3
            or not all(type(value) in (int, float) for value in points)
            or type(done) is not bool
        ):
            raise InvalidBoardEdit("invalid stroke")


@transaction.atomic
def persist_board_changes(team_id: int, changes: dict) -> int:
    validate_changes(changes)
    board = lock_board(team_id)
    document = board.snapshot.get("document")
    if not isinstance(document, dict):
        document = {}
    records = board_records(board.snapshot)
    for key, stroke in changes["strokes"].items():
        record = records.get(key)
        props = record.get("props") if isinstance(record, dict) else None
        points = props.get("pts") if isinstance(props, dict) else None
        if not isinstance(points, list) or len(points) != stroke["offset"]:
            raise BoardEditConflict("stroke has changed")
        records[key] = {
            **record,
            "props": {
                **props,
                "pts": points + stroke["points"],
                "done": stroke["done"],
            },
        }
    records.update(changes["records"])
    for key in changes["removed"]:
        records.pop(key, None)
    board.snapshot = {**board.snapshot, "document": {**document, "store": records}}
    size = len(
        json.dumps(board.snapshot, ensure_ascii=False, separators=(",", ":")).encode()
    )
    if size > MAX_BOARD_BODY:
        raise InvalidBoardEdit("board exceeds size limit")
    board.revision += 1
    board.save(update_fields=["snapshot", "revision"])
    return board.revision


def load_legacy_diff(team_id: int, record_ids: list[str]) -> dict:
    records = board_records(load_board_snapshot(team_id))
    return {
        "added": {},
        "updated": {key: [None, records[key]] for key in record_ids if key in records},
        "removed": {key: {} for key in record_ids if key not in records},
    }
