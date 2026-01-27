"""
Conversation Model
New for Phase 3 - Extends Phase 2 User model
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime
from datetime import datetime
import sys
import os

# Add parent backend directory to path to import Phase 2 models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))


class Conversation(SQLModel, table=True):
    """Chat session between user and AI assistant"""

    __tablename__ = "conversations"

    id: str = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default="NOW()")
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default="NOW()")
    )

    # Relationships
    # Note: These will be lazy-loaded to avoid circular imports
    # user: User = Relationship(back_populates="conversations")
    # messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)
