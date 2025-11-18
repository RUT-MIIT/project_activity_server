import os

from django.core.management.base import BaseCommand
import pandas as pd

from accounts.models import Role


class Command(BaseCommand):
    help = "Импорт ролей из Excel-файла roles.xlsx (рядом с этим файлом)"

    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(__file__), "roles.xlsx")
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"Файл {file_path} не найден."))
            return
        df = pd.read_excel(file_path)
        count = 0
        for _, row in df.iterrows():
            code = str(row["code"]).strip()
            name = str(row["name"]).strip()
            obj, created = Role.objects.update_or_create(
                code=code, defaults={"name": name}
            )
            count += 1
            self.stdout.write(f"{'Создана' if created else 'Обновлена'} роль: {obj}")
        self.stdout.write(self.style.SUCCESS(f"Импортировано ролей: {count}"))
