from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response

from simple_planning_poker.models.userprofile import UserProfile

# class CustomRegisterAnonThrottle(AnonRateThrottle):
#     rate = '3/hour'

# class CustomRegisterUserThrottle(UserRateThrottle):
#     rate = '3/hour'

# Register
class RegisterView(APIView):
    # throttle_classes = [CustomRegisterAnonThrottle, UserRateThrottle]
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        nickname = request.data.get('nickname')
        password = request.data.get('password')
        if not username or not password or not nickname:
            return Response({'error': 'Username, nickname and password required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, nickname=nickname)

        token = Token.objects.create(user=user)

        json_response = Response({'accessToken': token.key}, status = 201)
                
        json_response.set_cookie(
            key='accessToken',
            value=token.key,
            max_age=60*60*24, # 1 day
            httponly=True,
            secure=True,
            samesite='Lax',
            path='/',
        )
        return json_response
    