from sqlalchemy.orm import Session
from ..models.resume import Resume
from ..models.candidate import Candidate
from ..schemas.resume import ResumeCreate, ResumeUpdate
from ..schemas.candidate import CandidateCreate
from ..services.candidate_service import create_candidate
from ..services.document_processing import DocumentProcessor
import uuid
from datetime import datetime

def create_resume(db: Session, resume: ResumeCreate, user_id: str):
    # Check if candidate exists
    db_candidate = db.query(Candidate).filter(Candidate.candidateId == resume.candidateId).first()
    
    if not db_candidate:
        # Parse candidate details from resume (simplified example)
        name_parts = resume.currentRoleDescription.split()
        first_name = name_parts[0] if name_parts else "Unknown"
        last_name = name_parts[-1] if len(name_parts) > 1 else "Unknown"
        
        # Create candidate from resume data
        candidate_data = CandidateCreate(
            firstName=first_name,
            lastName=last_name,
            currentRole=resume.role,
            currentEmployer=resume.currentEmployer,
            currentCTC="",  # Will be updated from resume parsing
            expectedCTC="",
            contactDate=None,
            tags={},
            status="NEW",
            latestJDReference=resume.latestJDReference,
            createdBy=user_id,
            lastUpdateBy=user_id
        )
        db_candidate = create_candidate(db, candidate_data, user_id)
    
    # Create the resume
    db_resume = Resume(
        resumeId=str(uuid.uuid4()),
        candidateId=db_candidate.candidateId,
        role=resume.role,
        currentEmployer=resume.currentEmployer,
        jdReference=resume.jdReference,
        referringEmployee=resume.referringEmployee,
        experienceSummary=resume.experienceSummary,
        currentRoleDescription=resume.currentRoleDescription,
        experienceHistory=resume.experienceHistory,
        skills=resume.skills,
        certifications=resume.certifications,
        publications=resume.publications,
        industryContributions=resume.industryContributions,
        originalResume=resume.originalResume,
        employmentHistory=resume.employmentHistory,
        Photo=resume.Photo,
        latestJDReference=resume.latestJDReference,
        created_by=user_id,
        last_update_by=user_id
    )
    
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume
def get_resume(db: Session, resume_id: str):
    return db.query(Resume).filter(Resume.resumeId == resume_id).first()

def get_all_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resume).offset(skip).limit(limit).all()

def update_resume(db: Session, resume_id: str, resume: ResumeUpdate, user_id: str):
    db_resume = get_resume(db, resume_id)
    if not db_resume:
        return None
    
    update_data = resume.model_dump(exclude_unset=True)
    
    # Map field names to SQLAlchemy columns
    field_mapping = {
        'lastUpdateBy': 'last_update_by'
    }
    
    for field, value in update_data.items():
        db_field = field_mapping.get(field, field)
        if hasattr(db_resume, db_field):
            setattr(db_resume, db_field, value)
    
    db.commit()
    db.refresh(db_resume)
    return db_resume

def delete_resume(db: Session, resume_id: str):
    db_resume = get_resume(db, resume_id)
    if not db_resume:
        return None
    
    db.delete(db_resume)
    db.commit()
    return db_resume

def get_resumes_by_candidate(db: Session, candidate_id: str):
    return db.query(Resume).filter(Resume.candidateId == candidate_id).all()