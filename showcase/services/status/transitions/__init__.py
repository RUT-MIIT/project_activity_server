"""
Конкретные реализации переходов между статусами.

Каждый переход реализует специфическую бизнес-логику
для определенных пар статусов.
"""

from .base import BaseStatusTransition
from .author_involvement import AuthorInvolvementTransition

__all__ = [
    'BaseStatusTransition',
    'AuthorInvolvementTransition',
]

