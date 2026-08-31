"""Тесты клиента prod API для обновления prod_users.json."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
from prod_users_client import (
    fetch_users,
    obtain_token,
    refresh_prod_users_json,
    resolve_api_url,
    resolve_token,
)
import pytest


def test_resolve_api_url_default() -> None:
    """Возвращает prod URL по умолчанию."""
    assert resolve_api_url() == "https://pd.rut-miit.ru"


def test_resolve_api_url_legacy_domain() -> None:
    """Старый домен pd.emiit.ru заменяется на актуальный."""
    assert resolve_api_url("https://pd.emiit.ru") == "https://pd.rut-miit.ru"


def test_resolve_api_url_strips_trailing_slash() -> None:
    """Убирает завершающий слэш из URL."""
    assert resolve_api_url("https://example.com/") == "https://example.com"


def test_obtain_token() -> None:
    """Получает access token через login."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"access": "jwt-token"}
    mock_response.raise_for_status = MagicMock()

    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.post.return_value = mock_response

    with patch("prod_users_client.httpx.Client", return_value=mock_client):
        token = obtain_token("https://pd.emiit.ru", "admin@x.ru", "secret")

    assert token == "jwt-token"
    mock_client.post.assert_called_once_with(
        "https://pd.emiit.ru/api/accounts/login/",
        json={"email": "admin@x.ru", "password": "secret"},
    )


def test_fetch_users() -> None:
    """Загружает список пользователей с API."""
    users = [{"id": 1, "full_name": "Test", "email": "t@x.ru"}]
    mock_response = MagicMock()
    mock_response.json.return_value = users
    mock_response.raise_for_status = MagicMock()

    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.get.return_value = mock_response

    with patch("prod_users_client.httpx.Client", return_value=mock_client):
        result = fetch_users("https://pd.emiit.ru", "jwt-token")

    assert result == users
    mock_client.get.assert_called_once_with(
        "https://pd.emiit.ru/api/accounts/users/",
        headers={"Authorization": "Bearer jwt-token"},
    )


def test_refresh_prod_users_json(tmp_path: Path) -> None:
    """Сохраняет пользователей в JSON-файл."""
    users = [{"id": 1, "full_name": "Test", "email": "t@x.ru"}]
    out_path = tmp_path / "prod_users.json"

    with patch("prod_users_client.fetch_users", return_value=users):
        result = refresh_prod_users_json(
            out_path,
            "https://pd.emiit.ru",
            "jwt-token",
        )

    assert result == users
    saved = json.loads(out_path.read_text(encoding="utf-8"))
    assert saved == users


def test_resolve_token_from_cli() -> None:
    """CLI-токен имеет приоритет."""
    assert resolve_token("https://pd.emiit.ru", cli_token="cli-token") == "cli-token"


def test_resolve_token_missing_credentials() -> None:
    """Ошибка, если не заданы ни токен, ни учётные данные."""
    with (
        patch.dict("os.environ", {}, clear=True),
        pytest.raises(ValueError, match="Не задан токен"),
    ):
        resolve_token("https://pd.emiit.ru")
