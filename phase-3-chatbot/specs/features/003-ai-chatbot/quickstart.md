# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Phase**: 3
**Date**: 2026-01-22

---

## Overview

This guide will help you quickly set up and run the AI-Powered Todo Chatbot locally. The chatbot allows users to manage todo tasks through natural language conversation using OpenAI's GPT-4o and MCP tools.

---

## Prerequisites

### Required Software

- **Python 3.13+**: [Download here](https://www.python.org/downloads/)
- **Node.js 20+**: [Download here](https://nodejs.org/)
- **Git**: For cloning the repository
- **PostgreSQL Client**: To verify database (optional)

### Required Accounts

- **OpenAI API Key**: [Get API key here](https://platform.openai.com/api-keys)
  - You'll need GPT-4o model access
  - Add credits (estimate: $5-10 for development/testing)

### Environment Variables

You'll need these from Phase 2:
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret for token signing
- `OPENAI_API_KEY`: Your OpenAI API key (new for Phase 3)

---

## Setup Instructions

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Hackathone2/phase-3-chatbot
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Create `backend/requirements.txt`:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.14
openai>=1.0.0
python-multipart==0.0.6
alembic==1.13.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

### Step 3: Environment Configuration

Create `backend/.env`:
```bash
# Database (from Phase 2)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key-here

# JWT Secret (from Phase 2)
JWT_SECRET=your-jwt-secret-here

# App Settings
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Step 4: Database Migration

```bash
# Run migrations to create Phase 3 tables
cd backend
alembic upgrade head

# Expected output:
# INFO  [alembic.runtime] Migration 003_add_conversations.py -> OK
# INFO  [alembic.runtime] Running upgrade...
```

### Step 5: Start Backend Server

```bash
# From backend directory
uvicorn main:app --reload --port 8000

# Expected output:
# INFO:     Started server process [12345]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 6: Frontend Setup (Optional)

```bash
# Navigate to frontend (Phase 2 extended)
cd ../frontend  # Go to root frontend directory

# Install dependencies
npm install

# Start development server
npm run dev

# Access at: http://localhost:3000
```

---

## Testing the Chatbot

### Method 1: cURL Commands

**1. Create a Task:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add buy milk to my tasks"
  }'

# Expected response:
# {
#   "success": true,
#   "data": {
#     "response": "I've added 'Buy milk' to your tasks (ID: ...)",
#     "conversation_id": "...",
#     "tool_calls": [...]
#   },
#   "error": null
# }
```

**2. Query Tasks:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/YOUR_USER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "What are my tasks?",
    "conversation_id": "FIRST_RESPONSE_CONVERSATION_ID"
  }'

# Expected response lists your tasks
```

**3. Complete a Task:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/YOUR_USER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "I finished buying milk"
  }'

# Expected: Task marked complete with confirmation
```

### Method 2: Frontend Chat Interface

1. Open browser to `http://localhost:3000`
2. Navigate to `/chat` page
3. Type messages in the input box:
   ```
   Add buy milk to my tasks
   What do I need to do?
   I finished the milk task
   ```
4. Press Enter to send

---

## Conversation Examples

### Example 1: Basic Task Management

**User**: "Add buy milk to my tasks"
**Assistant**: "I've added 'Buy milk' to your tasks (ID: abc-123)"

**User**: "Add walk the dog"
**Assistant**: "I've added 'Walk the dog' to your tasks (ID: def-456)"

**User**: "Show me my tasks"
**Assistant**: "You have 2 tasks:\n1. Buy milk (pending)\n2. Walk the dog (pending)"

**User**: "Mark the first one as done"
**Assistant**: "Marked 'Buy milk' as complete ✓"

---

### Example 2: Contextual References

**User**: "Add call mom tomorrow"
**Assistant**: "I've added 'Call mom' to your tasks (ID: xyz-789)"

**User**: "Change it to call mom at 5pm"
**Assistant**: "I've updated task xyz-789: 'Call mom at 5pm' (was: 'Call mom')"

**User**: "Remove it"
**Assistant**: "Which task would you like me to delete? I found: 'Call mom at 5pm'"

**User**: "Delete that one"
**Assistant**: "Deleted 'Call mom at 5pm' (ID: xyz-789)"

---

### Example 3: Error Handling

**User**: "Complete task 999999"
**Assistant**: "I couldn't find task 999999. Would you like to see your tasks?"

**User**: "Yes"
**Assistant**: "[Shows list of actual tasks]"

---

## Troubleshooting

### Common Issues

**1. "Module not found" error**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. "Database connection failed"**
```bash
# Solution: Check DATABASE_URL in .env
# Verify PostgreSQL is running
psql -h localhost -U user -d dbname
```

**3. "OpenAI API key invalid"**
```bash
# Solution: Check OPENAI_API_KEY in .env
# Verify key has GPT-4o access
export OPENAI_API_KEY=sk-...
```

**4. "Conversation not found"**
```bash
# Solution: Don't provide conversation_id for first message
# Let the system auto-create a new conversation
```

**5. Response time > 3 seconds**
```bash
# Check OpenAI API status
curl https://status.openai.com/api/v1/status.json

# If API is degraded, retry request
```

---

## Development Tips

### View Conversation History

```sql
-- PostgreSQL query to see all messages
SELECT
  c.id as conversation_id,
  m.role,
  m.content,
  m.created_at
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
WHERE c.user_id = 'your-user-id'
ORDER BY m.created_at;
```

### Debug Tool Calls

The `tool_calls` array in the response shows which MCP tools were executed:

```json
{
  "tool_calls": [
    {
      "tool": "add_task",
      "success": true,
      "result": {
        "task_id": "...",
        "title": "Buy milk"
      }
    }
  ]
}
```

### Clear All Data (Development Only)

```bash
# WARNING: This deletes all conversations and messages
alembic downgrade base  # Remove Phase 3 tables
alembic upgrade head     # Recreate Phase 3 tables
```

---

## Next Steps

After successful local testing:

1. **Run Integration Tests**: `pytest backend/tests/integration/`
2. **Performance Testing**: Load test with 100 concurrent users
3. **Deploy to Production**: Follow Phase 2 deployment process (Vercel)
4. **Monitor Metrics**: Track response times, error rates, success criteria

---

## Support

- **Documentation**: See [spec.md](spec.md) for requirements
- **Data Model**: See [data-model.md](data-model.md) for entity definitions
- **API Contract**: See [contracts/openapi.yaml](contracts/openapi.yaml) for API specification
- **Issues**: Create issue in project repository

---

**Status**: ✅ Quickstart Complete - Ready for local development
**Estimated Setup Time**: 15-20 minutes
