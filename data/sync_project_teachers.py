"""Парсинг расписания РУТ и сверка преподавателей с пользователями prod PD."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
import sys

DATA_DIR = Path(__file__).resolve().parent
TIMETABLE_DIR = DATA_DIR / "timetable"
DEFAULT_OUTPUT = DATA_DIR / "project_teachers_marked.xlsx"
DEFAULT_USERS_JSON = DATA_DIR / "prod_users.json"

sys.path.insert(0, str(DATA_DIR))
sys.path.insert(0, str(TIMETABLE_DIR))

from prod_users_client import (  # noqa: E402
    load_project_env,
    refresh_prod_users_json,
    resolve_api_url,
    resolve_token,
)
from src.api import RutMiitClient  # noqa: E402
from src.export_xlsx import export_marked_xlsx  # noqa: E402
from src.extract import fetch_group_result, flatten_groups_catalog  # noqa: E402
from teacher_matching import (  # noqa: E402
    build_user_indexes,
    find_user,
    load_users_from_json,
)


def _format_teachers(result) -> str:
    if not result.teachers:
        return result.status
    return "; ".join(teacher.short_fio for teacher in result.teachers)


async def parse_all_groups(concurrency: int) -> list:
    """Парсит преподавателей «Проектная деятельность» по всем группам."""
    async with RutMiitClient(concurrency=concurrency) as client:
        catalog = await client.get_groups_catalog()
        groups = flatten_groups_catalog(catalog)
        total = len(groups)
        print(f"Найдено групп: {total}")

        results: list = [None] * total

        async def process(index: int, group) -> None:
            result = await fetch_group_result(client, group)
            results[index] = result
            print(
                f"[{index + 1}/{total}] {group.group_name} -> "
                f"{_format_teachers(result)}",
                flush=True,
            )

        await asyncio.gather(*(process(i, group) for i, group in enumerate(groups)))

    return results


def _print_parse_summary(results: list, output_path: Path) -> int:
    """Печатает сводку парсинга и возвращает exit code."""
    found = sum(1 for result in results if result.status == "найдено")
    no_lessons = sum(1 for result in results if result.status == "нет занятий")
    no_schedule = sum(1 for result in results if result.status == "нет расписания")
    errors = sum(1 for result in results if result.status == "ошибка загрузки")

    print()
    print(f"Готово: {output_path}")
    print(f"  с занятиями: {found}")
    print(f"  без занятий: {no_lessons}")
    print(f"  без расписания: {no_schedule}")
    print(f"  ошибки: {errors}")
    return 1 if errors else 0


def main() -> None:
    """Обновляет prod_users.json, парсит расписание и сохраняет помеченный Excel."""
    load_project_env()

    parser = argparse.ArgumentParser(
        description=(
            "Парсинг преподавателей «Проектная деятельность» по группам РУТ (МИИТ) "
            "и сверка с пользователями prod PD"
        )
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Путь к выходному Excel (по умолчанию: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--concurrency",
        "-c",
        type=int,
        default=8,
        help="Число параллельных HTTP-запросов к RUT API",
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default=None,
        help="Базовый URL prod API (env PROD_PD_API_URL или https://pd.rut-miit.ru)",
    )
    parser.add_argument(
        "--users-json",
        type=Path,
        default=DEFAULT_USERS_JSON,
        help=f"Путь к JSON-снимку пользователей (по умолчанию: {DEFAULT_USERS_JSON})",
    )
    parser.add_argument(
        "--skip-refresh-users",
        action="store_true",
        help="Не обновлять prod_users.json с prod API",
    )
    args = parser.parse_args()

    if args.concurrency < 1:
        print("concurrency должен быть >= 1", file=sys.stderr)
        sys.exit(2)

    base_url = resolve_api_url(args.api_url)
    users_json = args.users_json.resolve()

    if not args.skip_refresh_users:
        print(f"Обновление пользователей с {base_url}...")
        token = resolve_token(base_url)
        users = refresh_prod_users_json(users_json, base_url, token)
        print(f"Сохранено пользователей: {len(users)} -> {users_json}")
    else:
        if not users_json.is_file():
            print(f"Файл не найден: {users_json}", file=sys.stderr)
            sys.exit(2)
        users = load_users_from_json(users_json)
        print(f"Пользователей в JSON: {len(users)}")

    by_name, by_tokens = build_user_indexes(users)

    def match_teacher(name: str | None):
        return find_user(name, by_name=by_name, by_tokens=by_tokens)

    results = asyncio.run(parse_all_groups(args.concurrency))
    output_path = args.output.resolve()
    found, missing = export_marked_xlsx(results, str(output_path), match_teacher)

    print()
    print(f"Сверка с PD (строки с преподавателем): {found + missing}")
    print(f"  найдено в системе: {found}")
    print(f"  не найдено: {missing}")

    exit_code = _print_parse_summary(results, output_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
