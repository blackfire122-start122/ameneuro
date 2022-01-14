from django.urls import path
from . import views

urlpatterns = [
    path('add_friend', views.add_friend_ajax, name='add_friend_ajax'),
    path('want_add_friend', views.want_add_friend_ajax, name='want_add_friend_ajax'),
    path('add_chat', views.add_chat_ajax, name='add_chat_ajax'),
    path('like', views.like_ajax, name='like_ajax'),
]