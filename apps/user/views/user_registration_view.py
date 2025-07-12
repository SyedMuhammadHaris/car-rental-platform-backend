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

"Handle errros globally"

class UserRegistrationView(APIView):
    @extend_schema(
        summary="Register a new user",
        description="Create a new user account with email, password, and personal information",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: None,
        },
        examples=[
            OpenApiExample(
                'Success Response',
                value={
                    "success": {
                        "code": 201,
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
                        "message": "User registered successfully"
                    }
                },
                response_only=True,
                status_codes=['201']
            ),
            OpenApiExample(
                'Error Response',
                value={
                    "error": {
                        "code": 400,
                        "data": None,
                        "message": "Password is required"
                    }
                },
                response_only=True,
                status_codes=['400']
            )
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
