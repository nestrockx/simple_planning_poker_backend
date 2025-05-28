from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from simple_planning_poker.authentication import CookieTokenAuthentication
from simple_planning_poker.serializers.story import StorySerializer

class StoryCreateView(generics.CreateAPIView):
    serializer_class = StorySerializer
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]