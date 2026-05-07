from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    is_verified: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class VerifyEmail(BaseModel):
    token: str
