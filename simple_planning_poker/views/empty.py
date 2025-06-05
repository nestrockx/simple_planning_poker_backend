from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from simple_planning_poker.authentication import CookieTokenAuthentication
from rest_framework.authentication import TokenAuthentication

class EmptyView(APIView):
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(status=204)  # No Content
