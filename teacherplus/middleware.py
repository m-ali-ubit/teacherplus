import logging
from collections import OrderedDict

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from teacherplus.utils.response_handler import get_default_message

logger = logging.getLogger(name=__name__)


class TransformResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        # pylint: disable=unused-argument, no-self-use
        if isinstance(response, Response):
            if isinstance(response.data, str):
                message = response.data
                data = {"message": message}
            elif response.data:
                data = response.data
                if isinstance(data, (OrderedDict, dict)):
                    message = response.data.pop(
                        "message", get_default_message(response.status_code)
                    )
                    data["message"] = message
            else:
                message = get_default_message(response.status_code)
                data = {"message": message}
            response.data = data
        return response

    def process_exception(self, request, exception):
        # pylint: disable=unused-argument, no-self-use
        error_message = f"An exception has occurred with error: {exception}"
        response_data = {"data": [], "message": error_message}
        logger.error(error_message)
        return JsonResponse(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
