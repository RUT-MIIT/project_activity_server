import os

from django.core.management.base import BaseCommand
from django.db import connection, transaction
import pandas as pd

from accounts.models import Department
from showcase.models import ProjectApplication, Tag


class Command(BaseCommand):
    help = "Импорт справочника тегов из CSV файла"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="tags.csv",
            help="Путь к CSV файлу с данными тегов",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        # Если путь относительный, ищем файл в папке commands
        if not os.path.isabs(file_path):
            commands_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(commands_dir, file_path)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Файл {file_path} не найден"))
            return

        try:
            # Читаем CSV файл
            df = pd.read_csv(file_path)

            with transaction.atomic():
                # Очищаем все связи тегов с проектными заявками
                self.stdout.write("Отцепление тегов от проектных заявок...")
                ProjectApplication.tags.through.objects.all().delete()

                # Удаляем все теги
                deleted_count = Tag.objects.count()
                Tag.objects.all().delete()
                self.stdout.write(f"Удалено {deleted_count} тегов")

                # Сбрасываем счетчик ID
                self._reset_id_sequence()

                # Создаем новые записи
                created_count = 0
                updated_count = 0
                for _, row in df.iterrows():
                    # Обработка departments (может быть ID или название)
                    departments = []
                    if "department" in row and pd.notna(row["department"]):
                        department_value = row["department"]
                        # Пытаемся найти по ID (если это число)
                        department = None
                        try:
                            department_id = int(department_value)
                            department = Department.objects.filter(
                                pk=department_id
                            ).first()
                        except (ValueError, TypeError):
                            pass

                        # Если не нашли по ID, ищем по названию
                        if department is None:
                            department = Department.objects.filter(
                                name=department_value
                            ).first()

                        if department is None:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Подразделение '{department_value}' не найдено для тега '{row['name']}'"
                                )
                            )
                        else:
                            departments = [department]

                    # Создаем новый тег (все теги были удалены, поэтому всегда создаем новый)
                    tag = Tag.objects.create(
                        name=row["name"],
                        category=row["category"],
                        is_base=True,
                    )
                    if departments:
                        tag.departments.set(departments)
                    created_count += 1
                    self.stdout.write(f"Создан тег: {tag}")

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Импорт завершен. Создано {created_count} тегов, "
                        f"обновлено {updated_count} тегов."
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при импорте: {str(e)}"))

    def _reset_id_sequence(self):
        """Сбрасывает счетчик ID для таблицы тегов."""
        db_backend = connection.vendor

        with connection.cursor() as cursor:
            if db_backend == "postgresql":
                cursor.execute(
                    "SELECT setval(pg_get_serial_sequence('showcase_tag', 'id'), 1, false);"
                )
            elif db_backend == "sqlite":
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='showcase_tag';")
            elif db_backend == "mysql":
                cursor.execute("ALTER TABLE showcase_tag AUTO_INCREMENT = 1;")
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Неизвестный тип БД: {db_backend}. "
                        "Счетчик ID не был сброшен автоматически."
                    )
                )
                return

        self.stdout.write("Счетчик ID сброшен")
