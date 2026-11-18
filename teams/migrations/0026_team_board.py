from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("teams", "0025_team_semester_mentors_m2m")]

    operations = [
        migrations.CreateModel(
            name="TeamBoard",
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
                ("snapshot", models.JSONField()),
                (
                    "team",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name="board",
                        to="teams.teamsemester",
                    ),
                ),
            ],
        ),
    ]
