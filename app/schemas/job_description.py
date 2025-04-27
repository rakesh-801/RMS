from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class JobDescriptionBase(BaseModel):
    jdName: str
    role: str
    responsibilities: str
    primarySkills: str
    secondarySkills: str
    academicQualifications: str
    requiredCertifications: str
    status: str
    tags: Optional[dict] = None

class JobDescriptionCreate(JobDescriptionBase):
    createdBy: str
    lastUpdateBy: str

class JobDescriptionUpdate(JobDescriptionBase):
    jdName: Optional[str] = None
    role: Optional[str] = None
    responsibilities: Optional[str] = None
    primarySkills: Optional[str] = None
    secondarySkills: Optional[str] = None
    academicQualifications: Optional[str] = None
    requiredCertifications: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[dict] = None
    lastUpdateBy: str

class JobDescription(JobDescriptionBase):
    jdId: str
    createdTime: datetime
    lastUpdateTime: datetime
    createdBy: str
    lastUpdateBy: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # This allows aliasing
        alias_generator=lambda x: {
            'createdTime': 'created_time',
            'lastUpdateTime': 'last_update_time',
            'createdBy': 'created_by',
            'lastUpdateBy': 'last_update_by'
        }.get(x, x)
    )