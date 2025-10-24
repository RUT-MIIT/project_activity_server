import pytest
from django.contrib.auth import get_user_model

from showcase.models import ApplicationStatus, ProjectApplication, Institute
from accounts.models import Role
from showcase.services.status import StatusServiceFactory
from showcase.services.status.role_actions import RoleActionType


User = get_user_model()


@pytest.fixture
def statuses(db):
    created, _ = ApplicationStatus.objects.get_or_create(
        code='created', defaults={'name': 'Создана', 'position': 1, 'is_active': True}
    )
    rejected, _ = ApplicationStatus.objects.get_or_create(
        code='rejected', defaults={'name': 'Отклонена', 'position': 99, 'is_active': True}
    )
    rejected_dept, _ = ApplicationStatus.objects.get_or_create(
        code='rejected_department', defaults={'name': 'Отклонена департаментом', 'position': 50, 'is_active': True}
    )
    rejected_inst, _ = ApplicationStatus.objects.get_or_create(
        code='rejected_institute', defaults={'name': 'Отклонена институтом', 'position': 51, 'is_active': True}
    )
    rejected_cpds, _ = ApplicationStatus.objects.get_or_create(
        code='rejected_cpds', defaults={'name': 'Отклонена ЦПДС', 'position': 52, 'is_active': True}
    )
    await_dept, _ = ApplicationStatus.objects.get_or_create(
        code='await_department', defaults={'name': 'Ожидает департамент', 'position': 10, 'is_active': True}
    )
    await_inst, _ = ApplicationStatus.objects.get_or_create(
        code='await_institute', defaults={'name': 'Ожидает институт', 'position': 20, 'is_active': True}
    )
    await_cpds, _ = ApplicationStatus.objects.get_or_create(
        code='await_cpds', defaults={'name': 'Ожидает ЦПДС', 'position': 30, 'is_active': True}
    )
    return {
        'created': created,
        'rejected': rejected,
        'rejected_department': rejected_dept,
        'rejected_institute': rejected_inst,
        'rejected_cpds': rejected_cpds,
        'await_department': await_dept,
        'await_institute': await_inst,
        'await_cpds': await_cpds,
    }


@pytest.fixture
def institute(db):
    inst, _ = Institute.objects.get_or_create(
        code='ti',
        defaults={
            'name': 'Тестовый институт',
            'position': 1,
            'is_active': True,
        }
    )
    return inst


@pytest.fixture
def user_department_validator(db):
    role, _ = Role.objects.get_or_create(code='department_validator', defaults={'name': 'Валидатор департамента', 'is_active': True})
    user, _ = User.objects.get_or_create(email='dept@test.local', defaults={'first_name': 'Dept', 'last_name': 'Validator'})
    user.role = role
    user.save()
    return user


@pytest.fixture
def user_institute_validator(db):
    role, _ = Role.objects.get_or_create(code='institute_validator', defaults={'name': 'Валидатор института', 'is_active': True})
    user, _ = User.objects.get_or_create(email='inst@test.local', defaults={'first_name': 'Inst', 'last_name': 'Validator'})
    user.role = role
    user.save()
    return user


@pytest.fixture
def application(db, statuses, institute, user_department_validator):
    app = ProjectApplication.objects.create(
        author=user_department_validator,
        status=statuses['created'],
        author_firstname='Имя',
        author_lastname='Фамилия',
        author_email='a@b.c',
        author_phone='+100000000',
        company='Компания',
        company_contacts='contact@company',
    )
    app.target_institutes.add(institute)
    return app


def test_creation_log_has_from_none(db, application):
    manager = StatusServiceFactory.create_status_manager()
    _, log = manager.create_application_with_log(application, actor=application.author)
    assert log.from_status is None
    assert log.to_status == application.status


@pytest.mark.parametrize('intermediate_code', [
    'rejected_department', 'rejected_institute', 'rejected_cpds'
])
def test_auto_transition_to_rejected(db, application, statuses, user_department_validator, intermediate_code):
    manager = StatusServiceFactory.create_status_manager()
    # первый переход пользователем в промежуточный статус
    manager.change_status(
        application=application,
        new_status=statuses[intermediate_code],
        actor=user_department_validator,
        comments=[{'field': 'reason', 'text': 'Причина'}]
    )

    application.refresh_from_db()
    # должен произойти автопереход во второй лог
    assert application.status == statuses['rejected']
    logs = list(application.status_logs.filter(action_type='status_change'))
    assert len(logs) == 2
    # второй лог — системный
    assert logs[0].actor is None
    assert logs[0].to_status == statuses['rejected']
    # первый лог — пользовательский
    assert logs[1].actor == user_department_validator
    assert logs[1].to_status == statuses[intermediate_code]


def test_no_auto_transition_when_no_rule(db, application, statuses, user_department_validator):
    manager = StatusServiceFactory.create_status_manager()
    # используем статус без правила
    manager.change_status(
        application=application,
        new_status=statuses['await_department'],
        actor=user_department_validator,
    )
    application.refresh_from_db()
    assert application.status == statuses['await_department']
    logs = list(application.status_logs.filter(action_type='status_change'))
    assert len(logs) == 1


def test_role_reject_writes_all_comments(db, application, user_department_validator):
    service = StatusServiceFactory.create_role_status_service()
    new_status = service.apply_action_by_role(
        RoleActionType.REJECT,
        application,
        user_department_validator,
        reason='Неверно',
        comments=[{'field': 'stakeholders', 'text': 'Ошибка'}, {'field': 'recommended_tools', 'text': 'Не то'}]
    )
    assert new_status is not None
    # После применения REJECT у department_validator произойдёт автопереход → rejected
    application.refresh_from_db()
    logs = list(application.status_logs.filter(action_type='status_change'))
    assert len(logs) == 2
    # Проверим, что первый лог содержит все комментарии
    user_log = logs[1]
    fields = {c.field for c in user_log.comments.all()}
    assert {'rejection_reason', 'stakeholders', 'recommended_tools'} <= fields


