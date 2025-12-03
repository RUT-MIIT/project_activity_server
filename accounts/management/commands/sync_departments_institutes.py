import os
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import ProtectedError

from accounts.models import Department
from showcase.models import Institute


class Command(BaseCommand):
    """Команда для импорта/экспорта подразделений и институтов в Excel."""

    help = (
        "Импорт/экспорт справочников подразделений и институтов.\n"
        "Режимы работы задаются флагами --mode и --entity.\n"
        "Примеры:\n"
        "  python manage.py sync_departments_institutes --mode export --entity departments\n"
        "  python manage.py sync_departments_institutes --mode import --entity institutes\n"
    )

    def add_arguments(self, parser: Any) -> None:
        """Добавляет аргументы командной строки."""
        parser.add_argument(
            "--mode",
            type=str,
            choices=["export", "import"],
            required=True,
            help="Режим работы команды: export или import.",
        )
        parser.add_argument(
            "--entity",
            type=str,
            choices=["departments", "institutes"],
            required=True,
            help="Справочник: departments или institutes.",
        )
        parser.add_argument(
            "--file",
            type=str,
            help=(
                "Путь к Excel файлу (.xlsx). "
                "Если не указан, используется файл рядом с командой: "
                "departments.xlsx или institutes.xlsx."
            ),
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Точка входа команды."""
        mode: str = options["mode"]
        entity: str = options["entity"]
        file_path: str = self._resolve_file_path(options.get("file"), entity)

        if mode == "export":
            if entity == "departments":
                self._export_departments(file_path)
            else:
                self._export_institutes(file_path)
        else:
            if not os.path.exists(file_path):
                raise CommandError(f"Файл '{file_path}' не найден.")

            if entity == "departments":
                self._import_departments(file_path)
            else:
                self._import_institutes(file_path)

    def _resolve_file_path(self, file_option: Optional[str], entity: str) -> str:
        """Определяет путь к файлу Excel."""
        if file_option:
            if os.path.isabs(file_option):
                return file_option
            commands_dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(commands_dir, file_option)

        default_name = (
            "departments.xlsx" if entity == "departments" else "institutes.xlsx"
        )
        commands_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(commands_dir, default_name)

    # ===== EXPORT =====

    def _export_departments(self, file_path: str) -> None:
        """Экспортирует все подразделения в Excel."""
        departments: Iterable[Department] = Department.objects.all().order_by("name")

        data: List[Dict[str, Any]] = []
        for dep in departments:
            data.append(
                {
                    "name": dep.name,
                    "short_name": dep.short_name,
                    "parent_name": dep.parent.name if dep.parent else None,
                    "can_save_project_applications": dep.can_save_project_applications,
                }
            )

        if not data:
            self.stdout.write(self.style.WARNING("Подразделения в базе не найдены."))

        pd.DataFrame(data).to_excel(file_path, index=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Экспортировано подразделений: {len(data)}. Файл сохранён в {file_path}"
            )
        )

    def _export_institutes(self, file_path: str) -> None:
        """Экспортирует все институты в Excel."""
        institutes: Iterable[Institute] = Institute.objects.all().order_by(
            "position", "code"
        )

        data: List[Dict[str, Any]] = []
        for inst in institutes:
            data.append(
                {
                    "code": inst.code,
                    "name": inst.name,
                    "position": inst.position,
                    "is_active": inst.is_active,
                    "department_name": (
                        inst.department.name if inst.department else None
                    ),
                }
            )

        if not data:
            self.stdout.write(self.style.WARNING("Институты в базе не найдены."))

        pd.DataFrame(data).to_excel(file_path, index=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Экспортировано институтов: {len(data)}. Файл сохранён в {file_path}"
            )
        )

    # ===== IMPORT =====

    def _import_departments(self, file_path: str) -> None:
        """Импортирует подразделения из Excel с обновлением и удалением лишних."""
        df = pd.read_excel(file_path)
        df = df.where(pd.notnull(df), None)

        required_columns = {"name", "short_name"}
        missing = required_columns - set(df.columns)
        if missing:
            raise CommandError(
                f"В файле '{file_path}' отсутствуют обязательные столбцы: {', '.join(sorted(missing))}"
            )

        with transaction.atomic():
            # Собираем имена подразделений из файла
            file_names: List[str] = []
            parent_map: Dict[str, Optional[str]] = {}

            created_count = 0
            updated_count = 0

            # Первый проход: создаём/обновляем без родителя
            for _, row in df.iterrows():
                name = str(row["name"]).strip()
                short_name = str(row["short_name"]).strip() if row["short_name"] else ""
                parent_name = (
                    str(row["parent_name"]).strip()
                    if "parent_name" in df.columns and row["parent_name"]
                    else None
                )

                can_save_value = False
                if (
                    "can_save_project_applications" in df.columns
                    and row["can_save_project_applications"] is not None
                ):
                    can_save_value = bool(row["can_save_project_applications"])

                file_names.append(name)
                parent_map[name] = parent_name

                dep, created = Department.objects.update_or_create(
                    name=name,
                    defaults={
                        "short_name": short_name,
                        "can_save_project_applications": can_save_value,
                        "parent": None,
                    },
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            # Второй проход: проставляем родительские подразделения
            deps_by_name: Dict[str, Department] = {
                d.name: d for d in Department.objects.all()
            }
            warnings: List[str] = []
            for name, parent_name in parent_map.items():
                if not parent_name:
                    continue
                dep = deps_by_name.get(name)
                parent = deps_by_name.get(parent_name)
                if not parent:
                    warnings.append(
                        f"Для подразделения '{name}' не найден родитель '{parent_name}'"
                    )
                    continue
                if dep.parent_id != parent.id:
                    dep.parent = parent
                    dep.save(update_fields=["parent"])

            # Удаляем подразделения, которых нет в файле
            existing_deps: Iterable[Department] = Department.objects.all()
            deleted_count = 0
            for dep in existing_deps:
                if dep.name not in file_names:
                    try:
                        dep.delete()
                        deleted_count += 1
                    except ProtectedError:
                        warnings.append(
                            f"Не удалось удалить подразделение '{dep.name}' из-за связанных объектов."
                        )

        for w in warnings:
            self.stdout.write(self.style.WARNING(w))

        self.stdout.write(
            self.style.SUCCESS(
                "Импорт подразделений завершён. "
                f"Создано: {created_count}, обновлено: {updated_count}, удалено: {deleted_count}."
            )
        )

    def _import_institutes(self, file_path: str) -> None:
        """Импортирует институты из Excel с обновлением и удалением лишних."""
        df = pd.read_excel(file_path)
        df = df.where(pd.notnull(df), None)

        required_columns = {"code", "name", "position"}
        missing = required_columns - set(df.columns)
        if missing:
            raise CommandError(
                f"В файле '{file_path}' отсутствуют обязательные столбцы: {', '.join(sorted(missing))}"
            )

        with transaction.atomic():
            file_codes: List[str] = []
            created_count = 0
            updated_count = 0

            for _, row in df.iterrows():
                code = str(row["code"]).strip()
                name = str(row["name"]).strip()
                position = int(row["position"])

                is_active = True
                if "is_active" in df.columns and row["is_active"] is not None:
                    is_active = bool(row["is_active"])

                department = None
                if "department_name" in df.columns and row["department_name"]:
                    dep_name = str(row["department_name"]).strip()
                    department = Department.objects.filter(name=dep_name).first()

                file_codes.append(code)

                inst, created = Institute.objects.update_or_create(
                    code=code,
                    defaults={
                        "name": name,
                        "position": position,
                        "is_active": is_active,
                        "department": department,
                    },
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            # Удаляем институты, которых нет в файле
            existing_institutes: Iterable[Institute] = Institute.objects.all()
            deleted_count = 0
            for inst in existing_institutes:
                if inst.code not in file_codes:
                    inst.delete()
                    deleted_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Импорт институтов завершён. "
                f"Создано: {created_count}, обновлено: {updated_count}, удалено: {deleted_count}."
            )
        )
