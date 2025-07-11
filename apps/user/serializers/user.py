from rest_framework import serializers
from models import User  # Adjust the import based on your User model location
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']

    
    def validate_email(self, data):
        try:
            validate_email(data["email"])
            return data
        except ValidationError:
            return serializers.ValidationError({"email": "Invalid email format."})
        
    def validate_password(self, data):
        password = data.get("password")
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        return data


    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            passsword=validated_data["password"],
            status=1,  # Assuming default status is 1 for active users
        )
        return user

    def to_representation(self, instance):
        return super().to_representation(instance) 