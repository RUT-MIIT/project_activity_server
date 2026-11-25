import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


@pytest.mark.django_db(transaction=True)
def test_customer_type_migration_round_trip():
    executor = MigrationExecutor(connection)
    previous = [("showcase", "0042_project_application_kind")]
    current = [("showcase", "0043_projectapplication_customer_type")]
    try:
        executor.migrate(previous)
        old_model = executor.loader.project_state(previous).apps.get_model("showcase", "ProjectApplication")
        inner = old_model.objects.create(is_internal_customer=True)
        outer = old_model.objects.create(is_internal_customer=False)
        executor = MigrationExecutor(connection)
        executor.migrate(current)
        new_model = executor.loader.project_state(current).apps.get_model("showcase", "ProjectApplication")
        assert new_model.objects.get(pk=inner.pk).customer_type == "internal"
        assert new_model.objects.get(pk=outer.pk).customer_type == "external"
        new_model.objects.filter(pk=outer.pk).update(customer_type="representative")
        executor = MigrationExecutor(connection)
        executor.migrate(previous)
        old_model = executor.loader.project_state(previous).apps.get_model("showcase", "ProjectApplication")
        assert old_model.objects.get(pk=inner.pk).is_internal_customer is True
        assert old_model.objects.get(pk=outer.pk).is_internal_customer is False
    finally:
        MigrationExecutor(connection).migrate(current)
