from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0022_preregistration_generalize"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserWithEmailProvision",
            fields=[],
            options={
                "verbose_name": "Создать пользователя (с письмом)",
                "verbose_name_plural": "Создать пользователя (с письмом)",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("accounts.user",),
        ),
    ]
