from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from simple_planning_poker.models.userprofile import UserProfile

class DeleteUserDataView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid username or password'}, status=401)

        # Delete associated UserProfile
        UserProfile.objects.filter(user=user).delete()

        # Delete user
        user.delete()

        return Response({'success': 'User and all associated data deleted'}, status=200)