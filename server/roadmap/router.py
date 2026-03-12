"""
router.py — FastAPI router for the ``/api/roadmap`` endpoints.

Provides the ``POST /generate`` endpoint that accepts a list of missing
skills, delegates to the Claude service, and returns a validated
learning-roadmap JSON payload.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.auth import models
from server.auth.deps import get_current_active_user
from server.database import get_db
from server.roadmap.schemas import RoadmapGenerateRequest, RoadmapGenerateResponse
from server.roadmap.services import (
    ClaudeAPIError,
    ClaudeAuthError,
    ClaudeParseError,
    ClaudeTimeoutError,
    generate_roadmap_with_claude,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate", response_model=RoadmapGenerateResponse)
async def generate_roadmap(
    request: RoadmapGenerateRequest,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> RoadmapGenerateResponse:
    """
    Generate a personalised learning roadmap using Claude AI.

    Accepts a list of missing skills (and optional raw JD text), calls the
    Anthropic Claude API, and returns a structured roadmap containing:
    - A phased timeline with milestones
    - Course recommendations per skill
    - Hands-on project ideas
    - Aggregate summary statistics

    Args:
        request (RoadmapGenerateRequest): The client payload with
            ``missing_skills`` (required) and ``jd_text`` (optional).

    Returns:
        RoadmapGenerateResponse: The validated learning roadmap.

    Raises:
        HTTPException 504: Claude API timed out.
        HTTPException 502: Claude returned an error or unparseable response.
        HTTPException 500: API key authentication failed.
    """
    try:
        roadmap_response = await generate_roadmap_with_claude(
            missing_skills=request.missing_skills,
            jd_text=request.jd_text,
        )
    except ClaudeTimeoutError as exc:
        logger.error("Roadmap generation timed out: %s", exc)
        raise HTTPException(
            status_code=504,
            detail="Claude API request timed out. Please try again later.",
        ) from exc
    except ClaudeAuthError as exc:
        logger.error("Roadmap generation auth error: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Claude API key authentication failed. "
            "Please verify ANTHROPIC_API_KEY is configured.",
        ) from exc
    except ClaudeAPIError as exc:
        logger.error("Roadmap generation API error: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"Claude API returned an error: {exc}",
        ) from exc
    except ClaudeParseError as exc:
        logger.error("Roadmap response parse error: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"Failed to parse Claude's response: {exc}",
        ) from exc

    # Persist the newly generated roadmap to the user's profile
    current_user.roadmap = roadmap_response.roadmap.model_dump()
    db.commit()

    return roadmap_response
