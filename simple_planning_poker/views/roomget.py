from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from simple_planning_poker.authentication import CookieTokenAuthentication
from simple_planning_poker.models.room import Room
from simple_planning_poker.serializers.room import RoomSerializer
from rest_framework.authentication import TokenAuthentication

class RoomGetByCodeView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        code = self.kwargs.get("code")
        try:
            return Room.objects.get(code=code)
        except Room.DoesNotExist:
            raise NotFound("Room with this code does not exist.")
