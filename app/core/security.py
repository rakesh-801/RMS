# app/core/security.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
import secrets
import bcrypt

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its bcrypt hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_random_password(length: int = 16) -> str:
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        # Ensure password meets complexity requirements
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%^&*" for c in password)):
            return password

def get_password_strength(password: str) -> dict:
    """Analyze password strength"""
    strength = {
        'length': len(password) >= 8,
        'lowercase': any(c.islower() for c in password),
        'uppercase': any(c.isupper() for c in password),
        'digit': any(c.isdigit() for c in password),
        'special': any(c in "!@#$%^&*" for c in password),
    }
    strength['score'] = sum(strength.values())
    return strength