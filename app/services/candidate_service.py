from sqlalchemy.orm import Session
from ..models.candidate import Candidate
import uuid
from datetime import datetime
from ..schemas.candidate import CandidateCreate, CandidateUpdate

def create_candidate(db: Session, candidate: CandidateCreate, user_id: str = None):
    """
    Create a new candidate
    
    Args:
        db: Database session
        candidate: Candidate data
        user_id: Optional user ID (will use candidate.createdBy if not provided)
    """
    # Use provided user_id or fall back to candidate.createdBy
    created_by = user_id if user_id is not None else candidate.createdBy
    last_update_by = user_id if user_id is not None else candidate.lastUpdateBy
    
    db_candidate = Candidate(
        candidateId=str(uuid.uuid4()),
        firstName=candidate.firstName,
        lastName=candidate.lastName,
        currentRole=candidate.currentRole,
        currentEmployer=candidate.currentEmployer,
        currentCTC=candidate.currentCTC,
        expectedCTC=candidate.expectedCTC,
        contactDate=candidate.contactDate,
        tags=candidate.tags,
        status=candidate.status,
        latestJDReference=candidate.latestJDReference,
        created_by=created_by,
        last_update_by=last_update_by
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def get_candidate(db: Session, candidate_id: str):
    return db.query(Candidate).filter(Candidate.candidateId == candidate_id).first()

def get_all_candidates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Candidate).offset(skip).limit(limit).all()

def update_candidate(db: Session, candidate_id: str, candidate: CandidateUpdate, user_id: str):
    db_candidate = get_candidate(db, candidate_id)
    if not db_candidate:
        return None
    
    update_data = candidate.model_dump(exclude_unset=True)
    
    # Map field names to SQLAlchemy columns
    field_mapping = {
        'lastUpdateBy': 'last_update_by'
    }
    
    for field, value in update_data.items():
        db_field = field_mapping.get(field, field)
        if hasattr(db_candidate, db_field):
            setattr(db_candidate, db_field, value)
    
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def delete_candidate(db: Session, candidate_id: str):
    db_candidate = get_candidate(db, candidate_id)
    if not db_candidate:
        return None
    
    db.delete(db_candidate)
    db.commit()
    return db_candidate