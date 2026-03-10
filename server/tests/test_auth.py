from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler

def visit_ARRAY(self, type_, **kw):
    return "TEXT"
SQLiteTypeCompiler.visit_ARRAY = visit_ARRAY
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from server.main import app
from server.database import Base, get_db
from server.auth import models

# Setup an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_user():
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "anotherpassword"}
    )
    assert response.status_code == 400


def test_login_user():
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_incorrect_password():
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_read_users_me():
    # Login first
    login_response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Access protected route
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_read_users_me_unauthorized():
    response = client.get("/api/auth/me")
    assert response.status_code == 401
