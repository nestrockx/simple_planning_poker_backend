from rest_framework import serializers
from simple_planning_poker.models.vote import Vote
from simple_planning_poker.serializers.user import UserSerializer

class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'story_id', 'user', 'value', 'voted_at']
        read_only_fields = ['user_id', 'voted_at']