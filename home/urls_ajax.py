from django.urls import path
from . import ajax_views

urlpatterns = [
    path('post', ajax_views.post_ajax, name='post_ajax'),
    path('video', ajax_views.video_ajax, name='video_ajax'),
    path('post_user', ajax_views.post_user_ajax, name='post_user_ajax'),
    path('video_user', ajax_views.video_user_ajax, name='video_user_ajax'),
    path('comment', ajax_views.comment_ajax, name='comment_ajax'),
    path('comment_video', ajax_views.comment_video_ajax, name='comment_video_ajax'),
    path('chat_options', ajax_views.chat_options_ajax, name='chat_options_ajax'),
    path('chat_get_mess', ajax_views.chat_get_mess_ajax, name='chat_get_mess_ajax'),
    path('send_file_mes', ajax_views.send_file_mes_ajax, name='send_file_mes_ajax'),
    path('musics_all', ajax_views.musics_all_ajax, name='musics_all_ajax'),
    path('user_find', ajax_views.user_find_ajax, name='user_find_ajax'),
    path('users_get', ajax_views.users_get_ajax, name='users_get_ajax'),
    path('saves_posts', ajax_views.saves_posts_ajax, name='saves_posts_ajax'),
    path('music_get', ajax_views.music_get_ajax, name='music_get_ajax'),
    path('playlist_get', ajax_views.playlist_get_ajax, name='playlist_get_ajax'),
    path('video_get', ajax_views.video_get_ajax, name='video_get_ajax'),
    path('playlist_find', ajax_views.playlist_find_ajax, name='playlist_find_ajax'),
    path('music_find', ajax_views.music_find_ajax, name='music_find_ajax'),
    path('video_find', ajax_views.video_find_ajax, name='video_find_ajax'),
    path('playlists', ajax_views.playlists_ajax, name='playlists_ajax'),
    path('share_ch', ajax_views.share_ch_ajax, name='share_ch_ajax'),
    path('activity_mess', ajax_views.activity_mess_ajax, name='activity_mess_ajax'),

]

