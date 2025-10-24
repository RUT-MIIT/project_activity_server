from django.core.management.base import BaseCommand
from django.db import transaction
from showcase.models import Institute
import pandas as pd
import os


class Command(BaseCommand):
    help = 'Импорт справочника институтов из Excel файла'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='institutes.csv',
            help='Путь к CSV файлу с данными институтов'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        # Если путь относительный, ищем файл в папке commands
        if not os.path.isabs(file_path):
            commands_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(commands_dir, file_path)
        
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'Файл {file_path} не найден')
            )
            return
        
        try:
            # Читаем CSV файл
            df = pd.read_csv(file_path)
            
            with transaction.atomic():
                # Очищаем существующие данные
                Institute.objects.all().delete()
                
                # Создаем новые записи
                created_count = 0
                for _, row in df.iterrows():
                    institute, created = Institute.objects.get_or_create(
                        code=row['code'],
                        defaults={
                            'name': row['name'],
                            'position': int(row['position']),
                            'is_active': True
                        }
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(f'Создан институт: {institute}')
                    else:
                        self.stdout.write(f'Институт уже существует: {institute}')
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Импорт завершен. Создано {created_count} институтов.'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте: {str(e)}')
            )
