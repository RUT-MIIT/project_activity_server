from django.core.management.base import BaseCommand
from accounts.models import Department
import pandas as pd


class Command(BaseCommand):
    help = 'Импортирует подразделения из xlsx-файла (pandas, путь в коде).'

    def handle(self, *args, **options):
        filepath = 'accounts/management/commands/departments.xlsx'
        df = pd.read_excel(filepath)
        dep_cache = {}
        for _, row in df.iterrows():
            name = row['Название подразделения']
            short_name = row['Краткое название']
            parent_name = row['Родительское подразделение']
            parent = None
            if pd.notna(parent_name) and parent_name:
                parent = dep_cache.get(parent_name) or Department.objects.filter(
                    name=parent_name
                ).first()
            dep, created = Department.objects.get_or_create(
                name=name,
                defaults={
                    'short_name': short_name,
                    'parent': parent
                }
            )
            if not created:
                dep.short_name = short_name
                dep.parent = parent
                dep.save()
            dep_cache[name] = dep
        self.stdout.write(self.style.SUCCESS('Импорт подразделений завершён.'))
