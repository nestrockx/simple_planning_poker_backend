from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.http import HttpResponse

class CustomAnonThrottle(AnonRateThrottle):
    rate = '10/hour'

class CustomUserThrottle(UserRateThrottle):
    rate = '10/hour'

# Login (token auth)
class CustomAuthToken(ObtainAuthToken):
    throttle_classes = [CustomAnonThrottle, CustomUserThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        
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