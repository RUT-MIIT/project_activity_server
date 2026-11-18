"""ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_application = get_asgi_application()

# Consumers import Django models, so initialize Django first.
from teams.board_consumer import TeamBoardConsumer  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": OriginValidator(
            URLRouter(
                [path("ws/teams/<int:team_id>/board/", TeamBoardConsumer.as_asgi())]
            ),
            settings.BOARD_ALLOWED_ORIGINS,
        ),
    }
)
