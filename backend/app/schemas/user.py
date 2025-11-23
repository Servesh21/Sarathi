from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    phone_number: str
    name: str
    email: Optional[EmailStr] = None
    vehicle_type: Optional[str] = None
    city: Optional[str] = None
    preferred_language: str = "en"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    phone_number: str
    password: str


class UserResponse(UserBase):
    id: int
    whatsapp_number: Optional[str] = None
    whatsapp_verified: bool = False
    is_active: bool = True
    is_verified: bool = False
    monthly_income_target: float = 0.0
    monthly_expense_average: float = 0.0
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    vehicle_type: Optional[str] = None
    city: Optional[str] = None
    preferred_language: Optional[str] = None
    monthly_income_target: Optional[float] = None
    monthly_expense_average: Optional[float] = None


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
