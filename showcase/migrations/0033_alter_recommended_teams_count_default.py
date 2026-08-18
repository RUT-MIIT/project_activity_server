"""Установить recommended_teams_count=3 для существующих заявок и default=3."""

import django.core.validators
from django.db import migrations, models


def set_recommended_teams_count_to_three(apps, schema_editor):
    """Проставляет 3 для всех существующих проектных заявок."""
    ProjectApplication = apps.get_model("showcase", "ProjectApplication")
    ProjectApplication.objects.all().update(recommended_teams_count=3)


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0032_projectapplication_track_fields"),
    ]

    operations = [
        migrations.RunPython(
            set_recommended_teams_count_to_three,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="projectapplication",
            name="recommended_teams_count",
            field=models.PositiveIntegerField(
                default=3,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Рекомендуемое количество команд",
            ),
        ),
    ]
