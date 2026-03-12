"""
test_extraction.py — Tests for the extraction engine (pure unit) and the
                      /api/extract HTTP endpoint.

Coverage targets
----------------
Engine (server/extraction/engine.py)
  * extract_skills         – empty inputs, language matching, framework matching,
                             database skills, boundary matching (c++/node.js),
                             cloud/ML tools, purely bonus skills
  * calculate_match_score  – 0/0, all have, none have, partial, rounding
  * extract_company_and_position – both found, only position, neither found

Endpoint (server/extraction/router.py)
  * POST /api/extract      – valid payload, empty JD, missing fields
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from server.extraction.engine import (
    CURATED_SKILLS,
    calculate_match_score,
    extract_company_and_position,
    extract_skills,
)

# ══════════════════════════════════════════════════════════════════════════════
# Pure-unit: extract_skills
# ══════════════════════════════════════════════════════════════════════════════


class TestExtractSkills:
    """Tests for the core keyword-extraction logic."""

    def test_empty_jd_returns_empty_categories(self) -> None:
        """An empty job description must produce all-empty categories."""
        result = extract_skills("", [])
        assert result == {"have": [], "missing": [], "bonus": []}

    def test_non_string_jd_returns_empty_categories(self) -> None:
        """A non-string JD (e.g. None) must be handled gracefully."""
        result = extract_skills(None, [])  # type: ignore[arg-type]
        assert result == {"have": [], "missing": [], "bonus": []}

    def test_no_matches_returns_only_bonus(self) -> None:
        """When the JD mentions no recognised skills, all user skills go to bonus."""
        result = extract_skills("We love great team players!", ["python", "react"])
        assert result["have"] == []
        assert result["missing"] == []
        assert "python" in result["bonus"]
        assert "react" in result["bonus"]

    def test_language_matching(self) -> None:
        """Python, TypeScript, Go must be correctly categorised."""
        jd = "Looking for a Python developer with TypeScript experience. Good to have Go."
        result = extract_skills(jd, ["Python", "JavaScript", "Go"])
        assert "python" in result["have"]
        assert "go" in result["have"]
        assert "typescript" in result["missing"]
        assert "javascript" in result["bonus"]

    def test_framework_matching(self) -> None:
        """React / FastAPI / Django must be split into have/missing/bonus."""
        jd = "Experience with React, FastAPI, Django, and UIAutomator."
        result = extract_skills(jd, ["react", "fastapi", "vue"])
        assert set(result["have"]) == {"react", "fastapi"}
        assert "django" in result["missing"]
        assert "uiautomator" in result["missing"]
        assert set(result["bonus"]) == {"vue"}

    def test_database_skill_matching(self) -> None:
        """PostgreSQL / Redis / MongoDB must be split correctly."""
        jd = "Knowledge of PostgreSQL and Redis."
        result = extract_skills(jd, ["PostgreSQL", "MongoDB"])
        assert "postgresql" in result["have"]
        assert "redis" in result["missing"]
        assert "mongodb" in result["bonus"]

    def test_devops_and_ml_skills(self) -> None:
        """Cloud, container, and ML framework skills must match."""
        jd = "Deploy with Docker, Kubernetes on AWS. ML experience with PyTorch, scikit-learn, LangChain."
        result = extract_skills(
            jd, ["Docker", "Git", "AWS", "TensorFlow", "scikit-learn"]
        )
        assert {"docker", "aws", "scikit-learn"}.issubset(set(result["have"]))
        assert {"kubernetes", "pytorch", "langchain"}.issubset(set(result["missing"]))
        assert "git" in result["bonus"]
        assert "tensorflow" in result["bonus"]

    def test_word_boundary_prevents_false_positive(self) -> None:
        """'java' in 'javascript' must NOT be matched as a separate java hit."""
        jd = "We use JavaScript heavily."
        result = extract_skills(jd, [])
        assert "javascript" in result["missing"]
        # 'java' by itself should NOT be in missing (it's a substring of javascript)
        assert "java" not in result["missing"]

    def test_special_characters_match(self) -> None:
        """Skills containing special chars like C++ and Node.js must be matched."""
        jd = "Must know C++, Node.js, and Java. Also JavaScript."
        result = extract_skills(jd, ["c++", "Node.js"])
        assert "c++" in result["have"]
        assert "node.js" in result["have"]
        assert "javascript" in result["missing"]

    def test_case_insensitive_user_skills(self) -> None:
        """User skill capitalisation should not affect matching."""
        jd = "We use python and docker."
        result = extract_skills(jd, ["PYTHON", "DOCKER"])
        assert "python" in result["have"]
        assert "docker" in result["have"]

    def test_empty_user_skills_yields_only_missing(self) -> None:
        """If user has no skills, everything in the JD is 'missing'."""
        jd = "We need python and react."
        result = extract_skills(jd, [])
        assert "python" in result["missing"]
        assert "react" in result["missing"]
        assert result["have"] == []
        assert result["bonus"] == []

    def test_all_user_skills_match_jd(self) -> None:
        """If user has ALL required JD skills, missing and bonus are empty."""
        jd = "We need python and react."
        result = extract_skills(jd, ["python", "react"])
        assert "python" in result["have"]
        assert "react" in result["have"]
        assert result["missing"] == []
        assert result["bonus"] == []

    def test_user_skill_not_in_curated_set_still_matched(self) -> None:
        """User skills that are not in CURATED_SKILLS should still be matched in the JD."""
        jd = "We use bizarroframework heavily."
        result = extract_skills(jd, ["bizarroframework"])
        assert "bizarroframework" in result["have"]

    def test_result_keys_always_present(self) -> None:
        """The result dict must always contain exactly the three expected keys."""
        result = extract_skills("some random text", ["python"])
        assert set(result.keys()) == {"have", "missing", "bonus"}


# ══════════════════════════════════════════════════════════════════════════════
# Pure-unit: calculate_match_score
# ══════════════════════════════════════════════════════════════════════════════


class TestCalculateMatchScore:
    """Tests for the match-score computation function."""

    def test_empty_inputs_return_zero(self) -> None:
        assert calculate_match_score([], []) == 0.0

    def test_full_match_returns_100(self) -> None:
        assert calculate_match_score(["python", "react"], []) == 100.0

    def test_no_match_returns_zero(self) -> None:
        assert calculate_match_score([], ["python", "react"]) == 0.0

    def test_partial_match_50_percent(self) -> None:
        """2 have out of 4 total → 50.0."""
        assert (
            calculate_match_score(["python", "react"], ["django", "postgres"]) == 50.0
        )

    def test_rounding_two_decimal_places(self) -> None:
        """2 / 3 = 66.666… → rounds to 66.67."""
        assert calculate_match_score(["python", "react"], ["django"]) == 66.67

    def test_single_skill_match(self) -> None:
        assert calculate_match_score(["python"], []) == 100.0

    def test_single_skill_miss(self) -> None:
        assert calculate_match_score([], ["python"]) == 0.0

    def test_large_skill_list(self) -> None:
        """Score should be calculable for realistic-size skill sets."""
        have = [f"skill_{i}" for i in range(40)]
        missing = [f"skill_{i}" for i in range(40, 50)]
        score = calculate_match_score(have, missing)
        # 40 / 50 = 80.0
        assert score == 80.0


# ══════════════════════════════════════════════════════════════════════════════
# Pure-unit: extract_company_and_position
# ══════════════════════════════════════════════════════════════════════════════


class TestExtractCompanyAndPosition:
    """Tests for the heuristic company/position extraction."""

    def test_both_company_and_role_found(self) -> None:
        jd = "Company: TechLogix Inc.\nRole: Senior Developer"
        result = extract_company_and_position(jd)
        assert result["company_name"] == "TechLogix Inc."
        assert result["position_name"] == "Senior Developer"

    def test_position_keyword_variants(self) -> None:
        """Different keywords (Title, Position, Job) should all be picked up."""
        for keyword in ("Title", "Position", "Job"):
            jd = f"{keyword}: Software Engineer"
            result = extract_company_and_position(jd)
            assert (
                result["position_name"] == "Software Engineer"
            ), f"Failed for keyword: {keyword}"

    def test_only_position_found(self) -> None:
        jd = "We are hiring! Position: Software Engineer"
        result = extract_company_and_position(jd)
        assert result["company_name"] is None
        assert result["position_name"] == "Software Engineer"

    def test_neither_found_returns_none(self) -> None:
        jd = "No obvious fields here."
        result = extract_company_and_position(jd)
        assert result["company_name"] is None
        assert result["position_name"] is None

    def test_case_insensitive_company_field(self) -> None:
        jd = "COMPANY: MegaCorp\nROLE: Lead Engineer"
        result = extract_company_and_position(jd)
        assert result["company_name"] == "MegaCorp"
        assert result["position_name"] == "Lead Engineer"

    def test_result_always_has_both_keys(self) -> None:
        result = extract_company_and_position("")
        assert "company_name" in result
        assert "position_name" in result


# ══════════════════════════════════════════════════════════════════════════════
# Integration: POST /api/extract endpoint
# ══════════════════════════════════════════════════════════════════════════════


class TestExtractEndpoint:
    """HTTP-level tests for the extraction endpoint (no auth required)."""

    def test_extract_happy_path(self, client: TestClient) -> None:
        """Valid request must return categorised skills + extracted metadata."""
        payload = {
            "job_description": "Company: Acme Corp.\nRole: Backend Dev.\nWe need Python and Docker.",
            "user_skills": ["python", "react"],
        }
        r = client.post("/api/extract", json=payload)
        assert r.status_code == 200
        body = r.json()
        assert "have" in body
        assert "missing" in body
        assert "bonus" in body
        assert "python" in body["have"]
        assert "docker" in body["missing"]
        assert "react" in body["bonus"]
        assert body["company_name"] == "Acme Corp."
        assert body["position_name"] == "Backend Dev."

    def test_extract_empty_jd_returns_empty_categories(
        self, client: TestClient
    ) -> None:
        """Empty JD string → all skill lists empty."""
        r = client.post("/api/extract", json={"job_description": "", "user_skills": []})
        assert r.status_code == 200
        body = r.json()
        assert body["have"] == []
        assert body["missing"] == []
        assert body["bonus"] == []

    def test_extract_no_metadata_in_jd(self, client: TestClient) -> None:
        """JD without Company/Role → company_name and position_name are None."""
        r = client.post(
            "/api/extract",
            json={"job_description": "We need python.", "user_skills": []},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["company_name"] is None
        assert body["position_name"] is None

    def test_extract_missing_job_description_field_returns_422(
        self, client: TestClient
    ) -> None:
        """Missing required field → 422 Unprocessable Entity."""
        r = client.post("/api/extract", json={"user_skills": ["python"]})
        assert r.status_code == 422

    def test_extract_missing_user_skills_field_returns_422(
        self, client: TestClient
    ) -> None:
        """Missing user_skills → 422 Unprocessable Entity."""
        r = client.post("/api/extract", json={"job_description": "Need python."})
        assert r.status_code == 422

    def test_extract_empty_user_skills_is_valid(self, client: TestClient) -> None:
        """Explicitly providing an empty user_skills list is valid."""
        r = client.post(
            "/api/extract",
            json={"job_description": "Need python and react.", "user_skills": []},
        )
        assert r.status_code == 200
        body = r.json()
        assert "python" in body["missing"] or "python" in body["have"]


# ══════════════════════════════════════════════════════════════════════════════
# Sanity check: CURATED_SKILLS set
# ══════════════════════════════════════════════════════════════════════════════


class TestCuratedSkillsSet:
    """Validate the curated skills constant itself."""

    def test_curated_skills_is_a_set(self) -> None:
        assert isinstance(CURATED_SKILLS, set)

    def test_curated_skills_all_lowercase(self) -> None:
        """All entries must be lowercase for matching to work correctly."""
        non_lower = [s for s in CURATED_SKILLS if s != s.lower()]
        assert non_lower == [], f"Non-lowercase skills found: {non_lower}"

    def test_core_skills_present(self) -> None:
        """Key skills used throughout the app must be in the set."""
        expected = {"python", "react", "docker", "fastapi", "postgresql", "typescript"}
        assert expected.issubset(CURATED_SKILLS)
