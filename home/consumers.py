import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.first = True

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
        self.first = False

    @database_sync_to_async
    def new_mes(self):
        mes = Message(user = self.user, text=self.text_data_json["msg"])
        mes.save()
        self.chat.messages.add(mes)
        self.mes_date = mes.date


    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)

        if self.first:
            await self.first_conn()
            return

        await self.new_mes()

        self.text_data_json["time"]=str(self.mes_date)
        self.text_data_json["user"]=str(self.user)
        
        await self.channel_layer.group_send(
            self.room_group_name,    
            {
                "type": "chat.message",
                "text": self.text_data_json,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["text"]))