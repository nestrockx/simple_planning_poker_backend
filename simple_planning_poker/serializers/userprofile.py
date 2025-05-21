from rest_framework import serializers

from simple_planning_poker.models.userprofile import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'moderator']