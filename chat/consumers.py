# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import AsyncWebsocketConsumer
# from datetime import datetime
# from django.utils import timezone

# from .models import Message
# from django.conf import settings
# from account.models import Profile
# from django.contrib.auth import get_user_model
# User = get_user_model()


# class ChatConsumer(AsyncWebsocketConsumer):

#     async def fetch_messages(self, data):
#         messages = Message.last_30_messages()
#         content = {
#             'messages': self.messages_to_json(messages)
#         }
#         self.send_chat_message(content)

#     def new_message(self, data):
#         author = User.objects.get(username=data['from'])
#         author_user = Profile.objects.get(user__username=author.username)
#         message = Message.objects.create(timestamp=datetime.now(), author=author_user,
#                                          content=data['message'])
#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         return self.send_chat_message(content)

#     commands = {
#         'fetch_messages': fetch_messages,
#         'new_message': new_message
#     }

#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result

#     def message_to_json(self, message):
#         return {
#             'author': message.author.user.username,
#             'content': message.content,
#             'timestamp': str(message.timestamp.strftime("%Y-%m-%d, %H:%M"))
#         }

#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):

#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         await self.commands[data['command']](self, data)

#     async def send_chat_message(self, message):
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#             }
#         )

#     async def send_message(self, message):
#         await self.send(text_data=json.dumps(message))

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps(message))


# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))