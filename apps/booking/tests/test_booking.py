import pytest
from rest_framework.test import APIClient
from apps.user.models import User
from apps.vehicle.models import Vehicle
from apps.booking.models import Booking
from datetime import datetime, timedelta

@pytest.fixture
def user():
    return User.objects.create(
        email="bookinguser@example.com",
        password="pytestpass123",
        first_name="Booking",
        last_name="User",
        phone="1234567890",
        status=1
    )

@pytest.fixture
def auth_client(user):
    client = APIClient()
    from apps.user.serializers.user_serializer import UserSerializer
    access_token = UserSerializer(user).data.get("access_token")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client

@pytest.fixture
def vehicle(user):
    return Vehicle.objects.create(
        user=user,
        make="Toyota",
        model="Corolla",
        year=2020,
        plate="BOOK123"
    )

@pytest.fixture
def booking_url():
    return "/api/v1/booking"

@pytest.mark.django_db
def test_create_booking_success(auth_client, user, vehicle, booking_url):
    start = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    end = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
    payload = {
        "vehicle_id": vehicle.id,
        "start_date": start,
        "end_date": end
    }
    response = auth_client.post(booking_url, payload, format="json")
    data = response.data["success"]
    assert data["code"] == 201
    assert data["message"] == "Booking created successfully"
    assert data["data"]["vehicle_id"] == vehicle.id

@pytest.mark.django_db
def test_create_booking_missing_vehicle(auth_client, booking_url):
    start = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    end = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
    payload = {
        "start_date": start,
        "end_date": end
    }
    response = auth_client.post(booking_url, payload, format="json")
    data = response.data["error"]
    assert data["code"] == 400
    assert data["message"] == "Vehicle ID is required"

@pytest.mark.django_db
def test_create_booking_invalid_dates(auth_client, vehicle, booking_url):
    start = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
    end = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
    payload = {
        "vehicle_id": vehicle.id,
        "start_date": start,
        "end_date": end
    }
    response = auth_client.post(booking_url, payload, format="json")
    data = response.data["error"]
    assert data["code"] == 400
    assert data["message"] == "Start date cannot be after end date"

@pytest.mark.django_db
def test_create_booking_conflict(auth_client, user, vehicle, booking_url):
    start = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    end = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
    Booking.objects.create(
        user=user,
        vehicle=vehicle,
        start_date=datetime.strptime(start, "%Y-%m-%d %H:%M"),
        end_date=datetime.strptime(end, "%Y-%m-%d %H:%M"),
        status=1
    )
    payload = {
        "vehicle_id": vehicle.id,
        "start_date": start,
        "end_date": end
    }
    response = auth_client.post(booking_url, payload, format="json")
    data = response.data["error"]
    assert data["code"] == 400
    assert "Vehicle is already booked" in data["message"]

@pytest.mark.django_db
def test_get_user_bookings(auth_client, user, vehicle, booking_url):
    start = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    end = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
    Booking.objects.create(
        user=user,
        vehicle=vehicle,
        start_date=datetime.strptime(start, "%Y-%m-%d %H:%M"),
        end_date=datetime.strptime(end, "%Y-%m-%d %H:%M"),
        status=1
    )
    response = auth_client.get(booking_url)
    data = response.data["success"]
    assert data["code"] == 200
    assert data["message"] == "Bookings retrieved successfully"
    assert any(b["vehicle_id"] == vehicle.id for b in data["data"])
