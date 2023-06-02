# chat/consumers.py
import importlib
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.user_inbox = f'inbox_{self.user.id}'
        if self.user.is_authenticated:
            # connection has to be accepted
            await self.accept()
            # join the room group
            await self.channel_layer.group_add(
                self.user_inbox,
                self.channel_name,
            )

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # delete the user inbox for private messages
            await self.channel_layer.group_discard(
                self.user_inbox,
                self.channel_name,
            )

    async def notification(self, event):
        await self.send(json.dumps(event))

    async def receive(self, text_data=None, bytes_data=None):
        receive_handler_path = settings.SIMPLE_NOTIFICATION_SETTINGS['receive_handler_path']
        # Split the function path into module and function names
        module_name, function_name = receive_handler_path.rsplit('.', 1)

        # Import the module dynamically
        module = importlib.import_module(module_name)

        # Get the function from the module
        receive_handler = getattr(module, function_name)

        sync_to_async(receive_handler(json.loads(text_data)))
