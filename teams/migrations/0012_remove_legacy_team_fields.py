# Remove legacy Team.leader, Team.project_application and TeamMember.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0011_migrate_team_data"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="teammember",
            name="unique_team_member",
        ),
        migrations.DeleteModel(
            name="TeamMember",
        ),
        migrations.RemoveField(
            model_name="team",
            name="leader",
        ),
        migrations.RemoveField(
            model_name="team",
            name="project_application",
        ),
    ]
