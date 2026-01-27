"""
Conversation Service
Manages conversation persistence and retrieval
"""

import uuid
from datetime import datetime
from sqlmodel import Session, select
from typing import Optional
from models import Conversation, Message


class ConversationService:
    """Service for conversation CRUD operations with database persistence"""

    def create_conversation(self, user_id: str, session: Session) -> str:
        """
        Create a new conversation for a user.

        Args:
            user_id: User ID who owns this conversation
            session: Database session

        Returns:
            New conversation ID
        """
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return conversation_id

    def get_conversation(
        self,
        conversation_id: str,
        user_id: str,
        session: Session
    ) -> Optional[Conversation]:
        """
        Get conversation by ID with user ownership validation.

        Args:
            conversation_id: Conversation ID to retrieve
            user_id: User ID for ownership validation
            session: Database session

        Returns:
            Conversation object or None if not found/invalid ownership
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )

        return session.execute(statement).first()

    def update_conversation_timestamp(
        self,
        conversation_id: str,
        session: Session
    ) -> None:
        """
        Update conversation's updated_at timestamp.

        Args:
            conversation_id: Conversation ID to update
            session: Database session
        """
        from sqlalchemy import text

        # Use raw SQL to update timestamp
        sql = text("UPDATE conversations SET updated_at = NOW() WHERE id = :conv_id")
        session.execute(sql, {"conv_id": conversation_id})
        session.commit()

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        session: Session
    ) -> str:
        """
        Add a message to a conversation.

        Args:
            conversation_id: Conversation ID
            role: Message role ("user" or "assistant")
            content: Message content
            session: Database session

        Returns:
            New message ID
        """
        try:
            message_id = str(uuid.uuid4())
            message = Message(
                id=message_id,
                conversation_id=conversation_id,
                role=role,
                content=content,
                created_at=datetime.utcnow()
            )

            session.add(message)

            # Update conversation timestamp
            self.update_conversation_timestamp(conversation_id, session)

            session.commit()
            session.refresh(message)

            return message_id

        except Exception as e:
            session.rollback()
            # Try again without timestamp update
            message_id = str(uuid.uuid4())
            message = Message(
                id=message_id,
                conversation_id=conversation_id,
                role=role,
                content=content,
                created_at=datetime.utcnow()
            )

            session.add(message)
            session.commit()
            session.refresh(message)

            return message_id

    def get_messages(
        self,
        conversation_id: str,
        session: Session,
        limit: Optional[int] = None
    ) -> list[Message]:
        """
        Get all messages for a conversation in chronological order.

        Args:
            conversation_id: Conversation ID
            session: Database session
            limit: Optional limit on number of messages

        Returns:
            List of Message objects ordered by created_at ASC
        """
        from sqlalchemy import text

        # Use raw SQL to avoid ORM issues
        sql = text("""
            SELECT id, conversation_id, role, content, created_at
            FROM messages
            WHERE conversation_id = :conv_id
            ORDER BY created_at ASC
        """)

        if limit:
            sql = text("""
                SELECT id, conversation_id, role, content, created_at
                FROM messages
                WHERE conversation_id = :conv_id
                ORDER BY created_at ASC
                LIMIT :limit
            """)

        params = {"conv_id": conversation_id}
        if limit:
            params["limit"] = limit

        results = session.execute(sql, params).all()

        # Convert Row objects to Message model objects
        messages = []
        for row in results:
            msg = Message(
                id=row[0],
                conversation_id=row[1],
                role=row[2],
                content=row[3],
                created_at=row[4]
            )
            messages.append(msg)

        return messages
