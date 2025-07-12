import logging
from apps.vehicle.models.vehicle import Vehicle
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.vehicle.serializers.vehicle_serializer import VehicleSerializer
from utils.custom_responses import SuccessResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class VehicleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new vehicle",
        description="Add a new vehicle to the authenticated user's account",
        request=VehicleSerializer,
        responses={
            201: VehicleSerializer,
            400: None,
        },
        examples=[
            OpenApiExample(
                'Success Response',
                value={
                    "success": {
                        "code": 201,
                        "data": {
                            "object": "vehicle",
                            "id": 1,
                            "user_id": 1,
                            "make": "Toyota",
                            "model": "Corolla",
                            "year": 2020,
                            "plate": "ABC123",
                            "created_at": "2024-01-01T00:00:00Z",
                            "updated_at": "2024-01-01T00:00:00Z"
                        },
                        "message": "Vehicle created successfully"
                    }
                },
                response_only=True,
                status_codes=['201']
            ),
            OpenApiExample(
                'Duplicate Plate Error',
                value={
                    "error": {
                        "code": 400,
                        "data": None,
                        "message": "Plate already exists"
                    }
                },
                response_only=True,
                status_codes=['400']
            )
        ]
    )
    def post(self, request):
        user = request.user
        print(f"User: {user.id}")
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
            OpenApiExample(
                'Success Response',
                value={
                    "success": {
                        "code": 200,
                        "data": [
                            {
                                "object": "vehicle",
                                "id": 1,
                                "user_id": 1,
                                "make": "Toyota",
                                "model": "Corolla",
                                "year": 2020,
                                "plate": "ABC123",
                                "created_at": "2024-01-01T00:00:00Z",
                                "updated_at": "2024-01-01T00:00:00Z"
                            }
                        ],
                        "message": "Vehicles retrieved successfully"
                    }
                },
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'No Vehicles Found',
                value={
                    "success": {
                        "code": 404,
                        "data": [],
                        "message": "No vehicles"
                    }
                },
                response_only=True,
                status_codes=['404']
            )
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
