from django.urls import path
from . import ajax_views

urlpatterns = [
    path('add_friend', ajax_views.add_friend_ajax, name='add_friend_ajax'),
    path('follow', ajax_views.follow_ajax, name='follow_ajax'),
    path('want_add_friend', ajax_views.want_add_friend_ajax, name='want_add_friend_ajax'),
    path('add_chat', ajax_views.add_chat_ajax, name='add_chat_ajax'),
    path('post', ajax_views.post_ajax, name='post_ajax'),
    path('like', ajax_views.like_ajax, name='like_ajax'),
    path('comment', ajax_views.comment_ajax, name='comment_ajax'),
    path('comment_like', ajax_views.comment_like_ajax, name='comment_like_ajax'),
    path('comment_user', ajax_views.comment_user_ajax, name='comment_user_ajax'),
    path('comment_reply', ajax_views.comment_reply_ajax, name='comment_reply_ajax'),
    path('chat_options', ajax_views.chat_options_ajax, name='chat_options_ajax'),
    path('chat_get_mess', ajax_views.chat_get_mess_ajax, name='chat_get_mess_ajax'),
    path('send_file_mes', ajax_views.send_file_mes_ajax, name='send_file_mes_ajax'),
    path('musics_all', ajax_views.musics_all_ajax, name='musics_all_ajax'),
    path('delete_post', ajax_views.delete_post_ajax, name='delete_post_ajax'),
    path('user_find', ajax_views.user_find_ajax, name='user_find_ajax'),
    path('users_get', ajax_views.users_get_ajax, name='users_get_ajax'),
]