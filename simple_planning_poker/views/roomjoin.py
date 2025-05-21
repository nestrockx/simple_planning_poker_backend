from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from simple_planning_poker.models.room import Room
from simple_planning_poker.serializers.room import RoomSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class RoomJoinByCodeView(APIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
        
    def post(self, request, code):
        try:
            room = Room.objects.get(code=code)
        except Room.DoesNotExist:
            raise NotFound("Room with this code does not exist.")
        user = request.user
        room.participants.add(user)
        room.save()
        return Response({
            "message": f"You joined room {room.name}",
            "room_code": room.code,
            "participants": [user.username for user in room.participants.all()]
        })