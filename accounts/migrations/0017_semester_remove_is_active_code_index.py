from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0016_semester_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="semester",
            name="is_active",
        ),
        migrations.AlterField(
            model_name="semester",
            name="code",
            field=models.CharField(
                db_index=True,
                max_length=64,
                unique=True,
                verbose_name="Код",
            ),
        ),
    ]
