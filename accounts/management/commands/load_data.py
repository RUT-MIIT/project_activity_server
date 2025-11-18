from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Загружает все необходимые справочники и данные (роли, статусы и т.д.)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Импорт ролей..."))
        try:
            call_command("import_roles")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка при импорте ролей: {e}"))
        self.stdout.write(self.style.MIGRATE_HEADING("Импорт статусов..."))

        try:
            call_command("import_statuses")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка при импорте статусов: {e}"))
        self.stdout.write(self.style.MIGRATE_HEADING("Импорт подразделений..."))

        try:
            call_command("import_departments")
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Ошибка при импорте подразделений: {e}")
            )

        self.stdout.write(self.style.SUCCESS("Импорт данных завершён!"))
