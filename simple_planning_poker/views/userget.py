from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth.models import User

from simple_planning_poker.authentication import CookieTokenAuthentication
from simple_planning_poker.serializers.user import UserSerializer
from rest_framework.authentication import TokenAuthentication

class UserGetByTokenView(APIView):
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserGetByIdView(APIView):
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user)
            
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    