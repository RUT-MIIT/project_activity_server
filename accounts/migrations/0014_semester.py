from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0013_department_can_save_project_applications"),
    ]

    operations = [
        migrations.CreateModel(
            name="Semester",
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
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название семестра"),
                ),
                (
                    "position",
                    models.PositiveIntegerField(verbose_name="Позиция для сортировки"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активен"),
                ),
            ],
            options={
                "verbose_name": "Семестр",
                "verbose_name_plural": "Семестры",
                "ordering": ["position"],
            },
        ),
    ]
