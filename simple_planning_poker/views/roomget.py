from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from simple_planning_poker.models.room import Room
from simple_planning_poker.serializers.room import RoomSerializer

class RoomGetByCodeView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        code = self.kwargs.get("code")
        try:
            return Room.objects.get(code=code)
        except Room.DoesNotExist:
            raise NotFound("Room with this code does not exist.")
