"""
Тесты для AuthorInvolvementTransition: добавление автора и его департамента
в причастные при базовых переходах.
"""

from showcase.services.status import StatusServiceFactory


def test_author_added_on_creation_transition(db, application, user_department_validator):
    manager = StatusServiceFactory.create_status_manager()
    manager.create_application_with_log(application, actor=user_department_validator)
    assert application.involved_users.filter(user=application.author).exists()


def test_author_added_on_created_to_created(db, application, user_department_validator, statuses):
    manager = StatusServiceFactory.create_status_manager()
    manager.change_status(application, statuses['created'], actor=user_department_validator)
    assert application.involved_users.filter(user=application.author).exists()


