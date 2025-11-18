from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Синхронизация не требуется: roles хранятся в accounts.Role"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                "Команда более не требуется. Используйте импорт в accounts.Role."
            )
        )
