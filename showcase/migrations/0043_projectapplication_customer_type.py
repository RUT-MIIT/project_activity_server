from django.db import migrations, models


def forwards(apps, schema_editor):
    application = apps.get_model("showcase", "ProjectApplication")
    application.objects.using(schema_editor.connection.alias).filter(
        is_internal_customer=True
    ).update(customer_type="internal")


def backwards(apps, schema_editor):
    application = apps.get_model("showcase", "ProjectApplication")
    application.objects.using(schema_editor.connection.alias).filter(
        customer_type="internal"
    ).update(is_internal_customer=True)


class Migration(migrations.Migration):
    dependencies = [("showcase", "0042_project_application_kind")]

    operations = [
        migrations.AddField(
            model_name="projectapplication",
            name="customer_type",
            field=models.CharField(choices=[("internal", "Внутренний"), ("representative", "Через представителя"), ("external", "Внешний")], default="external", max_length=14, verbose_name="Тип заказчика"),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(model_name="projectapplication", name="is_internal_customer"),
    ]
