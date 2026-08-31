"""Тесты сопоставления ФИО преподавателей с пользователями PD."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from teacher_matching import (
    build_user_indexes,
    find_user,
    load_users_from_json,
    normalize_name,
    token_key,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Иванов Иван Иванович", "иванов иван иванович"),
        ("  Ёлкин-Петров  ", "елкинпетров"),
        ("", ""),
        (None, ""),
    ],
)
def test_normalize_name(value: str | None, expected: str) -> None:
    """Нормализует ФИО для сравнения."""
    assert normalize_name(value) == expected


def test_token_key_sorted_tokens() -> None:
    """Ключ токенов не зависит от порядка слов."""
    assert token_key("Иванов Иван") == token_key("Иван Иванов")


def test_find_user_exact_match() -> None:
    """Находит пользователя по точному совпадению ФИО."""
    users = [{"id": 1, "full_name": "Иванов Иван Иванович", "email": "a@x.ru"}]
    by_name, by_tokens = build_user_indexes(users)
    user = find_user(
        "Иванов Иван Иванович",
        by_name=by_name,
        by_tokens=by_tokens,
    )
    assert user is not None
    assert user["id"] == 1


def test_find_user_token_match_reordered() -> None:
    """Находит пользователя при перестановке частей ФИО."""
    users = [{"id": 2, "full_name": "Петров Пётр Петрович", "email": "b@x.ru"}]
    by_name, by_tokens = build_user_indexes(users)
    user = find_user(
        "Пётр Петрович Петров",
        by_name=by_name,
        by_tokens=by_tokens,
    )
    assert user is not None
    assert user["id"] == 2


def test_find_user_ambiguous_returns_none() -> None:
    """При нескольких совпадениях по токенам возвращает None."""
    users = [
        {"id": 1, "full_name": "Иванов Иван Петрович", "email": "a@x.ru"},
        {"id": 2, "full_name": "Петрович Иван Иванов", "email": "b@x.ru"},
    ]
    by_name, by_tokens = build_user_indexes(users)
    assert (
        find_user("Иван Петрович Иванов", by_name=by_name, by_tokens=by_tokens) is None
    )


def test_find_user_no_match() -> None:
    """Возвращает None, если пользователь не найден."""
    users = [{"id": 1, "full_name": "Сидоров Сидор", "email": "c@x.ru"}]
    by_name, by_tokens = build_user_indexes(users)
    assert find_user("Несуществующий", by_name=by_name, by_tokens=by_tokens) is None


def test_load_users_from_json(tmp_path: Path) -> None:
    """Загружает пользователей из JSON-файла."""
    path = tmp_path / "users.json"
    payload = [{"id": 1, "full_name": "Test", "email": "t@x.ru"}]
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert load_users_from_json(path) == payload
