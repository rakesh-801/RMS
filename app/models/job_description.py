from sqlalchemy import Column, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.database.session import Base
from .base import TimeStampedModel
import uuid

class JobDescription(Base, TimeStampedModel):
    __tablename__ = "job_descriptions"
    
    jdId = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    jdName = Column(String)
    role = Column(String)
    responsibilities = Column(Text)
    primarySkills = Column(Text)
    secondarySkills = Column(Text)
    academicQualifications = Column(Text)
    requiredCertifications = Column(Text)
    status = Column(String)
    tags = Column(JSON)