from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken

from teacherplus.utils.strings import (
    DEFAULT_FAILURE_MESSAGE,
    DEFAULT_SUCCESS_MESSAGE,
)


def get_default_message(status_code):
    if status_code in [
        status.HTTP_200_OK,
        status.HTTP_201_CREATED,
        status.HTTP_204_NO_CONTENT,
    ]:
        return DEFAULT_SUCCESS_MESSAGE
    return DEFAULT_FAILURE_MESSAGE


def validation_exception_handler(validation_exception):
    data = {}
    for key in validation_exception.detail.keys():
        data[key] = "".join(str(validation_exception.detail.get(key)))
    return {"errors": data}


def custom_exception_handler(exc, context):

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    errors_mappings = {
        InvalidToken: ["Provided token is invalid"],
        Http404: ["Object with given ID does not exist"],
        NotAuthenticated: ["Authentication credentials were not provided"],
    }

    error_types = tuple([ValidationError, InvalidToken, Http404, NotAuthenticated])

    is_an_error = isinstance(exc, error_types)

    if response and is_an_error:

        for error_type, error_messages in errors_mappings.items():
            if isinstance(exc, error_type):
                response.data = {"details": error_messages}

        data = {"errors": {}}

        for key, value in response.data.items():
            if key != "message":
                data["errors"][key] = value
        response.data = data

    return response
