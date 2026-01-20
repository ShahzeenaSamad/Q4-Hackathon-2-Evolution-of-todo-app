"""
Task Model - SQLModel for Todo Tasks
"""
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from models.user import User


class Task(SQLModel, table=True):
    """
    Task model for todo items.
    Each task belongs to a specific user.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

    # New fields
    priority: str = Field(default="medium", index=True)  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    category: Optional[str] = Field(default=None, index=True)  # work, personal, shopping, etc.

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship to user
    user: User = Relationship()


class TaskCreate:
    """Schema for creating a new task"""
    title: str
    description: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    due_date: Optional[datetime] = None
    category: Optional[str] = None


class TaskUpdate:
    """Schema for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    category: Optional[str] = None
