from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0014_semester"),
        ("showcase", "0021_projectapplication_is_internal_customer"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectapplication",
            name="semester",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="project_applications",
                to="accounts.semester",
                verbose_name="Семестр",
            ),
        ),
    ]
