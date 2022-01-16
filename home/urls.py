from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('chats', views.chats, name='chats'),
    path('chat/<chat_id>', views.chat, name='chat'),
    path('login', views.login_user, name='login'),
    path('sigin', views.sigin_user, name='sigin'),
    path('user/<name>', views.user, name='user'),
    path('user_find', views.user_find, name='user_find'),
    path('friends', views.friends, name='friends'),
    path('post/<int:id>', views.post, name='post'),
    path('add_post', views.add_post, name='add_post'),
    path('stream_video_post/<int:id>',views.streaming_post,name='stream_video_post'),

    path('ajax/', include("home.urls_ajax"))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
