import jwt

from rest_framework import authentication, exceptions

from accounts.models import RevokedToken, User
from accounts.token import decode_access_token


class JWTAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate_header(self, request):
        return self.keyword

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).decode("utf-8")

        if not header:
            return None

        parts = header.split()

        if len(parts) != 2 or parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed(
                "Use Authorization: Bearer <token>."
            )

        token = parts[1]

        try:
            payload = decode_access_token(token)

        except jwt.ExpiredSignatureError as exc:
            raise exceptions.AuthenticationFailed(
                "Token expired."
            ) from exc

        except jwt.InvalidTokenError as exc:
            raise exceptions.AuthenticationFailed(
                "Invalid token."
            ) from exc

        if RevokedToken.objects.filter(jti=payload["jti"]).exists():
            raise exceptions.AuthenticationFailed(
                "Token revoked."
            )

        try:
            user = User.objects.select_related("role").get(
                id=payload["sub"],
                is_active=True,
            )

        except User.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed(
                "User is inactive or does not exist."
            ) from exc

        return user, payload