from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

# Login (token auth)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        
        response = HttpResponse(status=201)
        response.set_cookie(
            key='accessToken',
            value=token.key,
            max_age=60*60*24,  # 1 day
            httponly=True,
            secure=False, # Set to True in production with HTTPS
            samesite='Lax',
            path='/',
        )
        return response