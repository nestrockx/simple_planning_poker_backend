from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieOrHeaderTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope.get("headers", []))

        # Try to get token from cookies
        raw_cookie = headers.get(b"cookie", b"").decode("utf-8")
        cookies = {}
        for item in raw_cookie.split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                cookies[key] = value

        token = cookies.get("accessToken")

        # If no token in cookie, try Authorization header
        if not token:
            auth_header = headers.get(b"authorization", b"").decode("utf-8")
            if auth_header.lower().startswith("token "):
                token = auth_header[6:].strip()  # Strip "Token "

        if not token:
            raise AuthenticationFailed("No token provided.")

        try:
            user, _ = await database_sync_to_async(TokenAuthentication().authenticate_credentials)(token)
            scope["user"] = user
        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid token or user.")

        return await super().__call__(scope, receive, send)
