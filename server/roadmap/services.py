"""
services.py — Async service layer for Claude-powered roadmap generation.

Responsibilities
----------------
* Build the prompt from the caller's missing-skills list (and optional JD text).
* Call the Anthropic Messages API with a strict timeout.
* Parse & validate the JSON response into Pydantic models.
* Surface clear, typed exceptions so the router can return proper HTTP codes.

The ``ANTHROPIC_API_KEY`` is read exclusively from ``server.core.config.settings``
which itself loads from ``.env`` — **never** hard-coded.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from anthropic import (
    APIStatusError,
    APITimeoutError,
    AsyncAnthropic,
    AuthenticationError,
)
from pydantic import ValidationError

from server.core.config import settings
from server.roadmap.schemas import RoadmapGenerateResponse

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

# Model mandated by project rules (.antigravityrules §1)
CLAUDE_MODEL: str = "claude-sonnet-4-20250514"

# Maximum tokens for the response
MAX_TOKENS: int = 4096

# Timeout in seconds for the Anthropic API call
API_TIMEOUT_SECONDS: float = 120.0


# ── Custom exceptions ────────────────────────────────────────────────────────


class ClaudeTimeoutError(Exception):
    """Raised when the Anthropic API call times out."""


class ClaudeAPIError(Exception):
    """Raised on any non-timeout Anthropic API error."""


class ClaudeAuthError(Exception):
    """Raised when the API key is invalid or missing."""


class ClaudeParseError(Exception):
    """Raised when Claude's response cannot be parsed into valid JSON / Pydantic."""


# ── Prompt builder ────────────────────────────────────────────────────────────


def _build_prompt(missing_skills: list[str], jd_text: str | None = None) -> str:
    """
    Build the user prompt for Claude.

    Args:
        missing_skills: Skills the user needs to learn.
        jd_text: Optional raw job-description for extra context.

    Returns:
        A formatted prompt string instructing Claude to produce a
        structured JSON learning roadmap.
    """
    skills_csv = ", ".join(missing_skills)
    jd_section = ""
    if jd_text:
        jd_section = (
            f"\n\nThe following is the original job description for context:\n"
            f"---\n{jd_text}\n---"
        )

    return (
        f"I need to learn the following skills: {skills_csv}.{jd_section}\n\n"
        "Please generate a **personalized structured learning roadmap** for me. "
        "The response MUST be **pure JSON only** (no markdown, no commentary, no "
        "code fences) with the following top-level structure:\n\n"
        "{\n"
        '  "roadmap": {\n'
        '    "missing_skills": [...],\n'
        '    "total_estimated_duration_weeks": <int>,\n'
        '    "timeline": [\n'
        "      {\n"
        '        "phase": <int>,\n'
        '        "title": "<string>",\n'
        '        "duration_weeks": <int>,\n'
        '        "start_week": <int>,\n'
        '        "end_week": <int>,\n'
        '        "focus_skills": [...],\n'
        '        "weekly_commitment_hours": <int>,\n'
        '        "milestones": [...]\n'
        "      }\n"
        "    ],\n"
        '    "course_recommendations": [\n'
        "      {\n"
        '        "skill": "<string>",\n'
        '        "courses": [\n'
        "          {\n"
        '            "title": "<string>",\n'
        '            "platform": "<string>",\n'
        '            "instructor": "<string>",\n'
        '            "level": "<string>",\n'
        '            "duration_hours": <int>,\n'
        '            "url": "<string>",\n'
        '            "priority": "primary" | "supplementary"\n'
        "          }\n"
        "        ]\n"
        "      }\n"
        "    ],\n"
        '    "project_ideas": [\n'
        "      {\n"
        '        "id": "<string>",\n'
        '        "title": "<string>",\n'
        '        "description": "<string>",\n'
        '        "skills_practiced": [...],\n'
        '        "difficulty": "<string>",\n'
        '        "estimated_hours": <int>,\n'
        '        "phase": <int>,\n'
        '        "deliverables": [...]\n'
        "      }\n"
        "    ],\n"
        '    "summary": {\n'
        '      "total_courses": <int>,\n'
        '      "total_projects": <int>,\n'
        '      "total_learning_hours": <int>,\n'
        '      "recommended_weekly_pace": "<string>",\n'
        '      "completion_target": "<ISO date string>"\n'
        "    }\n"
        "  }\n"
        "}\n\n"
        "Important rules:\n"
        "1. Return ONLY the JSON object — no extra text.\n"
        "2. Every skill in missing_skills must appear in at least one timeline phase.\n"
        "3. Provide at least two courses per skill (one primary, one supplementary).\n"
        "4. The final phase should be a capstone integrating all skills."
    )


