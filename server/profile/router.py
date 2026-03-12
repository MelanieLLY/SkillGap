import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.auth.deps import get_current_active_user
from server.auth.models import User
from server.database import get_db
from server.extraction.engine import CURATED_SKILLS
from server.profile.schemas import ResumeExtractRequest, SkillAddRequest

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/skills", response_model=list[str])
def get_skills(current_user: User = Depends(get_current_active_user)) -> list[str]:
    """
    Retrieve the current user's skills.

    Args:
        current_user (User): The currently authenticated user instance.

    Returns:
        List[str]: A list of skill strings associated with the user.
    """
    return current_user.skills if current_user.skills else []

@router.post("/skills", response_model=list[str])
def add_skill(
    request: SkillAddRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> list[str]:
    """
    Add a single skill to the current user's profile.

    Args:
        request (SkillAddRequest): The request payload containing the skill to add.
        current_user (User): The currently authenticated user instance.
        db (Session): The synchronous database session.

    Returns:
        List[str]: The updated list of skills for the user.

    Raises:
        HTTPException: If the provided skill is empty string.
    """
    skill = request.skill.strip()
    if not skill:
        raise HTTPException(status_code=400, detail="Skill cannot be empty")

    current_skills = list(current_user.skills) if current_user.skills else []

    # Check if skill already exists (case insensitive)
    if any(s.lower() == skill.lower() for s in current_skills):
        return current_skills

    current_skills.append(skill)
    current_user.skills = current_skills
    db.commit()
    return current_skills

@router.delete("/skills/{skill_name}", response_model=list[str])
def remove_skill(
    skill_name: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> list[str]:
    """
    Remove a specific skill from the user's profile.

    Args:
        skill_name (str): The name of the skill to be removed.
        current_user (User): The currently authenticated user instance.
        db (Session): The synchronous database session.

    Returns:
        List[str]: The updated list of skills for the user after removal.

    Raises:
        HTTPException: If the skill is not found in the user's profile.
    """
    current_skills = list(current_user.skills) if current_user.skills else []

    # Filter out exactly matching or case-insensitive matching
    new_skills = [s for s in current_skills if s.lower() != skill_name.lower()]

    if len(new_skills) == len(current_skills):
        raise HTTPException(status_code=404, detail="Skill not found in profile")

    current_user.skills = new_skills
    db.commit()
    return new_skills

@router.post("/extract-resume", response_model=list[str])
def extract_from_resume(
    request: ResumeExtractRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> list[str]:
    """
    Extract skills from a provided resume text and save them to the user's profile.

    Args:
        request (ResumeExtractRequest): The request payload containing the resume text.
        current_user (User): The currently authenticated user instance.
        db (Session): The synchronous database session.

    Returns:
        List[str]: The updated list of skills for the user after extraction and saving.
    """
    resume_text = request.resume_text.lower()

    current_skills = list(current_user.skills) if current_user.skills else []
    current_skills_lower = {s.lower() for s in current_skills}

    found_skills = set()

    for skill in CURATED_SKILLS:
        # Prevent re-adding if they already have it
        if skill.lower() in current_skills_lower:
            continue

        escaped_skill = re.escape(skill)
        pattern = rf"(?<![a-zA-Z0-9+#]){escaped_skill}(?![a-zA-Z0-9+#])"
        if re.search(pattern, resume_text):
            found_skills.add(skill)

    if found_skills:
        current_skills.extend(list(found_skills))
        current_user.skills = current_skills
        db.commit()

    return current_skills
