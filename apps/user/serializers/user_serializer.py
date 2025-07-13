from rest_framework import serializers
from apps.user.models import User  # Adjust the import based on your User model location
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from config.settings import env


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Email already exists")
        ],
        error_messages={
            "required": "Email is required",
        },
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        error_messages={
            "required": "Password is required",
            "min_length": "Password must be at least 8 characters long",
        },
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "password"]
    
    def validate_phone(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Phone number must be numeric and at least 10 digits long.")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            password=make_password(
                validated_data.get("password"),
                salt=env("PASSWORD_SALT"),
                hasher="default",
            ),
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            status=1,
        )
        user.save()
        return user
    

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        return {
            "object": "user",
            "id": instance.id,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "phone": instance.phone,
            "status": instance.status,
            "phone_verified": instance.phone_verified,
            "email_verified": instance.email_verified,
            "access_token": str(token.access_token),
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
