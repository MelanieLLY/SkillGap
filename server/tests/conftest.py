"""
conftest.py — Shared pytest fixtures for the SkillGap test suite.

Architecture notes
------------------
* The production models use ``ARRAY(String)`` from ``sqlalchemy.dialects.postgresql``.
  SQLite (used here for an isolated, zero-infrastructure test DB) does not support
  PostgreSQL dialects.  We patch every ARRAY column at import-time with a custom
  ``TypeDecorator`` (``JsonEncodedList``) that stores JSON-encoded strings so the
  column behaves identically from SQLAlchemy's perspective.

* All tests use ``app.dependency_overrides`` to swap the real ``get_db`` session
  for a session bound to the in-memory SQLite engine.  This guarantees full isolation
  between test runs without touching any external service.

* A ``auth_headers`` fixture registers + logs in a brand-new user, then returns an
  ``Authorization: Bearer <token>`` dict ready to be passed to ``client.get/post/…``.

IMPORTANT — ARRAY shim design rationale
-----------------------------------------
We patch ``pg_dialect.ARRAY`` with a *factory function* (not a class).
If we assigned the class itself, the call ``ARRAY(String)`` would pass the
``String`` *class object* as the positional ``length`` argument to the
underlying ``String`` impl constructor, causing:
  TypeError: %d format: a real number is required, not type
The factory function simply discards all arguments and returns a
ready ``JsonEncodedList()`` instance.
"""

from __future__ import annotations

import json
from collections.abc import Generator

import pytest

# ─── Patch ARRAY columns BEFORE application modules are imported ───────────────
import sqlalchemy.dialects.postgresql as pg_dialect
from fastapi.testclient import TestClient
from sqlalchemy import String, create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.types import TypeDecorator


class JsonEncodedList(TypeDecorator):  # type: ignore[type-arg]
    """Store a Python list as a JSON string in SQLite; transparent on read.

    Handles the case where the SQLite DB stores the PostgreSQL server_default
    literal ``'{}'`` (which JSON-decodes to a dict, not a list) by always
    coercing the result to a list.
    """

    impl = String
    cache_ok = True

    def process_bind_param(self, value: object, dialect: object) -> str | None:  # noqa: ANN001
        if value is None:
            return "[]"
        if isinstance(value, (list, tuple, set)):
            return json.dumps(list(value))
        # Fallback: treat any other value as an already-serialised string
        return str(value)

    def process_result_value(self, value: object, dialect: object) -> list[str]:  # noqa: ANN001
        if value is None:
            return []
        # Handle the PostgreSQL `'{}'` server_default which SQLite stores as-is.
        if value == "{}":
            return []
        try:
            parsed = json.loads(str(value))
            # If the DB somehow stored a JSON object (`{}`), coerce to list
            if isinstance(parsed, dict):
                return []
            if isinstance(parsed, list):
                return parsed
            return []
        except (json.JSONDecodeError, TypeError):
            return []


def _array_factory(*args: object, **kwargs: object) -> JsonEncodedList:
    """
    Drop-in replacement for ``pg_dialect.ARRAY``.

    Accepts and ignores all arguments (item type, dimensions, etc.) that
    ``ARRAY`` normally requires, and returns a ``JsonEncodedList()`` instance
    that SQLite can work with.
    """
    return JsonEncodedList()


# Monkey-patch the dialect so importing models doesn't blow up with SQLite.
pg_dialect.ARRAY = _array_factory  # type: ignore[attr-defined]

# ─── Now it is safe to import application modules ─────────────────────────────
from server.auth import models as auth_models  # noqa: E402
from server.database import get_db  # noqa: E402
from server.history import models as history_models  # noqa: E402
from server.main import app  # noqa: E402

# ─── SQLite in-memory engine ──────────────────────────────────────────────────
SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# SQLite doesn't enforce foreign keys by default — enable them so our FK
# constraints are actually tested.
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_conn, connection_record) -> None:  # noqa: ANN001
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ─── Schema creation / teardown ───────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def create_test_tables() -> Generator[None, None, None]:
    """Create all tables once for the entire test session, then drop them."""
    auth_models.Base.metadata.create_all(bind=engine)
    history_models.Base.metadata.create_all(bind=engine)
    yield
    auth_models.Base.metadata.drop_all(bind=engine)
    history_models.Base.metadata.drop_all(bind=engine)


# ─── Per-test DB session (rolls back after each test) ─────────────────────────
@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """
    Yield a *transactional* SQLAlchemy session that is rolled back after each
    test so tests never leave data behind for each other.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


# ─── FastAPI test client wired to the test DB ─────────────────────────────────
@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Return a ``TestClient`` whose ``get_db`` dependency is replaced by the
    current test's in-memory session.  Dependency overrides are cleaned up
    automatically after each test.
    """

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ─── Registered test user + JWT token fixtures ────────────────────────────────
TEST_EMAIL = "fixture_user@example.com"
TEST_PASSWORD = "fixture_password_123"


@pytest.fixture()
def registered_user(client: TestClient) -> dict:
    """Register a fresh test user and return the JSON response body."""
    response = client.post(
        "/api/auth/register",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert response.status_code == 201, f"Registration failed: {response.text}"
    return response.json()


@pytest.fixture()
def auth_headers(client: TestClient, registered_user: dict) -> dict:
    """
    Register a user and obtain a valid JWT token.

    Returns:
        dict: ``{"Authorization": "Bearer <token>"}`` ready for use in
              ``client.get/post(…, headers=auth_headers)``.
    """
    response = client.post(
        "/api/auth/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
