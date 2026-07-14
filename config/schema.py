"""Хуки и расширения для drf-spectacular."""

from __future__ import annotations


def exclude_auth_api_duplicate(
    endpoints: list[tuple],
) -> list[tuple]:
    """
    Исключает дублирующие маршруты /api/auth/* (зеркалят /api/accounts/*).

    В Postman и Swagger остаётся один канонический префикс /api/accounts/.
    """
    filtered = []
    for path, path_regex, method, callback in endpoints:
        if path.startswith("/api/auth/"):
            continue
        filtered.append((path, path_regex, method, callback))
    return filtered
