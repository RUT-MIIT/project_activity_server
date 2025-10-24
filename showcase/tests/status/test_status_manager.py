"""
Тесты для StatusManager: создание лога при создании заявки, смена статуса,
пост-хук автоперехода и корректная работа без автоперехода при actor=None.
"""

from showcase.services.status import StatusServiceFactory


def test_create_application_log_from_none(db, application):
    manager = StatusServiceFactory.create_status_manager()
    _, log = manager.create_application_with_log(application, actor=application.author)
    assert log.from_status is None
    assert log.to_status == application.status


def test_change_status_produces_status_change_log(db, application, statuses, user_department_validator):
    manager = StatusServiceFactory.create_status_manager()
    manager.change_status(application, statuses['await_department'], actor=user_department_validator)
    application.refresh_from_db()
    assert application.status == statuses['await_department']
    status_logs = application.status_logs.filter(action_type='status_change')
    assert status_logs.count() >= 1


def test_post_hook_not_triggered_when_actor_is_none(db, application, statuses):
    manager = StatusServiceFactory.create_status_manager()
    # Принудительно ставим intermediate статус системным переводом
    manager.change_status(application, statuses['rejected_department'], actor=None)
    application.refresh_from_db()
    # Не должно быть автоперехода, т.к. actor=None
    assert application.status == statuses['rejected_department']


