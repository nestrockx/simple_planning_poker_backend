from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get headers and extract the 'cookie' header
        headers = dict(scope.get("headers", []))
        raw_cookie = headers.get(b"cookie", b"").decode("utf-8")

        # Parse the cookie string into a dict
        cookies = {}
        for item in raw_cookie.split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                cookies[key] = value

        token = cookies.get("accessToken")

        if not token:
            raise AuthenticationFailed("No token provided.")

        try:
            user, _ = await database_sync_to_async(TokenAuthentication().authenticate_credentials)(token)
            scope["user"] = user
        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid token or user.")

        return await super().__call__(scope, receive, send)
