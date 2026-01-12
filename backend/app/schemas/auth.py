from pydantic import BaseModel
from typing import Optional
from app.schemas.user import User


class TokenResponse(BaseModel):
    """Response schema for authentication tokens"""
    access_token: str
    token_type: str = "bearer"
    user: User


class GoogleAuthURL(BaseModel):
    """Response schema for Google OAuth authorization URL"""
    authorization_url: str


class GoogleCallback(BaseModel):
    """Schema for Google OAuth callback parameters"""
    code: str
    state: Optional[str] = None


class LogoutResponse(BaseModel):
    """Response schema for logout"""
    message: str
