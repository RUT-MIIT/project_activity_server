from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0019_projectapplication_main_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectapplication",
            name="is_external",
            field=models.BooleanField(default=False, verbose_name="Внешняя заявка"),
        ),
    ]
