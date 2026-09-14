"""Тесты доменных правил лобби команд."""

from types import SimpleNamespace

import pytest

from showcase.constants import DEFAULT_MAX_TEAM_MEMBERS, DEFAULT_MIN_TEAM_MEMBERS
from teams.domain.team_lobby import TeamLobbyDomain


def _fake_track(*, min_team_members: int, max_team_members: int) -> SimpleNamespace:
    return SimpleNamespace(
        min_team_members=min_team_members,
        max_team_members=max_team_members,
    )


class TestResolveMemberLimits:
    def test_single_group_track(self):
        track = _fake_track(min_team_members=3, max_team_members=6)
        assert TeamLobbyDomain.resolve_member_limits(None, group_tracks=[track]) == (
            3,
            6,
        )

    def test_multiple_group_tracks_soft_union(self):
        tracks = [
            _fake_track(min_team_members=5, max_team_members=7),
            _fake_track(min_team_members=4, max_team_members=10),
        ]
        assert TeamLobbyDomain.resolve_member_limits(None, group_tracks=tracks) == (
            4,
            10,
        )

    def test_team_track_overrides_group_tracks(self):
        team_track = _fake_track(min_team_members=2, max_team_members=5)
        group_tracks = [
            _fake_track(min_team_members=5, max_team_members=7),
            _fake_track(min_team_members=4, max_team_members=10),
        ]
        assert TeamLobbyDomain.resolve_member_limits(
            team_track, group_tracks=group_tracks
        ) == (2, 5)

    def test_empty_group_tracks_defaults(self):
        assert TeamLobbyDomain.resolve_member_limits(None, group_tracks=[]) == (
            DEFAULT_MIN_TEAM_MEMBERS,
            DEFAULT_MAX_TEAM_MEMBERS,
        )
        assert TeamLobbyDomain.resolve_member_limits(None, group_tracks=None) == (
            DEFAULT_MIN_TEAM_MEMBERS,
            DEFAULT_MAX_TEAM_MEMBERS,
        )


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
        with pytest.raises(ValueError, match="проектных треков"):
            TeamLobbyDomain.ensure_invitee_in_track_scope(
                invitee_group_id=9,
                allowed_group_ids={1, 3, 5},
            )

    def test_ensure_invitee_in_track_scope_rejects_none(self):
        with pytest.raises(ValueError, match="проектных треков"):
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
