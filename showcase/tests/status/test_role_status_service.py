"""
Тесты для RoleStatusService: применение универсального метода действий по роли
для CREATE и REJECT, генерация комментариев и совместимость с автопереходом.
"""

from showcase.services.status import StatusServiceFactory
from showcase.services.status.role_actions import RoleActionType


def test_create_action_mentor_moves_to_await_department(db, application, statuses, user_mentor):
    service = StatusServiceFactory.create_role_status_service()
    new_status = service.apply_action_by_role(
        RoleActionType.CREATE,
        application,
        user_mentor,
    )
    assert new_status is not None
    application.refresh_from_db()
    assert application.status.code in {'await_department', 'created'}


def test_reject_department_validator_writes_all_comments_and_autotransitions(db, application, statuses, user_department_validator):
    service = StatusServiceFactory.create_role_status_service()
    new_status = service.apply_action_by_role(
        RoleActionType.REJECT,
        application,
        user_department_validator,
        reason='Причина',
        comments=[{'field': 'stakeholders', 'text': 'Ошибка'}]
    )
    assert new_status is not None
    application.refresh_from_db()
    logs = list(application.status_logs.filter(action_type='status_change'))
    assert len(logs) == 2
    user_log = logs[1]
    fields = {c.field for c in user_log.comments.all()}
    assert {'rejection_reason', 'stakeholders'} <= fields


