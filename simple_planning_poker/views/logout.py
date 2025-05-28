from django.http import HttpResponse
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from simple_planning_poker.authentication import CookieTokenAuthentication

class LogoutView(APIView):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = HttpResponse(status=204)
        response.delete_cookie(
            key = "accessToken",
            samesite="None",
            path="/",
        )
        return response
