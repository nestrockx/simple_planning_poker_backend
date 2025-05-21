from rest_framework import serializers
from django.contrib.auth.models import User

from simple_planning_poker.serializers.userprofile import UserProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']