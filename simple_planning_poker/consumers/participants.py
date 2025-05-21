import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ParticipantsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('ParticipantsConsumer connect')
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f"participants_{self.room_code}"
        self.user = self.scope['user']

        print(f"User: {self.user.username}")
        print(f"GroupName: {self.group_name}")
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'participant_add',
                'participants': {
                    'id': self.user.id,
                    'username': self.user.username,
                }
            }
        )

        asyncio.create_task(self.save_add_participant())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'participant_remove',
                'participants': {
                    'id': self.user.id,
                    'username': self.user.username,
                }
            }
        )

        asyncio.create_task(self.save_remove_participant())

    async def receive(self, text_data):
        pass

    async def participant_add(self, event):
        """
        Send the added participant to the client.
        """
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'participants': event['participants']
        }))

    async def participant_remove(self, event):
        """
        Notify the group that a participant has left.
        """
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'participants': event['participants']
        }))

    @database_sync_to_async
    def save_add_participant(self):
        from simple_planning_poker.models.room import Room
        try:
            room = Room.objects.get(code=self.room_code)
            if not room.participants.filter(id=self.user.id).exists():
                room.participants.add(self.user)
        except Room.DoesNotExist:
            pass

    @database_sync_to_async
    def save_remove_participant(self):
        from simple_planning_poker.models.room import Room
        try:
            room = Room.objects.get(code=self.room_code)
            if room.participants.filter(id=self.user.id).exists():
                room.participants.remove(self.user)
        except Room.DoesNotExist:
            pass