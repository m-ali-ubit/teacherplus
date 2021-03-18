import logging
from datetime import datetime, timedelta
import jwt
from django.core.cache import cache


from config.settings import local as settings
from teacherplus.exceptions import DataNullOrTokenInvalidException

logger = logging.getLogger(__name__)


class UpdatePasswordHelper:
    key_prefix = "UPDATE_PASSWORD"

    @classmethod
    def generate_update_password_url(cls, user, base_url):
        user_payload = {
            "sub": user.id,
            "exp": datetime.now()
            + timedelta(seconds=settings.UPDATE_PASSWORD_TOKEN_TIMEOUT),
        }
        encoded_token = jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256")
        cache.set(
            cls.get_key_value_from_email(user.email),
            user_payload,
            settings.UPDATE_PASSWORD_TOKEN_TIMEOUT,
        )
        update_password_link = (
            base_url
            + settings.UPDATE_PASSWORD_REDIRECT_URL
            + f'?token={encoded_token.decode("utf-8")}&email={user.email}'
        )

        logger.info(
            f"Payload successfully saved for the update password token of {user.email}"
        )
        return update_password_link

    @classmethod
    def verify_update_password(cls, token: str, email: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            payload_data_cache = cache.get(cls.get_key_value_from_email(email))
            if payload == payload_data_cache:
                logger.info(f"Update password token verified for {email}")
                return True
            logger.info(f"Update password token is invalid for {email}")
            raise DataNullOrTokenInvalidException
        except jwt.ExpiredSignatureError:
            logger.error("Token Signature has been expired")
            return False

    @classmethod
    def get_key_value_from_email(cls, email: str):
        return f"{cls.key_prefix}:{email}"

    @classmethod
    def invalidate_reset_password_token(cls, email: str):
        key = cls.get_key_value_from_email(email)
        cache.delete(key)
        logger.info(f"{key} key removed from the cache")