# ── Core service function ────────────────────────────────────────────────────


async def generate_roadmap_with_claude(
    missing_skills: list[str],
    jd_text: str | None = None,
) -> RoadmapGenerateResponse:
    """
    Call the Anthropic Claude API to generate a structured learning roadmap.

    Args:
        missing_skills: Non-empty list of skill strings the user is missing.
        jd_text: Optional raw job-description text for additional context.

    Returns:
        RoadmapGenerateResponse: A fully validated Pydantic model containing
        the generated learning roadmap.

    Raises:
        ClaudeAuthError: API key is invalid or not configured.
        ClaudeTimeoutError: The API call exceeded the timeout.
        ClaudeAPIError: Any non-timeout API error from Anthropic.
        ClaudeParseError: Claude returned non-JSON or schema-invalid output.
    """
    client = AsyncAnthropic(
        api_key=settings.anthropic_api_key,
        timeout=API_TIMEOUT_SECONDS,
    )

    prompt = _build_prompt(missing_skills, jd_text)

    try:
        response = await client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
    except AuthenticationError as exc:
        logger.error("Anthropic authentication failed: %s", exc)
        raise ClaudeAuthError(
            "The ANTHROPIC_API_KEY is invalid or not configured."
        ) from exc
    except APITimeoutError as exc:
        logger.error("Anthropic API timeout after %.0fs: %s", API_TIMEOUT_SECONDS, exc)
        raise ClaudeTimeoutError(
            f"Claude API timed out after {API_TIMEOUT_SECONDS}s."
        ) from exc
    except APIStatusError as exc:
        logger.error("Anthropic API error (status %s): %s", exc.status_code, exc)
        raise ClaudeAPIError(
            f"Claude API returned status {exc.status_code}: {exc.message}"
        ) from exc

    # ── Parse the text response ───────────────────────────────────────────
    raw_text = _extract_text(response)
    data = _parse_json(raw_text)
    return _validate_roadmap(data)


# ── Internal helpers ──────────────────────────────────────────────────────────


def _extract_text(response: Any) -> str:
    """
    Pull the first ``text`` content block from an Anthropic response.

    Args:
        response: The raw Anthropic Message object.

    Returns:
        The raw text string from the first text block.

    Raises:
        ClaudeParseError: If no text block is found.
    """
    for block in response.content:
        if getattr(block, "type", None) == "text":
            return block.text
    raise ClaudeParseError("Claude response contained no text content block.")


def _parse_json(raw_text: str) -> dict[str, Any]:
    """
    Parse a raw string as JSON.

    Args:
        raw_text: The raw text from Claude's response.

    Returns:
        Parsed JSON as a dictionary.

    Raises:
        ClaudeParseError: If the text is not valid JSON.
    """
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse Claude response as JSON: %s", exc)
        raise ClaudeParseError(
            f"Could not parse Claude's response as JSON: {exc}"
        ) from exc


def _validate_roadmap(data: dict[str, Any]) -> RoadmapGenerateResponse:
    """
    Validate parsed JSON against the ``RoadmapGenerateResponse`` Pydantic model.

    Args:
        data: Parsed JSON dictionary.

    Returns:
        RoadmapGenerateResponse: A validated Pydantic model.

    Raises:
        ClaudeParseError: If the JSON does not match the expected schema.
    """
    try:
        return RoadmapGenerateResponse.model_validate(data)
    except ValidationError as exc:
        logger.error("Roadmap schema validation failed: %s", exc)
        raise ClaudeParseError(
            f"Claude's response did not match the expected roadmap schema: {exc}"
        ) from exc
