import os

from django.core.management.base import BaseCommand
from django.db import transaction
import pandas as pd

from showcase.models import Tag


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
                # Создаем или обновляем записи
                created_count = 0
                updated_count = 0
                for _, row in df.iterrows():
                    tag, created = Tag.objects.get_or_create(
                        name=row["name"],
                        defaults={
                            "category": row["category"],
                        },
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(f"Создан тег: {tag}")
                    else:
                        # Обновляем категорию, если она изменилась
                        if tag.category != row["category"]:
                            tag.category = row["category"]
                            tag.save()
                            updated_count += 1
                            self.stdout.write(f"Обновлен тег: {tag}")

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Импорт завершен. Создано {created_count} тегов, "
                        f"обновлено {updated_count} тегов."
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при импорте: {str(e)}"))
