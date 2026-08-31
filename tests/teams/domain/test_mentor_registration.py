"""Тесты domain-слоя назначения групп наставнику при регистрации."""

from __future__ import annotations

import pytest

from accounts.models import PreRegisteredStudent
from teams.domain.mentor_registration import (
    build_mentor_full_name,
    build_mentor_registration_context,
    mentor_full_name_matches,
    normalize_personnel_number,
)


class TestNormalizePersonnelNumber:
    def test_strips_float_suffix(self) -> None:
        assert normalize_personnel_number("1054855.0") == "1054855"

    def test_empty_returns_empty(self) -> None:
        assert normalize_personnel_number("") == ""


class TestMentorFullNameMatches:
    def test_exact_match(self) -> None:
        assert mentor_full_name_matches(
            "Иванов Иван Иванович",
            "Иванов Иван Иванович",
        )

    def test_token_match_with_different_order(self) -> None:
        assert mentor_full_name_matches(
            "Иванов Иван Иванович",
            "Иван Иванович Иванов",
        )

    def test_no_match(self) -> None:
        assert not mentor_full_name_matches(
            "Иванов Иван Иванович",
            "Петров Пётр Петрович",
        )


@pytest.mark.django_db
class TestBuildMentorRegistrationContext:
    def test_builds_from_pre_registered(self) -> None:
        pre_registered = PreRegisteredStudent(
            last_name="Ишханян",
            first_name="Маргарита",
            middle_name="Владимировна",
            personnel_number="1347607.0",
            role_id="mentor",
        )

        context = build_mentor_registration_context(pre_registered)

        assert context.personnel_number == "1347607"
        assert context.full_name == build_mentor_full_name(
            last_name="Ишханян",
            first_name="Маргарита",
            middle_name="Владимировна",
        )
