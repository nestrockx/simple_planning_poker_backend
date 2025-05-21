import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class VoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('VoteConsumer connect')
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f"vote_{self.room_code}"
        self.user = self.scope['user']

        print(f"User: {self.user.username}")
        print(f"GroupName: {self.group_name}")
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Called when a vote is received from the WebSocket.
        """
        data = json.loads(text_data)
        story_id = data['story_id']
        vote_value = data['value']

        # Broadcast vote update to all group members
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'vote_update',
                'vote': {
                    'story_id': story_id,
                    'username': self.user.username,
                    'value': vote_value,
                }
            }
        )

        # Save or update vote
        asyncio.create_task(self.safe_save_vote_update(story_id, self.user, vote_value))
        # await self.save_vote_update(story_id, self.user, vote_value)

    async def vote_update(self, event):
        """
        Send the updated vote to the client.
        """
        await self.send(text_data=json.dumps(event['vote']))

    async def safe_save_vote_update(self, story_id, user, value):
        """
        Safely update the vote in the database.
        """
        try:
            await self.save_vote_update(story_id, user, value)
        except Exception as e:
            print(f"Async DB update failed: {e}")

    @database_sync_to_async
    def save_vote_update(self, story_id, user, value):
        from simple_planning_poker.models.vote import Vote
        from simple_planning_poker.models.story import Story
        """
        Save or update the vote in the database.
        """
        story = Story.objects.get(id=story_id)

        # Create or update the vote
        Vote.objects.update_or_create(
            story_id=story,
            user_id=user,
            defaults={'value': value}
        )