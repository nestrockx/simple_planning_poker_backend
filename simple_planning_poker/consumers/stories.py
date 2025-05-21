import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class StoriesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('StoriesConsumer connect')
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f"stories_{self.room_code}"
        self.user = self.scope['user']

        print(f"User: {self.user.username}")
        print(f"GroupName: {self.group_name}")
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Called when a stories update command is received.
        """
        data = json.loads(text_data)
        story_id = data['story_id']
        title = data['title']
        is_revealed = data['is_revealed']
        action = data['action']

        if action == 'add':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'add_story',
                    'story': {
                        'id': story_id,
                        'title': title,
                        'is_revealed': is_revealed,
                        'username': self.user.username,
                    }
                }
            )
            asyncio.create_task(self.safe_story_reveal_update(story_id, True))
        elif action == 'remove':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'remove_story',
                    'story': {
                        'id': story_id,
                        'title': title,
                        'is_revealed': is_revealed,
                        'username': self.user.username,
                    }
                }
            )
            asyncio.create_task(self.safe_story_reveal_update(story_id, True))


    async def add_story(self, event):
        """
        Send the story addition to the clients.
        """
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'story': event['story']
        }))

    async def remove_story(self, event):
        """
        Send the story removal to the clients.
        """
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'story': event['story']
        }))

    ## limit users in the room to 10
    ## limit stories in the room to 10
    ## stories consumer
    ## users consumer
    ## join button for spectator user
    ## zustand redux
    ## celery for speed
    ## more reactive with useEffect
    ## validating existing user
    ## resetvotesconsumer