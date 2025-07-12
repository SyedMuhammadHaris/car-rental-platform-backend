from rest_framework import status
from rest_framework.response import Response


class SuccessResponse(Response):
    def __init__(self, data=None, status_code=None, message=None):
        response_data = {
            "code": status_code if status_code else 200,
            "data": data if data else None,
            "message": message if message else None,
        }
        super().__init__(data={"success": response_data}, status=200)


class ErrorResponse(Response):
    def __init__(self, data=None, status_code=None, message=None):
        response_data = {
            "code": status_code if status_code else 200,
            "data": data if data else None,
            "message": message if message else None,
        }
        super().__init__(data={"error": response_data}, status=status.HTTP_200_OK)