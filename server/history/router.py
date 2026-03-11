from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import schemas
from . import models as history_models
from server.database import get_db
from server.auth.deps import get_current_active_user
from server.auth import models as auth_models
from server.extraction.engine import calculate_match_score

router = APIRouter()

@router.get("/", response_model=List[schemas.HistoryResponse])
def get_user_history(
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_active_user)
):
    """
    Retrieve all analysis history records for the current authenticated user.
    """
    history_records = db.query(history_models.AnalysisHistory)\
        .filter(history_models.AnalysisHistory.user_id == current_user.id)\
        .order_by(history_models.AnalysisHistory.date_analyzed.desc())\
        .all()
    return history_records

@router.post("/", response_model=schemas.HistoryResponse)
def create_history(
    history_in: schemas.HistoryCreate,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_active_user)
):
    """
    Create a new analysis history record for the current authenticated user.
    """
    match_score = calculate_match_score(history_in.have_skills, history_in.missing_skills)

    db_history = history_models.AnalysisHistory(
        user_id=current_user.id,
        match_score=match_score,
        **history_in.model_dump()
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

@router.put("/{history_id}", response_model=schemas.HistoryResponse)
def update_history(
    history_id: int,
    history_update: schemas.HistoryUpdate,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_active_user)
):
    """
    Update an existing history record (company name or position name).
    Enforces that the record belongs to the authenticated user.
    """
    db_history = db.query(history_models.AnalysisHistory).filter(history_models.AnalysisHistory.id == history_id).first()
    
    if not db_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History record not found")
        
    if db_history.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to update this history record"
        )
        
    update_data = history_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_history, key, value)
        
    db.commit()
    db.refresh(db_history)
    return db_history
