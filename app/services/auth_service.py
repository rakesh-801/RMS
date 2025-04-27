from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.core.email import send_welcome_email, send_password_reset_email
import uuid

def register_candidate(db: Session, candidate_data: CandidateCreate):
    # Check if email already exists
    if db.query(User).filter(User.email == candidate_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    db_user = User(
        id=str(uuid.uuid4()),
        email=candidate_data.email,
        hashed_password=get_password_hash(candidate_data.password),
        is_hr=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create candidate profile
    db_candidate = Candidate(
        userId=db_user.id,
        firstName=candidate_data.firstName,
        lastName=candidate_data.lastName,
        email=candidate_data.email,
        phone=candidate_data.phone,
        status="ACTIVE"
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    # Send welcome email
    send_welcome_email(candidate_data.email, candidate_data.firstName)
    
    return db_candidate

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def initiate_password_reset(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    # Generate temporary password
    temp_password = str(uuid.uuid4())[:8]
    user.hashed_password = get_password_hash(temp_password)
    db.commit()
    
    # Send email with temp password
    send_password_reset_email(email, temp_password)
    
    return {"message": "Password reset email sent"}