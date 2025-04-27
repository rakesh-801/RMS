from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.resume import ResumeCreate, ResumeUpdate, Resume
from ..services.resume_service import (
    create_resume, 
    get_resume, 
    get_all_resumes, 
    update_resume, 
    delete_resume,
    get_resumes_by_candidate
)
from ..services.document_processing import DocumentProcessor
from typing import List
import uuid

router = APIRouter(prefix="/rms/resumes", tags=["Resumes"])

@router.post("/", response_model=Resume)
def create_resume_endpoint(
    resume: ResumeCreate, 
    db: Session = Depends(get_db),
    current_user: str = "system"  # Replace with actual auth
):
    return create_resume(db=db, resume=resume, user_id=current_user)

@router.get("/", response_model=List[Resume])
def read_resumes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return get_all_resumes(db=db, skip=skip, limit=limit)

@router.get("/{resumeId}", response_model=Resume)
def read_resume(
    resumeId: str, 
    db: Session = Depends(get_db)
):
    db_resume = get_resume(db=db, resume_id=resumeId)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume

@router.put("/{resumeId}", response_model=Resume)
def update_resume_endpoint(
    resumeId: str, 
    resume: ResumeUpdate, 
    db: Session = Depends(get_db),
    current_user: str = "system"  # Replace with actual auth
):
    # Set the lastUpdateBy field
    resume.lastUpdateBy = current_user
    
    db_resume = update_resume(
        db=db, 
        resume_id=resumeId, 
        resume=resume,
        user_id=current_user
    )
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume

@router.delete("/{resumeId}")
def delete_resume_endpoint(
    resumeId: str, 
    db: Session = Depends(get_db)
):
    db_resume = delete_resume(db=db, resume_id=resumeId)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume deleted successfully"}

@router.post("/upload/")
async def upload_resume_file(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: str = "system"  # Replace with actual auth
):
    processor = DocumentProcessor()
    file_contents = await file.read()
    resume_text = processor.extract_text_from_pdf(file_contents)
    resume_data = processor.parse_resume(resume_text)
    print(f"Parsed Data: {resume_data}")  
    
    if not resume_data:
        raise HTTPException(status_code=400, detail="Failed to parse resume document")
    
    return resume_data

