# Generated manually for showcase enroll count lookups.

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0022_backfill_team_semester_track"),
        ("accounts", "0020_user_mentor_fields"),
        ("showcase", "0040_institute_semester_settings"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="teamsemester",
            name="team_sem_enroll_lookup_idx",
        ),
        migrations.AddIndex(
            model_name="teamsemester",
            index=models.Index(
                fields=["semester", "project_track", "project_application"],
                name="team_sem_enroll_lookup_idx",
                condition=models.Q(project_application__isnull=False),
            ),
        ),
    ]
