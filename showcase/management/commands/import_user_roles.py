import os

from django.core.management.base import BaseCommand
from django.db import transaction
import pandas as pd

from accounts.models import Role as AccountRole


class Command(BaseCommand):
    help = "Импорт справочника ролей пользователей из Excel файла"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="user_roles.csv",
            help="Путь к CSV файлу с данными ролей пользователей",
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
                # Очищаем существующие данные в accounts.Role
                AccountRole.objects.all().delete()

                # Создаем новые записи
                created_count = 0
                for _, row in df.iterrows():
                    account_role, created = AccountRole.objects.get_or_create(
                        code=row["code"],
                        defaults={
                            "name": row["name"],
                            "requires_department": bool(row["requires_department"]),
                            "is_active": True,
                        },
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(f"Создана роль: {account_role}")
                    else:
                        self.stdout.write(f"Роль уже существует: {account_role}")

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Импорт завершен. Создано {created_count} ролей."
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при импорте: {str(e)}"))
