from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.application import ApplicationCreate, Application
from ..services.application_service import (
    create_application,
    get_applications_by_candidate,
    get_applications_by_jd,
    update_application_status,
    withdraw_application
)
from ..auth.keycloak import get_candidate_user, get_hr_user
from typing import List

router = APIRouter(prefix="/rms/applications", tags=["Applications"])

@router.post("/", response_model=Application)
def apply_for_job(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_candidate_user)
):
    return create_application(db=db, application=application, user_id=current_user.get("sub"))

@router.get("/candidate/{candidateId}", response_model=List[Application])
def get_candidate_applications(
    candidateId: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_candidate_user)
):
    # Verify candidate owns these applications
    if current_user.get("sub") != candidateId:
        raise HTTPException(status_code=403, detail="Can only view your own applications")
    return get_applications_by_candidate(db=db, candidate_id=candidateId)

@router.get("/jd/{jdId}", response_model=List[Application])
def get_jd_applications(
    jdId: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_hr_user)  # Only HR can view applications by JD
):
    return get_applications_by_jd(db=db, jd_id=jdId)

@router.put("/{applicationId}/status", response_model=Application)
def update_application(
    applicationId: str,
    status: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_hr_user)  # Only HR can update status
):
    return update_application_status(db=db, application_id=applicationId, status=status)

@router.delete("/{applicationId}", response_model=Application)
def withdraw_application_endpoint(
    applicationId: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_candidate_user)
):
    return withdraw_application(db=db, application_id=applicationId, user_id=current_user.get("sub"))