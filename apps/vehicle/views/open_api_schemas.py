from drf_spectacular.utils import OpenApiExample, OpenApiParameter

from drf_spectacular.utils import OpenApiExample

add_vehcile_payload_schema = {
    "application/json": {
        "type": "object",
        "properties": {
            "make": {"type": "string", "example": "Toyota"},
            "model": {"type": "string", "example": "Corolla"},
            "year": {"type": "integer", "example": 2022},
            "plate": {"type": "string", "example": "ABC-1234"},
        },
        "required": ["make", "model", "year", "plate"],
    }
}

# Vehicle POST examples
vehicle_create_success_example = OpenApiExample(
    "Success Response",
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
                "updated_at": "2024-01-01T00:00:00Z",
            },
            "message": "Vehicle created successfully",
        }
    },
    response_only=True,
    status_codes=["201"],
)

vehicle_create_duplicate_plate_example = OpenApiExample(
    "Duplicate Plate Error",
    value={"error": {"code": 400, "data": None, "message": "Plate already exists"}},
    response_only=True,
    status_codes=["400"],
)

# Vehicle GET examples
vehicle_list_success_example = OpenApiExample(
    "Success Response",
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
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            ],
            "message": "Vehicles retrieved successfully",
        }
    },
    response_only=True,
    status_codes=["200"],
)

vehicle_list_not_found_example = OpenApiExample(
    "No Vehicles Found",
    value={"success": {"code": 404, "data": [], "message": "No vehicles"}},
    response_only=True,
    status_codes=["404"],
)

# Vehicle PUT/DELETE examples (for vehicle_detail_view)
vehicle_update_success_example = OpenApiExample(
    "Success Response",
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
                "updated_at": "2024-01-01T00:00:00Z",
            },
            "message": "Vehicle updated successfully",
        }
    },
    response_only=True,
    status_codes=["200"],
)

vehicle_update_not_found_example = OpenApiExample(
    "Vehicle Not Found",
    value={"success": {"code": 404, "data": None, "message": "Vehicle not found"}},
    response_only=True,
    status_codes=["404"],
)

vehicle_delete_success_example = OpenApiExample(
    "Success Response",
    value={
        "success": {
            "code": 200,
            "data": None,
            "message": "Vehicle deleted successfully",
        }
    },
    response_only=True,
    status_codes=["200"],
)

vehicle_delete_active_booking_example = OpenApiExample(
    "Vehicle Has Active Booking",
    value={
        "success": {
            "code": 400,
            "data": None,
            "message": "Cannot delete vehicle while it has active booking",
        }
    },
    response_only=True,
    status_codes=["400"],
)

vehicle_delete_not_found_example = OpenApiExample(
    "Vehicle Not Found",
    value={"success": {"code": 404, "data": None, "message": "Vehicle not found"}},
    response_only=True,
    status_codes=["404"],
)
