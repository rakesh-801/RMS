from sqlalchemy import Column, String, Text, JSON, LargeBinary, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from .base import TimeStampedModel
import uuid

class Resume(Base, TimeStampedModel):
    __tablename__ = "resumes"
    
    resumeId = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    candidateId = Column(String, ForeignKey('candidates.candidateId'))
    isPrimary = Column(Boolean, default=False)
    role = Column(String)
    currentEmployer = Column(String)
    jdReference = Column(String)
    referringEmployee = Column(String)
    experienceSummary = Column(Text)
    currentRoleDescription = Column(Text)
    experienceHistory = Column(Text)
    skills = Column(Text)
    certifications = Column(Text)
    publications = Column(Text)
    industryContributions = Column(Text)
    originalResume = Column(Text)
    employmentHistory = Column(JSON)
    Photo = Column(LargeBinary)
    latestJDReference = Column(String)
    
    candidate = relationship("Candidate", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")