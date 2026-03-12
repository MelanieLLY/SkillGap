from pydantic import BaseModel


class SkillAddRequest(BaseModel):
    skill: str


class ResumeExtractRequest(BaseModel):
    resume_text: str
