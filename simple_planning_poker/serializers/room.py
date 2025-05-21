from rest_framework import serializers
from simple_planning_poker.models.room import Room
from simple_planning_poker.serializers.user import UserSerializer
from simple_planning_poker.serializers.story import StorySerializer

class RoomSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    

    class Meta:
        model = Room
        fields = ['id', 'name', 'type', 'code', 'participants', 'created_by', 'created_at']
        read_only_fields = ['code']