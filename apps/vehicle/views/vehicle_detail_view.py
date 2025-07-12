from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.booking.models.booking import Booking
from apps.vehicle.models.vehicle import Vehicle
from apps.vehicle.serializers.vehicle_serializer import VehicleSerializer
from constants.common_status import CommonStatus
from utils.custom_responses import SuccessResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class VehicleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update a vehicle",
        description="Update vehicle details for the authenticated user's vehicle",
        parameters=[
            OpenApiParameter(
                name='vehicle_id',
                location=OpenApiParameter.PATH,
                description='ID of the vehicle to update',
                required=True,
                type=int
            )
        ],
        request=VehicleSerializer,
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
                        "data": {
                            "object": "vehicle",
                            "id": 1,
                            "user_id": 1,
                            "make": "Toyota",
                            "model": "Camry",
                            "year": 2021,
                            "plate": "ABC123",
                            "created_at": "2024-01-01T00:00:00Z",
                            "updated_at": "2024-01-01T00:00:00Z"
                        },
                        "message": "Vehicle updated successfully"
                    }
                },
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'Vehicle Not Found',
                value={
                    "success": {
                        "code": 404,
                        "data": None,
                        "message": "Vehicle not found"
                    }
                },
                response_only=True,
                status_codes=['404']
            )
        ]
    )
    def put(self, request, vehicle_id):
        user = request.user
        vehicle = Vehicle.objects.filter(id=vehicle_id, user=user).first()
        if not vehicle:
            return SuccessResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                message="Vehicle not found",
            )
        
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            updated_vehicle = serializer.save()
            return SuccessResponse(
                status_code=status.HTTP_200_OK,
                data=serializer.to_representation(updated_vehicle),
                message="Vehicle updated successfully",
            )
    
    @extend_schema(
        summary="Delete a vehicle",
        description="Delete a vehicle if it has no active bookings",
        parameters=[
            OpenApiParameter(
                name='vehicle_id',
                location=OpenApiParameter.PATH,
                description='ID of the vehicle to delete',
                required=True,
                type=int
            )
        ],
        responses={
            200: None,
            400: None,
            404: None,
        },
        examples=[
            OpenApiExample(
                'Success Response',
                value={
                    "success": {
                        "code": 200,
                        "data": None,
                        "message": "Vehicle deleted successfully"
                    }
                },
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'Vehicle Has Active Booking',
                value={
                    "success": {
                        "code": 400,
                        "data": None,
                        "message": "Cannot delete vehicle while it has active booking"
                    }
                },
                response_only=True,
                status_codes=['400']
            ),
            OpenApiExample(
                'Vehicle Not Found',
                value={
                    "success": {
                        "code": 404,
                        "data": None,
                        "message": "Vehicle not found"
                    }
                },
                response_only=True,
                status_codes=['404']
            )
        ]
    )
    def delete(self, request, vehicle_id):
        user = request.user
        vehicle = Vehicle.objects.filter(id=vehicle_id, user=user).first()
        if not vehicle:
            return SuccessResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                message="Vehicle not found",
            )
        
        # Ensure the vehicle is not booked before deletion
        booking = Booking.objects.filter(vehicle_id=vehicle.pk, status=CommonStatus.ACTIVE.value).first()
        if booking:
            return SuccessResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                data=None,
                message="Cannot delete vehicle while it has active booking",
            )
    
        vehicle.delete()
        return SuccessResponse(
            status_code=status.HTTP_200_OK,
            data=None,
            message="Vehicle deleted successfully",
        )