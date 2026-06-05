from datetime import timedelta
from uuid import uuid4
import jwt
from django.conf import settings
from django.utils import timezone

def create_access_token(user):
    now = timezone.now()
    expires_at = now + timedelta(minutes=settings.JWT_ACCESS_TTL_MINUTES)
    payload = {
        "sub": str(user.id),
        'email': user.email,
        'role': user.role.code,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": uuid4().hex,
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, payload

def decode_access_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
