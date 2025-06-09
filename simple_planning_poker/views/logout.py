from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response(status=204)
        response.delete_cookie(
            key = "accessToken",
            samesite="Lax",
            path="/",
        )
        return response
