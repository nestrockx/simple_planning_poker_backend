"""
ASGI config for simple_planning_poker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

# from simple_planning_poker.middlewares.tokenauth import TokenAuthMiddleware
# from simple_planning_poker.middlewares.cookietokenauth import CookieTokenAuthMiddleware
from simple_planning_poker.middlewares.combinedtokenauth import CombinedTokenAuthMiddleware
from simple_planning_poker.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_planning_poker.settings")
django.setup()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": CombinedTokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
