from django.http import HttpResponse
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from simple_planning_poker.authentication import CookieTokenAuthentication
from rest_framework.authentication import TokenAuthentication

class LogoutView(APIView):
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = HttpResponse(status=204)
        response.delete_cookie(
            key = "accessToken",
            samesite="Lax",
            path="/",
        )
        return response
