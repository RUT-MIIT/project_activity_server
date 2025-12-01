from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_registrationrequest_role"),
        ("showcase", "0017_tag_projectapplication_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="institute",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="institutes",
                to="accounts.department",
                verbose_name="Связанное подразделение",
            ),
        ),
    ]
