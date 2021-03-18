import logging

from rest_framework.permissions import BasePermission

from teacherplus.users.helpers import UpdatePasswordHelper

logger = logging.getLogger(__name__)


class UpdatePasswordPermission(BasePermission):
    """ Permission class to check if the user updated password token in valid"""

    def has_permission(self, request, view):
        try:
            token = request.data.get("token")
            email = request.data.get("email")
            return UpdatePasswordHelper.verify_update_password(token, email)
        except Exception as permission_error:
            message = f"An exception has occurred while validating the token {permission_error}"
            logger.error(message)
            return False
