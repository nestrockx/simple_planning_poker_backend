from rest_framework import generics, permissions
from simple_planning_poker.models.room import Room
from simple_planning_poker.serializers.room import RoomSerializer

class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by('created_at')
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)