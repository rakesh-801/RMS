from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating a new application
class ApplicationCreate(BaseModel):
    candidateId: str
    resumeId: str
    jdId: str
    status: str  # Possible values: APPLIED, SHORTLISTED, REJECTED, HIRED
    referredBy: Optional[str] = None
    isActive: Optional[bool] = True

    class Config:
        orm_mode = True


# Schema for reading an application (retrieving data)
class Application(BaseModel):
    applicationId: str
    candidateId: str
    resumeId: str
    jdId: str
    status: str
    referredBy: Optional[str] = None
    isActive: bool
    createdAt: Optional[datetime]  # from TimeStampedModel (inherits createdAt)
    updatedAt: Optional[datetime]  # from TimeStampedModel (inherits updatedAt)

    class Config:
        orm_mode = True
