from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("teams", "0026_team_board")]

    operations = [
        migrations.AddField(
            model_name="teamboard",
            name="revision",
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
