"""
History Builder Service
Reconstructs conversation history for agent context
"""

from sqlmodel import Session
from typing import List, Dict, Any
from models import Message
from .conversation_svc import ConversationService


class HistoryBuilder:
    """Service for building conversation history from database"""

    def __init__(self):
        self.conversation_svc = ConversationService()

    def build_history(
        self,
        conversation_id: str,
        session: Session
    ) -> List[Dict[str, str]]:
        """
        Load conversation history from database for agent context.

        Args:
            conversation_id: Conversation ID
            session: Database session

        Returns:
            List of message dicts in format: {role: "user"|"assistant", content: "..."}
        """
        messages = self.conversation_svc.get_messages(conversation_id, session)
        return self.format_for_agent(messages)

    def format_for_agent(
        self,
        messages: List[Message]
    ) -> List[Dict[str, str]]:
        """
        Format database messages into agent-compatible format.

        Args:
            messages: List of Message model objects

        Returns:
            List of message dicts with "role" and "content" keys
        """
        formatted = []

        for message in messages:
            formatted.append({
                "role": message.role,
                "content": message.content
            })

        return formatted

    def build_with_limit(
        self,
        conversation_id: str,
        session: Session,
        max_messages: int = 50
    ) -> List[Dict[str, str]]:
        """
        Load conversation history with a limit (for summarization).

        If conversation has more than max_messages, load only the most recent.
        This prevents token limits for long conversations.

        Args:
            conversation_id: Conversation ID
            session: Database session
            max_messages: Maximum number of messages to load

        Returns:
            List of message dicts
        """
        # Get most recent N messages
        messages = self.conversation_svc.get_messages(
            conversation_id,
            session,
            limit=max_messages
        )

        return self.format_for_agent(messages)
