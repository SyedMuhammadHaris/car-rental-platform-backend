from datetime import datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import stripe
from apps.booking.models.booking import Booking
from apps.booking.serializers.booking_serializer import BookingSerializer
from apps.vehicle.models.vehicle import Vehicle
from constants.common_status import CommonStatus
from utils.custom_responses import SuccessResponse
from utils.error_handler import CustomAPIException
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .open_api_schemas import (
    booking_create_success_example,
    booking_create_missing_vehicle_example,
    booking_create_vehicle_not_found_example,
    booking_create_conflict_example,
    booking_list_success_example,
    booking_list_not_found_example,
    create_booking_payload_schema
)


class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new booking",
        description="Create a new vehicle booking for the authenticated user",
        request=create_booking_payload_schema,
        responses={
            201: BookingSerializer,
            400: None,
            404: None,
        },
        examples=[
            booking_create_success_example,
            booking_create_missing_vehicle_example,
            booking_create_vehicle_not_found_example,
            booking_create_conflict_example
        ]
    )
    def post(self, request):
        user = request.user
        vehicle_id = request.data.get("vehicle_id")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        if not vehicle_id:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Vehicle ID is required",
            )

        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        if not vehicle:
            return SuccessResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                message="Vehicle not found",
            )

        if not start_date or not end_date:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Start date and end date are required",
            )

        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")

        if start_date > end_date:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Start date cannot be after end date",
            )

        if start_date < datetime.now():
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Cannot book dates in the past",
            )

        conflicting_booking = Booking.objects.filter(
            vehicle_id=vehicle_id,
            status=CommonStatus.ACTIVE.value,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).first()

        if conflicting_booking:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"Vehicle is already booked for the selected dates.",
            )

        payload = {"user": user.id, "vehicle": vehicle_id, **request.data}
        serializer = BookingSerializer(data=payload)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return SuccessResponse(
                status_code=status.HTTP_201_CREATED,
                data=serializer.data,
                message="Booking created successfully",
            )
    

    @extend_schema(
        summary="Get user bookings",
        description="Retrieve all bookings for the authenticated user, optionally filtered by from date",
        parameters=[
            OpenApiParameter(
                name='from',
                location=OpenApiParameter.QUERY,
                description='Filter bookings from this date (YYYY-MM-DD format)',
                required=False,
                type=str
            )
        ],
        responses={
            200: BookingSerializer,
            404: None,
        },
        examples=[
            booking_list_success_example,
            booking_list_not_found_example
        ]
    )
    def get(self, request):
        user = request.user
        from_date = request.query_params.get("from")
        
        user_bookings = Booking.objects.none()
        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            user_bookings = Booking.objects.filter(
                user=user, start_date__gte=from_date
            ).order_by("-created_at")
        else:
            user_bookings = Booking.objects.filter(user=user).order_by("-created_at")

        if user_bookings.exists() == False:
            return SuccessResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                message="No bookings found for this user",
            )
        
        serializer = BookingSerializer(user_bookings, many=True)
        # amount_payable = 20 * 2 #(rental rate * number of days)
        # session = stripe.checkout.Session.create(
        #         success_url="https://example.com/success",
        #         line_items=[
        #             {
        #                 "currency": "usd",
        #                 "unit_amount": int(amount_payable * 100),
        #                 "product_data": {
        #                     "name": "Car Rental Booking",
        #                 },
        #             }
        #         ],
        #         metadata={"booking_id": serializer.data["id"], "user_id": user.id},
        #         mode="payment",
        #     )
        return SuccessResponse(
            status_code=status.HTTP_200_OK,
            data=serializer.data,
            message="Bookings retrieved successfully",
        )
