from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from simple_planning_poker.authentication import CookieTokenAuthentication
from simple_planning_poker.models.vote import Vote
from simple_planning_poker.serializers.vote import VoteSerializer
from rest_framework.authentication import TokenAuthentication

class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        story_id = serializer.validated_data['story_id']
        user_id = self.request.user
        value = serializer.validated_data['value']

        Vote.objects.update_or_create(
            story_id=story_id,
            user_id=user_id,
            defaults={'value': value}
        )