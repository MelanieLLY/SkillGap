from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
import uuid

from server.main import app
from server.database import get_db, engine, SessionLocal
from server.auth import models

# Use the real database configuration, omitting the override
# We will use a unique test user email per run so it doesn't collide
TEST_EMAIL = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
TEST_PASSWORD = "testpassword123"


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/api/auth/register",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == TEST_EMAIL
    assert "id" in data


def test_register_duplicate_user():
    response = client.post(
        "/api/auth/register",
        json={"email": TEST_EMAIL, "password": "anotherpassword"}
    )
    assert response.status_code == 400


def test_login_user():
    response = client.post(
        "/api/auth/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_incorrect_password():
    response = client.post(
        "/api/auth/login",
        data={"username": TEST_EMAIL, "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_read_users_me():
    # Login first
    login_response = client.post(
        "/api/auth/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    token = login_response.json()["access_token"]
    
    # Access protected route
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == TEST_EMAIL


def test_read_users_me_unauthorized():
    response = client.get("/api/auth/me")
    assert response.status_code == 401
