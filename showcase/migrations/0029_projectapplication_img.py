from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0028_projectapplication_has_unseen_changes"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectapplication",
            name="img",
            field=models.CharField(
                blank=True,
                default="",
                max_length=512,
                null=True,
                verbose_name="Изображение",
            ),
        ),
    ]
