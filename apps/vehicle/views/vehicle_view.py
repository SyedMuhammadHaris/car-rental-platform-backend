import logging
from apps.vehicle.models.vehicle import Vehicle
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.vehicle.serializers.vehicle_serializer import VehicleSerializer
from utils.custom_responses import SuccessResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .open_api_schemas import (
    vehicle_create_success_example,
    vehicle_create_duplicate_plate_example,
    vehicle_list_success_example,
    vehicle_list_not_found_example,
    add_vehcile_payload_schema
)


class VehicleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new vehicle",
        description="Add a new vehicle to the authenticated user's account",
        request=add_vehcile_payload_schema,
        responses={
            201: VehicleSerializer,
            400: None,
        },
        examples=[
            vehicle_create_success_example,
            vehicle_create_duplicate_plate_example
        ]
    )
    def post(self, request):
        user = request.user
        payload = {"user": user.id, **request.data}
        serializer = VehicleSerializer(data=payload)
        if serializer.is_valid(raise_exception=True):
            vehicle = serializer.save()
            return SuccessResponse(
                status_code=status.HTTP_201_CREATED,
                data=serializer.to_representation(vehicle),
                message="Vehicle created successfully",
            )
    
    @extend_schema(
        summary="Get user vehicles",
        description="Retrieve all vehicles belonging to the authenticated user",
        responses={
            200: VehicleSerializer,
            404: None,
        },
        examples=[
            vehicle_list_success_example,
            vehicle_list_not_found_example
        ]
    )
    def get(self, request):
        user = request.user
        vehicles = Vehicle.objects.filter(user=user)
        if not vehicles.exists():
            return SuccessResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                data=[],
                message="No vehicles",
            )
        serializer = VehicleSerializer(vehicles, many=True)
        return SuccessResponse(
            status_code=status.HTTP_200_OK,
            data=serializer.data,
            message="Vehicles retrieved successfully",
        )
