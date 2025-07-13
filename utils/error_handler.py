import logging

from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated, APIException
from rest_framework_simplejwt.exceptions import InvalidToken
from utils.custom_responses import ErrorResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logging.exception(exc)
    message = "Something went wrong"

    if response:
        message = response.data.get("detail", message)

    if response is None:
        message = str(exc) or "Internal server error"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if hasattr(exc, "status_code"):
            status_code = exc.status_code

        return ErrorResponse(status_code=status_code, data=None, message=message)

    if isinstance(exc, InvalidToken) or isinstance(exc, NotAuthenticated):
        return ErrorResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            data=None,
            message="Unauthenticated",
        )

    if isinstance(exc, ValidationError):
        error_messages = []
        for field, errors in response.data.items():
            for error in errors:
                if isinstance(error, dict):
                    # Handle nested serializer errors
                    for nested_errors in error.items():
                        for nested_error in nested_errors:
                            error_messages.append(f"{nested_error}")
                else:
                    error_messages.append(f"{error}")

        message = ", ".join(error_messages)

    return ErrorResponse(status_code=response.status_code, data=None, message=message)


class CustomAPIException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(message)
