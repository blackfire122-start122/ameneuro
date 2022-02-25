import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from django.db.models import Max

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.theme = {}
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
        self.user = User.objects.get(username=self.text_data_json['user'])
        self.chat = Chat.objects.get(chat_id=self.room_name)
        self.text_data_json['musics_url'] = []

        for u in self.chat.users.all():
            for m in u.music.all():
                if not ('/streaming_music/'+str(m.id),m.id) in self.text_data_json['musics_url']:
                    self.text_data_json['musics_url'].append(('/streaming_music/'+str(m.id),m.id))

    @database_sync_to_async
    def new_mes(self,text):
        mes = Message(user = self.user,text=text,type_m=TypeMes.objects.get(type_m=self.text_data_json["type"]))
        mes.save()
        self.text_data_json["time"]=str(mes.date)
        self.text_data_json["user"]=str(self.user)
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
        if end_mes.user != self.user:
            end_mes.readeble = True
            end_mes.save()
        self.text_data_json["readeble"]=str(end_mes.readeble)

    @database_sync_to_async
    def share(self):
        self.chat = Chat.objects.get(chat_id=self.room_name)
        self.user = User.objects.get(username=self.text_data_json['user'])

    @database_sync_to_async
    def new_mes_share(self):
        post = Post.objects.get(pk=int(self.text_data_json["id_share"]))
        mes = Message(type_file=post.type_p, file=post.file, user=self.user,text=self.text_data_json["msg"],type_m=TypeMes.objects.get(type_m=self.text_data_json["type"]))
        mes.save()

        self.text_data_json["time"]=str(mes.date)
        self.text_data_json["user"]=str(self.user)
        self.text_data_json["url_file"]=mes.file.url
        self.text_data_json["url_post"]="/post/" + str(post.id)
        self.chat.messages.add(mes)
        self.text_data_json["type_file"] = post.type_p.type_f


    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)

        if self.text_data_json['type']=='first_msg':
            await self.first_conn()
            self.text_data_json['focus_mus']=1
            await self.send(text_data=json.dumps(self.text_data_json))
            return
            
        elif self.text_data_json['type']=='end_readable':
            await self.end_readable()

        elif self.text_data_json['type']=='new_theme':
            await self.new_theme()
            await self.new_mes(self.user.username+" changed "+self.chat.theme.name)
            self.text_data_json["msg_new_theme"]=self.user.username+" changed "+self.chat.theme.name

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
        self.theme = {}
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
        self.user = User.objects.get(username=self.text_data_json['user'])
   
    @database_sync_to_async
    def add_mus_share(self):
        mus = Music.objects.get(pk=self.text_data_json["id"])
        self.user.music.add(mus)
        self.user.music_shared.remove(mus)

    @database_sync_to_async
    def not_add_mus_share(self):
        self.user.music_shared.remove(Music.objects.get(pk=self.text_data_json["id"]))
    
    @database_sync_to_async
    def add_to_me(self):
        self.user.music.add(Music.objects.get(pk=self.text_data_json["id"]))

    @database_sync_to_async
    def delete_mus(self):
        self.user.music.remove(Music.objects.get(pk=self.text_data_json["id"]))
    
    @database_sync_to_async
    def mus_share(self):
        User.objects.get(pk=int(self.text_data_json["to_user"])).music_shared.add(Music.objects.get(pk=self.text_data_json["id"]))

    @database_sync_to_async
    def save_post(self):
        self.user.saves_posts.add(Post.objects.get(pk=int(self.text_data_json["id"])))

    @database_sync_to_async
    def not_save(self):
        self.user.saves_posts.remove(Post.objects.get(pk=int(self.text_data_json["id"])))

    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)

        if self.text_data_json['type']=='first_conn':
            await self.first_conn()
            await self.send(text_data=json.dumps(self.text_data_json))
            # print(self.room_name == self.user.username)
            return

        elif self.text_data_json['type']=='add_mus_share':
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
        await self.channel_layer.group_send(
            self.room_group_name,{
                "type": "chat.message",
                "text": self.text_data_json,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["text"]))