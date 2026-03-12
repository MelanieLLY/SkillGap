"""
test_profile.py — Tests for /api/profile/* endpoints.

Coverage targets
----------------
* GET    /api/profile/skills             – authenticated, returns skills list
* POST   /api/profile/skills             – add new skill, add duplicate, add empty
* DELETE /api/profile/skills/{name}      – remove existing, remove non-existent
* POST   /api/profile/extract-resume     – extracts curated skills from resume text

All tests are fully isolated using the SQLite in-memory fixtures from conftest.py.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

# ══════════════════════════════════════════════════════════════════════════════
# GET /api/profile/skills
# ══════════════════════════════════════════════════════════════════════════════


class TestGetSkills:
    """Tests that list a user's current skills."""

    def test_get_skills_returns_empty_list_for_new_user(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Freshly registered user should have zero skills."""
        r = client.get("/api/profile/skills", headers=auth_headers)
        assert r.status_code == 200
        assert r.json() == []

    def test_get_skills_returns_expected_skills(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """After adding skills, GET should return them."""
        client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )
        client.post(
            "/api/profile/skills", json={"skill": "react"}, headers=auth_headers
        )

        r = client.get("/api/profile/skills", headers=auth_headers)
        assert r.status_code == 200
        skills = r.json()
        assert "python" in skills
        assert "react" in skills

    def test_get_skills_requires_authentication(self, client: TestClient) -> None:
        """Unauthenticated GET → 401."""
        r = client.get("/api/profile/skills")
        assert r.status_code == 401


# ══════════════════════════════════════════════════════════════════════════════
# POST /api/profile/skills
# ══════════════════════════════════════════════════════════════════════════════


class TestAddSkill:
    """Tests for adding a single skill to the user profile."""

    def test_add_skill_returns_updated_list(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Adding a valid new skill → 200 with the skill in the returned list."""
        r = client.post(
            "/api/profile/skills", json={"skill": "docker"}, headers=auth_headers
        )
        assert r.status_code == 200
        assert "docker" in r.json()

    def test_add_multiple_skills_accumulates(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Adding skills one by one should accumulate all of them."""
        client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )
        r = client.post(
            "/api/profile/skills", json={"skill": "fastapi"}, headers=auth_headers
        )
        skills = r.json()
        assert "python" in skills
        assert "fastapi" in skills

    def test_add_duplicate_skill_is_idempotent(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Adding the same skill twice should not create a duplicate entry."""
        client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )
        r = client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )
        assert r.status_code == 200
        skills = r.json()
        assert skills.count("python") == 1

    def test_add_duplicate_case_insensitive(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Adding 'Python' when 'python' already exists should not duplicate."""
        client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )
        r = client.post(
            "/api/profile/skills", json={"skill": "Python"}, headers=auth_headers
        )
        assert r.status_code == 200
        # Should still be exactly one entry
        assert r.json().count("python") + r.json().count("Python") == 1

    def test_add_empty_skill_returns_400(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Posting an empty string skill → 400."""
        r = client.post("/api/profile/skills", json={"skill": ""}, headers=auth_headers)
        assert r.status_code == 400
        assert "empty" in r.json()["detail"].lower()

    def test_add_whitespace_only_skill_returns_400(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Whitespace-only skill string → 400 (via .strip())."""
        r = client.post(
            "/api/profile/skills", json={"skill": "   "}, headers=auth_headers
        )
        assert r.status_code == 400

    def test_add_skill_requires_authentication(self, client: TestClient) -> None:
        """Unauthenticated POST → 401."""
        r = client.post("/api/profile/skills", json={"skill": "python"})
        assert r.status_code == 401


# ══════════════════════════════════════════════════════════════════════════════
# DELETE /api/profile/skills/{skill_name}
# ══════════════════════════════════════════════════════════════════════════════


class TestRemoveSkill:
    """Tests for removing a specific skill from the user profile."""

    def test_remove_existing_skill(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Add then remove a skill → skill no longer in the list."""
        client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )
        client.post(
            "/api/profile/skills", json={"skill": "fastapi"}, headers=auth_headers
        )

        r = client.delete("/api/profile/skills/fastapi", headers=auth_headers)
        assert r.status_code == 200
        assert "fastapi" not in r.json()
        assert "python" in r.json()

    def test_remove_skill_case_insensitive(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Removing 'Python' when 'python' exists should succeed."""
        client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )
        r = client.delete("/api/profile/skills/Python", headers=auth_headers)
        assert r.status_code == 200
        assert "python" not in r.json()
        assert "Python" not in r.json()

    def test_remove_non_existent_skill_returns_404(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Removing a skill the user does not have → 404."""
        r = client.delete("/api/profile/skills/nonexistent", headers=auth_headers)
        assert r.status_code == 404
        assert "not found" in r.json()["detail"].lower()

    def test_remove_skill_requires_authentication(self, client: TestClient) -> None:
        """Unauthenticated DELETE → 401."""
        r = client.delete("/api/profile/skills/python")
        assert r.status_code == 401


# ══════════════════════════════════════════════════════════════════════════════
# POST /api/profile/extract-resume
# ══════════════════════════════════════════════════════════════════════════════


class TestExtractResume:
    """Tests for the resume-based skill extraction endpoint."""

    def test_extract_curated_skills_from_resume(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Skills mentioned in resume text that are in CURATED_SKILLS are added."""
        resume = "I have 5 years of experience with React, Python, and AWS."
        r = client.post(
            "/api/profile/extract-resume",
            json={"resume_text": resume},
            headers=auth_headers,
        )
        assert r.status_code == 200
        skills = r.json()
        assert "python" in skills
        assert "react" in skills
        assert "aws" in skills

    def test_extract_resume_does_not_duplicate_existing_skills(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Skills already in the profile should not be duplicated."""
        # Add python first
        client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )

        resume = "I have experience with Python, React, and Docker."
        r = client.post(
            "/api/profile/extract-resume",
            json={"resume_text": resume},
            headers=auth_headers,
        )
        assert r.status_code == 200
        skills = r.json()
        assert skills.count("python") == 1  # no duplicates

    def test_extract_resume_with_no_curated_skills(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Resume mentioning no curated skills returns existing skills unchanged."""
        client.post(
            "/api/profile/skills", json={"skill": "python"}, headers=auth_headers
        )

        resume = "I enjoy hiking, cooking, and painting."
        r = client.post(
            "/api/profile/extract-resume",
            json={"resume_text": resume},
            headers=auth_headers,
        )
        assert r.status_code == 200
        # python was already there; no new skills added
        assert "python" in r.json()

    def test_extract_resume_requires_authentication(self, client: TestClient) -> None:
        """Unauthenticated POST → 401."""
        r = client.post(
            "/api/profile/extract-resume",
            json={"resume_text": "I know Python."},
        )
        assert r.status_code == 401

    def test_extract_resume_missing_field_returns_422(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Missing resume_text field → 422."""
        r = client.post("/api/profile/extract-resume", json={}, headers=auth_headers)
        assert r.status_code == 422
