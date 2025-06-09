from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response

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