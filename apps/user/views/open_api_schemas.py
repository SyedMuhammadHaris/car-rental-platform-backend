from drf_spectacular.utils import OpenApiExample

user_login_payload_schema = {
    "application/json": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "format": "email",
                "example": "john.doe@example.com",
            },
            "password": {"type": "string", "example": "mysecretpassword"},
        },
        "required": ["email", "password"],
    }
}
# User Registration examples
user_register_success_example = OpenApiExample(
    "Success Response",
    value={
        "success": {
            "code": 201,
            "data": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890",
                "status": 1,
            },
            "message": "User registered successfully",
        }
    },
    response_only=True,
    status_codes=["201"],
)

user_register_duplicate_email_example = OpenApiExample(
    "Duplicate Email Error",
    value={"error": {"code": 400, "data": None, "message": "Email already exists"}},
    response_only=True,
    status_codes=["400"],
)

# User Login examples
user_login_success_example = OpenApiExample(
    "Success Response",
    value={
        "success": {
            "code": 200,
            "data": {
                "access_token": "<jwt-token>",
                "refresh_token": "<jwt-refresh-token>",
            },
            "message": "Login successful",
        }
    },
    response_only=True,
    status_codes=["200"],
)

user_login_invalid_credentials_example = OpenApiExample(
    "Invalid Credentials",
    value={
        "error": {"code": 401, "data": None, "message": "Invalid email or password"}
    },
    response_only=True,
    status_codes=["401"],
)
