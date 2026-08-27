"""Денормализация суммы recommended_teams_count на ProjectTrack."""

from django.db import migrations, models
from django.db.models import Sum
from django.db.models.functions import Coalesce


def backfill_track_recommended_teams_count(apps, schema_editor):
    """Проставляет сумму recommended_teams_count из связанных заявок."""
    ProjectTrack = apps.get_model("showcase", "ProjectTrack")
    ProjectTrackApplication = apps.get_model("showcase", "ProjectTrackApplication")

    for track in ProjectTrack.objects.all().iterator():
        total = (
            ProjectTrackApplication.objects.filter(project_track_id=track.pk)
            .aggregate(
                total=Coalesce(
                    Sum("project_application__recommended_teams_count"),
                    0,
                )
            )
            .get("total")
            or 0
        )
        ProjectTrack.objects.filter(pk=track.pk).update(recommended_teams_count=total)


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0036_projecttrack_team_member_limits"),
    ]

    operations = [
        migrations.AddField(
            model_name="projecttrack",
            name="recommended_teams_count",
            field=models.PositiveIntegerField(
                default=0,
                help_text=(
                    "Денормализованная сумма ProjectApplication.recommended_teams_count "
                    "по заявкам трека. Пересчитывается при изменении состава заявок."
                ),
                verbose_name="Сумма рекомендуемых команд по заявкам трека",
            ),
        ),
        migrations.RunPython(
            backfill_track_recommended_teams_count,
            migrations.RunPython.noop,
        ),
    ]
