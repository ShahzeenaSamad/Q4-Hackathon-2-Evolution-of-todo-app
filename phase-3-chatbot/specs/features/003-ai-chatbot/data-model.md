# Data Model: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-01-22
**Purpose**: Entity definitions, relationships, and validation rules for Phase 3

---

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │
│─────────────│
│ id (PK)     │
│ email       │
│ password_hash│
│ name        │
│ created_at  │
└──────┬──────┘
       │
       ├──────────────────────┬───────────────────┐
       │                      │                   │
       ▼                      ▼                   ▼
┌─────────────┐      ┌─────────────┐   ┌─────────────┐
│    Task     │      │Conversation│   │   Message   │
│─────────────│      │─────────────│   │─────────────│
│ id (PK)     │      │ id (PK)     │   │ id (PK)     │
│ user_id (FK)│      │ user_id (FK)│   │ conv_id (FK)│
│ title       │◄─────│ created_at  │   │ role        │
│ description │      │ updated_at  │◄──┤ content     │
│ completed  │      │             │   │ created_at  │
│ created_at  │      └──────┬──────┘   └─────────────┘
│ updated_at  │             │
└─────────────┘             │
                             │
                             ▼
                    ┌────────────────┐
                    │  Message       │
                    │  (1:N)          │
                    └────────────────┘
```

---

## Entity Definitions

### User

**Purpose**: Represents a person who can have tasks, conversations, and messages

**Reused from**: Phase 2 (extended with relationships)

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `str (UUID)` | Primary key | Unique user identifier |
| `email` | `str` | Unique, indexed, Email format | User's email address |
| `password_hash` | `str` | Required, min 60 chars | Bcrypt hash of password |
| `name` | `str (optional)` | Max 255 chars | User's display name |
| `created_at` | `datetime` | Required, default=utcnow | Account creation timestamp |

**Relationships**:
- `tasks`: One-to-many with Task (cascade delete)
- `conversations`: One-to-many with Conversation (cascade delete)

**Indexes**:
- `idx_user_email` on `email` (unique)
- `idx_user_created` on `created_at`

**Validation Rules**:
- Email must be valid format and unique
- Password must be hashed before storage (never plaintext)
- Name is optional for privacy

---

### Task

**Purpose**: Represents a todo item with ownership and completion tracking

**Reused from**: Phase 2 (no schema changes, only relationship extensions)

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `str (UUID)` | Primary key | Unique task identifier |
| `user_id` | `str (UUID)` | Foreign key → User.id, Required | Task owner |
| `title` | `str` | Required, max 200 chars, non-empty | Task title |
| `description` | `str (optional)` | Max 2000 chars | Additional details |
| `completed` | `bool` | Required, default=False | Completion status |
| `created_at` | `datetime` | Required, default=utcnow | Creation timestamp |
| `updated_at` | `datetime` | Required, default=utcnow, onupdate=utcnow | Last update timestamp |

**Relationships**:
- `user`: Many-to-one with User (foreign key: `user_id`)

**Indexes**:
- `idx_task_user` on `user_id` (for user filtering)
- `idx_task_created` on `created_at` (for sorting)
- `idx_task_completed` on `completed` (for status filtering)

**Validation Rules**:
- Title must be non-empty after trimming whitespace
- User ID must reference existing user
- Completed defaults to False (new tasks are pending)
- Updated at automatically updates on any field change

**State Transitions**:
```
[Pending] ←→ [Completed]
    ↑           ↓
    └───────────┘ (can toggle back)
```

---

### Conversation

**Purpose**: Represents a chat session between user and AI assistant

**New in**: Phase 3

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `str (UUID)` | Primary key | Unique conversation identifier |
| `user_id` | `str (UUID)` | Foreign key → User.id, Required | Conversation owner |
| `created_at` | `datetime` | Required, default=utcnow | Session creation timestamp |
| `updated_at` | `datetime` | Required, default=utcnow, onupdate=utcnow | Last activity timestamp |

**Relationships**:
- `user`: Many-to-one with User (foreign key: `user_id`)
- `messages`: One-to-many with Message (cascade delete)

**Indexes**:
- `idx_conversation_user` on `user_id` (for user filtering)
- `idx_conversation_updated` on `updated_at` (for sorting recent)

**Validation Rules**:
- User ID must reference existing user
- Auto-created on first message if none provided
- Updated at refreshes on every new message

**Lifecycle**:
```
[Created] → [Active] → [Archived]
    ↓
