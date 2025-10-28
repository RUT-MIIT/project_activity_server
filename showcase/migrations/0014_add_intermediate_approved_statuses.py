# Generated migration to add intermediate approved statuses

from django.db import migrations


def add_intermediate_approved_statuses(apps, schema_editor):
    """
    Добавляет промежуточные статусы одобрения в БД.
    """
    ApplicationStatus = apps.get_model('showcase', 'ApplicationStatus')
    
    # Определяем новые статусы с их позициями
    new_statuses = [
        {
            'code': 'approved_department',
            'name': 'Одобрено подразделением',
            'position': 25,
            'is_active': True
        },
        {
            'code': 'approved_institute',
            'name': 'Одобрено институтом',
            'position': 26,
            'is_active': True
        },
    ]
    
    for status_data in new_statuses:
        ApplicationStatus.objects.update_or_create(
            code=status_data['code'],
            defaults=status_data
        )
        print(f"Created/updated status: {status_data['code']}")


def remove_intermediate_approved_statuses(apps, schema_editor):
    """
    Удаляет промежуточные статусы одобрения из БД.
    """
    ApplicationStatus = apps.get_model('showcase', 'ApplicationStatus')
    
    codes_to_remove = ['approved_department', 'approved_institute']
    
    for code in codes_to_remove:
        ApplicationStatus.objects.filter(code=code).delete()
        print(f"Removed status: {code}")


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0013_refactor_comments'),
    ]

    operations = [
        migrations.RunPython(add_intermediate_approved_statuses, remove_intermediate_approved_statuses),
    ]

