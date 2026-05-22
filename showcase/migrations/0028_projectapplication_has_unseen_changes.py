from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0027_alter_tag_category_blank"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectapplication",
            name="has_unseen_changes",
            field=models.BooleanField(
                default=False,
                verbose_name="Есть изменения с последнего просмотра автором",
            ),
        ),
    ]
