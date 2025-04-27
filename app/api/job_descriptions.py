from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..schemas.job_description import JobDescriptionCreate, JobDescriptionUpdate, JobDescription
from ..services.job_description_service import create_jd, get_jd, get_all_jds, update_jd, delete_jd
from ..services.document_processing import DocumentProcessor
from typing import List
import uuid

router = APIRouter(prefix="/rms/jds", tags=["Job Descriptions"])

@router.post("/", response_model=JobDescription)
def create_job_description(
    jd: JobDescriptionCreate,  # This now includes createdBy/lastUpdateBy
    db: Session = Depends(get_db)
):
    """Create a new job description"""
    return create_jd(db=db, jd=jd)

@router.get("/", response_model=List[JobDescription])
def read_job_descriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_jds(db=db, skip=skip, limit=limit)

@router.get("/{jdId}", response_model=JobDescription)
def read_job_description(jdId: str, db: Session = Depends(get_db)):
    db_jd = get_jd(db=db, jd_id=jdId)
    if db_jd is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    return db_jd

@router.put("/{jdId}", response_model=JobDescription)
def update_job_description(
    jdId: str, 
    jd: JobDescriptionUpdate, 
    db: Session = Depends(get_db)
):
    # Convert Pydantic model to dict, excluding unset fields
    update_data = jd.model_dump(exclude_unset=True)
    
    # Add system fields
    update_data.update({
        "lastUpdateBy": jd.lastUpdateBy,
        "lastUpdateTime": datetime.utcnow()
    })
    
    # Perform the update
    db_jd = update_jd(db=db, jd_id=jdId, update_data=update_data)
    if db_jd is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Convert SQLAlchemy model to Pydantic model
    return JobDescription.model_validate(db_jd)

@router.delete("/{jdId}")
def delete_job_description(jdId: str, db: Session = Depends(get_db)):
    db_jd = delete_jd(db=db, jd_id=jdId)
    if db_jd is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {"message": "Job description deleted successfully"}


@router.post("/preview/", response_model=JobDescriptionCreate)
async def preview_jd_file(
    file: UploadFile = File(...),
    processor: DocumentProcessor = Depends(DocumentProcessor)
):
    file_contents = await file.read()
    jd_text = processor.extract_text_from_pdf(file_contents)
    jd_data = processor.parse_job_description(jd_text)
    
    if not jd_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to parse JD document"
        )
    
    # Return the parsed data for preview
    return JobDescriptionCreate(
        jdName=jd_data.get("jdName", "Unnamed JD"),
        role=jd_data.get("role", ""),
        responsibilities=jd_data.get("responsibilities", ""),
        primarySkills=jd_data.get("primarySkills", ""),
        secondarySkills=jd_data.get("secondarySkills", ""),
        academicQualifications=jd_data.get("academicQualifications", ""),
        requiredCertifications=jd_data.get("requiredCertifications", ""),
        status=jd_data.get("status", "DRAFT"),  # Default to DRAFT for preview
        tags={},
        createdBy="preview",  # Will be replaced on actual submit
        lastUpdateBy="preview"
    )

# Modified create endpoint (now expects explicit submission)
@router.post("/", response_model=JobDescription)
async def create_job_description(
    jd: JobDescriptionCreate,  # Now comes from form submission
    db: Session = Depends(get_db)
):
    # Actual database creation
    return create_job_description(jd=jd, db=db)