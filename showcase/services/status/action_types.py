"""Типы действий с заявками."""

from enum import Enum


class RoleActionType(Enum):
    """Типы действий с заявками по ролям."""

    CREATE = "create"
    REJECT = "reject"
    APPROVE = "approve"
    REQUEST_REVISION = "request_revision"
