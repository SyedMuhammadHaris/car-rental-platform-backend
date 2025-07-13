import logging
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.serializers.user_serializer import UserSerializer
from utils.custom_responses import ErrorResponse, SuccessResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .open_api_schemas import (
    user_register_success_example,
    user_register_duplicate_email_example
)

"Handle errros globally"

class UserRegistrationView(APIView):
    @extend_schema(
        summary="Register a new user",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: None,
        },
        examples=[
            user_register_success_example,
            user_register_duplicate_email_example
        ]
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(
            data=serializer.data,
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED,
        )
