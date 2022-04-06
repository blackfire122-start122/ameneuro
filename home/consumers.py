import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from django.db.models import Max
from .services import *

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
        try:self.chat = Chat.objects.get(chat_id=self.room_name)
        except: self.close()

        self.text_data_json['musics_url'] = []

        for u in self.chat.users.all():
            for m in u.music.all():
                if not ('/streaming_music/'+str(m.id),m.id) in self.text_data_json['musics_url']:
                    self.text_data_json['musics_url'].append(('/streaming_music/'+str(m.id),m.id))

    @database_sync_to_async
    def new_mes(self,text):
        if self.scope["user"] in self.chat.users.all():  
            mes = Message(user = self.scope["user"],text=text,type_m=TypeMes.objects.get(type_m=self.text_data_json["type"]))
            mes.save()
            self.text_data_json["time"]=str(mes.date)
            self.text_data_json["user"]=str(self.scope["user"])
            self.chat.messages.add(mes)

    @database_sync_to_async
    def new_theme(self):
        self.chat.theme = Theme.objects.get(pk = int(self.text_data_json['theme_id']))
        self.chat.save()

    @database_sync_to_async
    def delete_theme(self):
        if self.chat.theme.id == int(self.text_data_json['th_id']):
            self.text_data_json['error'] = "This chat theme"
        else:
            Theme.objects.get(pk = int(self.text_data_json['th_id'])).delete()

    @database_sync_to_async
    def end_readable(self):
        end_mes = self.chat.messages.last()
        if end_mes.user != self.scope["user"]:
            end_mes.readeble = True
            end_mes.save()
        self.text_data_json["readeble"]=str(end_mes.readeble)

    @database_sync_to_async
    def share(self):
        self.chat = Chat.objects.get(chat_id=self.room_name)
        self.scope["user"] = User.objects.get(username=self.text_data_json['user'])

    @database_sync_to_async
    def new_mes_share(self):
        post = Post.objects.get(pk=int(self.text_data_json["id_share"]))
        mes = Message(type_file=post.type_p, file=post.file, user=self.scope["user"],text=self.text_data_json["msg"],type_m=TypeMes.objects.get(type_m=self.text_data_json["type"]))
        mes.save()

        self.text_data_json["time"]=str(mes.date)
        self.text_data_json["user"]=str(self.scope["user"])
        self.text_data_json["url_file"]=mes.file.url
        self.text_data_json["url_post"]="/post/" + str(post.id)
        self.chat.messages.add(mes)
        self.text_data_json["type_file"] = post.type_p.type_f


    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)

        if self.__dict__.get("chat")==None and self.text_data_json["type"] in close_less_chat:
            return await self.close()

        if self.text_data_json['type']=='first_msg':
            await self.first_conn()
            self.text_data_json['focus_mus']=1
            await self.send(text_data=json.dumps(self.text_data_json))
            return
            
        elif self.text_data_json['type']=='end_readable':
            await self.end_readable()

        elif self.text_data_json['type']=='new_theme':
            await self.new_theme()
            await self.new_mes(self.scope["user"].username+" changed "+self.chat.theme.name)
            self.text_data_json["msg_new_theme"]=self.scope["user"].username+" changed "+self.chat.theme.name

        elif self.text_data_json['type']=='delete_theme':
            await self.delete_theme()
            await self.send(text_data=json.dumps(self.text_data_json))
            return

        elif self.text_data_json['type']=='msg':
            await self.new_mes(self.text_data_json['msg'])
        
        elif self.text_data_json['type']=='share':
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
        mus = Music.objects.get(pk=self.text_data_json["id"])
        self.scope["user"].music.add(mus)
        self.scope["user"].music_shared.remove(mus)

    @database_sync_to_async
    def not_add_mus_share(self):
        self.scope["user"].music_shared.remove(Music.objects.get(pk=self.text_data_json["id"]))
    
    @database_sync_to_async
    def add_to_me(self):
        self.scope["user"].music.add(Music.objects.get(pk=self.text_data_json["id"]))

    @database_sync_to_async
    def delete_mus(self):
        self.scope["user"].music.remove(Music.objects.get(pk=self.text_data_json["id"]))
    
    @database_sync_to_async
    def mus_share(self):
        user = User.objects.get(pk=int(self.text_data_json["to_user"]))
        mus = Music.objects.get(pk=self.text_data_json["id"])
        user.music_shared.add(mus)

        ma = MessageActivity(text="you shared music: "+mus.name,from_user=self.scope["user"],readeble=False)
        ma.save()
        user.message_activity.add(ma)

    @database_sync_to_async
    def save_post(self):
        self.scope["user"].saves_posts.add(Post.objects.get(pk=int(self.text_data_json["id"])))

    @database_sync_to_async
    def not_save(self):
        self.scope["user"].saves_posts.remove(Post.objects.get(pk=int(self.text_data_json["id"])))

    @database_sync_to_async
    def delete_friend(self):
        self.scope["user"].friends.remove(self.text_data_json['id'])

    @database_sync_to_async
    def add_friend(self):
        friend = User.objects.get(pk=self.text_data_json['id'])
        self.scope["user"].friends.add(friend.id)
        self.scope["user"].friend_want_add.remove(friend)

    @database_sync_to_async
    def want_add_friend(self):
        friend = User.objects.get(pk=self.text_data_json['id'])
        friend.friend_want_add.add(self.scope["user"].id)

    @database_sync_to_async
    def follow(self):
        follow_to = User.objects.get(pk=self.text_data_json['id'])
        follow_to.followers.add(self.scope["user"].id)
        self.scope["user"].follow.add(follow_to.id)

        ma = MessageActivity(text="on you follow: "+self.scope["user"].username,from_user=self.scope["user"],readeble=False)  
        ma.save()
        follow_to.message_activity.add(ma)

    @database_sync_to_async
    def add_chat(self):
        friend = User.objects.get(pk=self.text_data_json["id"])

        theme = Theme(background=None, color_mes='#FFFFFF',color_mes_bg='#000000',name=friend.username+self.scope["user"].username)
        theme.save()

        chat = Chat(chat_id=gen_rand_id(30))
        chat.theme=theme
        chat.save()

        chat.users.add(self.scope["user"].id)
        chat.users.add(friend.id)

        self.scope["user"].chats.add(chat.id)
        friend.chats.add(chat.id)

        self.scope["user"].themes.add(theme.id)
        friend.themes.add(theme.id)

    @database_sync_to_async
    def like(self):
        post = Post.objects.get(pk=self.text_data_json["id"])
        post.likes.add(self.scope["user"].id)

    @database_sync_to_async
    def comment_like(self):
        com = Comment.objects.get(pk=self.text_data_json["id"])
        com.likes.add(self.scope["user"].id)

    @database_sync_to_async
    def comment_user(self):
        com = Comment(user=self.scope["user"],text=self.text_data_json["text"])
        com.save()

        post = Post.objects.get(pk=self.text_data_json["id"])
        post.comments.add(com.id)

    @database_sync_to_async
    def comment_reply(self):
        com = Comment(user=self.scope["user"],text=self.text_data_json["text"])
        com.parent = Comment.objects.get(pk=int(self.text_data_json["com_id"]))
        com.save()

        post = Post.objects.get(pk=int(self.text_data_json["post_id"]))
        post.comments.add(com.id)
        ma = MessageActivity(text="you reply comment: "+com.text,from_user=self.scope["user"],file=post.file,readeble=False,type_f=post.type_p)
        
        ma.save()
        com.parent.user.message_activity.add(ma)

    @database_sync_to_async
    def delete_post(self):
        try:post = Post.objects.get(pk=self.text_data_json["id"])
        except: self.text_data_json["data_text"] = "error"

        if post.user_pub == self.scope["user"]:
            post.delete()
            self.text_data_json["data_text"] = "OK"
        else: self.text_data_json["data_text"] = "error"

    @database_sync_to_async
    def new_theme_all(self):
        self.scope["user"].theme_all = AllTheme.objects.get(pk = self.text_data_json["id"])
        self.scope["user"].save()

    @database_sync_to_async
    def delete_theme_all(self):
        theme_del = AllTheme.objects.get(pk = self.text_data_json["id"])
        if not theme_del.default:theme_del.delete()

    @database_sync_to_async
    def visible_ma(self):
        ma = MessageActivity.objects.get(pk=self.text_data_json["id"])
        ma.readeble=True
        ma.save()

    @database_sync_to_async
    def session_save(self):
        self.scope["session"].save()

    @database_sync_to_async
    def get_first_music(self):
        self.text_data_json["id"] = Playlist.objects.get(pk=self.text_data_json["id_playlist"]).musics.all()[0].id

    @database_sync_to_async
    def add_to_playlists(self):
        ps = Playlist.objects.get(pk=self.text_data_json["playlist_id"])
        if self.scope["user"]!=ps.autor:
            return
        ps.musics.add(self.text_data_json["music_id"])

    @database_sync_to_async
    def not_add_to_playlists(self):
        ps = Playlist.objects.get(pk=self.text_data_json["playlist_id"])
        if self.scope["user"]!=ps.autor:
            return
        ps.musics.remove(self.text_data_json["music_id"])

    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)

        if self.text_data_json['type']=='add_mus_share':
            await self.add_mus_share()
            return
        elif self.text_data_json['type']=='not_add_mus_share':
            await self.not_add_mus_share()
            return
        elif self.text_data_json['type']=='add_to_me':
            await self.add_to_me()
            return
        elif self.text_data_json['type']=='delete_mus':
            await self.delete_mus()
            return
        elif self.text_data_json['type']=='mus_share':
            await self.mus_share()
            return
        elif self.text_data_json['type']=='save_post':
            await self.save_post()
            return
        elif self.text_data_json['type']=='not_save':
            await self.not_save()
            return
        elif self.text_data_json['type']=='delete_friend':
            await self.delete_friend()
            return  
        elif self.text_data_json['type']=='add_friend':
            await self.add_friend()
            return
        elif self.text_data_json['type']=='want_add_friend':
            await self.want_add_friend()
            return
        elif self.text_data_json['type']=='follow':
            await self.follow()
            return
        elif self.text_data_json['type']=='add_chat':
            await self.add_chat()
            return
        elif self.text_data_json['type']=='like':
            await self.like()
            return
        elif self.text_data_json['type']=='comment_like':
            await self.comment_like()
            return
        elif self.text_data_json['type']=='comment_user':
            await self.comment_user()
            return
        elif self.text_data_json['type']=='comment_reply':
            await self.comment_reply()
            return
        elif self.text_data_json['type']=='delete_post':
            await self.delete_post()
        elif self.text_data_json['type']=='new_theme_all':
            await self.new_theme_all()
            return
        elif self.text_data_json['type']=='delete_theme_all':
            await self.delete_theme_all()
            return
        elif self.text_data_json['type']=='visible_ma':
            await self.visible_ma()
            return
        elif self.text_data_json['type']=='play_in_all':
            if self.text_data_json["type_media"]=="playlist":
                self.scope["session"]["playlist_play_in_all"]=self.text_data_json["id_playlist"]
                if self.text_data_json["id"]=="first_id_music":
                    await self.get_first_music()
                else:self.scope["session"]["music_play_in_all"] = self.text_data_json["id"]
            else:self.scope["session"]["music_play_in_all"] = self.text_data_json["id"]
            self.scope["session"]["music_play_in_all_currentTime"]=self.text_data_json["currentTime"]
            self.scope["session"]["music_play_in_all_type"]=self.text_data_json["type_media"]
            return

        elif self.text_data_json['type']=='get_play_in_all':
            if self.scope["session"].get("music_play_in_all_type")=='playlist':
                self.text_data_json["id_playlist"]=self.scope["session"]["playlist_play_in_all"]    
            
            self.text_data_json["id"]=self.scope["session"].get("music_play_in_all")
            self.text_data_json["currentTime"]=self.scope["session"].get("music_play_in_all_currentTime")
            self.text_data_json["type_media"]=self.scope["session"].get("music_play_in_all_type")

        elif self.text_data_json['type']=='play_in_all_current_time':
            self.scope["session"]["music_play_in_all_currentTime"]=self.text_data_json["currentTime"]
            return

        elif self.text_data_json['type']=='add_to_playlists':
            await self.add_to_playlists()
        elif self.text_data_json['type']=='not_add_to_playlists':
            await self.not_add_to_playlists()

        await self.channel_layer.group_send(
            self.room_group_name,{
                "type": "chat.message",
                "text": self.text_data_json,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["text"]))