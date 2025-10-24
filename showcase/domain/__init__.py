"""
Domain слой - чистая бизнес-логика без побочных эффектов.

Этот слой содержит только чистые функции и бизнес-правила.
Никаких обращений к БД, HTTP, файлам или другим эффектам.
"""

from .application import ProjectApplicationDomain
from .capabilities import ApplicationCapabilities

__all__ = [
    'ProjectApplicationDomain',
    'ApplicationCapabilities',
]
