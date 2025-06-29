from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CombinedTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Try to get token from cookies
        headers = dict(scope.get("headers", []))
        raw_cookie = headers.get(b"cookie", b"").decode("utf-8")
        cookies = {}
        for item in raw_cookie.split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                cookies[key] = value

        token = cookies.get("accessToken")

        # If no token in cookie, try query string token
        if not token:
            query_string = scope.get('query_string', b'').decode()
            query_params = parse_qs(query_string)
            token_list = query_params.get('token', None)
            if token_list:
                token = token_list[0]

        if not token:
            raise AuthenticationFailed("No token provided.")

        try:
            user, _ = await database_sync_to_async(TokenAuthentication().authenticate_credentials)(token)
            scope['user'] = user
        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid token or user.")

        return await super().__call__(scope, receive, send)
