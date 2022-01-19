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
        self.chat = Chat.objects.get(chat_id=self.text_data_json['chat'])

    @database_sync_to_async
    def new_mes(self,type_m,text):
        mes = Message(user = self.user,text=text,type_m=type_m)
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
        if self.chat.theme.id == int(self.text_data_json['theme_id']):
            self.text_data_json['error'] = "This chat theme"
        else:
            Theme.objects.get(pk = int(self.text_data_json['theme_id'])).delete()

    @database_sync_to_async
    def end_readable(self):
        end_mes = self.chat.messages.last()
        if end_mes.user != self.user:
            end_mes.readeble = True
            end_mes.save()
        self.text_data_json["readeble"]=str(end_mes.readeble)

    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)

        if self.text_data_json['type']=='first_msg':
            await self.first_conn()
            return


        elif self.text_data_json['type']=='end_readable':
            await self.end_readable()

            await self.channel_layer.group_send(
                self.room_group_name,    
                {
                    "type": "chat.message",
                    "text": self.text_data_json,
                }
            )

            return


        elif self.text_data_json['type']=='new_theme':
            await self.new_theme()
            await self.new_mes(self.text_data_json['type'],self.user.username+" "+self.chat.theme.name)

            self.text_data_json["msg_new_theme"]=self.user.username+" "+self.chat.theme.name

            await self.channel_layer.group_send(
                self.room_group_name,    
                {
                    "type": "chat.message",
                    "text": self.text_data_json,
                }
            )
            return

        elif self.text_data_json['type']=='delete_theme':
            await self.delete_theme()
            await self.send(text_data=json.dumps(self.text_data_json))
            return

        elif self.text_data_json['type']=='msg':
            await self.new_mes(self.text_data_json['type'],self.text_data_json['msg'])
            
            await self.channel_layer.group_send(
                self.room_group_name,    
                {
                    "type": "chat.message",
                    "text": self.text_data_json,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["text"]))