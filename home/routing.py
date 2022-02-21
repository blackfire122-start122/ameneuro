from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('chat/<str:room_name>', consumers.ChatConsumer.as_asgi(),name="ws_chat"),
    path('user/<str:room_name>', consumers.UserConsumer.as_asgi(),name="ws_user"),
]