from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.candidate import CandidateCreate, CandidateUpdate, Candidate
from ..services.candidate_service import (
    create_candidate, 
    get_candidate, 
    get_all_candidates, 
    update_candidate, 
    delete_candidate
)
from ..auth.keycloak import get_candidate_user, get_hr_user
from typing import List

router = APIRouter(prefix="/rms/candidates", tags=["Candidates"])

@router.post("/", response_model=Candidate)
def create_candidate_endpoint(
    candidate: CandidateCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_candidate_user)
):
    return create_candidate(db=db, candidate=candidate, user_id=current_user.get("sub"))

@router.get("/", response_model=List[Candidate])
def read_candidates(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_hr_user)  # Only HR can list all candidates
):
    return get_all_candidates(db=db, skip=skip, limit=limit)

@router.get("/{candidateId}", response_model=Candidate)
def read_candidate(
    candidateId: str, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_candidate_user)
):
    # Candidates can only view their own profile
    if "candidate" in current_user.get("realm_access", {}).get("roles", []):
        db_candidate = get_candidate(db=db, candidate_id=candidateId)
        if db_candidate.userId != current_user.get("sub"):
            raise HTTPException(status_code=403, detail="Can only view your own profile")
    
    db_candidate = get_candidate(db=db, candidate_id=candidateId)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.put("/{candidateId}", response_model=Candidate)
def update_candidate_endpoint(
    candidateId: str,
    candidate: CandidateUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_candidate_user)
):
    # Candidates can only update their own profile
    db_candidate = get_candidate(db=db, candidate_id=candidateId)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    if "candidate" in current_user.get("realm_access", {}).get("roles", []):
        if db_candidate.userId != current_user.get("sub"):
            raise HTTPException(status_code=403, detail="Can only update your own profile")
    
    # Set lastUpdateBy from the current user
    candidate.lastUpdateBy = current_user.get("sub")
    
    updated_candidate = update_candidate(
        db=db,
        candidate_id=candidateId,
        candidate=candidate,
        user_id=current_user.get("sub")
    )
    
    return updated_candidate

@router.delete("/{candidateId}")
def delete_candidate_endpoint(
    candidateId: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_candidate_user)
):
    # Candidates can only delete their own profile
    db_candidate = get_candidate(db=db, candidate_id=candidateId)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    if "candidate" in current_user.get("realm_access", {}).get("roles", []):
        if db_candidate.userId != current_user.get("sub"):
            raise HTTPException(status_code=403, detail="Can only delete your own profile")
    
    delete_candidate(db=db, candidate_id=candidateId)
    return {"message": "Candidate deleted successfully"}
