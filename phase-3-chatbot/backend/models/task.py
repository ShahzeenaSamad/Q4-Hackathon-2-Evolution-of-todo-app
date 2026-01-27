"""
Task Model - SQLModel for Todo Tasks
"""
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Task(SQLModel, table=True):
    """
    Task model for todo items.
    Each task belongs to a specific user.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

    # New fields
    priority: str = Field(default="medium", index=True)  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    category: Optional[str] = Field(default=None, index=True)  # work, personal, shopping, etc.

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


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
