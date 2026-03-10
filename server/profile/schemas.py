from pydantic import BaseModel
from typing import List

class SkillAddRequest(BaseModel):
    skill: str

class ResumeExtractRequest(BaseModel):
    resume_text: str
