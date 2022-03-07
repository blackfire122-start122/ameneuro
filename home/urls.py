from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('chats', views.chats.as_view(), name='chats'),
    path('chat/<chat_id>', views.chat.as_view(), name='chat'),

    path('login', views.login_user, name='login'),
    path('sigin', views.sigin_user, name='sigin'),

    path('user/<name>', views.user.as_view(), name='user'),
    path('user_change', views.user_change, name='user_change'),
    path('find', views.find.as_view(), name='find'),
    path('friends', views.friends, name='friends'),

    path('post/<int:id>', views.post, name='post'),
    path('add_post', views.add_post, name='add_post'),

    path('stream_post/<int:id>',views.streaming_post,name='stream_post'),

    path('stream_mess/<int:id>',views.streaming_mess,name='stream_mess'),
    
    path('streaming_music/<int:id>',views.streaming_music,name='streaming_music'),
    path('musics', views.musics_all, name='musics'),
    path('add_music', views.add_music.as_view(), name='add_music'),
    path('saves_posts', views.saves_posts.as_view(), name='saves_posts'),
    path('playlists/<name>', views.playlists.as_view(), name='playlists'),

    path('ajax/', include("home.urls_ajax"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
