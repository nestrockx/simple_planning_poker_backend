from rest_framework import generics, permissions
from simple_planning_poker.serializers.story import StorySerializer

class StoryCreateView(generics.CreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]