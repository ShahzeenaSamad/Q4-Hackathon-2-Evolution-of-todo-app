# AI-Powered Todo Chatbot Backend

FastAPI backend for AI-powered todo task management using OpenAI GPT-4o and MCP tools.

## Features

- **Natural Language Task Management**: Create, query, update, and delete tasks through chat
- **Stateless Architecture**: No server-side state, full conversation persistence
- **Tool-First AI Design**: All operations through MCP tools (Principle 8 compliance)
- **OpenAI GPT-4o**: Advanced intent understanding and tool orchestration

## Setup

### Prerequisites

- Python 3.13+
- PostgreSQL database (Neon Serverless recommended)
- OpenAI API key with GPT-4o access

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create `.env` file:

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

### Database Migrations

```bash
# Run migrations
alembic upgrade head
```

### Run Server

```bash
uvicorn main:app --reload --port 8000
```

API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/v1/chat/{user_id}` - Send chat message
- `GET /health` - Health check
- `GET /` - Root endpoint

## Architecture

```
backend/
├── main.py                 # FastAPI application
├── models/                 # Database models (Task, Conversation, Message)
├── mcp_tools/              # MCP tools for task operations
├── agents/                 # OpenAI agent configuration
├── routes/                 # API endpoints
├── services/               # Business logic
└── tests/                  # Unit, integration, contract tests
```

## Development

See [Phase 3 Quickstart](../specs/features/003-ai-chatbot/quickstart.md) for detailed setup and testing instructions.
