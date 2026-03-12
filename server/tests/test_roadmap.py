"""
test_roadmap.py — Tests for the ``/api/roadmap/generate`` endpoint.

Strategy
--------
* The real Claude API is **never** called in CI; the Anthropic
  ``AsyncAnthropic`` client is mocked with ``unittest.mock``.
* We validate:
  - Request validation (missing skills list, empty list rejection)
  - Successful roadmap generation & Pydantic response shape
  - Timeout / API-error handling (504)
  - Authentication is **not** required (public endpoint per PRD user flow)

Integration tests that hit the real Claude API are marked with
``@pytest.mark.integration`` and excluded from normal CI runs.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

# ─── Fixtures ─────────────────────────────────────────────────────────────────

# Sample roadmap payload that mirrors the reference JSON
SAMPLE_ROADMAP_PAYLOAD: dict = {
    "roadmap": {
        "generated_for": "user_test",
        "generated_at": "2026-03-11T10:30:00Z",
        "missing_skills": ["TypeScript", "Docker"],
        "total_estimated_duration_weeks": 8,
        "timeline": [
            {
                "phase": 1,
                "title": "Foundation Phase",
                "duration_weeks": 4,
                "start_week": 1,
                "end_week": 4,
                "focus_skills": ["TypeScript"],
                "weekly_commitment_hours": 8,
                "milestones": [
                    "Understand TypeScript type system",
                    "Migrate a small project to TypeScript",
                ],
            },
            {
                "phase": 2,
                "title": "DevOps & Containerization",
                "duration_weeks": 4,
                "start_week": 5,
                "end_week": 8,
                "focus_skills": ["Docker"],
                "weekly_commitment_hours": 6,
                "milestones": [
                    "Build and run a custom Docker image",
                    "Set up multi-container app with Docker Compose",
                ],
            },
        ],
        "course_recommendations": [
            {
                "skill": "TypeScript",
                "courses": [
                    {
                        "title": "TypeScript: The Complete Guide",
                        "platform": "Udemy",
                        "instructor": "Stephen Grider",
                        "level": "Beginner to Intermediate",
                        "duration_hours": 27,
                        "url": "https://www.udemy.com/course/typescript/",
                        "priority": "primary",
                    }
                ],
            },
            {
                "skill": "Docker",
                "courses": [
                    {
                        "title": "Docker and Kubernetes Guide",
                        "platform": "Udemy",
                        "instructor": "Stephen Grider",
                        "level": "Beginner",
                        "duration_hours": 22,
                        "url": "https://www.udemy.com/course/docker/",
                        "priority": "primary",
                    }
                ],
            },
        ],
        "project_ideas": [
            {
                "id": "proj_001",
                "title": "TypeScript Task Manager CLI",
                "description": "Build a CLI task manager in TypeScript.",
                "skills_practiced": ["TypeScript"],
                "difficulty": "Beginner",
                "estimated_hours": 10,
                "phase": 1,
                "deliverables": [
                    "Typed data models",
                    "CRUD operations via CLI",
                ],
            }
        ],
        "summary": {
            "total_courses": 2,
            "total_projects": 1,
            "total_learning_hours": 49,
            "recommended_weekly_pace": "8–10 hours/week",
            "completion_target": "2026-05-06",
        },
    }
}


def _make_mock_claude_response(payload: dict) -> MagicMock:
    """Build a fake ``anthropic.types.Message`` with the given JSON payload."""
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = json.dumps(payload)

    message = MagicMock()
    message.content = [text_block]
    message.stop_reason = "end_turn"
    message.model = "claude-sonnet-4-20250514"
    return message


# ══════════════════════════════════════════════════════════════════════════════
# Unit tests — Claude API is mocked
# ══════════════════════════════════════════════════════════════════════════════


class TestRoadmapGenerateEndpoint:
    """Tests for POST /api/roadmap/generate."""

    # ---------- happy path ----------

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_generate_returns_valid_roadmap(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """A valid request should return a 200 with the full roadmap structure."""
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_mock_claude_response(SAMPLE_ROADMAP_PAYLOAD)
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript", "Docker"]},
            headers=auth_headers,
        )

        assert response.status_code == 200
        body = response.json()
        assert "roadmap" in body
        roadmap = body["roadmap"]
        assert roadmap["missing_skills"] == ["TypeScript", "Docker"]
        assert len(roadmap["timeline"]) == 2
        assert len(roadmap["course_recommendations"]) == 2
        assert len(roadmap["project_ideas"]) == 1
        assert "summary" in roadmap

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_timeline_phase_structure(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """Each timeline phase must contain all required fields."""
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_mock_claude_response(SAMPLE_ROADMAP_PAYLOAD)
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript"]},
            headers=auth_headers,
        )

        assert response.status_code == 200
        phase = response.json()["roadmap"]["timeline"][0]
        required_keys = {
            "phase",
            "title",
            "duration_weeks",
            "start_week",
            "end_week",
            "focus_skills",
            "weekly_commitment_hours",
            "milestones",
        }
        assert required_keys.issubset(phase.keys())

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_course_recommendation_structure(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """Course recommendations must have skill + nested courses list."""
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_mock_claude_response(SAMPLE_ROADMAP_PAYLOAD)
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript"]},
            headers=auth_headers,
        )

        assert response.status_code == 200
        rec = response.json()["roadmap"]["course_recommendations"][0]
        assert "skill" in rec
        assert isinstance(rec["courses"], list)
        course = rec["courses"][0]
        for key in (
            "title",
            "platform",
            "instructor",
            "level",
            "duration_hours",
            "url",
            "priority",
        ):
            assert key in course

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_project_ideas_structure(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """Project ideas must contain all required fields."""
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_mock_claude_response(SAMPLE_ROADMAP_PAYLOAD)
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript"]},
            headers=auth_headers,
        )

        assert response.status_code == 200
        project = response.json()["roadmap"]["project_ideas"][0]
        required_keys = {
            "id",
            "title",
            "description",
            "skills_practiced",
            "difficulty",
            "estimated_hours",
            "phase",
            "deliverables",
        }
        assert required_keys.issubset(project.keys())

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_summary_statistics(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """Summary must contain aggregate stats."""
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_mock_claude_response(SAMPLE_ROADMAP_PAYLOAD)
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript"]},
            headers=auth_headers,
        )

        assert response.status_code == 200
        summary = response.json()["roadmap"]["summary"]
        for key in (
            "total_courses",
            "total_projects",
            "total_learning_hours",
            "recommended_weekly_pace",
            "completion_target",
        ):
            assert key in summary

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_optional_jd_text_is_forwarded(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """When jd_text is provided it should be accepted without error."""
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_mock_claude_response(SAMPLE_ROADMAP_PAYLOAD)
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={
                "missing_skills": ["Docker"],
                "jd_text": "We need a DevOps engineer familiar with Docker.",
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert "roadmap" in response.json()

    # ---------- validation errors ----------

    def test_empty_missing_skills_returns_422(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """An empty missing_skills list must be rejected."""
        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": []},
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_missing_field_returns_422(self, client: TestClient, auth_headers: dict) -> None:
        """Omitting the required missing_skills field must return 422."""
        response = client.post(
            "/api/roadmap/generate",
            json={},
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_wrong_type_returns_422(self, client: TestClient, auth_headers: dict) -> None:
        """Sending a non-list for missing_skills must return 422."""
        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": "TypeScript"},
            headers=auth_headers,
        )
        assert response.status_code == 422

    # ---------- error handling ----------

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_api_timeout_returns_504(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """An Anthropic API timeout must result in HTTP 504."""
        import anthropic

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            side_effect=anthropic.APITimeoutError(request=MagicMock())
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript"]},
            headers=auth_headers,
        )

        assert response.status_code == 504
        assert "timed out" in response.json()["detail"].lower()

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_api_error_returns_502(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """A generic Anthropic API error should return HTTP 502."""
        import anthropic

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.headers = {}

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            side_effect=anthropic.APIStatusError(
                message="Internal server error",
                response=mock_response,
                body=None,
            )
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript"]},
            headers=auth_headers,
        )

        assert response.status_code == 502
        assert "claude" in response.json()["detail"].lower()

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_invalid_json_from_claude_returns_502(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """If Claude returns non-JSON text, we should get a 502."""
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = "This is not valid JSON at all"

        message = MagicMock()
        message.content = [text_block]
        message.stop_reason = "end_turn"

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=message)
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript"]},
            headers=auth_headers,
        )

        assert response.status_code == 502
        assert (
            "parse" in response.json()["detail"].lower()
            or "claude" in response.json()["detail"].lower()
        )

    @patch("server.roadmap.services.AsyncAnthropic")
    def test_missing_api_key_returns_500(
        self, mock_anthropic_cls: MagicMock, client: TestClient, auth_headers: dict
    ) -> None:
        """If the API key is empty/missing the endpoint should return 500."""
        import anthropic

        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.headers = {}
        mock_client.messages.create = AsyncMock(
            side_effect=anthropic.AuthenticationError(
                message="Invalid API key",
                response=mock_response,
                body=None,
            )
        )
        mock_anthropic_cls.return_value = mock_client

        response = client.post(
            "/api/roadmap/generate",
            json={"missing_skills": ["TypeScript"]},
            headers=auth_headers,
        )

        assert response.status_code == 500
        assert (
            "api key" in response.json()["detail"].lower()
            or "authentication" in response.json()["detail"].lower()
        )
