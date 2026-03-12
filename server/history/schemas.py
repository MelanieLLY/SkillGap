from datetime import datetime

from pydantic import BaseModel, Field


class HistoryBase(BaseModel):
    company_name: str | None = None
    position_name: str | None = None
    have_skills: list[str]
    missing_skills: list[str]
    bonus_skills: list[str]

class HistoryCreate(HistoryBase):
    pass

class HistoryUpdate(BaseModel):
    company_name: str | None = None
    position_name: str | None = None

class HistoryResponse(HistoryBase):
    id: int
    user_id: int
    match_score: float = Field(..., ge=0, le=100)
    date_analyzed: datetime

    class Config:
        from_attributes = True
