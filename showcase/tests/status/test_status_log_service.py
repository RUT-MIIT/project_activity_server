"""
Тесты для StatusLogService: корректная установка from_status при создании
и добавление массива комментариев, а также previous_status_log.
"""

from showcase.services.status import StatusServiceFactory


def test_create_log_sets_from_status_none_on_creation(db, application):
    manager = StatusServiceFactory.create_status_manager()
    _, log = manager.create_application_with_log(application, actor=application.author)
    assert log.from_status is None
    assert log.to_status == application.status


def test_previous_status_log_linked(db, application, statuses, user_department_validator):
    manager = StatusServiceFactory.create_status_manager()
    manager.create_application_with_log(application, actor=user_department_validator)
    manager.change_status(
        application,
        statuses['await_department'],
        actor=user_department_validator,
        comments=[{'field': 'note', 'text': 'Комментарий'}]
    )
    logs = list(application.status_logs.filter(action_type='status_change').order_by('-changed_at'))
    assert len(logs) >= 2
    assert logs[0].previous_status_log is not None
    assert logs[0].previous_status_log.application_id == application.id
    # проверим, что комментарий записан
    comment_fields = {c.field for c in logs[1].comments.all()} | {c.field for c in logs[0].comments.all()}
    assert 'note' in comment_fields

