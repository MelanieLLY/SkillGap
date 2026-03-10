from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional

from .engine import extract_skills, extract_company_and_position

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
    company_name: Optional[str] = None
    position_name: Optional[str] = None


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
    extracted_info = extract_company_and_position(request.job_description)
    
    # Return as a dictionary that matches the ExtractResponse model
    return {
        **result,
        "company_name": extracted_info.get("company_name"),
        "position_name": extracted_info.get("position_name")
    }
