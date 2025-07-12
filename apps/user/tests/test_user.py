import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def register_url():
    return "/api/v1/user/register"

@pytest.fixture
def login_url():
    return "/api/v1/user/login"

@pytest.mark.django_db
def test_register_user_success(client, register_url):
    payload = {
        "email": "john.doe@example.com",
        "password": "pytestpass123",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "1234567890"
    }
    response = client.post(register_url, payload, format="json")
    data = response.data["success"]
    assert data["code"] == 201
    assert data["message"] == "User registered successfully"
    assert data["data"]["email"] == payload["email"]

@pytest.mark.django_db
def test_register_user_missing_password(client, register_url):
    payload = {
        "email": "jane.smith@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "phone": "1234567890"
    }
    response = client.post(register_url, payload, format="json")
    data = response.data["error"]
    assert data["code"] == 400
    assert data["message"] == "Password is required"

@pytest.mark.django_db
def test_register_user_duplicate_email(client, register_url):
    payload = {
        "email": "alice.johnson@example.com",
        "password": "pytestpass123",
        "first_name": "Alice",
        "last_name": "Johnson",
        "phone": "1234567890"
    }
    # First registration
    client.post(register_url, payload, format="json")
    # Duplicate registration
    response = client.post(register_url, payload, format="json")
    data = response.data["error"]
    assert data["code"] == 400
    assert "Email already exists" in data["message"]

@pytest.mark.django_db
def test_login_invalid_password(client, register_url, login_url):
    payload = {
        "email": "michael.brown@example.com",
        "password": "pytestpass123",
        "first_name": "Michael",
        "last_name": "Brown",
        "phone": "1234567890"
    }
    client.post(register_url, payload, format="json")
    login_payload = {
        "email": payload["email"],
        "password": "wrongpassword"
    }
    response = client.post(login_url, login_payload, format="json")
    data = response.data["error"]
    assert data["code"] == 400
    assert "Incorect password" in data["message"]

@pytest.mark.django_db
def test_login_success(client, register_url, login_url):
    payload = {
        "email": "emily.wilson@example.com",
        "password": "pytestpass123",
        "first_name": "Emily",
        "last_name": "Wilson",
        "phone": "1234567890"
    }
    client.post(register_url, payload, format="json")
    login_payload = {
        "email": payload["email"],
        "password": payload["password"]
    }
    response = client.post(login_url, login_payload, format="json")
    data = response.data["success"]
    assert data["code"] == 200
    assert data["message"] == "User login successfully"
    assert data["data"]["email"] == payload["email"] 