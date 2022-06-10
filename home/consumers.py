import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from .services import *
import logging

logger = logging.getLogger(__name__)

close_less_chat = [
    "end_readable",
    "new_theme",
    "delete_theme",
    "msg"
]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.theme = {}

        if self.scope["user"].is_anonymous:
            return await self.close()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
 
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def first_conn(self):
        try:self.chat = Chat.objects.get(pk=self.text_data_json.get("chat"))
        except:return "close"
    @database_sync_to_async
    def new_mes(self,text):
        if self.scope["user"] == self.chat.user:
            mes = Message(user = self.scope["user"],text=text,type_m=TypeMes.objects.get(type_m=self.text_data_json.get("type")))
            mes.save()
            self.text_data_json["time"]=str(mes.date)
            self.text_data_json["user"]=str(self.scope["user"])
            self.chat.messages.add(mes)
            self.chat.chat_friend.messages.add(mes)

    @database_sync_to_async
    def new_theme(self):
        self.chat.theme = Theme.objects.get(pk = int(self.text_data_json.get('theme_id')))
        self.chat.save()

    @database_sync_to_async
    def delete_theme(self):
        if self.chat.theme.id == int(self.text_data_json.get('th_id')):
            self.text_data_json['error'] = "This chat theme"
        else:
            Theme.objects.get(pk = int(self.text_data_json.get('th_id'))).delete()

    @database_sync_to_async
    def end_readable(self):
        end_mes = self.chat.messages.last()
        if end_mes.user != self.scope["user"]:
            end_mes.readeble = True
            end_mes.save()
        self.text_data_json["readeble"]=str(end_mes.readeble)

    @database_sync_to_async
    def share(self):
        self.chat = Chat.objects.get(pk=self.text_data_json.get("chat"))
        self.scope["user"] = User.objects.get(username=self.text_data_json.get('user'))

    @database_sync_to_async
    def new_mes_share(self):
        post = Post.objects.get(pk=int(self.text_data_json.get("id_share")))
        mes = Message(type_file=post.type_p, file=post.file, user=self.scope["user"],text=self.text_data_json.get("msg"),type_m=TypeMes.objects.get(type_m=self.text_data_json.get("type")))
        mes.save()

        self.text_data_json["time"]=str(mes.date)
        self.text_data_json["user"]=str(self.scope["user"])
        self.text_data_json["url_file"]=mes.file.url
        self.text_data_json["url_post"]="/post/" + str(post.id)
        self.chat.messages.add(mes)
        self.chat.chat_friend.messages.add(mes)
        self.text_data_json["type_file"] = post.type_p.type_f


    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)

        if self.__dict__.get("chat")==None and self.text_data_json.get("type") in close_less_chat:
            return await self.close()

        if self.text_data_json.get('type')=='first_msg':
            if await self.first_conn() == "close":
                return await self.close()
            self.text_data_json['focus_mus']=1
            await self.send(text_data=json.dumps(self.text_data_json))
            return
            
        elif self.text_data_json.get('type')=='end_readable':
            await self.end_readable()

        elif self.text_data_json.get('type')=='new_theme':
            await self.new_theme()
        elif self.text_data_json.get('type')=='delete_theme':
            await self.delete_theme()
            await self.send(text_data=json.dumps(self.text_data_json))
            return

        elif self.text_data_json.get('type')=='msg':
            await self.new_mes(self.text_data_json.get('msg'))
        
        elif self.text_data_json.get('type')=='share':
            await self.share()
            await self.new_mes_share()

        await self.channel_layer.group_send(
            self.room_group_name,{
                "type": "chat.message",
                "text": self.text_data_json,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["text"]))

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        if self.scope["user"].is_anonymous:
            return await self.close()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        self.text_data_json = {'type':'disconnect','user_in':self.scope["user"].username}

        await self.channel_layer.group_send(
            self.room_group_name,{
                "type": "chat.message",
                "text": self.text_data_json,
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.session_save()
        
    @database_sync_to_async
    def add_mus_share(self):
        mus = Music.objects.get(pk=self.text_data_json.get("id"))
        self.scope["user"].music.add(mus)
        self.scope["user"].music_shared.remove(mus)

    @database_sync_to_async
    def not_add_mus_share(self):
        self.scope["user"].music_shared.remove(Music.objects.get(pk=self.text_data_json.get("id")))
    
    @database_sync_to_async
    def add_to_me(self):
        self.scope["user"].music.add(Music.objects.get(pk=self.text_data_json.get("id")))

    @database_sync_to_async
    def delete_mus(self):
        self.scope["user"].music.remove(Music.objects.get(pk=self.text_data_json.get("id")))
    
    @database_sync_to_async
    def mus_share(self):
        if self.text_data_json.get("to_user") and self.text_data_json.get("id"):
            user = User.objects.get(pk=int(self.text_data_json.get("to_user")))
            mus = Music.objects.get(pk=self.text_data_json.get("id"))
            user.music_shared.add(mus)
            type_f = TypeFile.objects.get(type_f="audio")

            ma = MessageActivity(text="you shared music: "+mus.name,from_user=self.scope["user"],readeble=False,type_f=type_f)
            ma.save()
            user.message_activity.add(ma)

    @database_sync_to_async
    def save_post(self):
        self.scope["user"].saves_posts.add(Post.objects.get(pk=int(self.text_data_json.get("id"))))

    @database_sync_to_async
    def not_save(self):
        self.scope["user"].saves_posts.remove(Post.objects.get(pk=int(self.text_data_json.get("id"))))

    @database_sync_to_async
    def delete_friend(self):
        self.scope["user"].friends.remove(self.text_data_json.get('id'))

    @database_sync_to_async
    def add_friend(self):
        friend = User.objects.get(pk=self.text_data_json.get('id'))
        self.scope["user"].friends.add(friend.id)
        self.scope["user"].friend_want_add.remove(friend)

    @database_sync_to_async
    def want_add_friend(self):
        friend = User.objects.get(pk=self.text_data_json.get('id'))
        friend.friend_want_add.add(self.scope["user"].id)
 
        type_f = TypeFile.objects.filter(type_f="img")[0]

        ma = MessageActivity(text="to you what add to friends: "+friend.username,from_user=self.scope["user"],readeble=False,type_f=type_f,file=friend.img.url)
        ma.save()
        friend.message_activity.add(ma)

    @database_sync_to_async
    def follow(self):
        follow_to = User.objects.get(pk=self.text_data_json.get('id'))
        follow_to.followers.add(self.scope["user"].id)
        self.scope["user"].follow.add(follow_to.id)

        ma = MessageActivity(text="on you follow: "+self.scope["user"].username,from_user=self.scope["user"],readeble=False)  
        ma.save()
        follow_to.message_activity.add(ma)

    @database_sync_to_async
    def add_chat(self):
        friend = User.objects.get(pk=self.text_data_json.get("id"))

        theme_chat = Theme(background=None, color_mes='#FFFFFF',color_mes_bg='#000000',name=friend.username+self.scope["user"].username)
        friend_theme_chat = Theme(background=None, color_mes='#FFFFFF',color_mes_bg='#000000',name=self.scope["user"].username+friend.username)
        friend_theme_chat.save()
        theme_chat.save()

        chat = Chat(chat_id=gen_rand_id(30))
        chat_friend = Chat()
        chat_friend.chat_id = chat.chat_id
        
        chat.theme=theme_chat
        chat_friend.theme=friend_theme_chat

        chat.user=self.scope["user"]
        chat_friend.user = friend

        chat.save()
        chat_friend.save()

        chat.chat_friend=chat_friend
        chat_friend.chat_friend = chat

        chat.save()
        chat_friend.save()

        self.scope["user"].chats.add(chat.id)
        friend.chats.add(chat_friend.id)

    @database_sync_to_async
    def like(self):
        post = Post.objects.get(pk=self.text_data_json.get("id"))
        post.likes.add(self.scope["user"].id)

    @database_sync_to_async
    def not_like(self):
        post = Post.objects.get(pk=self.text_data_json.get("id"))
        post.likes.remove(self.scope["user"].id)

    @database_sync_to_async
    def comment_like(self):
        com = Comment.objects.get(pk=self.text_data_json.get("id"))
        com.likes.add(self.scope["user"].id)

    @database_sync_to_async
    def not_comment_like(self):
        com = Comment.objects.get(pk=self.text_data_json.get("id"))
        com.likes.remove(self.scope["user"].id)

    @database_sync_to_async
    def comment_user(self):
        com = Comment(user=self.scope["user"],text=self.text_data_json.get("text"))
        com.save()

        post = Post.objects.get(pk=self.text_data_json.get("id"))
        post.comments.add(com.id)

    @database_sync_to_async
    def comment_reply(self):
        com = Comment(user=self.scope["user"],text=self.text_data_json.get("text"))
        com.parent = Comment.objects.get(pk=int(self.text_data_json.get("com_id")))
        com.save()

        post = Post.objects.get(pk=int(self.text_data_json.get("post_id")))
        post.comments.add(com.id)
        ma = MessageActivity(text="you reply comment: "+com.text,from_user=self.scope["user"],file=post.file,readeble=False,type_f=post.type_p)
        
        ma.save()
        com.parent.user.message_activity.add(ma)

    @database_sync_to_async
    def delete_post(self):
        try:post = Post.objects.get(pk=self.text_data_json.get("id"))
        except: self.text_data_json["data_text"] = "error"

        if post.user_pub == self.scope["user"]:
            post.delete()
            self.text_data_json["data_text"] = "OK"
        else: self.text_data_json["data_text"] = "error"

    @database_sync_to_async
    def delete_video(self):
        try:video = Video.objects.get(pk=self.text_data_json.get("id"))
        except: self.text_data_json["data_text"] = "error"

        if video.user_pub == self.scope["user"]:
            video.delete()
            self.text_data_json["data_text"] = "OK"
        else: self.text_data_json["data_text"] = "error"

    @database_sync_to_async
    def new_theme_all(self):
        self.scope["user"].theme_all = AllTheme.objects.get(pk = self.text_data_json.get("id"))
        self.scope["user"].save()

    @database_sync_to_async
    def delete_theme_all(self):
        try:theme_del = AllTheme.objects.get(pk = self.text_data_json.get("id"))
        except:pass
        if not theme_del.default:theme_del.delete()

    @database_sync_to_async
    def visible_ma(self):
        ma = MessageActivity.objects.get(pk=self.text_data_json.get("id"))
        ma.readeble=True
        ma.save()

    @database_sync_to_async
    def session_save(self):
        try:self.scope.get("session").save()
        except Exception as e:logger.warning(str(e))

    @database_sync_to_async
    def get_first_music(self):
        self.text_data_json["id"] = Playlist.objects.get(pk=self.text_data_json.get("id_playlist")).musics.all()[0].id

    @database_sync_to_async
    def add_to_playlists(self):
        ps = Playlist.objects.get(pk=self.text_data_json.get("playlist_id"))
        if self.scope["user"]!=ps.autor:
            return
        ps.musics.add(self.text_data_json.get("music_id"))

    @database_sync_to_async
    def not_add_to_playlists(self):
        ps = Playlist.objects.get(pk=self.text_data_json.get("playlist_id"))
        if self.scope["user"]!=ps.autor:
            return
        ps.musics.remove(self.text_data_json.get("music_id"))

    @database_sync_to_async
    def like_video(self):
        Video.objects.get(pk=self.text_data_json.get("id")).likes.add(self.scope["user"])
    
    @database_sync_to_async
    def not_like_video(self):
        Video.objects.get(pk=self.text_data_json.get("id")).likes.remove(self.scope["user"])

    @database_sync_to_async
    def comment_video_user(self):
        com = Comment(user=self.scope["user"],text=self.text_data_json.get("text"))
        com.save()

        video = Video.objects.get(pk=self.text_data_json.get("id"))
        video.comments.add(com.id)

    @database_sync_to_async
    def comment_video_reply(self):
        com = Comment(user=self.scope["user"],text=self.text_data_json.get("text"))
        com.parent = Comment.objects.get(pk=int(self.text_data_json.get("com_id")))
        com.save()

        video = Video.objects.get(pk=int(self.text_data_json.get("video_id")))
        video.comments.add(com.id)
        type_f = TypeFile.objects.get(type_f="video")
        ma = MessageActivity(text="you reply comment: "+com.text,from_user=self.scope["user"],file=video.file,readeble=False,type_f=type_f)
        
        ma.save()
        com.parent.user.message_activity.add(ma)

    @database_sync_to_async
    def add_ps_share(self):
        ps = Playlist.objects.get(pk=self.text_data_json.get("id"))
        self.scope["user"].playlists.add(ps)
        self.scope["user"].playlists_shared.remove(ps)

    @database_sync_to_async
    def not_add_ps_share(self):
        self.scope["user"].playlists_shared.remove(Playlist.objects.get(pk=self.text_data_json.get("id")))

    @database_sync_to_async
    def delete_ps_form_me(self):
        self.scope["user"].playlists.remove(Playlist.objects.get(pk=self.text_data_json.get("id")))

    @database_sync_to_async
    def ps_share(self):
        if self.text_data_json.get("to_user") and self.text_data_json.get("id"):
            user = User.objects.get(pk=int(self.text_data_json.get("to_user")))
            ps = Playlist.objects.get(pk=self.text_data_json.get("id"))
            user.playlists_shared.add(ps)
            type_f = TypeFile.objects.get(type_f="audio")

            ma = MessageActivity(text="you shared playlist: "+ps.name,from_user=self.scope["user"],readeble=False,type_f=type_f)
            ma.save()
            user.message_activity.add(ma)

    types = {'add_mus_share':add_mus_share,
        'not_add_mus_share':not_add_mus_share,
        'add_to_me':add_to_me,
        'delete_mus':delete_mus,
        'mus_share':mus_share,
        'save_post':save_post,
        'not_save':not_save,
        'delete_friend':delete_friend,
        'add_friend':add_friend,
        'want_add_friend':want_add_friend,
        'follow':follow,
        'add_chat':add_chat,
        'like':like,
        'not_like':not_like,
        'comment_like':comment_like,
        'not_comment_like':not_comment_like,
        'comment_user':comment_user,
        'comment_reply':comment_reply,
        'delete_post':delete_post,
        'new_theme_all':new_theme_all,
        'delete_theme_all':delete_theme_all,
        'visible_ma':visible_ma,
        'like_video':like_video,
        'not_like_video':not_like_video,
        'comment_video_user':comment_video_user,
        'comment_video_reply':comment_video_reply,
        'ps_share':ps_share,
        'add_ps_share':add_ps_share,
        'not_add_ps_share':not_add_ps_share,
        'delete_ps_form_me':delete_ps_form_me
    }
    types_not_return = {
        'add_to_playlists':add_to_playlists,
        'not_add_to_playlists':not_add_to_playlists,
        'delete_video':delete_video,
    }

    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)

        if self.text_data_json.get('type') in self.types.keys():
            await self.types.get(self.text_data_json.get('type'))(self)
            return
        elif self.text_data_json.get('type') in self.types_not_return.keys():
            await self.types_not_return.get(self.text_data_json.get('type'))(self)

        elif self.text_data_json.get('type')=='play_in_all':
            if self.text_data_json.get("type_media")=="playlist":
                self.scope["session"]["playlist_play_in_all"]=self.text_data_json.get("id_playlist")
                if self.text_data_json.get("id")=="first_id_music":
                    await self.get_first_music()
                else:self.scope["session"]["music_play_in_all"] = self.text_data_json.get("id")
            else:self.scope["session"]["music_play_in_all"] = self.text_data_json.get("id")
            self.scope["session"]["music_play_in_all_currentTime"]=self.text_data_json.get("currentTime")
            self.scope["session"]["music_play_in_all_type"]=self.text_data_json.get("type_media")
            return

        elif self.text_data_json.get('type')=='get_play_in_all':
            if self.scope["session"].get("music_play_in_all_type")=='playlist':
                self.text_data_json["id_playlist"]=self.scope["session"]["playlist_play_in_all"]    
            
            self.text_data_json["id"]=self.scope["session"].get("music_play_in_all")
            self.text_data_json["currentTime"]=self.scope["session"].get("music_play_in_all_currentTime")
            self.text_data_json["type_media"]=self.scope["session"].get("music_play_in_all_type")

        elif self.text_data_json.get('type')=='play_in_all_current_time':
            self.scope["session"]["music_play_in_all_currentTime"]=self.text_data_json.get("currentTime")
            return

        await self.channel_layer.group_send(
            self.room_group_name,{
                "type": "chat.message",
                "text": self.text_data_json,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["text"]))