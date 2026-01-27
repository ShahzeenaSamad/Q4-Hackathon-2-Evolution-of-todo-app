"""Add conversations and messages tables

Revision ID: 9625e18cb288
Revises: 
Create Date: 2026-01-22 02:11:13.361571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9625e18cb288'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table (using TEXT for IDs to match Phase 2 users table)
    op.create_table(
        'conversations',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='conversations_user_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='conversations_pkey')
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('conversation_id', sa.Text(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name='messages_conversation_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )

    # Create indexes for conversations
    op.create_index('idx_conversation_user', 'conversations', ['user_id'])
    op.create_index('idx_conversation_updated', 'conversations', ['updated_at'])

    # Create indexes for messages
    op.create_index('idx_message_conversation', 'messages', ['conversation_id', 'created_at'])
    op.create_index('idx_message_role', 'messages', ['role'])


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_message_role', 'messages')
    op.drop_index('idx_message_conversation', 'messages')
    op.drop_index('idx_conversation_updated', 'conversations')
    op.drop_index('idx_conversation_user', 'conversations')

    # Drop tables
    op.drop_table('messages')
    op.drop_table('conversations')
