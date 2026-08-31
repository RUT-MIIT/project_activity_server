"""Сопоставление ФИО преподавателей с пользователями PD."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


def normalize_name(value: str | None) -> str:
    """Нормализует ФИО для сравнения."""
    if not value:
        return ""
    text = str(value).strip().lower().replace("ё", "е")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zа-я0-9\s]", "", text)
    return text


def token_key(value: str | None) -> tuple[str, ...]:
    """Ключ из набора слов ФИО (устойчив к перестановке частей)."""
    normalized = normalize_name(value)
    if not normalized:
        return tuple()
    return tuple(sorted(normalized.split()))


def build_user_indexes(
    users: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, ...], list[dict[str, Any]]]]:
    """Строит индексы пользователей по ФИО."""
    by_name: dict[str, dict[str, Any]] = {}
    by_tokens: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for user in users:
        full_name = user.get("full_name") or ""
        norm = normalize_name(full_name)
        if norm:
            by_name.setdefault(norm, user)
        tokens = token_key(full_name)
        if tokens:
            by_tokens.setdefault(tokens, []).append(user)
    return by_name, by_tokens


def find_user(
    teacher_name: str | None,
    *,
    by_name: dict[str, dict[str, Any]],
    by_tokens: dict[tuple[str, ...], list[dict[str, Any]]],
) -> dict[str, Any] | None:
    """Ищет пользователя по ФИО преподавателя."""
    norm = normalize_name(teacher_name)
    if not norm:
        return None
    if norm in by_name:
        return by_name[norm]
    matches = by_tokens.get(token_key(teacher_name), [])
    if len(matches) == 1:
        return matches[0]
    return None


def load_users_from_json(path: Path) -> list[dict[str, Any]]:
    """Загружает список пользователей из JSON-файла."""
    return json.loads(path.read_text(encoding="utf-8"))
