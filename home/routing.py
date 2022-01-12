from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('<str:room_name>', consumers.ChatConsumer.as_asgi()),
]