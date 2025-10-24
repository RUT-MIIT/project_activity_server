import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    # Автоматически включаем доступ к базе для всех тестов pytest
    pass


