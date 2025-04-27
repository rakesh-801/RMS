from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic_settings import BaseSettings  # ✅ correct
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

from pydantic import Field
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:root@localhost/hiring2"
    KEYCLOAK_SERVER_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "hiring_realm"
    KEYCLOAK_CLIENT_ID: str = "hiring_client"
    KEYCLOAK_CLIENT_SECRET: str = "your-client-secret"
    MISTRAL_API_KEY: str
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str = "noreply@hiringplatform.com"
    
    class Config:
        env_file = ".env"

settings = Settings()