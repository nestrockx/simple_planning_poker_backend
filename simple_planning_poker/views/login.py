from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.http import HttpResponse

# class CustomLoginAnonThrottle(AnonRateThrottle):
#     rate = '10/hour'

# class CustomLoginUserThrottle(UserRateThrottle):
#     rate = '10/hour'

# Login (token auth)
class CustomAuthToken(ObtainAuthToken):
    # throttle_classes = [CustomLoginAnonThrottle, CustomLoginUserThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        
        response = HttpResponse(status=201)
        response.set_cookie(
            key='accessToken',
            value=token.key,
            max_age=60*60*24, # 1 day
            httponly=True,
            secure=True,
            samesite='Lax',
            path='/',
        )
        return response