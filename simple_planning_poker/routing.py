from django.urls import re_path
from simple_planning_poker.consumers.revealvotes import RevealVotesConsumer

websocket_urlpatterns = [
    re_path(r'ws/reveal/(?P<room_code>\w+)/$', RevealVotesConsumer.as_asgi()),
]