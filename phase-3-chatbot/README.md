# Phase 3: AI-Powered Todo Chatbot

**Status:** 🚧 Planning Phase
**Phase:** III of V
**Parent Project:** Hackathon II - Evolution of Todo

## Overview

Phase 3 transforms the todo application into an AI-native chatbot that manages tasks through natural language. Users can interact with the system conversationally instead of using UI forms or command-line interfaces.

## Technology Stack

### AI Framework
- **OpenAI Agents SDK** - Agent orchestration and decision making
- **GPT-4o** - Natural language understanding
- **MCP (Model Context Protocol)** - Tool interface layer

### Backend
- **FastAPI** - REST API and WebSocket server
- **PostgreSQL** - Database (Neon Serverless)
- **SQLModel** - ORM and models

### Frontend
- **WebSocket Client** - Real-time chat interface
- **React/Next.js** - UI components (reusing Phase 2 components)

## Architecture

```
phase-3-chatbot/
├── agents/              # Agent configurations and prompts
├── api/                 # API specifications (REST + WebSocket)
├── backend/             # FastAPI server implementation
│   ├── main.py         # Application entry point
│   ├── routes/         # API routes
│   ├── services/       # Business logic
│   └── db.py           # Database connection
├── database/            # Database schemas and migrations
│   ├── schema.md       # Database design
│   └── migrations/     # Migration scripts
├── docs/                # Phase 3 documentation
├── frontend/            # Chat interface
│   ├── components/     # React components
│   └── pages/          # Chat pages
├── mcp-tools/           # MCP tool implementations
│   ├── add_task.py     # Create task tool
│   ├── list_tasks.py   # Query tasks tool
│   ├── update_task.py  # Modify task tool
│   ├── complete_task.py# Mark complete tool
│   └── delete_task.py  # Remove task tool
└── specs/               # Feature specifications
    ├── overview.md     # Phase 3 overview
    └── features/       # Detailed feature specs
```

## Key Principles

### Tool-First AI Design
- ✅ AI agents interact ONLY through MCP tools
- ❌ NO direct database access by agents
- ✅ Every action logged and explainable
- ✅ Stateless operations (idempotent where possible)

### Agent Behavior Standards
- **Clarification over assumption** - Ask when intent is unclear
- **Confirmation of actions** - Always confirm successful operations
- **Safe defaults** - Use sensible defaults instead of failing
- **No hallucination** - Never invent task IDs or content
- **Friendly tone** - Conversational, helpful assistant

### Data Integrity
- User data isolation enforced at tool level
- Conversations persist across requests
- No data loss on server restart
- Database-backed state management

## MCP Tools

### Core Todo Operations

| Tool | Purpose | When Used |
|------|---------|-----------|
| `add_task` | Create new task | User wants to add/create task |
| `list_tasks` | Query tasks | User asks to see/show tasks |
| `update_task` | Modify task | User wants to edit/change task |
| `complete_task` | Mark complete | User wants to finish/done task |
| `delete_task` | Remove task | User wants to delete/remove task |

### Tool Constraints

- Every tool validates `user_id` for data isolation
- Tools are stateless (no in-memory state)
- Each tool has explicit input/output contracts
- Error handling with user-friendly messages
- Tools log all operations for observability

## Phase 3 Deliverables

### Milestone 1: Core Chatbot (MVP)
- [ ] Basic WebSocket chat interface
- [ ] OpenAI Agents SDK integration
- [ ] MCP server with 5 core tools
- [ ] Database schema for conversations
- [ ] User authentication (reuse Phase 2)

### Milestone 2: Enhanced Interactions
- [ ] Natural language task parsing
- [ ] Multi-turn conversations
- [ ] Task query by filters (status, date)
- [ ] Bulk operations (complete all, delete all)

### Milestone 3: Advanced Features
- [ ] Task reminders via chat
- [ ] Recurring task support
- [ ] Conversation history export
- [ ] Analytics and insights

## Performance Budgets

| Metric | Target | Priority |
|--------|--------|----------|
| Chat response time | <500ms | P0 |
| Tool execution | <200ms | P0 |
| Database query | <50ms | P1 |
| WebSocket latency | <100ms | P1 |

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL database (Neon)
- OpenAI API key

### Setup
```bash
# Clone repo
cd phase-3-chatbot

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install

# Run backend
uvicorn main:app --reload

# Run frontend
npm run dev
```

## Documentation

- [Constitution](../../.specify/memory/constitution.md) - Project governance
- [Phase 1](../../phase-1-console/) - Console Todo App
- [Phase 2](../../phase-2-web/) - Web Todo App
- [API Specs](api/) - REST and WebSocket API
- [Database Schema](database/schema.md) - Database design

## Status

**Current Phase:** III - AI Chatbot
**Progress:** 10% (Planning phase)
**Next Steps:**
1. Create feature specification (`/sp.spec`)
2. Design MCP tool contracts
3. Implement WebSocket server
4. Integrate OpenAI Agents SDK

---

**Note:** All Phase 3 development follows the [Constitution](../../.specify/memory/constitution.md) v2.0 governance rules, particularly Principles 8 (Tool-First AI Design) and 9 (Agent Behavior Standards).
