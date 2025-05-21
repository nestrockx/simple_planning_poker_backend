from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token_list = query_params.get('token', None)

        if not token_list:
            raise AuthenticationFailed("No token provided.")

        token = token_list[0]

        try:
            user, auth = await database_sync_to_async(TokenAuthentication().authenticate_credentials)(token)
            scope['user'] = user
        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid token or user.")

        return await super().__call__(scope, receive, send)
