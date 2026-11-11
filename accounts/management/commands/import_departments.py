import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import Department


UNIVERSITY_ID = 37


class Command(BaseCommand):
    help = "Импорт подразделений из data/miit_departments.json."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file", type=Path, default=settings.BASE_DIR / "data/miit_departments.json"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            rows = json.loads(Path(options["file"]).read_text(encoding="utf-8"))["departments"]
        except (OSError, ValueError, KeyError) as exc:
            raise CommandError(f"Не удалось прочитать справочник: {exc}") from exc

        ids = {row["id"] for row in rows}
        if not rows or len(ids) != len(rows):
            raise CommandError("Справочник пуст или содержит повторяющиеся ID")

        departments = {}
        parents = {}
        names = set()
        for row in rows:
            key = row["id"]
            if row.get("error") or not row.get("name"):
                raise CommandError(f"Карточка {key} не загружена полностью")
            if key == UNIVERSITY_ID:
                continue

            parent_ids = set(row["parent_ids"]) - {UNIVERSITY_ID}
            if len(parent_ids) > 1 or not parent_ids <= ids:
                raise CommandError(f"Некорректный родитель в карточке {key}")
            parents[key] = next(iter(parent_ids), None)

            name = row["name"]
            full_name, separator, short_name = name.rpartition(", ")
            if separator and len(short_name) <= 64:
                name = full_name
            else:
                short_name = name if len(name) <= 64 else " ".join(
                    word[0] for word in name.split()
                )[:64]
            if len(name) > 255 and key == 27487:
                name = short_name
            if len(name) > 255 or name in names:
                raise CommandError(f"Слишком длинное или повторяющееся имя в карточке {key}")
            names.add(name)

            department, _ = Department.objects.get_or_create(
                name=name, defaults={"short_name": short_name}
            )
            department.short_name = short_name
            departments[key] = department

        for key, department in departments.items():
            visited = {key}
            ancestor = parents[key]
            while ancestor is not None:
                if ancestor in visited:
                    raise CommandError(f"Цикл в иерархии подразделения {key}")
                visited.add(ancestor)
                ancestor = parents[ancestor]
            department.parent = departments.get(parents[key])
        Department.objects.bulk_update(departments.values(), ["short_name", "parent"])
        self.stdout.write(self.style.SUCCESS(f"Импортировано подразделений: {len(departments)}"))
