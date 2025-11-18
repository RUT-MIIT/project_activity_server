import os

from django.core.management.base import BaseCommand
import pandas as pd

from showcase.models import ApplicationStatus


class Command(BaseCommand):
    help = "Импорт статусов заявок из Excel-файла statuses.xlsx (рядом с этим файлом)"

    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(__file__), "statuses.xlsx")
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"Файл {file_path} не найден."))
            return
        df = pd.read_excel(file_path)
        count = 0
        for _, row in df.iterrows():
            code = str(row["code"]).strip()
            name = str(row["name"]).strip()
            position = int(row["position"])
            is_active = bool(row["is_active"])
            obj, created = ApplicationStatus.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "position": position,
                    "is_active": is_active,
                },
            )
            count += 1
            self.stdout.write(f"{'Создан' if created else 'Обновлён'}: {obj}")
        self.stdout.write(self.style.SUCCESS(f"Импортировано статусов: {count}"))
