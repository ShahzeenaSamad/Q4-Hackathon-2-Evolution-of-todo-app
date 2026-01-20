"""
User Model - Better Auth Compatible SQLModel
"""
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    """
    User model compatible with Better Auth schema.
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str = Field()
    name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)


class UserCreate:
    """Schema for creating a new user"""
    email: str
    password: str
    name: Optional[str] = None


class UserLogin:
    """Schema for user login"""
    email: str
    password: str
