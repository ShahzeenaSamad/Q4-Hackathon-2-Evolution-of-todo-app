"""
Authentication Schemas - Request/Response Models
"""
from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request schema for POST /api/v1/auth/signup"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str | None = None


class LoginRequest(BaseModel):
    """Request schema for POST /api/v1/auth/login"""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Response schema for auth endpoints"""
    success: bool
    data: dict | None = None
    error: dict | None = None


class UserResponse(BaseModel):
    """User data returned in auth responses"""
    id: str
    email: str
    name: str | None = None
    created_at: str
