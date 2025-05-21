import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class RevealVotesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('RevealVotesConsumer connect')
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f"reveal_{self.room_code}"
        self.user = self.scope['user']

        print(f"User: {self.user.username}")
        print(f"GroupName: {self.group_name}")
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Called when a reveal command is received.
        """
        data = json.loads(text_data)
        story_id = data['story_id']
        action = data['action']

        if action == 'reveal':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'reveal_votes',
                    'reveal': {
                        'story_id': story_id,
                        'username': self.user.username,
                        'value': True,
                    }
                }
            )
            asyncio.create_task(self.safe_story_reveal_update(story_id, True))
        elif action == 'unreveal':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'reveal_votes',
                    'reveal': {
                        'story_id': story_id,
                        'username': self.user.username,
                        'value': False,
                    }
                }
            )
            asyncio.create_task(self.safe_story_reveal_update(story_id, False))
        elif action == 'reset':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'reset_votes',
                    'reset': {
                        'story_id': story_id,
                        'username': self.user.username,
                    }
                }
            )
            asyncio.create_task(self.safe_story_reveal_update(story_id, False))

    async def reveal_votes(self, event):
        """
        Send the reveal flag to the clients.
        """
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'reveal': event['reveal']
        }))

    async def reset_votes(self, event):
        """
        Send the reveal flag to the clients.
        """
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'reset': event['reset']
        }))

    async def safe_story_reveal_update(self, story_id, reveal):
        """
        Safely update the story in the database.
        """
        try:
            await self.story_reveal_update(story_id, reveal)
        except Exception as e:
            print(f"Async DB update failed: {e}")

    @database_sync_to_async
    def story_reveal_update(self, story_id, reveal):
        from simple_planning_poker.models.story import Story
        """
        Save or update the story in the database.
        """
        try:
            story = Story.objects.get(id=story_id)
            story.is_revealed = reveal
            story.save()
        except Story.DoesNotExist:
            print(f"Story {story_id} does not exist")
        except Exception as e:
            print(f"Error updating story: {e}")


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