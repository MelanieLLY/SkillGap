from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from .engine import extract_company_and_position, extract_skills

router = APIRouter()


class ExtractRequest(BaseModel):
    """Request body for the skill extraction endpoint."""
    job_description: str
    user_skills: list[str]


class ExtractResponse(BaseModel):
    """Response body with categorized skills."""
    have: list[str]
    missing: list[str]
    bonus: list[str]
    company_name: str | None = None
    position_name: str | None = None


@router.post("/extract", response_model=ExtractResponse)
async def extract_endpoint(request: ExtractRequest) -> dict[str, Any]:
    """
    Extract skills and categorize them into 'have', 'missing', and 'bonus'.
    Also attempts to extract the company name and position name from the job description.

    Args:
        request (ExtractRequest): The request payload containing user skills and job description.

    Returns:
        Dict[str, Any]: A dictionary containing categorized skills along with extracted
                        company name and position name, adhering to ExtractResponse.
    """
    result = extract_skills(
        job_description=request.job_description,
        user_skills=request.user_skills,
    )
    extracted_info = extract_company_and_position(request.job_description)

    # Return as a dictionary that matches the ExtractResponse model
    return {
        **result,
        "company_name": extracted_info.get("company_name"),
        "position_name": extracted_info.get("position_name")
    }
