# Generated manually

from django.db import migrations, models
import django.db.models.deletion


def delete_all_comments(apps, schema_editor):
    """Удаляем все существующие комментарии"""
    ProjectApplicationComment = apps.get_model('showcase', 'ProjectApplicationComment')
    ProjectApplicationComment.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0012_projectapplicationstatuslog_action_type_and_more'),
    ]

    operations = [
        # Удаляем все комментарии
        migrations.RunPython(delete_all_comments, reverse_code=migrations.RunPython.noop),
        
        # Удаляем старый ForeignKey
        migrations.RemoveField(
            model_name='projectapplicationcomment',
            name='status_log',
        ),
        
        # Добавляем новый ForeignKey
        migrations.AddField(
            model_name='projectapplicationcomment',
            name='application',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='showcase.projectapplication',
                verbose_name='Заявка',
            ),
            preserve_default=False,
        ),
    ]

