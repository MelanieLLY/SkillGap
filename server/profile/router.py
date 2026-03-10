from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from server.database import get_db
from server.auth import models, deps
from server.profile import schemas
from server.extraction.engine import CURATED_SKILLS
import re

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/skills", response_model=List[str])
def get_skills(current_user: models.User = Depends(deps.get_current_active_user)):
    return current_user.skills or []

@router.post("/skills", response_model=List[str])
def add_skill(
    skill_req: schemas.SkillAddRequest, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    skill = skill_req.skill.strip()
    if not skill:
        raise HTTPException(status_code=400, detail="Skill cannot be empty")
        
    current_skills = current_user.skills or []
    if skill not in current_skills:
        new_skills = list(current_skills)
        new_skills.append(skill)
        current_user.skills = new_skills
        db.commit()
        db.refresh(current_user)
        
    return current_user.skills or []

@router.delete("/skills/{skill_name}", response_model=List[str])
def remove_skill(
    skill_name: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    current_skills = current_user.skills or []
    if skill_name in current_skills:
        new_skills = [s for s in current_skills if s != skill_name]
        current_user.skills = new_skills
        db.commit()
        db.refresh(current_user)
        
    return current_user.skills or []

@router.post("/extract-resume", response_model=List[str])
def extract_resume_skills(
    req: schemas.ResumeExtractRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    if not req.resume_text:
        return current_user.skills or []
        
    resume_text = req.resume_text.lower()
    current_skills = current_user.skills or []
    current_skills_set = set([s.lower() for s in current_skills])
    
    found_skills = set()
    for skill in CURATED_SKILLS:
        escaped_skill = re.escape(skill)
        pattern = rf"(?<![a-zA-Z0-9+#]){escaped_skill}(?![a-zA-Z0-9+#])"
        if re.search(pattern, resume_text):
            found_skills.add(skill)
            
    # Add newly found skills to user profile
    new_skills_to_add = []
    for skill in found_skills:
        if skill.lower() not in current_skills_set:
            new_skills_to_add.append(skill)
            
    if new_skills_to_add:
        updated_skills = list(current_skills) + new_skills_to_add
        current_user.skills = updated_skills
        db.commit()
        db.refresh(current_user)
        
    return current_user.skills or []
