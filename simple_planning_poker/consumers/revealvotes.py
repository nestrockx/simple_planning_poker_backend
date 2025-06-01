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
        """
        Called when a reveal command is received.
        """
        data = json.loads(text_data)
        action = data['action']
        story_id = data['story_id']

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
        elif action == 'vote':
            vote_value = data['value']
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
            asyncio.create_task(self.safe_save_vote_update(story_id, self.user, vote_value))
        elif action == 'add_story':
            title = data['title']
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'add_story',
                    'story': {
                        'id': story_id,
                        'title': title,
                        'is_revealed': False,
                    }
                }
            )
        elif action == 'remove_story':
            title = data['title']
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'remove_story',
                    'story': {
                        'id': story_id,
                        'title': title,
                        'is_revealed': False,
                    }
                }
            )
        elif action == 'summon':
            title = data['title']
            is_revealed = data['is_revealed']
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'summon',
                    'story': {
                        'id': story_id,
                        'title': title,
                        'is_revealed': is_revealed,
                    }
                }
            )

    async def summon(self, event):
        """
        Send the active story to the clients.
        """
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'story': event['story']
        }))

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

    async def vote_update(self, event):
        """
        Send the updated vote to the client.
        """
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'vote': event['vote']
        }))

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

    ## limit users in the room to 10
    ## limit stories in the room to 10
    ## zustand redux
    ## celery for speed
    ## more reactive with useEffect
    ## validating existing user
    ## editable user nickname
    ## emoji wheel