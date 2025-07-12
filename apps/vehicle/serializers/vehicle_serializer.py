from rest_framework import serializers
from apps.vehicle.models import Vehicle
from rest_framework.validators import UniqueValidator

class VehicleSerializer(serializers.ModelSerializer):
    make = serializers.CharField(
        required=True,
        error_messages={
            "required": "Make is required",
        },
    )
    model = serializers.CharField(
        required=True,
        error_messages={
            "required": "Model is required",
        },
    )
    year = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "Year is required",
            "invalid": "Year must be a valid integer",
        },
    )
    plate = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=Vehicle.objects.all(), message="Plate already exists")
        ],
        error_messages={
            "required": "Plate is required",
        },
    )

    class Meta:
        model = Vehicle
        fields = [
            "user",
            "make",
            "model",
            "year",
            "plate",
        ]

    def create(self, validated_data):
        vehicle = Vehicle(
            user=validated_data["user"],  # Assuming the user is passed in the context
            make=validated_data["make"],
            model=validated_data["model"],
            year=validated_data["year"],
            plate=validated_data["plate"],
        )
        vehicle.save()
        return vehicle

    def to_representation(self, instance):
        return {
            "object": "vehicle",
            "id": instance.id,
            "user_id": instance.user_id,
            "make": instance.make,
            "model": instance.model,
            "year": instance.year,
            "plate": instance.plate,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
