from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResumeBase(BaseModel):
    candidateId: str
    role: str
    currentEmployer: str
    jdReference: Optional[str] = None
    referringEmployee: Optional[str] = None
    experienceSummary: str
    currentRoleDescription: str
    experienceHistory: str
    skills: str
    certifications: str
    publications: Optional[str] = None
    industryContributions: Optional[str] = None
    originalResume: str
    employmentHistory: dict
    Photo: Optional[bytes] = None
    latestJDReference: Optional[str] = None

class ResumeCreate(ResumeBase):
    createdBy: str  # Will map to created_by in SQLAlchemy
    lastUpdateBy: str  # Will map to last_update_by in SQLAlchemy

class ResumeUpdate(ResumeBase):
    lastUpdateBy: Optional[str] = None  # For updates

class Resume(ResumeBase):
    resumeId: str
    createdTime: datetime  # Maps to created_time
    lastUpdateTime: datetime  # Maps to last_update_time
    createdBy: str  # Maps to created_by
    lastUpdateBy: str  # Maps to last_update_by

    class Config:
        from_attributes = True
        populate_by_name = True
        alias_generator = lambda x: {
            'createdTime': 'created_time',
            'lastUpdateTime': 'last_update_time',
            'createdBy': 'created_by',
            'lastUpdateBy': 'last_update_by'
        }.get(x, x)