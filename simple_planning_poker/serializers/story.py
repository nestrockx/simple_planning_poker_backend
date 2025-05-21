from rest_framework import serializers
from simple_planning_poker.models.story import Story
from simple_planning_poker.serializers.vote import VoteSerializer

class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = ['id', 'title', 'is_active', 'is_revealed', 'room_id', 'created_at']