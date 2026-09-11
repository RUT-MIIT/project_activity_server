"""Тесты доменной логики окна регистрации института."""

from __future__ import annotations

from datetime import timedelta
from types import SimpleNamespace

from django.utils import timezone
import pytest

from teams.domain.institute_responsible import InstituteResponsibleDomain


def _settings(
    *,
    opens_at=None,
    closed_by_decision: bool = False,
) -> SimpleNamespace:
    return SimpleNamespace(
        registration_opens_at=opens_at,
        closed_by_decision=closed_by_decision,
    )


@pytest.mark.parametrize(
    ("opens_at_delta", "closed", "expected"),
    [
        (-1, False, True),
        (-1, True, True),
        (1, False, False),
        (1, True, False),
        (None, False, False),
        (None, True, False),
    ],
)
def test_is_registration_opened_by_schedule(
    opens_at_delta: int | None,
    closed: bool,
    expected: bool,
) -> None:
    now = timezone.now()
    opens_at = None if opens_at_delta is None else now + timedelta(days=opens_at_delta)
    settings = _settings(opens_at=opens_at, closed_by_decision=closed)
    assert (
        InstituteResponsibleDomain.is_registration_opened_by_schedule(settings, now=now)
        is expected
    )


def test_is_registration_opened_by_schedule_none_settings() -> None:
    assert InstituteResponsibleDomain.is_registration_opened_by_schedule(None) is False


def test_is_registration_open_respects_closed_by_decision() -> None:
    now = timezone.now()
    settings = _settings(
        opens_at=now - timedelta(days=1),
        closed_by_decision=True,
    )
    assert InstituteResponsibleDomain.is_registration_open(settings, now=now) is False
    assert (
        InstituteResponsibleDomain.is_registration_opened_by_schedule(settings, now=now)
        is True
    )
