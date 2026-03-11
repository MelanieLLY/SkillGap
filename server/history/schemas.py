from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class HistoryBase(BaseModel):
    company_name: Optional[str] = None
    position_name: Optional[str] = None
    have_skills: List[str]
    missing_skills: List[str]
    bonus_skills: List[str]

class HistoryCreate(HistoryBase):
    pass

class HistoryUpdate(BaseModel):
    company_name: Optional[str] = None
    position_name: Optional[str] = None

class HistoryResponse(HistoryBase):
    id: int
    user_id: int
    match_score: float = Field(..., ge=0, le=100)
    date_analyzed: datetime

    class Config:
        from_attributes = True
