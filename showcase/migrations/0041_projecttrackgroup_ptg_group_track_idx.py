# Generated manually for student/mentor showcase group→tracks lookup.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0040_institute_semester_settings"),
        ("teams", "0021_studygroup_external_ids"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="projecttrackgroup",
            index=models.Index(
                fields=["study_group", "project_track"],
                name="ptg_group_track_idx",
            ),
        ),
    ]
