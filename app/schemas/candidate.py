from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CandidateBase(BaseModel):
    firstName: str
    lastName: str
    currentRole: str
    currentEmployer: str
    currentCTC: str
    expectedCTC: str
    contactDate: Optional[datetime] = None
    tags: Optional[dict] = None
    status: str
    latestJDReference: Optional[str] = None

class CandidateCreate(CandidateBase):
    createdBy: str  # Will map to created_by in SQLAlchemy
    lastUpdateBy: str  # Will map to last_update_by in SQLAlchemy

class CandidateUpdate(CandidateBase):
    lastUpdateBy: Optional[str] = None  # For updates, we might only change this

class Candidate(CandidateBase):
    candidateId: str
    createdTime: datetime  # Maps to created_time in SQLAlchemy
    lastUpdateTime: datetime  # Maps to last_update_time in SQLAlchemy
    createdBy: str  # Maps to created_by in SQLAlchemy
    lastUpdateBy: str  # Maps to last_update_by in SQLAlchemy

    class Config:
        from_attributes = True
        populate_by_name = True  # Allows alias mapping
        alias_generator = lambda x: {
            'createdTime': 'created_time',
            'lastUpdateTime': 'last_update_time',
            'createdBy': 'created_by',
            'lastUpdateBy': 'last_update_by'
        }.get(x, x)