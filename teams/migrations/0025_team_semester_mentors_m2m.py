"""M2M-наставники у TeamSemester + перенос из одиночного FK mentor."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def copy_mentor_fk_to_m2m(apps, schema_editor):
    TeamSemester = apps.get_model("teams", "TeamSemester")
    for enrollment in TeamSemester.objects.exclude(mentor_id=None).iterator():
        enrollment.mentors.add(enrollment.mentor_id)


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0024_admin_mixed_team_create_proxy"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="teamsemester",
            name="mentors",
            field=models.ManyToManyField(
                blank=True,
                help_text="Несколько наставников команды в семестре.",
                limit_choices_to={"role__code": "mentor"},
                related_name="mentored_team_semesters_m2m",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Наставники",
            ),
        ),
        migrations.RunPython(copy_mentor_fk_to_m2m, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="teamsemester",
            name="mentor",
            field=models.ForeignKey(
                blank=True,
                help_text="Денормализация для API: первый из списка наставников.",
                limit_choices_to={"role__code": "mentor"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="mentored_team_semesters",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Наставник (основной)",
            ),
        ),
    ]
