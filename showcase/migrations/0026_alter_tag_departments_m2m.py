# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_semester'),
        ('showcase', '0025_alter_tag_unique_name_department'),
    ]

    operations = [
        # Добавляем поле is_base
        migrations.AddField(
            model_name='tag',
            name='is_base',
            field=models.BooleanField(default=False, verbose_name='Базовый тег'),
        ),
        # Удаляем unique_together constraint
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set(),
        ),
        # Удаляем ForeignKey department
        migrations.RemoveField(
            model_name='tag',
            name='department',
        ),
        # Добавляем ManyToManyField departments
        migrations.AddField(
            model_name='tag',
            name='departments',
            field=models.ManyToManyField(
                blank=True,
                related_name='tags',
                to='accounts.department',
                verbose_name='Подразделения',
            ),
        ),
    ]
