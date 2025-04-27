from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for creating a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_hr: Optional[bool] = False

    class Config:
        orm_mode = True

# Schema for reading a user
class User(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    is_hr: bool

    class Config:
        orm_mode = True

# Schema for updating a user (optional)
class UserUpdate(BaseModel):
    email: Optional[str]
    is_active: Optional[bool]
    is_hr: Optional[bool]

    class Config:
        orm_mode = True
