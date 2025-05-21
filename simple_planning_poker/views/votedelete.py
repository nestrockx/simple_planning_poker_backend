from django.shortcuts import get_object_or_404
from simple_planning_poker.models.story import Story
from simple_planning_poker.serializers.vote import VoteSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class VoteDeleteByStoryView(APIView):
    def delete(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        votes = story.votes.all()
        votes.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)