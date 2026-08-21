"""Добавить min/max количества участников команды в заявку."""

from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0034_remove_projecttrack_max_teams"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectapplication",
            name="min_team_members",
            field=models.PositiveIntegerField(
                default=1,
                validators=[MinValueValidator(1)],
                verbose_name="Минимальное количество человек в команде",
            ),
        ),
        migrations.AddField(
            model_name="projectapplication",
            name="max_team_members",
            field=models.PositiveIntegerField(
                default=10,
                validators=[MinValueValidator(1)],
                verbose_name="Максимальное количество человек в команде",
            ),
        ),
    ]
