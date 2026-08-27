"""Добавить min/max количества участников команды в проектный трек."""

from django.core.validators import MinValueValidator
from django.db import migrations, models


def backfill_track_limits_from_applications(apps, schema_editor):
    """Проставляет лимиты трека из первой связанной заявки."""
    ProjectTrack = apps.get_model("showcase", "ProjectTrack")
    for track in ProjectTrack.objects.all().iterator():
        link = (
            track.application_links.select_related("project_application")
            .order_by("id")
            .first()
        )
        if link is None:
            continue
        application = link.project_application
        ProjectTrack.objects.filter(pk=track.pk).update(
            min_team_members=application.min_team_members,
            max_team_members=application.max_team_members,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0035_projectapplication_team_member_limits"),
    ]

    operations = [
        migrations.AddField(
            model_name="projecttrack",
            name="min_team_members",
            field=models.PositiveIntegerField(
                default=1,
                validators=[MinValueValidator(1)],
                verbose_name="Минимальное количество человек в команде",
            ),
        ),
        migrations.AddField(
            model_name="projecttrack",
            name="max_team_members",
            field=models.PositiveIntegerField(
                default=10,
                validators=[MinValueValidator(1)],
                verbose_name="Максимальное количество человек в команде",
            ),
        ),
        migrations.RunPython(
            backfill_track_limits_from_applications,
            migrations.RunPython.noop,
        ),
    ]
