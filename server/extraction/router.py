from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from .engine import extract_skills

router = APIRouter()


class ExtractRequest(BaseModel):
    """Request body for the skill extraction endpoint."""
    job_description: str
    user_skills: List[str]


class ExtractResponse(BaseModel):
    """Response body with categorized skills."""
    have: List[str]
    missing: List[str]
    bonus: List[str]


@router.post("/extract", response_model=ExtractResponse)
async def extract_endpoint(request: ExtractRequest) -> Dict[str, List[str]]:
    """
    Accepts a job description and a list of user skills,
    returns them categorized into 'have', 'missing', and 'bonus'.
    """
    result = extract_skills(
        job_description=request.job_description,
        user_skills=request.user_skills,
    )
    return result
