# Car Rental Backend

A Django REST API backend for a car rental platform, supporting user registration/login, vehicle management, and booking operations. Built with Django, Django REST Framework, JWT authentication, and PostgreSQL.

---

## Features
- User registration and authentication (JWT)
- Vehicle CRUD for authenticated users
- Booking creation and management
- Custom error handling and response format
- API documentation with Swagger (drf-spectacular)

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL (14 or later)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/SyedMuhammadHaris/car-rental-platform-backend.git
   cd car-rental-backend
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy or create an environment file in `env/.local.env` (or the appropriate environment, e.g., `.prod.env`).
   - Required variables include:
     - `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, `JWT_AUDIENCE`, `JWT_ISSUER`, `PASSWORD_SALT`

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

### Running the Server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/` by default.

---

## Running Tests

This project uses `pytest` for testing.

```bash
pytest apps/module/tests
```

---

## API Documentation

Interactive API docs are available at:
- Swagger UI: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- OpenAPI schema: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## Main API Endpoints

| Endpoint                | Method | Description                       |
|------------------------|--------|-----------------------------------|
| `/api/v1/user/register` | POST   | Register a new user               |
| `/api/v1/user/login`    | POST   | User login (returns JWT)          |
| `/api/v1/vehicle`       | GET    | List vehicles (auth required)     |
| `/api/v1/vehicle`       | POST   | Create vehicle (auth required)    |
| `/api/v1/vehicle/<id>`  | PUT    | Update vehicle (auth required)    |
| `/api/v1/vehicle/<id>`  | DELETE | Delete vehicle (auth required)    |
| `/api/v1/booking`       | GET    | List bookings (auth required)     |
| `/api/v1/booking`       | POST   | Create booking (auth required)    |

All endpoints (except registration/login) require JWT authentication via the `Authorization: Bearer <token>` header.

---

---

## Custom Exception Handling

This project uses a custom exception handler for consistent error responses. It is set in Django REST Framework's settings as:

```python
REST_FRAMEWORK = {
    ...
    "EXCEPTION_HANDLER": "utils.error_handler.custom_exception_handler",
}
```

### How It Works
- All unhandled exceptions and DRF errors are processed by `custom_exception_handler` in `utils/error_handler.py`.
- Errors are logged and returned in a consistent JSON format.
- Handles authentication, validation, and server errors with clear messages.
- Uses a custom response class (`SuccessResponse`) for successful API responses.

#### Example Error Response
```json
{
  "error": {
    "code": 400,
    "data": null,
    "message": "Plate already exists"
  }
}
```

#### Example Success Response
```json
{
  "success": {
    "code": 201,
    "data": {
      "object": "vehicle",
      "id": 1,
      "make": "Toyota",
      ...
    },
    "message": "Vehicle created successfully"
  }
}
```

### Custom Exception Class
You can raise custom API exceptions in your views using:
```python
from utils.error_handler import CustomAPIException
raise CustomAPIException(status_code=400, message="Custom error message")
```

---

## Environment Variables
- All sensitive settings (DB credentials, secret keys, JWT settings) are loaded from environment files in the `env/` directory.
- Example: `env/.local.env`

---

## User Registration Example

### Request

**POST** `/api/v1/user/register`

Example payload:
```json
{
  "email": "haris.ahmed@gmail.com",
  "first_name": "haris",
  "last_name": "ahmed",
  "phone": "03211313212",
  "password": "yourpassword123"
}
```

### Response

```json
{
  "success": {
    "code": 200,
    "data": {
      "object": "user",
      "id": 12,
      "email": "haris.ahmed@gmail.com",
      "first_name": "haris",
      "last_name": "ahmed",
      "phone": "03211313212",
      "status": 1,
      "phone_verified": false,
      "email_verified": false,
      "access_token": "eyJhbGciOiJI**************************************",
      "created_at": "2025-07-11T16:38:52.024000Z",
      "updated_at": "2025-07-11T16:38:52.024000Z"
    },
    "message": "User registered successfully"
  }
}
```

