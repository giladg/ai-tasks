from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user (during OAuth)"""
    google_id: str
    picture_url: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    name: Optional[str] = None


class User(UserBase):
    """Schema for user response (public data only)"""
    id: int
    google_id: str
    picture_url: Optional[str] = None
    last_sync_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfile(User):
    """Extended user schema with additional profile information"""
    updated_at: datetime

    class Config:
        from_attributes = True
