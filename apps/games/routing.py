from django.urls import re_path
from importlib import import_module
GameConsumer = import_module('.consumers', package=__package__).GameConsumer

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<room_id>\d+)/$', GameConsumer.as_asgi()),
]