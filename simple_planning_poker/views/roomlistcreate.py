from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from simple_planning_poker.authentication import CookieTokenAuthentication
from simple_planning_poker.models.room import Room
from simple_planning_poker.serializers.room import RoomSerializer
from rest_framework.authentication import TokenAuthentication

class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by('created_at')
    serializer_class = RoomSerializer
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)