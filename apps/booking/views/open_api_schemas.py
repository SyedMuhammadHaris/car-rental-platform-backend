from drf_spectacular.utils import OpenApiExample, OpenApiParameter

create_booking_payload_schema = {
    "application/json": {
        "type": "object",
        "properties": {
            "vehicle_id": {"type": "integer", "example": 1},
            "start_date": {
                "type": "string",
                "format": "date-time",
                "example": "2024-01-15 10:00",
            },
            "end_date": {
                "type": "string",
                "format": "date-time",
                "example": "2024-01-16 10:00",
            },
        },
        "required": ["vehicle_id", "start_date", "end_date"],
    }
}

# Booking POST examples
booking_create_success_example = OpenApiExample(
    "Success Response",
    value={
        "success": {
            "code": 201,
            "data": {
                "object": "booking",
                "id": 1,
                "user_id": 1,
                "vehicle_id": 1,
                "start_date": "2024-01-15T10:00:00Z",
                "end_date": "2024-01-16T10:00:00Z",
                "status": 1,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            },
            "message": "Booking created successfully",
        }
    },
    response_only=True,
    status_codes=["201"],
)

booking_create_missing_vehicle_example = OpenApiExample(
    "Missing Vehicle ID",
    value={"error": {"code": 400, "data": None, "message": "Vehicle ID is required"}},
    response_only=True,
    status_codes=["400"],
)

booking_create_vehicle_not_found_example = OpenApiExample(
    "Vehicle Not Found",
    value={"success": {"code": 404, "data": None, "message": "Vehicle not found"}},
    response_only=True,
    status_codes=["404"],
)

booking_create_conflict_example = OpenApiExample(
    "Booking Conflict",
    value={
        "error": {
            "code": 400,
            "data": None,
            "message": "Vehicle is already booked for the selected dates.",
        }
    },
    response_only=True,
    status_codes=["400"],
)

# Booking GET examples
booking_list_success_example = OpenApiExample(
    "Success Response",
    value={
        "success": {
            "code": 200,
            "data": [
                {
                    "object": "booking",
                    "id": 1,
                    "user_id": 1,
                    "vehicle_id": 1,
                    "start_date": "2024-01-15T10:00:00Z",
                    "end_date": "2024-01-16T10:00:00Z",
                    "status": 1,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            ],
            "message": "Bookings retrieved successfully",
        }
    },
    response_only=True,
    status_codes=["200"],
)

booking_list_not_found_example = OpenApiExample(
    "No Bookings Found",
    value={
        "success": {
            "code": 404,
            "data": None,
            "message": "No bookings found for this user",
        }
    },
    response_only=True,
    status_codes=["404"],
)
