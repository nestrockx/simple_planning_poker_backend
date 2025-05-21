from simple_planning_poker.serializers.story import StorySerializer
from simple_planning_poker.models.story import Story
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class StoryDeleteView(APIView):
    def delete(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        story.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)