# Conversation Management Skill

## Description
Reusable skill for managing AI chatbot conversations with persistent storage, history building, and context management.

## When to Use
- Chatbot needs to maintain conversation history
- Agent requires context from previous messages
- Testing conversation flows
- Managing user sessions across requests

## Capabilities

### 1. Create Conversation
```python
from services import ConversationService

def create_conversation(user_id: str, db_session):
    """Create new conversation for user"""
    conv_svc = ConversationService()
    conv_id = conv_svc.create_conversation(user_id, db_session)
    return conv_id
```

### 2. Add Message
```python
def add_message(conv_id: str, role: str, content: str, db_session):
    """Add message to conversation"""
    conv_svc = ConversationService()
    msg_id = conv_svc.add_message(conv_id, role, content, db_session)
    return msg_id
```

### 3. Build Conversation History
```python
from services.history_builder import HistoryBuilder

def get_conversation_history(conv_id: str, db_session):
    """Get formatted conversation history for agent"""
    history_builder = HistoryBuilder()
    messages = history_builder.build_history(conv_id, db_session)
    return messages
```

### 4. Format for Agent
```python
def format_for_agent(messages):
    """Format messages for OpenAI agent"""
    formatted = []
    for msg in messages:
        formatted.append({
            "role": msg.role,
            "content": msg.content
        })
    return formatted
```

## Message Roles

### user
```python
add_message(
    conv_id,
    role="user",
    content="Add buy milk to my tasks",
    db_session
)
```

### assistant
```python
add_message(
    conv_id,
    role="assistant",
    content="I've added 'Buy milk' to your tasks (ID: 123)",
    db_session
)
```

## Complete Conversation Flow

```python
def handle_user_message(user_id: str, message: str, conv_id: str = None):
    """Handle complete conversation turn"""
    db = SessionLocal()

    try:
        # Create or get conversation
        if not conv_id:
            conv_id = create_conversation(user_id, db)

        # Store user message
        add_message(conv_id, "user", message, db)

        # Get conversation history
        history = get_conversation_history(conv_id, db)

        # Run agent
        agent = MockAgentRunner(use_tools=True)
        result = agent.run(message, history, db)

        # Store assistant response
        add_message(conv_id, "assistant", result["response"], db)

        return {
            "response": result["response"],
            "conversation_id": conv_id,
            "tool_calls": result["tool_calls"]
        }

    finally:
        db.close()
```

## History Formats

### For OpenAI Agent
```python
[
    {"role": "user", "content": "Add buy milk"},
    {"role": "assistant", "content": "I've added 'Buy milk'..."},
    {"role": "user", "content": "What are my tasks?"}
]
```

### For Mock Agent
```python
[
    {"role": "user", "content": "Add buy milk"},
    {"role": "assistant", "content": "I've added 'Buy milk'..."}
]
```

## Context Window Management

### Limit History Size
```python
def get_limited_history(conv_id: str, db_session, max_messages=20):
    """Get last N messages to fit in context window"""
    from sqlalchemy import text

    sql = text("""
        SELECT role, content
        FROM messages
        WHERE conversation_id = :conv_id
        ORDER BY created_at DESC
        LIMIT :limit
    """)

    results = db_session.execute(sql, {
        "conv_id": conv_id,
        "limit": max_messages
    }).all()

    # Reverse to get chronological order
    return [{"role": row[0], "content": row[1]} for row in reversed(results)]
```

### Token Counting
```python
import tiktoken

def count_tokens(messages):
    """Count tokens in conversation history"""
    encoding = tiktoken.encoding_for_model("gpt-4o")
    total = 0
    for msg in messages:
        total += len(encoding.encode(msg["content"]))
    return total
```

## Error Handling

### Invalid Conversation ID
```python
try:
    history = get_conversation_history(conv_id, db)
except ValueError as e:
    # Conversation doesn't exist
    return {"error": "Invalid conversation ID"}
```

### Database Errors
```python
try:
    add_message(conv_id, "user", message, db)
except Exception as e:
    db.rollback()
    logger.error(f"Failed to add message: {e}")
    return {"error": "Failed to store message"}
```

## Testing

### Test Conversation Flow
```python
def test_conversation_flow():
    db = SessionLocal()
    conv_svc = ConversationService()
    history_builder = HistoryBuilder()

    # Create conversation
    conv_id = conv_svc.create_conversation("user-123", db)

    # Add messages
    conv_svc.add_message(conv_id, "user", "Hello", db)
    conv_svc.add_message(conv_id, "assistant", "Hi there!", db)

    # Retrieve history
    messages = history_builder.build_history(conv_id, db)

    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"

    db.close()
```

## Best Practices
1. Always store both user and assistant messages
2. Use conversation IDs for session management
3. Limit history size to avoid token limits
4. Handle invalid conversation IDs gracefully
5. Commit messages immediately after adding
6. Close database sessions in finally blocks

## Dependencies
- ConversationService from services/conversation_svc.py
- HistoryBuilder from services/history_builder.py
- Database session from db.py
- Message model from models/message.py
