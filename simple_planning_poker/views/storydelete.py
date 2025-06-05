from simple_planning_poker.authentication import CookieTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from simple_planning_poker.models.story import Story
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

class StoryDeleteView(APIView):
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        story.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)