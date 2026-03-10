from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from server.database import Base

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    company_name = Column(String, nullable=True)
    position_name = Column(String, nullable=True)
    date_analyzed = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    match_score = Column(Float, nullable=False)
    have_skills = Column(ARRAY(String), nullable=False)
    missing_skills = Column(ARRAY(String), nullable=False)
    bonus_skills = Column(ARRAY(String), nullable=False)

    user = relationship("User", backref="analysis_history")
