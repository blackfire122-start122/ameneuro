from django.urls import path
from . import views
# from . import ajax_views

urlpatterns = [
    path('add_friend', views.add_friend_ajax, name='add_friend_ajax'),
    path('follow', views.follow_ajax, name='follow_ajax'),
    path('want_add_friend', views.want_add_friend_ajax, name='want_add_friend_ajax'),
    path('add_chat', views.add_chat_ajax, name='add_chat_ajax'),
    path('post', views.post_ajax, name='post_ajax'),
    path('like', views.like_ajax, name='like_ajax'),
    path('comment', views.comment_ajax, name='comment_ajax'),
    path('comment_like', views.comment_like_ajax, name='comment_like_ajax'),
    path('comment_user', views.comment_user_ajax, name='comment_user_ajax'),
    path('comment_reply', views.comment_reply_ajax, name='comment_reply_ajax'),
    path('chat_options', views.chat_options_ajax, name='chat_options_ajax'),
    path('chat_get_mess', views.chat_get_mess_ajax, name='chat_get_mess_ajax'),
    path('send_file_mes', views.send_file_mes_ajax, name='send_file_mes_ajax'),
    path('musics_all', views.musics_all_ajax, name='musics_all_ajax'),
]