## User Login Example

### Request

**POST** `/api/v1/user/login`

Example payload:
```json
{
  "email": "testUser@gmail.com",
  "password": "yourpassword123"
}
```

### Response

```json
{
  "success": {
    "code": 200,
    "data": {
      "object": "user",
      "id": 10,
      "email": "testUser@gmail.com",
      "first_name": "asddas",
      "last_name": "adad",
      "phone": "0323234242",
      "status": 1,
      "phone_verified": false,
      "email_verified": false,
      "access_token": "eyJhb**************************************",
      "created_at": "2025-07-11T16:38:52.024000Z",
      "updated_at": "2025-07-11T16:38:52.024000Z"
    },
    "message": "User login successfully"
  }
}
```

## Create Vehicle Example

**Note:** This endpoint requires authentication. Include the header:

```
Authorization: Bearer <your-access-token>
```

### Request

**POST** `/api/v1/vehicle`

Example payload:
```json
{
  "make": "Honda",
  "model": "City",
  "year": 2019,
  "plate": "ABC-5444"
}
```

### Response

```json
{
  "success": {
    "code": 201,
    "data": {
      "object": "vehicle",
      "id": 10,
      "user_id": 10,
      "make": "Honda",
      "model": "City",
      "year": 2019,
      "plate": "ABC-5444",
      "created_at": "2025-07-13T10:42:27.969374Z",
      "updated_at": "2025-07-13T10:42:27.969437Z"
    },
    "message": "Vehicle created successfully"
  }
}
```

## Create Booking Example

**Note:** This endpoint requires authentication. Include the header:

```
Authorization: Bearer <your-access-token>
```

### Request

**POST** `/api/v1/booking`

Example payload:
```json
{
  "vehicle_id": 10,
  "start_date": "2025-07-22 15:00:00",
  "end_date": "2025-07-26 17:00:00"
}
```

### Response

```json
{
  "success": {
    "code": 201,
    "data": {
      "object": "booking",
      "id": 6,
      "user_id": 10,
      "vehicle_id": 10,
      "start_date": "2025-07-22 15:00:00",
      "end_date": "2025-07-26 17:00:00",
      "status": 1,
      "created_at": "2025-07-13 15:48:35",
      "updated_at": "2025-07-13 15:48:35"
    },
    "message": "Booking created successfully"
  }
}
```

#### Response (Vehicle Already Booked)

If the vehicle is already booked for the selected dates, you will receive:

```json
{
  "error": {
    "code": 400,
    "data": null,
    "message": "Vehicle is already booked for the selected dates."
  }
}
```

## Delete Vehicle Example

**Note:** This endpoint requires authentication. Include the header:

```
Authorization: Bearer <your-access-token>
```

### Request

**DELETE** `/api/v1/vehicle/<vehicle_id>`

Replace `<vehicle_id>` with the actual ID of the vehicle you want to delete.

### Response (Success)

```json
{
  "success": {
    "code": 200,
    "data": null,
    "message": "Vehicle deleted successfully"
  }
}
```

### Response (Vehicle Has Active Booking)

If the vehicle has an active booking, you will receive:

```json
{
  "success": {
    "code": 400,
    "data": null,
    "message": "Cannot delete vehicle while it has active booking"
  }
}
```

## Get User Bookings Example

**Note:** This endpoint requires authentication. Include the header:

```
Authorization: Bearer <your-access-token>
```

### Request

**GET** `/api/v1/booking`

#### With Query Parameter

You can filter bookings from a specific date using the `from` query parameter (format: `YYYY-MM-DD`).

Example:
```
GET /api/v1/booking?from=2025-07-13
```

### Response

