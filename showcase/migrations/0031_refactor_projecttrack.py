# Generated manually for ProjectTrack refactor

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


def clear_project_tracks(apps, schema_editor):
    """Удаляет все записи старой модели ProjectTrack перед рефакторингом."""
    ProjectTrack = apps.get_model("showcase", "ProjectTrack")
    ProjectTrack.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0018_registrationrequest_email_partial_unique"),
        ("showcase", "0030_projecttrack"),
        ("teams", "0005_studygroup_institute_fk"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(clear_project_tracks, migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name="projecttrack",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="projecttrack",
            name="study_group",
        ),
        migrations.RemoveField(
            model_name="projecttrack",
            name="project_application",
        ),
        migrations.AddField(
            model_name="projecttrack",
            name="name",
            field=models.CharField(default="", max_length=255, verbose_name="Название"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projecttrack",
            name="description",
            field=models.TextField(blank=True, default="", verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="projecttrack",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_tracks",
                to="accounts.department",
                verbose_name="Подразделение",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projecttrack",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="authored_project_tracks",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projecttrack",
            name="max_teams",
            field=models.PositiveIntegerField(
                default=100,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Максимум групп",
            ),
        ),
        migrations.AlterModelOptions(
            name="projecttrack",
            options={
                "ordering": ["semester", "name"],
                "verbose_name": "Проектный трек",
                "verbose_name_plural": "Проектные треки",
            },
        ),
        migrations.CreateModel(
            name="ProjectTrackGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "project_track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group_links",
                        to="showcase.projecttrack",
                        verbose_name="Проектный трек",
                    ),
                ),
                (
                    "study_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="track_group_links",
                        to="teams.studygroup",
                        verbose_name="Учебная группа",
                    ),
                ),
            ],
            options={
                "verbose_name": "Группа в проектном треке",
                "verbose_name_plural": "Группы в проектных треках",
                "ordering": ["project_track", "study_group__name"],
                "unique_together": {("project_track", "study_group")},
            },
        ),
        migrations.CreateModel(
            name="ProjectTrackApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "project_track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="application_links",
                        to="showcase.projecttrack",
                        verbose_name="Проектный трек",
                    ),
                ),
                (
                    "project_application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="track_application_links",
                        to="showcase.projectapplication",
                        verbose_name="Проектная заявка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка в проектном треке",
                "verbose_name_plural": "Заявки в проектных треках",
                "ordering": ["project_track", "project_application__title"],
                "unique_together": {("project_track", "project_application")},
            },
        ),
    ]
