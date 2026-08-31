import asyncio
from typing import Any

import httpx

BASE_URL = "https://rut-miit.ru"
GROUPS_CATALOG_URL = f"{BASE_URL}/data-service/data/timetable/groups-catalog"
GROUP_TIMETABLES_URL = f"{BASE_URL}/data-service/data/timetable/v2/group"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; timetable-parser/0.1)",
    "Accept": "application/json",
}

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 1.0


class RutMiitClient:
    def __init__(self, concurrency: int = 8) -> None:
        self._semaphore = asyncio.Semaphore(concurrency)
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "RutMiitClient":
        self._client = httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=httpx.Timeout(30.0),
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._client is not None:
            await self._client.aclose()

    async def _get_json(self, url: str) -> dict[str, Any]:
        if self._client is None:
            raise RuntimeError("Client is not initialized. Use async with.")

        last_error: Exception | None = None
        for attempt in range(MAX_RETRIES):
            async with self._semaphore:
                try:
                    response = await self._client.get(url)
                    if response.status_code == 429 or response.status_code >= 500:
                        response.raise_for_status()
                    response.raise_for_status()
                    return response.json()
                except (httpx.HTTPError, ValueError) as exc:
                    last_error = exc
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))

        raise last_error or RuntimeError(f"Failed to fetch {url}")

    async def get_groups_catalog(self) -> dict[str, Any]:
        return await self._get_json(GROUPS_CATALOG_URL)

    async def get_group_timetables(self, group_id: int) -> dict[str, Any]:
        return await self._get_json(f"{GROUP_TIMETABLES_URL}/{group_id}")

    async def get_group_schedule(
        self, group_id: int, timetable_id: str
    ) -> dict[str, Any]:
        return await self._get_json(f"{GROUP_TIMETABLES_URL}/{group_id}/{timetable_id}")
