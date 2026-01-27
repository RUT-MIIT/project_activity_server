from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0026_alter_tag_departments_m2m"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="category",
            field=models.CharField(
                max_length=255,
                blank=True,
                default="",
                verbose_name="Категория тега",
            ),
        ),
    ]
