from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0033_alter_recommended_teams_count_default"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="projecttrack",
            name="max_teams",
        ),
    ]
