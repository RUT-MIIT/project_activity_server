"""
Тесты для AutoTransitionService: применение правил rejected_* → rejected,
запись системного лога и комментария, отсутствие срабатывания без правила.
"""

from showcase.services.status import StatusServiceFactory


def test_auto_transition_applies_rule(db, application, statuses, user_department_validator):
    manager = StatusServiceFactory.create_status_manager()
    manager.change_status(application, statuses['rejected_institute'], actor=user_department_validator)
    application.refresh_from_db()
    assert application.status == statuses['rejected']
    logs = list(application.status_logs.filter(action_type='status_change'))
    assert len(logs) == 2
    assert logs[0].actor is None
    assert logs[0].comments.filter(field='auto_transition').exists()


def test_no_auto_when_actor_none(db, application, statuses):
    manager = StatusServiceFactory.create_status_manager()
    manager.change_status(application, statuses['rejected_institute'], actor=None)
    application.refresh_from_db()
    assert application.status == statuses['rejected_institute']


