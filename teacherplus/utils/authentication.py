from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework_jwt.utils import jwt_payload_handler


def create_token(user, expiry):
    payload = jwt_payload_handler(user)
    payload["exp"] = expiry
    token = jwt.encode(payload, settings.JWT_SECRET_KEY)
    return token.decode("unicode_escape")


def create_login_token(user, _remember_me=False):
    expiry = timezone.now() + timedelta(days=30)
    return create_token(user, expiry)
