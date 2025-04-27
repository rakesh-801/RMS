from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.auth.keycloak import oauth2_scheme
from app.api import  candidates, job_descriptions, resumes, applications
from app.models import JobDescription, Candidate, Resume, Application
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(candidates.router)
app.include_router(job_descriptions.router)
app.include_router(resumes.router)
app.include_router(applications.router)

@app.get("/")
def read_root():
    return {"message": "Hiring Automation System"}