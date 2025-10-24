"""
Тесты для StatusTransitionService и реестра: регистрация/вызов стратегий
и применение AuthorInvolvementTransition при базовых переходах.
"""

from showcase.services.status import StatusServiceFactory


def test_registry_executes_registered_transition(db, application, statuses, user_department_validator):
    manager = StatusServiceFactory.create_status_manager()
    # При переходе created->created должен сработать AuthorInvolvementTransition
    manager.change_status(application, statuses['created'], actor=user_department_validator)
    # Автор должен быть добавлен в причастные
    assert application.involved_users.filter(user=application.author).exists()


def test_author_involvement_on_creation(db, application, user_department_validator):
    manager = StatusServiceFactory.create_status_manager()
    manager.create_application_with_log(application, actor=user_department_validator)
    # Автор и департамент должны появиться среди причастных
    assert application.involved_users.filter(user=application.author).exists()


