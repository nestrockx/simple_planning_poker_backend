from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from simple_planning_poker.authentication import CookieTokenAuthentication
from simple_planning_poker.serializers.userprofile import UserProfileSerializer

class UserProfileUpdateView(APIView):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        serializer = UserProfileSerializer(user_profile, data={'nickname': request.data.get('nickname')}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