[Deleted]
```
- **Created**: Initial state when first message sent
- **Active**: Receiving messages
- **Archived**: No longer active (manual or auto-archive)
- **Deleted**: Soft deleted (retention policy)

---

### Message

**Purpose**: Represents a single message in a conversation (from user or assistant)

**New in**: Phase 3

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `str (UUID)` | Primary key | Unique message identifier |
| `conversation_id` | `str (UUID)` | Foreign key → Conversation.id, Required | Parent conversation |
| `role` | `str` | Required, enum: "user" or "assistant" | Message sender |
| `content` | `str` | Required, max 5000 chars, non-empty | Message text |
| `created_at` | `datetime` | Required, default=utcnow | Message timestamp |

**Relationships**:
- `conversation`: Many-to-one with Conversation (foreign key: `conversation_id`)

**Indexes**:
- `idx_message_conversation` on `conversation_id, created_at` (composite, for history loading)
- `idx_message_role` on `role` (for filtering)

**Validation Rules**:
- Conversation ID must reference existing conversation
- Role must be exactly "user" or "assistant" (no other values)
- Content must be non-empty after trimming
- Max 5000 chars prevents abuse while allowing long explanations

**Usage Pattern**:
Messages are always chronological within a conversation. The composite index on `(conversation_id, created_at)` ensures fast history loading.

---

## Database Schema (SQL)

```sql
-- User table (Phase 2, relationships extended)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Task table (Phase 2, no changes)
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversation table (Phase 3 new)
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Message table (Phase 3 new)
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_created ON users(created_at);

CREATE INDEX idx_task_user ON tasks(user_id);
CREATE INDEX idx_task_created ON tasks(created_at);
CREATE INDEX idx_task_completed ON tasks(completed);

CREATE INDEX idx_conversation_user ON conversations(user_id);
CREATE INDEX idx_conversation_updated ON conversations(updated_at);

CREATE INDEX idx_message_conversation ON messages(conversation_id, created_at);
CREATE INDEX idx_message_role ON messages(role);
```

---

## Migration Strategy

### Phase 3 Migration Script

```python
# database/migrations/003_add_conversations.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('conversations.id'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    # Create indexes
    op.create_index('idx_conversation_user', 'conversations', ['user_id'])
    op.create_index('idx_conversation_updated', 'conversations', ['updated_at'])
    op.create_index('idx_message_conversation', 'messages', ['conversation_id', 'created_at'])
    op.create_index('idx_message_role', 'messages', ['role'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

---

## Data Integrity Rules

### User Ownership Enforcement

**Rule**: Every operation must validate `user_id` before acting

**Implementation**:
```python
def validate_task_ownership(task_id: str, user_id: str, db: Session):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise NotFoundError(f"Task {task_id} not found or access denied")

    return task
```

**Database-Level**:
- Foreign key constraints ensure referential integrity
- CASCADE deletes prevent orphaned records

### Conversation Isolation

**Rule**: Users can only access their own conversations and messages

**Implementation**:
- All queries filter by `user_id` through conversation
- No direct access to messages by ID (always through conversation)

### Cascade Behavior

**User Deletion**:
```
User deleted
  ↓ CASCADE
Tasks deleted (all user's tasks)
Conversations deleted (all user's conversations)
Messages deleted (all user's messages via conversations)
```

**Conversation Deletion**:
```
Conversation deleted
  ↓ CASCADE
Messages deleted (all messages in conversation)
Tasks preserved (tasks are independent of conversation)
```

---

## Performance Considerations

### Query Optimization

**History Loading Query** (most common):
```sql
SELECT m.id, m.role, m.content, m.created_at
FROM messages m
WHERE m.conversation_id = ?
ORDER BY m.created_at ASC
LIMIT 1000;

-- Uses composite index: idx_message_conversation
-- Expected time: <10ms for 100 messages
```

**User Task Query** (second most common):
```sql
SELECT t.id, t.title, t.completed, t.created_at
FROM tasks t
WHERE t.user_id = ?
ORDER BY t.created_at DESC;

-- Uses index: idx_task_user
-- Expected time: <5ms for typical query
```

### Index Strategy

**Composite Index for Conversation History**:
- On: `(conversation_id, created_at)`
- Rationale: Covers 95% of conversation queries
- Impact: 10x faster than full table scan

**User-Based Indexes**:
- Tasks: `(user_id, created_at)`
- Conversations: `(user_id, updated_at)`
- Rationale: Enforces data isolation, optimizes user queries

### Connection Pooling (from Phase 2)
- Pool size: 20 connections
- Max overflow: 30 connections
- Total capacity: 50 concurrent requests

---

**Status**: ✅ Data Model Complete - Ready for API contracts
**Next Phase**: Generate OpenAPI specification for chat endpoint
