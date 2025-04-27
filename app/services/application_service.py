# app/services/application_service.py

from sqlalchemy.orm import Session
from ..models.application import Application
from ..schemas.application import ApplicationCreate
from datetime import datetime
from uuid import uuid4

def create_application(db: Session, application: ApplicationCreate, user_id: str):
    db_application = Application(
        applicationId=str(uuid4()),
        candidateId=user_id,
        resumeId=application.resumeId,
        jdId=application.jdId,
        status="APPLIED",
        referredBy=application.referredBy,
        createdAt=datetime.utcnow(),
        isActive=True
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_applications_by_candidate(db: Session, candidate_id: str):
    return db.query(Application).filter(
        Application.candidateId == candidate_id,
        Application.isActive == True
    ).all()

def get_applications_by_jd(db: Session, jd_id: str):
    return db.query(Application).filter(
        Application.jdId == jd_id,
        Application.isActive == True
    ).all()

def update_application_status(db: Session, application_id: str, status: str):
    db_application = db.query(Application).filter(Application.applicationId == application_id).first()
    if not db_application:
        return None
    
    db_application.status = status
    db_application.updatedAt = datetime.utcnow()
    db.commit()
    db.refresh(db_application)
    return db_application

def withdraw_application(db: Session, application_id: str, user_id: str):
    db_application = db.query(Application).filter(
        Application.applicationId == application_id,
        Application.candidateId == user_id
    ).first()
    
    if not db_application:
        return None
    
    db_application.isActive = False
    db_application.updatedAt = datetime.utcnow()
    db.commit()
    db.refresh(db_application)
    return db_application