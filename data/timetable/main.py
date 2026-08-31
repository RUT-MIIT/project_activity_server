import argparse
import asyncio
import sys

from src.api import RutMiitClient
from src.export_xlsx import export_to_xlsx
from src.extract import fetch_group_result, flatten_groups_catalog


def _format_teachers(result) -> str:
    if not result.teachers:
        return result.status
    return "; ".join(teacher.short_fio for teacher in result.teachers)


async def run(output_path: str, concurrency: int) -> int:
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
                f"[{index + 1}/{total}] {group.group_name} -> {_format_teachers(result)}",
                flush=True,
            )

        await asyncio.gather(*(process(i, group) for i, group in enumerate(groups)))

    export_to_xlsx(results, output_path)

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

    return 0 if errors == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Парсинг преподавателей «Проектная деятельность» "
            "по всем группам РУТ (МИИТ)"
        )
    )
    parser.add_argument(
        "--output",
        "-o",
        default="project_teachers.xlsx",
        help="Путь к выходному Excel-файлу",
    )
    parser.add_argument(
        "--concurrency",
        "-c",
        type=int,
        default=8,
        help="Число параллельных HTTP-запросов",
    )
    args = parser.parse_args()

    if args.concurrency < 1:
        print("concurrency должен быть >= 1", file=sys.stderr)
        sys.exit(2)

    exit_code = asyncio.run(run(args.output, args.concurrency))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
