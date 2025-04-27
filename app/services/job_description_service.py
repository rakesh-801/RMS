from sqlalchemy.orm import Session
from ..models.job_description import JobDescription
from ..schemas.job_description import JobDescriptionCreate, JobDescriptionUpdate
from datetime import datetime
from uuid import uuid4
import uuid

def create_jd(db: Session, jd: JobDescriptionCreate):
    db_jd = JobDescription(
        jdId=str(uuid.uuid4()),
        jdName=jd.jdName,
        role=jd.role,
        responsibilities=jd.responsibilities,
        primarySkills=jd.primarySkills,
        secondarySkills=jd.secondarySkills,
        academicQualifications=jd.academicQualifications,
        requiredCertifications=jd.requiredCertifications,
        status=jd.status,
        tags=jd.tags or {},
        created_by=jd.createdBy,
        last_update_by=jd.lastUpdateBy
    )
    db.add(db_jd)
    db.commit()
    db.refresh(db_jd)
    return db_jd

def get_jd(db: Session, jd_id: str):
    return db.query(JobDescription).filter(JobDescription.jdId == jd_id).first()

def get_all_jds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(JobDescription).offset(skip).limit(limit).all()

def update_jd(db: Session, jd_id: str, update_data: dict):
    # Get the existing record - use SQLAlchemy model here
    db_jd = db.query(JobDescription).filter(JobDescription.jdId == jd_id).first()
    if not db_jd:
        return None
    
    # Map camelCase to snake_case for SQLAlchemy columns
    column_mapping = {
        'lastUpdateTime': 'last_update_time',
        'lastUpdateBy': 'last_update_by'
    }
    
    # Update only the fields that were provided
    for key, value in update_data.items():
        db_key = column_mapping.get(key, key)
        if hasattr(db_jd, db_key):
            setattr(db_jd, db_key, value)
    
    db.commit()
    db.refresh(db_jd)
    return db_jd

def delete_jd(db: Session, jd_id: str):
    db_jd = db.query(JobDescription).filter(JobDescription.jdId == jd_id).first()
    if db_jd:
        db.delete(db_jd)
        db.commit()
    return db_jd