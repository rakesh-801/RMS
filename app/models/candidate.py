from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from .base import TimeStampedModel
import uuid

class Candidate(Base, TimeStampedModel):
    __tablename__ = "candidates"
    
    candidateId = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = Column(String, ForeignKey('users.id'))
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    currentRole = Column(String)
    currentEmployer = Column(String)
    currentCTC = Column(String)
    expectedCTC = Column(String)
    contactDate = Column(DateTime)
    tags = Column(JSON)
    status = Column(String)
    latestJDReference = Column(String)
    
    resumes = relationship("Resume", back_populates="candidate")
    applications = relationship("Application", back_populates="candidate")
    
    user = relationship("User")