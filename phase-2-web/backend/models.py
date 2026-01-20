"""
Database Models - SQLModel definitions
"""

from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


# User Model (managed by Better Auth, but defined here for reference)
class User(SQLModel, table=True):
    """User table for authentication"""
    __tablename__ = "users"

    id: str = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    emailVerifiedAt: Optional[datetime] = None
    image: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


# Task Models
class TaskBase(SQLModel):
    """Base Task model with common fields"""
    title: str = Field(max_length=200)
    description: Optional[str] = None


class Task(TaskBase, table=True):
    """Task table"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """Model for creating a new task"""
    pass


class TaskUpdate(TaskBase):
    """Model for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None


class TaskRead(TaskBase):
    """Model for reading a task"""
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime


# User Models for Auth
class UserBase(SQLModel):
    """Base User model"""
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    """Model for creating a new user"""
    password: str


class UserRead(UserBase):
    """Model for reading a user"""
    id: str
    emailVerifiedAt: Optional[datetime] = None
    image: Optional[str] = None
    createdAt: datetime
