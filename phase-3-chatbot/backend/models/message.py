"""
Message Model
New for Phase 3
"""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, String, CheckConstraint
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """Single message in a conversation (from user or assistant)"""

    __tablename__ = "messages"

    id: str = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    role: str = Field(
        sa_column=Column("role", String(20), nullable=False)
    )  # "user" or "assistant"
    content: str = Field(max_length=5000)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default="NOW()")
    )

    # Relationships
    # conversation: Conversation = Relationship(back_populates="messages")

    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant')", name="check_message_role"),
    )