```json
{
  "success": {
    "code": 200,
    "data": [
      {
        "object": "booking",
        "id": 6,
        "user_id": 10,
        "vehicle_id": 10,
        "start_date": "2025-07-22 15:00:00",
        "end_date": "2025-07-26 17:00:00",
        "status": 1,
        "created_at": "2025-07-13 15:48:35",
        "updated_at": "2025-07-13 15:48:35"
      },
      {
        "object": "booking",
        "id": 4,
        "user_id": 10,
        "vehicle_id": 7,
        "start_date": "2025-07-13 19:05:00",
        "end_date": "2025-07-22 19:05:00",
        "status": 1,
        "created_at": "2025-07-12 22:23:19",
        "updated_at": "2025-07-12 22:23:19"
      },
      {
        "object": "booking",
        "id": 3,
        "user_id": 10,
        "vehicle_id": 2,
        "start_date": "2025-07-13 19:05:00",
        "end_date": "2025-07-22 19:05:00",
        "status": 1,
        "created_at": "2025-07-12 22:12:46",
        "updated_at": "2025-07-12 22:12:46"
      },
      {
        "object": "booking",
        "id": 5,
        "user_id": 10,
        "vehicle_id": 2,
        "start_date": "2025-07-02 19:05:00",
        "end_date": "2025-07-22 19:05:00",
        "status": 1,
        "created_at": "2025-07-12 22:12:46",
        "updated_at": "2025-07-12 22:12:46"
      },
      {
        "object": "booking",
        "id": 1,
        "user_id": 10,
        "vehicle_id": 8,
        "start_date": "2025-07-13 19:05:00",
        "end_date": "2025-07-22 19:05:00",
        "status": 1,
        "created_at": "2025-07-12 22:07:34",
        "updated_at": "2025-07-12 22:07:34"
      }
    ],
    "message": "Bookings retrieved successfully"
  }
}
```

## Get User Vehicles Example

**Note:** This endpoint requires authentication. Include the header:

```
Authorization: Bearer <your-access-token>
```

### Request

**GET** `/api/v1/vehicle`

### Response

```json
{
  "success": {
    "code": 200,
    "data": [
      {
        "object": "vehicle",
        "id": 2,
        "user_id": 10,
        "make": "dada",
        "model": "dasd",
        "year": 2313,
        "plate": "adasdad",
        "created_at": "2025-07-11T20:30:19.518352Z",
        "updated_at": "2025-07-11T20:30:19.518406Z"
      },
      {
        "object": "vehicle",
        "id": 5,
        "user_id": 10,
        "make": "dada",
        "model": "dasd",
        "year": 2313,
        "plate": "adaoosdad999",
        "created_at": "2025-07-12T09:01:06.003299Z",
        "updated_at": "2025-07-12T09:01:06.003359Z"
      },
      {
        "object": "vehicle",
        "id": 7,
        "user_id": 10,
        "make": "dada",
        "model": "dasd",
        "year": 2313,
        "plate": "adaoosdad99oo9",
        "created_at": "2025-07-12T09:03:33.911891Z",
        "updated_at": "2025-07-12T09:03:33.911912Z"
      },
      {
        "object": "vehicle",
        "id": 8,
        "user_id": 10,
        "make": "dada",
        "model": "hy",
        "year": 2313,
        "plate": "adaoosdad99ooccc9",
        "created_at": "2025-07-12T09:05:58.095923Z",
        "updated_at": "2025-07-12T16:21:49.790589Z"
      },
      {
        "object": "vehicle",
        "id": 9,
        "user_id": 10,
        "make": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "plate": "ABC-1234",
        "created_at": "2025-07-13T10:41:55.246809Z",
        "updated_at": "2025-07-13T10:41:55.246900Z"
      },
      {
        "object": "vehicle",
        "id": 10,
        "user_id": 10,
        "make": "Honda",
        "model": "City",
        "year": 2017,
        "plate": "ABC-5444",
        "created_at": "2025-07-13T10:42:27.969374Z",
        "updated_at": "2025-07-13T10:46:18.328088Z"
      }
    ],
    "message": "Vehicles retrieved successfully"
  }
}
```




