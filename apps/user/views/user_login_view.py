from rest_framework.views import APIView
from rest_framework import status
from apps.user.models.user import User
from apps.user.serializers.user_serializer import UserSerializer
from utils.common import is_valid_email
from utils.custom_responses import SuccessResponse
from utils.error_handler import CustomAPIException
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .open_api_schemas import user_login_success_example, user_login_invalid_credentials_example, user_login_payload_schema

class UserLoginView(APIView):
    @extend_schema(
        summary="User login",
        description="Authenticate user with email and password to get access token",
        request=user_login_payload_schema,
        responses={
            200: None,
            401: None,
        },
        examples=[user_login_success_example, user_login_invalid_credentials_example],
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
