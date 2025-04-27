from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from .base import TimeStampedModel
import uuid

class Application(Base, TimeStampedModel):
    __tablename__ = "applications"
    
    applicationId = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    candidateId = Column(String, ForeignKey('candidates.candidateId'))
    resumeId = Column(String, ForeignKey('resumes.resumeId'))
    jdId = Column(String, ForeignKey('job_descriptions.jdId'))
    status = Column(String)  # APPLIED, SHORTLISTED, REJECTED, HIRED
    referredBy = Column(String)
    isActive = Column(Boolean, default=True)
    
    candidate = relationship("Candidate", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    job_description = relationship("JobDescription")