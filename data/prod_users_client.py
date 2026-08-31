"""Клиент prod API для обновления снимка пользователей."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import httpx

DEFAULT_API_URL = "https://pd.rut-miit.ru"
LEGACY_API_URL = "https://pd.emiit.ru"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_API_URL = "PROD_PD_API_URL"
ENV_API_TOKEN = "PROD_PD_API_TOKEN"
ENV_EMAIL = "PROD_PD_EMAIL"
ENV_PASSWORD = "PROD_PD_PASSWORD"


def load_project_env() -> None:
    """Загружает переменные из .env в корне проекта."""
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")


def resolve_api_url(cli_value: str | None = None) -> str:
    """Возвращает базовый URL prod API."""
    if cli_value:
        url = cli_value.rstrip("/")
    else:
        url = os.environ.get(ENV_API_URL, DEFAULT_API_URL).rstrip("/")
    if url == LEGACY_API_URL:
        return DEFAULT_API_URL
    return url


def _http_client(**kwargs: object) -> httpx.Client:
    """HTTP-клиент с поддержкой редиректов prod."""
    return httpx.Client(follow_redirects=True, **kwargs)


def obtain_token(base_url: str, email: str, password: str) -> str:
    """Получает JWT access token по email и паролю."""
    url = f"{base_url}/api/accounts/login/"
    with _http_client(timeout=30.0) as client:
        response = client.post(url, json={"email": email, "password": password})
        response.raise_for_status()
        data = response.json()
    token = data.get("access")
    if not token:
        raise ValueError("Ответ login не содержит access token")
    return str(token)


def resolve_token(base_url: str, cli_token: str | None = None) -> str:
    """Возвращает Bearer token из CLI, env или login."""
    if cli_token:
        return cli_token
    env_token = os.environ.get(ENV_API_TOKEN)
    if env_token:
        return env_token
    email = os.environ.get(ENV_EMAIL)
    password = os.environ.get(ENV_PASSWORD)
    if email and password:
        return obtain_token(base_url, email, password)
    raise ValueError(
        "Не задан токен или учётные данные. "
        f"Укажите {ENV_API_TOKEN} или {ENV_EMAIL}+{ENV_PASSWORD}."
    )


def fetch_users(base_url: str, token: str) -> list[dict[str, Any]]:
    """Загружает список пользователей с prod API."""
    url = f"{base_url}/api/accounts/users/"
    headers = {"Authorization": f"Bearer {token}"}
    with _http_client(timeout=60.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    if not isinstance(data, list):
        raise ValueError("Ожидался список пользователей в ответе API")
    return data


def refresh_prod_users_json(
    path: Path,
    base_url: str,
    token: str,
) -> list[dict[str, Any]]:
    """Обновляет JSON-снимок пользователей prod."""
    users = fetch_users(base_url, token)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(users, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return users
