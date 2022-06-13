import asyncio
import json
from time import sleep

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from websocket_generic.models import Group, Chat



class MyWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        print('websocket connected')
        print("channel layer ...", self.channel_layer)
        print('channel name...', self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['GroupName']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # group = Group.objects.filter(name=self.group_name).first()
        # chats = []
        # if group:
        #     chats = Chat.objects.filter(group=self.group_name)
        # else:
        #     group = Group(name=self.group_name)
        #     group.save()
        self.accept()  # to accept the connection


        # self.close() # to forcefully close the connection

    def receive(self, text_data=None, bytes_data=None):
        print("Msg received from client", text_data)

        group = Group.objects.get(name=self.group_name)

        """ from 23-29:
        Server will send a message in a group, so group send has 2 params:
        1). group name (to which we send msg
        2).msg that server will send. 
        since group_send is a async method so we have to convert it to sync.
        chat.message is an event so we have to write chat_message handler. and 'event' in chat_handler will
         receive data from message key (which has value of text_data)
        """
        chat = Chat(
            content=text_data,
            group=group)
        chat.save()
        print("chatttt" ,type(chat))
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat.message',
                'message': text_data
            }
        )

        """ event will have text_data value /any value passed in message key above"""

    def chat_message(self, event):
        print("Event ...", event)
        print("Event ...", type(event))
        self.send(text_data=json.dumps({
            'msg': event['message']
        }))

        # for i in range(20):
        #     self.send(text_data=str(i))
        #     sleep(1)

    # self.send(bytes_data=data) to send binarydata
    #  self.close(code=4123) # for adding custome code error

    def disconnect(selfself, close_code):
        print("websocket disconnected ...", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )


class MyAsyncWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('websocket connected')
        self.group_name = self.scope['url_route']['kwargs']['GroupName']
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()  # to accept the connection
        # await self.close() # to forcefully close the connection

    async def receive(self, text_data=None, bytes_data=None):
        print("Msg received from client", text_data)
        # await self.send(text_data="Msg from server to client")
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        chat = Chat(
            content=text_data,
            group=group)
        if chat is not None:
           database_sync_to_async(chat.save)()
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': text_data
            }
        )
        """ event will have text_data value /any value passed in message key above"""

    def chat_message(self, event):
        print("Event ...", event)
        print("Event ...", type(event))
        self.send(text_data=json.dumps({
            'msg': event['message']
        }))

    # self.send(bytes_data=data) to send binarydata
    #  for i in range(20):
    #      await self.send(text_data=str(i))
    #      asyncio.sleep(1)
    # await self.close(code=4123) # for adding custome code error

    async def disconnect(self, close_code):
        print("websocket disconnected ...", close_code)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
