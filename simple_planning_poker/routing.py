from django.urls import re_path
from simple_planning_poker.consumers.participants import ParticipantsConsumer
from simple_planning_poker.consumers.revealvotes import RevealVotesConsumer
from simple_planning_poker.consumers.vote import VoteConsumer

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_code>\w+)/$', VoteConsumer.as_asgi()),
    re_path(r'ws/reveal/(?P<room_code>\w+)/$', RevealVotesConsumer.as_asgi()),
    re_path(r'ws/participant/(?P<room_code>\w+)/$', ParticipantsConsumer.as_asgi()),
]