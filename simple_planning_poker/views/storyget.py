from django.shortcuts import get_object_or_404
from simple_planning_poker.authentication import CookieTokenAuthentication
from simple_planning_poker.models.room import Room
from simple_planning_poker.serializers.story import StorySerializer
from simple_planning_poker.models.story import Story
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class StoryGetByRoomView(APIView):
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        stories = room.stories.all().order_by('created_at')
        serializer = StorySerializer(stories, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StoryGetByIdView(APIView):
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        serializer = StorySerializer(story)
        
        return Response(serializer.data, status=status.HTTP_200_OK)