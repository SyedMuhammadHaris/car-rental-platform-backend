import pytest
from rest_framework.test import APIClient
from apps.user.models import User
from apps.vehicle.models import Vehicle
from apps.booking.models import Booking
from datetime import datetime, timedelta

@pytest.fixture
def user():
    user = User.objects.create(
        email="vehicleuser@example.com",
        password="testpassword123",
        first_name="Vehicle",
        last_name="User",
        phone="1234567890",
        status=1
    )
    return user

@pytest.fixture
def auth_client(user):
    client = APIClient()
    from apps.user.serializers.user_serializer import UserSerializer
    access_token = UserSerializer(user).data.get("access_token")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client

@pytest.fixture
def vehicle_url():
    return "/api/v1/vehicle"

@pytest.mark.django_db
def test_create_vehicle_success(auth_client, vehicle_url):
    payload = {
        "make": "Honda",
        "model": "Civic",
        "year": 2022,
        "plate": "XYZ123"
    }
    response = auth_client.post(vehicle_url, payload, format="json")
    data = response.data["success"]
    assert data["code"] == 201
    assert data["message"] == "Vehicle created successfully"
    assert data["data"]["plate"] == payload["plate"]

@pytest.mark.django_db
def test_create_vehicle_duplicate_plate(auth_client, user, vehicle_url):
    Vehicle.objects.create(
        user=user,
        make="Toyota",
        model="Corolla",
        year=2020,
        plate="DUPLICATE1"
    )
    payload = {
        "make": "Ford",
        "model": "Focus",
        "year": 2021,
        "plate": "DUPLICATE1"
    }
    response = auth_client.post(vehicle_url, payload, format="json")
    data = response.data["error"]
    assert data["code"] == 400
    assert "Plate already exists" in data["message"]

@pytest.mark.django_db
def test_list_vehicles(auth_client, user, vehicle_url):
    Vehicle.objects.create(
        user=user,
        make="Mazda",
        model="3",
        year=2019,
        plate="LIST123"
    )
    response = auth_client.get(vehicle_url)
    data = response.data["success"]
    assert data["code"] == 200
    assert data["message"] == "Vehicles retrieved successfully"
    assert any(v["plate"] == "LIST123" for v in data["data"])

@pytest.mark.django_db
def test_update_vehicle_success(auth_client, user):
    vehicle = Vehicle.objects.create(
        user=user,
        make="Nissan",
        model="Altima",
        year=2018,
        plate="UPD123"
    )
    update_url = f"/api/v1/vehicle/{vehicle.id}"
    payload = {"model": "Sentra"}
    response = auth_client.put(update_url, payload, format="json")
    data = response.data["success"]
    assert data["code"] == 200
    assert data["message"] == "Vehicle updated successfully"
    assert data["data"]["model"] == "Sentra"

@pytest.mark.django_db
def test_delete_vehicle_success(auth_client, user):
    vehicle = Vehicle.objects.create(
        user=user,
        make="Chevy",
        model="Malibu",
        year=2017,
        plate="DEL123"
    )
    delete_url = f"/api/v1/vehicle/{vehicle.id}"
    response = auth_client.delete(delete_url)
    data = response.data["success"]
    assert data["code"] == 200
    assert data["message"] == "Vehicle deleted successfully"
    assert not Vehicle.objects.filter(id=vehicle.id).exists()

@pytest.mark.django_db
def test_delete_vehicle_with_active_booking(auth_client, user):
    vehicle = Vehicle.objects.create(
        user=user,
        make="BMW",
        model="X5",
        year=2021,
        plate="BOOKED123"
    )
    Booking.objects.create(
        user=user,
        vehicle=vehicle,
        start_date=datetime.now() + timedelta(days=1),
        end_date=datetime.now() + timedelta(days=2),
        status=1
    )
    delete_url = f"/api/v1/vehicle/{vehicle.id}"
    response = auth_client.delete(delete_url)
    data = response.data["success"]
    assert data["code"] == 400
    assert "Cannot delete vehicle while it has active booking" in data["message"]
    assert Vehicle.objects.filter(id=vehicle.id).exists()

@pytest.mark.django_db
def test_unauthenticated_access(vehicle_url):
    client = APIClient()
    payload = {
        "make": "Kia",
        "model": "Rio",
        "year": 2023,
        "plate": "NOAUTH123"
    }
    response = client.post(vehicle_url, payload, format="json")
    assert response.status_code in [401, 200]
    if response.status_code == 200:
        assert "Unauthenticated" in str(response.data)
