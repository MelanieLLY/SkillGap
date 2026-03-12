"""
test_history.py — Tests for /api/history/* endpoints.

Coverage targets
----------------
* GET  /api/history/              – returns user's history, auth required
* POST /api/history/              – creates record, match_score computed server-side
* PUT  /api/history/{id}          – updates company/position, auth + ownership check
* 404 / 403 edge cases on PUT

All tests use the SQLite in-memory fixtures from conftest.py for full isolation.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

# ─── Helper payload ────────────────────────────────────────────────────────────

HISTORY_PAYLOAD = {
    "company_name": "ACME Corp",
    "position_name": "Backend Engineer",
    "have_skills": ["python", "fastapi"],
    "missing_skills": ["kubernetes", "aws"],
    "bonus_skills": ["git"],
}


def _create_history(
    client: TestClient, auth_headers: dict, payload: dict | None = None
) -> dict:
    """POST a history entry and return its JSON body."""
    r = client.post(
        "/api/history/", json=payload or HISTORY_PAYLOAD, headers=auth_headers
    )
    assert r.status_code == 200, r.text
    return r.json()


# ══════════════════════════════════════════════════════════════════════════════
# POST /api/history/
# ══════════════════════════════════════════════════════════════════════════════


class TestCreateHistory:
    """Tests for creating a new analysis history record."""

    def test_create_history_returns_200(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Valid payload → 200 with full record body."""
        r = client.post("/api/history/", json=HISTORY_PAYLOAD, headers=auth_headers)
        assert r.status_code == 200

    def test_create_history_response_fields(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Response must contain all expected fields."""
        body = _create_history(client, auth_headers)
        assert "id" in body
        assert "user_id" in body
        assert "match_score" in body
        assert "date_analyzed" in body
        assert body["company_name"] == "ACME Corp"
        assert body["position_name"] == "Backend Engineer"

    def test_create_history_match_score_computed_server_side(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """match_score must be calculated by the backend: 2 have + 2 missing → 50.0."""
        body = _create_history(client, auth_headers)
        # have=["python","fastapi"] (2), missing=["kubernetes","aws"] (2) → 50.0
        assert body["match_score"] == 50.0

    def test_create_history_full_match_score_100(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """When missing_skills is empty, score should be 100."""
        payload = {**HISTORY_PAYLOAD, "have_skills": ["python"], "missing_skills": []}
        body = _create_history(client, auth_headers, payload)
        assert body["match_score"] == 100.0

    def test_create_history_zero_match_score(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """When have_skills is empty, score should be 0."""
        payload = {**HISTORY_PAYLOAD, "have_skills": [], "missing_skills": ["python"]}
        body = _create_history(client, auth_headers, payload)
        assert body["match_score"] == 0.0

    def test_create_history_without_company_or_position(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """company_name and position_name are optional → should default to null."""
        payload = {
            "have_skills": ["python"],
            "missing_skills": [],
            "bonus_skills": [],
        }
        r = client.post("/api/history/", json=payload, headers=auth_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["company_name"] is None
        assert body["position_name"] is None

    def test_create_history_missing_required_fields_returns_422(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Omitting have_skills → 422."""
        r = client.post(
            "/api/history/",
            json={"company_name": "X"},
            headers=auth_headers,
        )
        assert r.status_code == 422

    def test_create_history_requires_authentication(self, client: TestClient) -> None:
        """Unauthenticated POST → 401."""
        r = client.post("/api/history/", json=HISTORY_PAYLOAD)
        assert r.status_code == 401


# ══════════════════════════════════════════════════════════════════════════════
# GET /api/history/
# ══════════════════════════════════════════════════════════════════════════════


class TestGetHistory:
    """Tests for listing the current user's analysis history."""

    def test_get_history_empty_for_new_user(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """A brand-new user should have no history yet."""
        r = client.get("/api/history/", headers=auth_headers)
        assert r.status_code == 200
        assert r.json() == []

    def test_get_history_returns_created_records(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """After creating a record, it must appear in GET /history/."""
        _create_history(client, auth_headers)
        r = client.get("/api/history/", headers=auth_headers)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
        assert data[0]["company_name"] == "ACME Corp"

    def test_get_history_multiple_records(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """All records created by the user must be returned."""
        _create_history(client, auth_headers)
        _create_history(
            client,
            auth_headers,
            {**HISTORY_PAYLOAD, "company_name": "Globex"},
        )
        r = client.get("/api/history/", headers=auth_headers)
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_get_history_without_auth_returns_401(self, client: TestClient) -> None:
        """Unauthenticated GET → 401."""
        r = client.get("/api/history/")
        assert r.status_code == 401

    def test_get_history_response_has_required_fields(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Each history record should contain all mandatory fields."""
        _create_history(client, auth_headers)
        r = client.get("/api/history/", headers=auth_headers)
        record = r.json()[0]
        for field in ("id", "user_id", "match_score", "date_analyzed", "have_skills"):
            assert field in record, f"Missing field: {field}"


# ══════════════════════════════════════════════════════════════════════════════
# PUT /api/history/{id}
# ══════════════════════════════════════════════════════════════════════════════


class TestUpdateHistory:
    """Tests for patching metadata fields of a history record."""

    def test_update_company_name(self, client: TestClient, auth_headers: dict) -> None:
        """Updating company_name must be reflected in the response."""
        record = _create_history(client, auth_headers)
        r = client.put(
            f"/api/history/{record['id']}",
            json={"company_name": "Updated Corp"},
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["company_name"] == "Updated Corp"

    def test_update_position_name(self, client: TestClient, auth_headers: dict) -> None:
        """Updating position_name must be reflected in the response."""
        record = _create_history(client, auth_headers)
        r = client.put(
            f"/api/history/{record['id']}",
            json={"position_name": "Staff Engineer"},
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["position_name"] == "Staff Engineer"

    def test_update_both_fields(self, client: TestClient, auth_headers: dict) -> None:
        """Both fields can be updated in one request."""
        record = _create_history(client, auth_headers)
        r = client.put(
            f"/api/history/{record['id']}",
            json={"company_name": "NewCo", "position_name": "CTO"},
            headers=auth_headers,
        )
        assert r.status_code == 200
        body = r.json()
        assert body["company_name"] == "NewCo"
        assert body["position_name"] == "CTO"

    def test_update_match_score_is_preserved(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Metadata update must not change the match_score."""
        record = _create_history(client, auth_headers)
        original_score = record["match_score"]
        updated = client.put(
            f"/api/history/{record['id']}",
            json={"company_name": "Changed"},
            headers=auth_headers,
        ).json()
        assert updated["match_score"] == original_score

    def test_update_non_existent_record_returns_404(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Attempting to update a record that doesn't exist → 404."""
        r = client.put(
            "/api/history/99999",
            json={"company_name": "Ghost"},
            headers=auth_headers,
        )
        assert r.status_code == 404
        assert "not found" in r.json()["detail"].lower()

    def test_update_another_users_record_returns_403(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """A user must not be able to update another user's history → 403."""
        # user A creates a record
        record = _create_history(client, auth_headers)

        # user B registers + logs in
        client.post(
            "/api/auth/register",
            json={"email": "userb@example.com", "password": "passB123"},
        )
        login_r = client.post(
            "/api/auth/login",
            data={"username": "userb@example.com", "password": "passB123"},
        )
        token_b = login_r.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        r = client.put(
            f"/api/history/{record['id']}",
            json={"company_name": "Hacked"},
            headers=headers_b,
        )
        assert r.status_code == 403
        assert "not authorized" in r.json()["detail"].lower()

    def test_update_history_requires_authentication(self, client: TestClient) -> None:
        """Unauthenticated PUT → 401."""
        r = client.put("/api/history/1", json={"company_name": "X"})
        assert r.status_code == 401
