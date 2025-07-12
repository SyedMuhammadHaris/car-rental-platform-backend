from rest_framework.views import APIView
from rest_framework import status
from apps.user.models.user import User
from apps.user.serializers.user_serializer import UserSerializer
from utils.common import is_valid_email
from utils.custom_responses import SuccessResponse
from utils.error_handler import CustomAPIException
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class UserLoginView(APIView):
    @extend_schema(
        summary="User login",
        description="Authenticate user with email and password to get access token",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'format': 'email', 'example': 'john.doe@example.com'},
                    'password': {'type': 'string', 'example': 'mysecretpassword'}
                },
                'required': ['email', 'password']
            }
        },
        responses={
            200: UserSerializer,
            400: None,
            404: None,
        },
        examples=[
            OpenApiExample(
                'Success Response',
                value={
                    "success": {
                        "code": 200,
                        "data": {
                            "object": "user",
                            "id": 1,
                            "email": "john.doe@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "phone": "1234567890",
                            "status": 1,
                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                        },
                        "message": "User login successfully"
                    }
                },
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'Invalid Password',
                value={
                    "error": {
                        "code": 400,
                        "data": None,
                        "message": "Incorect password"
                    }
                },
                response_only=True,
                status_codes=['400']
            ),
            OpenApiExample(
                'User Not Found',
                value={
                    "error": {
                        "code": 404,
                        "data": None,
                        "message": "User not registered"
                    }
                },
                response_only=True,
                status_codes=['404']
            )
        ]
    )
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if not email or not password:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Email and password are required",
            )
        
        if is_valid_email(email) == False:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid email format",
            )
        
        print("Email:", email)
        user = User.objects.filter(email=email).first()
        if user is None:
            raise CustomAPIException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not registered",
            )
        if user.check_password(password) == False:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Incorect password",
            )
        
        return SuccessResponse(
            data=UserSerializer(user).data,
            message="User login successfully",
            status_code=status.HTTP_200_OK,
        )