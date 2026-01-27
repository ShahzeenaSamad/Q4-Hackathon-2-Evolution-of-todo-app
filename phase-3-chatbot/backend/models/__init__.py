"""
Models Package for Phase 3 AI Chatbot
Exports all database models
"""

# Phase 3 models
from .conversation import Conversation
from .message import Message

# Phase 2 models (local copy in phase-3-chatbot)
from .task import Task

# User model not needed for phase 3
User = None

__all__ = [
    "Conversation",
    "Message",
    "User",
    "Task",
]
