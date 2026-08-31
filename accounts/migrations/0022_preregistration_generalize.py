# Generated manually for preregistration generalization

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0021_user_placeholder_preregistered_flag"),
        ("teams", "0008_studygroup_profile_form"),
    ]

    operations = [
        migrations.AddField(
            model_name="preregisteredstudent",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pre_registrations",
                to="accounts.department",
                verbose_name="Подразделение",
            ),
        ),
        migrations.AddField(
            model_name="preregisteredstudent",
            name="role",
            field=models.ForeignKey(
                db_index=True,
                default="student",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pre_registrations",
                to="accounts.role",
                verbose_name="Роль",
            ),
        ),
        migrations.AlterField(
            model_name="preregisteredstudent",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pre_registered_students",
                to="teams.studygroup",
                verbose_name="Учебная группа",
            ),
        ),
        migrations.AlterField(
            model_name="preregisteredstudent",
            name="student_card",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                max_length=32,
                verbose_name="Студенческий билет",
            ),
        ),
        migrations.RenameField(
            model_name="preregisteredstudent",
            old_name="student",
            new_name="user",
        ),
        migrations.AlterModelOptions(
            name="preregisteredstudent",
            options={
                "ordering": ("last_name", "first_name"),
                "verbose_name": "Предрегистрация",
                "verbose_name_plural": "Предрегистрации",
            },
        ),
        migrations.RemoveConstraint(
            model_name="preregisteredstudent",
            name="unique_preregistered_student_snils",
        ),
        migrations.AddConstraint(
            model_name="preregisteredstudent",
            constraint=models.UniqueConstraint(
                condition=models.Q(("snils", ""), _negated=True),
                fields=("snils",),
                name="unique_preregistered_student_snils",
            ),
        ),
        migrations.AddConstraint(
            model_name="preregisteredstudent",
            constraint=models.UniqueConstraint(
                condition=models.Q(("student_card", ""), _negated=True),
                fields=("student_card",),
                name="unique_preregistered_student_card",
            ),
        ),
    ]
