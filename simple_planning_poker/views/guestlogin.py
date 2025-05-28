from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.throttling import AnonRateThrottle

from simple_planning_poker.models.userprofile import UserProfile

import random
import string

class CustomThrottle(AnonRateThrottle):
    rate = '5/hour'

class GuestLoginView(APIView):
    throttle_classes = [CustomThrottle]
    permission_classes = [AllowAny]

    def post(self, request):
        username = self._generate_guest_username()
        password = self._generate_random_password()

        user = User.objects.create_user(username=username, password=password)

        nickname = request.data.get('nickname')
        UserProfile.objects.create(user=user, nickname=nickname)

        token = Token.objects.create(user=user)

        response = HttpResponse(status=201)
        response.set_cookie(
            key='accessToken',
            value=token.key,
            max_age=60*60*24,  # 1 day
            httponly=True,
            secure=True, # Set to True in production with HTTPS
            samesite='None',
            path='/',
        )
        return response

    def _generate_guest_username(self):
        while True:
            suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            username = f"guest_{suffix}"
            if not User.objects.filter(username=username).exists():
                return username
            
    def _generate_random_password(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
