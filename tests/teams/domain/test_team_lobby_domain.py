"""Тесты доменных правил лобби команд."""

import pytest

from teams.domain.team_lobby import TeamLobbyDomain


class TestTeamLobbyDomainTrackScope:
    def test_ensure_track_selected_ok(self):
        assert TeamLobbyDomain.ensure_track_selected(7) == 7

    def test_ensure_track_selected_none(self):
        with pytest.raises(ValueError, match="Выберите проектный трек"):
            TeamLobbyDomain.ensure_track_selected(None)

    def test_ensure_invitee_in_track_scope_ok(self):
        TeamLobbyDomain.ensure_invitee_in_track_scope(
            invitee_group_id=3,
            allowed_group_ids={1, 3, 5},
        )

    def test_ensure_invitee_in_track_scope_rejects_outside(self):
        with pytest.raises(ValueError, match="проектного трека"):
            TeamLobbyDomain.ensure_invitee_in_track_scope(
                invitee_group_id=9,
                allowed_group_ids={1, 3, 5},
            )

    def test_ensure_invitee_in_track_scope_rejects_none(self):
        with pytest.raises(ValueError, match="проектного трека"):
            TeamLobbyDomain.ensure_invitee_in_track_scope(
                invitee_group_id=None,
                allowed_group_ids={1},
            )

    def test_ensure_invitee_registered(self):
        TeamLobbyDomain.ensure_invitee_registered(is_registered=True)
        with pytest.raises(ValueError, match="не зарегистрирован"):
            TeamLobbyDomain.ensure_invitee_registered(is_registered=False)

    def test_can_invite_candidate(self):
        assert (
            TeamLobbyDomain.can_invite_candidate(
                is_registered=True,
                in_team=False,
                has_pending_invitation=False,
                is_self=False,
            )
            is True
        )
        assert (
            TeamLobbyDomain.can_invite_candidate(
                is_registered=False,
                in_team=False,
                has_pending_invitation=False,
                is_self=False,
            )
            is False
        )
        assert (
            TeamLobbyDomain.can_invite_candidate(
                is_registered=True,
                in_team=True,
                has_pending_invitation=False,
                is_self=False,
            )
            is False
        )
        assert (
            TeamLobbyDomain.can_invite_candidate(
                is_registered=True,
                in_team=False,
                has_pending_invitation=True,
                is_self=False,
            )
            is False
        )
        assert (
            TeamLobbyDomain.can_invite_candidate(
                is_registered=True,
                in_team=False,
                has_pending_invitation=False,
                is_self=True,
            )
            is False
        )

    def test_parse_name_query(self):
        assert TeamLobbyDomain.parse_name_query("  Ива  ") == ["Ива"]
        assert TeamLobbyDomain.parse_name_query("Ива Пет") == ["Ива", "Пет"]
        with pytest.raises(ValueError, match="не менее 2"):
            TeamLobbyDomain.parse_name_query("")
        with pytest.raises(ValueError, match="не менее 2"):
            TeamLobbyDomain.parse_name_query("И")
        with pytest.raises(ValueError, match="не менее 2"):
            TeamLobbyDomain.parse_name_query("Ива П")
