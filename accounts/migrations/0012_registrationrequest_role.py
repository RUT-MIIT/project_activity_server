from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_role_options_role_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationrequest',
            name='role',
            field=models.ForeignKey(
                to='accounts.role',
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name='registration_requests',
                verbose_name='Роль (назначенная при одобрении)',
            ),
        ),
    ]
