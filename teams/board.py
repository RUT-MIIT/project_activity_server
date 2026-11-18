from teams.models import TeamBoard


def load_board_snapshot(team_id: int) -> dict:
    snapshot = (
        TeamBoard.objects.filter(team_id=team_id)
        .values_list("snapshot", flat=True)
        .first()
    )
    return {"document": {"store": {}}} if snapshot is None else snapshot
