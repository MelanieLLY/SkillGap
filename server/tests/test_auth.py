"""
test_auth.py — Tests for /api/auth/* endpoints.

Coverage targets
----------------
* POST /api/auth/register  →  happy path, duplicate email, invalid payload
* POST /api/auth/login     →  happy path, wrong password, unknown user, inactive user
* GET  /api/auth/me        →  authenticated, unauthenticated, invalid token, inactive user

All tests use the in-memory SQLite DB wired up in conftest.py.
No external services are required.
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from server.auth import models as auth_models
from server.auth import utils as auth_utils

# ─── Helpers ──────────────────────────────────────────────────────────────────

VALID_EMAIL = "auth_test@example.com"
VALID_PASSWORD = "secure_password_XY9!"


def _register(
    client: TestClient, email: str = VALID_EMAIL, password: str = VALID_PASSWORD
) -> dict:
    """Convenience: register a user and return the JSON body."""
    r = client.post("/api/auth/register", json={"email": email, "password": password})
    return r


def _login(
    client: TestClient, email: str = VALID_EMAIL, password: str = VALID_PASSWORD
):
    """Convenience: perform a form-encoded login."""
    return client.post(
        "/api/auth/login", data={"username": email, "password": password}
    )


# ══════════════════════════════════════════════════════════════════════════════
# POST /api/auth/register
# ══════════════════════════════════════════════════════════════════════════════


class TestRegister:
    """Unit tests for the user registration endpoint."""

    def test_register_returns_201_and_user_data(self, client: TestClient) -> None:
        """Happy path: valid unique email/password → 201 with user object."""
        r = _register(client)
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["email"] == VALID_EMAIL
        assert "id" in body
        assert body["is_active"] is True
        # Password MUST NOT be returned
        assert "password" not in body
        assert "hashed_password" not in body

    def test_register_returns_skills_as_empty_list(self, client: TestClient) -> None:
        """Newly registered user should have an empty skills list."""
        r = _register(client)
        assert r.status_code == 201
        assert r.json()["skills"] == []

    def test_register_duplicate_email_returns_400(self, client: TestClient) -> None:
        """Registering the same email twice must return 400."""
        _register(client)
        r = _register(client)
        assert r.status_code == 400
        assert "already registered" in r.json()["detail"].lower()

    def test_register_invalid_email_returns_422(self, client: TestClient) -> None:
        """Sending a non-email string should fail Pydantic validation → 422."""
        r = client.post(
            "/api/auth/register", json={"email": "not-an-email", "password": "pw"}
        )
        assert r.status_code == 422

    def test_register_missing_password_returns_422(self, client: TestClient) -> None:
        """Omitting the password field should fail Pydantic validation."""
        r = client.post("/api/auth/register", json={"email": "nopw@example.com"})
        assert r.status_code == 422

    def test_register_empty_body_returns_422(self, client: TestClient) -> None:
        """Empty body must be rejected by Pydantic."""
        r = client.post("/api/auth/register", json={})
        assert r.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# POST /api/auth/login
# ══════════════════════════════════════════════════════════════════════════════


class TestLogin:
    """Unit tests for the login endpoint."""

    def test_login_happy_path_returns_token(self, client: TestClient) -> None:
        """Valid credentials → 200 with access_token + token_type=bearer."""
        _register(client)
        r = _login(client)
        assert r.status_code == 200
        body = r.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        # Token must be a non-empty string
        assert isinstance(body["access_token"], str) and len(body["access_token"]) > 0

    def test_login_wrong_password_returns_401(self, client: TestClient) -> None:
        """Wrong password must return 401 Unauthorized."""
        _register(client)
        r = _login(client, password="wrong_password")
        assert r.status_code == 401
        assert "incorrect" in r.json()["detail"].lower()

    def test_login_unknown_email_returns_401(self, client: TestClient) -> None:
        """Unknown email must also return 401 (not expose user existence)."""
        r = _login(client, email="nobody@example.com")
        assert r.status_code == 401

    def test_login_requires_form_data_not_json(self, client: TestClient) -> None:
        """Login endpoint expects OAuth2 form-data, not JSON → 422 for JSON body."""
        _register(client)
        r = client.post(
            "/api/auth/login",
            json={"username": VALID_EMAIL, "password": VALID_PASSWORD},
        )
        assert r.status_code == 422

    def test_login_inactive_user_returns_400(
        self, client: TestClient, db_session
    ) -> None:
        """Inactive users should not be able to authenticate via /me."""
        # Register a normal user first
        _register(client)
        login_r = _login(client)
        assert login_r.status_code == 200, login_r.text
        token = login_r.json()["access_token"]

        # Mark as inactive directly in DB
        user = db_session.query(auth_models.User).filter_by(email=VALID_EMAIL).first()
        assert user is not None
        user.is_active = False
        db_session.commit()

        r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 400
        assert "inactive" in r.json()["detail"].lower()


# ══════════════════════════════════════════════════════════════════════════════
# GET /api/auth/me
# ══════════════════════════════════════════════════════════════════════════════


class TestReadMe:
    """Tests for the authenticated /me endpoint."""

    def test_read_me_returns_current_user(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Authenticated request must return the logged-in user's data."""
        r = client.get("/api/auth/me", headers=auth_headers)
        assert r.status_code == 200
        body = r.json()
        # Fixture user is fixture_user@example.com (from conftest.py)
        assert "email" in body
        assert "id" in body
        assert body["is_active"] is True

    def test_read_me_without_token_returns_401(self, client: TestClient) -> None:
        """No Authorization header → 401."""
        r = client.get("/api/auth/me")
        assert r.status_code == 401

    def test_read_me_with_invalid_token_returns_401(self, client: TestClient) -> None:
        """A garbage token string → 401."""
        r = client.get(
            "/api/auth/me", headers={"Authorization": "Bearer garbage.token.here"}
        )
        assert r.status_code == 401

    def test_read_me_with_malformed_bearer_returns_401(
        self, client: TestClient
    ) -> None:
        """Bearer prefix missing → 401."""
        r = client.get("/api/auth/me", headers={"Authorization": "Token somevalue"})
        assert r.status_code == 401


# ══════════════════════════════════════════════════════════════════════════════
# Unit tests for auth utility functions (no HTTP layer)
# ══════════════════════════════════════════════════════════════════════════════


class TestAuthUtils:
    """Pure-unit tests for password hashing and JWT utilities."""

    def test_password_hash_is_not_plaintext(self) -> None:
        """Hashed password must differ from the original."""
        hashed = auth_utils.get_password_hash("my_secret")
        assert hashed != "my_secret"
        assert len(hashed) > 10

    def test_verify_password_correct(self) -> None:
        """Correct plain password must verify successfully."""
        hashed = auth_utils.get_password_hash("correct_horse")
        assert auth_utils.verify_password("correct_horse", hashed) is True

    def test_verify_password_wrong(self) -> None:
        """Wrong plain password must not verify."""
        hashed = auth_utils.get_password_hash("correct_horse")
        assert auth_utils.verify_password("wrong_horse", hashed) is False

    def test_create_access_token_returns_string(self) -> None:
        """create_access_token must return a non-empty JWT string."""
        token = auth_utils.create_access_token(subject=42)
        assert isinstance(token, str)
        assert len(token) > 20
        # JWT tokens have 3 dot-separated parts
        assert token.count(".") == 2

    def test_create_access_token_with_custom_expiry(self) -> None:
        """Token created with custom expiry should still be a valid JWT."""
        from datetime import timedelta

        token = auth_utils.create_access_token(
            subject=1, expires_delta=timedelta(minutes=5)
        )
        assert token.count(".") == 2
