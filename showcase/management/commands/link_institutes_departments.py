from collections import defaultdict
from typing import Any, Dict, List

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Department
from showcase.models import Institute


class Command(BaseCommand):
    help = (
        "Для каждого Institute ищет Department с таким же названием "
        "и записывает его в поле 'Связанное подразделение'."
    )

    def handle(self, *args: Any, **options: Any) -> None:
        """Проставляет связи институтов с подразделениями по совпадению названий."""
        self.stdout.write("Начинаю проставление связей институтов с подразделениями...")

        departments_by_name: Dict[str, List[Department]] = defaultdict(list)
        for department in Department.objects.all():
            departments_by_name[department.name].append(department)

        if not departments_by_name:
            self.stdout.write(
                self.style.WARNING(
                    "В базе нет ни одного подразделения (accounts.Department)."
                )
            )

        updated_count: int = 0
        not_found_count: int = 0
        ambiguous_count: int = 0

        with transaction.atomic():
            for institute in Institute.objects.all():
                departments: List[Department] = departments_by_name.get(
                    institute.name, []
                )

                if not departments:
                    not_found_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Для института '{institute.name}' не найдено подразделение."
                        )
                    )
                    continue

                if len(departments) > 1:
                    ambiguous_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            "Найдено несколько подразделений с именем "
                            f"'{institute.name}'. Использую первое по id."
                        )
                    )

                department: Department = sorted(
                    departments,
                    key=lambda d: d.id,  # type: ignore[arg-type]
                )[0]

                if institute.department_id == department.id:
                    # Уже связано с нужным подразделением
                    continue

                institute.department = department
                institute.save(update_fields=["department"])
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Готово. Обновлено институтов: "
                f"{updated_count}, без соответствия: {not_found_count}, "
                f"с неоднозначным соответствием: {ambiguous_count}."
            )
        )
