# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import CustomUser, Match, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = f'chat_{self.match_id}'

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
        data = json.loads(text_data)
        event = data.get('type')

        if event == 'typing':
            # Forward typing indicator to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_message',
                    'user_id': data.get('user_id'),
                }
            )
        elif event == 'new_message':
            content_encrypted = data.get('content_encrypted')
            iv = data.get('iv')
            sender_id = data.get('sender_id')

            if not content_encrypted or not sender_id or not iv:
                return  # ignore invalid data

            message = await self.create_message(sender_id, content_encrypted, iv)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'id': message.id,
                        'sender_id': message.sender.id,
                        'receiver_id': message.receiver.id,
                        'content_encrypted': message.content_encrypted,
                        'iv': message.iv,  # dodaj iv do payloadu
                        'timestamp': message.timestamp.isoformat(),
                        'is_read': message.is_read,
                    }
                }
            )
        elif event == 'message_read':
            message_id = data.get('message_id')
            if message_id:
                await self.mark_message_read(message_id)
                # Notify group that message was read
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'message_read_event',
                        'message_id': message_id,
                    }
                )

    # Handlers to send to WebSocket

    async def typing_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': event['message'],
        }))

    async def message_read_event(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message_read',
            'message_id': event['message_id'],
        }))

    @database_sync_to_async
    def create_message(self, sender_id, content_encrypted, iv):
        try:
            match = Match.objects.get(id=self.match_id)
            sender = CustomUser.objects.get(id=sender_id)
        except (Match.DoesNotExist, CustomUser.DoesNotExist):
            return None

        receiver = match.user2 if sender == match.user1 else match.user1
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content_encrypted=content_encrypted,
            iv=iv  # zapisz IV do bazy
        )
        return message

    @database_sync_to_async
    def mark_message_read(self, message_id):
        try:
            msg = Message.objects.get(id=message_id)
            msg.is_read = True
            msg.save()
        except Message.DoesNotExist:
            pass
