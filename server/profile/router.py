from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from server.database import get_db
from server.auth.models import User
from server.auth.deps import get_current_active_user
from server.profile.schemas import SkillAddRequest, ResumeExtractRequest
from server.extraction.engine import CURATED_SKILLS
import re

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/skills", response_model=List[str])
def get_skills(current_user: User = Depends(get_current_active_user)):
    """Retrieve the current user's skills"""
    return current_user.skills if current_user.skills else []

@router.post("/skills", response_model=List[str])
def add_skill(
    request: SkillAddRequest, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a single skill to the current user's profile"""
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

@router.delete("/skills/{skill_name}", response_model=List[str])
def remove_skill(
    skill_name: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a skill from the user's profile"""
    current_skills = list(current_user.skills) if current_user.skills else []
    
    # Filter out exactly matching or case-insensitive matching
    new_skills = [s for s in current_skills if s.lower() != skill_name.lower()]
    
    if len(new_skills) == len(current_skills):
        raise HTTPException(status_code=404, detail="Skill not found in profile")
        
    current_user.skills = new_skills
    db.commit()
    return new_skills

@router.post("/extract-resume", response_model=List[str])
def extract_from_resume(
    request: ResumeExtractRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Extract skills from a resume text and save them to the user's profile."""
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
