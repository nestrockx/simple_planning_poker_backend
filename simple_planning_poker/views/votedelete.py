from django.shortcuts import get_object_or_404
from simple_planning_poker.authentication import CookieTokenAuthentication
from simple_planning_poker.models.story import Story
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class VoteDeleteByStoryView(APIView):
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        votes = story.votes.all()
        votes.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)