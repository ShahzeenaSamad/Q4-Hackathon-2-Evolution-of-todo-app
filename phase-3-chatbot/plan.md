# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot` | **Date**: 2026-01-22 | **Spec**: [spec.md](specs/features/003-ai-chatbot/spec.md)
**Input**: Feature specification from `phase-3-chatbot/specs/features/003-ai-chatbot/spec.md`

## Summary

Build a stateless AI-native chatbot that enables users to manage todo tasks through natural language conversation. The system uses OpenAI Agents SDK for intent interpretation, MCP (Model Context Protocol) tools for all task operations, and PostgreSQL-backed conversation persistence to ensure no server-side state between requests. Users can create, query, complete, update, and delete tasks through conversational commands without using traditional form-based interfaces.

## Technical Context

**Language/Version**: Python 3.13+ (backend), JavaScript/TypeScript (frontend chat interface)
**Primary Dependencies**:
- OpenAI Agents SDK (agent orchestration)
- GPT-4o (natural language understanding)
- FastAPI (backend server)
- MCP SDK (Model Context Protocol for tool definitions)
- SQLModel (database ORM)
**Storage**: Neon PostgreSQL (shared with Phase 2)
**Testing**: pytest (Python), Vitest (TypeScript), integration tests for agent flows
**Target Platform**: Server: Linux container (Vercel/Cloud Run), Client: Web browser
**Project Type**: web (backend + frontend)
**Performance Goals**: <3 second response time (95th percentile), <500ms tool execution
**Constraints**: Stateless architecture (no in-memory session data), tool-first design (AI never touches database directly), database-backed state only
**Scale/Scope**: 100 concurrent users, 1000 tasks per user, 100+ messages per conversation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle 1: Spec-Driven Development ✅
- Feature specification exists at `specs/features/003-ai-chatbot/spec.md`
- 34 functional requirements with acceptance criteria
- 7 user stories with independent test paths
- All requirements traceable to specification

### Principle 2: AI as Implementation Engine ✅
- OpenAI Agents SDK for AI orchestration
- MCP tools for all operations (no direct logic)
- Stateless design with database backing

### Principle 8: Tool-First AI Design ✅
- **MANDATORY**: AI agents interact ONLY through MCP tools
- **FORBIDDEN**: Direct database access by AI agents
- Every tool has explicit input/output contracts
- All operations logged and explainable

### Principle 9: Agent Behavior Standards ✅
- Clarification over assumption for ambiguous input
- Confirmation of all successful actions
- Safe defaults for missing parameters
- No hallucination of task IDs or content
- Friendly, helpful tone maintained

**GATE STATUS**: ✅ **ALL CHECKS PASSED** - No constitution violations

## Project Structure

### Documentation (Phase 3)

```text
phase-3-chatbot/
├── plan.md              # This file
├── specs/
│   └── features/
│       └── 003-ai-chatbot/
│           ├── spec.md          # Feature specification (complete)
│           └── checklists/
│               └── requirements.md  # Quality validation (passed)
├── api/                 # API contracts (Phase 1 output)
│   └── openapi.yaml     # OpenAPI specification for chat endpoint
├── database/            # Database design (Phase 1 output)
│   ├── schema.md        # Entity definitions
│   └── migrations/      # Migration scripts
├── mcp-tools/           # MCP tool implementations (Phase 2)
│   ├── add_task.py
│   ├── list_tasks.py
│   ├── update_task.py
│   ├── complete_task.py
│   └── delete_task.py
└── backend/             # Backend implementation
    ├── main.py          # FastAPI app entry point
    ├── routes/          # Chat endpoint
    ├── agents/          # Agent configuration
    ├── services/        # Business logic
    └── models/          # Database models
```

### Source Code (repository root)

```text
phase-3-chatbot/
└── backend/
    ├── main.py                 # FastAPI application
    ├── models/
    │   ├── task.py             # Task model (reuse from Phase 2)
    │   ├── conversation.py     # Conversation model
    │   └── message.py          # Message model
    ├── mcp_tools/
    │   ├── __init__.py
    │   ├── base.py             # Base MCP tool class
    │   ├── add_task.py         # Create task tool
    │   ├── list_tasks.py       # Query tasks tool
    │   ├── update_task.py      # Modify task tool
    │   ├── complete_task.py    # Mark complete tool
    │   └── delete_task.py      # Remove task tool
    ├── agents/
    │   ├── __init__.py
    │   ├── config.py           # Agent configuration
    │   └── runner.py           # Agent execution logic
    ├── routes/
    │   └── chat.py             # Chat endpoint
    ├── services/
    │   ├── conversation_svc.py # Conversation persistence
    │   └── history_builder.py  # Conversation history reconstruction
    └── tests/
        ├── unit/               # Tool tests
        ├── integration/        # Endpoint tests
        └── contract/           # API contract tests

frontend/ (reuse Phase 2 structure, add chat components)
└── src/
    ├── components/
    │   ├── chat/
    │   │   ├── ChatInterface.tsx   # Main chat UI
    │   │   ├── MessageList.tsx     # Message display
    │   │   └── MessageInput.tsx     # Input component
    │   └── auth/ (reuse from Phase 2)
    └── lib/
        └── chat.ts               # Chat API client
```

**Structure Decision**: Web application architecture (backend + frontend). Backend follows Phase 2 FastAPI structure with new agents/ and mcp_tools/ directories. Frontend extends Phase 2 Next.js app with chat components. No mobile application needed.

## Complexity Tracking

> No constitution violations - this section intentionally left empty

---

## Phase 0: Research & Technical Decisions

### Research Tasks

**Task 1: OpenAI Agents SDK Best Practices**
- **Question**: How to structure agents for tool-first design with GPT-4o?
- **Research**: OpenAI Agents SDK documentation, examples of tool-calling agents
- **Decision**: Use OpenAI Agents SDK with function calling for MCP tool orchestration

**Task 2: MCP (Model Context Protocol) Implementation**
- **Question**: How to define and implement MCP tools in Python?
- **Research**: Official MCP Python SDK, tool specification format
- **Decision**: Use official MCP SDK with JSON-RPC tool interface

**Task 3: Conversation History Management**
- **Question**: How to handle conversation context in stateless architecture?
- **Research**: Best practices for conversation persistence, context window optimization
- **Decision**: Load full history per request, implement summarization if >50 messages

**Task 4: WebSocket vs HTTP for Chat**
- **Question**: Should chat use WebSocket (persistent) or HTTP (request/response)?
- **Research**: Trade-offs between real-time updates and simplicity
- **Decision**: HTTP POST for statelessness (aligns with constitution), WebSocket for future real-time sync

### Technology Decisions

| Decision | Choice | Rationale | Alternatives Considered |
|----------|--------|-----------|--------------------------|
| AI Framework | OpenAI Agents SDK | Native tool-calling support, GPT-4o integration | LangChain (too heavy), Custom agents (reinventing wheel) |
| Tool Protocol | MCP (Model Context Protocol) | Industry standard for AI tool interfaces | OpenAPI (too generic), Custom format (proprietary) |
| Backend Framework | FastAPI | Async support, matches Phase 2, type-safe | Flask (sync only), Express (different stack) |
| Frontend Chat UI | Custom React components | Full control, reuses Phase 2 structure | ChatKit (opinionated), Stream (too heavy) |
| Conversation Storage | Full message history | Simplicity, no data loss, meets <3s goal | Summarization (added complexity), Windowing (data loss risk) |

### Key Architectural Decisions

**Decision 1: Stateless Request/Response Pattern**
- **Choice**: HTTP POST endpoint with full conversation history loaded each request
- **Rationale**: Aligns with constitution Principle 8 (stateless components), enables horizontal scaling
- **Trade-offs**: Slightly slower than in-memory (acceptable within <3s budget)
- **Alternatives**: WebSocket with server state (rejected: violates statelessness), Session storage (rejected: Phase 1 only)

**Decision 2: Tool Chaining Strategy**
- **Choice**: Automatic tool chaining by AI agent with atomic execution
- **Rationale**: Natural language queries often require multiple operations (list → identify → delete)
- **Trade-offs**: More complex error handling (mitigated by transaction patterns)
- **Alternatives**: Explicit user confirmation for each step (rejected: poor UX), Single operation only (rejected: insufficient functionality)

**Decision 3: Error Handling and User Messages**
- **Choice**: User-friendly error messages with actionable suggestions
- **Rationale**: Constitution Principle 9 requires helpful, conversational error responses
- **Examples**: "Task not found. Would you like to see your tasks?" vs "404 Task Not Found"
- **Trade-offs**: Longer error messages (acceptable for conversational interface)

**Decision 4: Duplicate Task Titles**
- **Choice**: Allow duplicate titles, use task IDs for disambiguation
- **Rationale**: Natural language doesn't prevent duplicates, users say "buy milk" multiple times legitimately
- **Trade-offs**: Ambiguous references require clarification (handled by agent)
- **Alternatives**: Auto-number titles (rejected: breaks natural language), Enforce uniqueness (rejected: too restrictive)

**Decision 5: Conversation History Length**
- **Choice**: Load full history, implement summarization if >50 messages
- **Rationale**: Balances context preservation with token limits and performance
- **Trade-offs**: Summary may lose details (acceptable for long conversations)
- **Alternatives**: Hard limit (rejected: data loss), Windowing (rejected: loses early context)

**Decision 6: Idempotency and Retry Behavior**
- **Choice**: Idempotent tool design with database-level constraints
- **Rationale**: Network failures require retry without duplicate operations
- **Implementation**: Unique constraints on tasks, transactional updates, optimistic locking
- **Trade-offs**: Slightly more complex database schema (acceptable for data integrity)

**Decision 7: MCP Tool Response Consistency**
- **Choice**: Standardized JSON response format for all tools
- **Rationale**: Agent needs predictable structure to format user responses
- **Format**: `{success: bool, data: any, error: {code: string, message: string}}`
- **Trade-offs**: Rigid structure (acceptable for clarity and debugging)

---

## Phase 1: Database & Data Models

### Entity Definitions

**Task** (reused from Phase 2, extended for chat context)
```python
class Task(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow, onupdate=utcnow)

    # Relationships
    user: User = relationship(back_populates="tasks")
```

**Conversation** (new for Phase 3)
```python
class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow, onupdate=utcnow)

    # Relationships
    user: User = relationship(back_populates="conversations")
    messages: List["Message"] = relationship(back_populates="conversation")
```

**Message** (new for Phase 3)
```python
class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id")
    role: str = Field(index=True)  # "user" or "assistant"
    content: str = Field(max_length=5000)
    created_at: datetime = Field(default_factory=utcnow)

    # Relationships
    conversation: Conversation = relationship(back_populates="messages")
```

**User** (reused from Phase 2, relationships extended)
```python
class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utcnow)

    # Relationships (extended)
    tasks: List["Task"] = relationship(back_populates="user")
    conversations: List["Conversation"] = relationship(back_populates="user")
```

### State Transitions

**Conversation Lifecycle**
```
[Created] → [Active] → [Archived]
     ↓
[Deleted]
```

**Message Flow**
```
User Message → [Processing] → Agent → Tools → Response → Assistant Message
```

### Validation Rules

**Task Validations**
- Title: Required, non-empty after trim, max 200 chars
- Description: Optional, max 2000 chars
- User ID: Required, must exist in users table
- Completed: Boolean, default False

**Conversation Validations**
- User ID: Required, must exist in users table
- Auto-created on first message if not provided

**Message Validations**
- Role: Must be "user" or "assistant"
- Content: Required, non-empty, max 5000 chars
- Conversation ID: Required, must exist in conversations table

---

## Phase 2: MCP Server & Tool Definitions

### MCP Tool Contracts

All MCP tools follow this standardized interface:

```python
class MCPTool(ABC):
    @abstractmethod
    async def execute(self, params: dict) -> dict:
        """Execute tool with given parameters"""
        pass

    @property
    @abstractmethod
    def schema(self) -> dict:
        """Return JSON schema for tool parameters"""
        pass
```

### Tool Specifications

**1. add_task Tool**
```python
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 1, "maxLength": 200},
        "description": {"type": "string", "maxLength": 2000},
        "user_id": {"type": "string"}
    },
    "required": ["title", "user_id"]
}

response = {
    "success": true,
    "data": {
        "task_id": "uuid",
        "title": "Buy milk",
        "created_at": "2026-01-22T10:00:00Z"
    },
    "error": null
}
```

**2. list_tasks Tool**
```python
schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
        "status": {"enum": ["all", "pending", "completed"], "default": "all"},
        "limit": {"type": "integer", "minimum": 1, "maximum": 100}
    },
    "required": ["user_id"]
}

response = {
    "success": true,
    "data": {
        "tasks": [
            {"id": "uuid", "title": "Buy milk", "completed": false}
        ],
        "total": 5,
        "pending": 3,
        "completed": 2
    },
    "error": null
}
```

**3. complete_task Tool**
```python
schema = {
    "type": "object",
    "properties": {
        "task_id": {"type": "string"},
        "user_id": {"type": "string"}
    },
    "required": ["task_id", "user_id"]
}

response = {
    "success": true,
    "data": {
        "task_id": "uuid",
        "title": "Buy milk",
        "completed": true
    },
    "error": null
}
```

**4. update_task Tool**
```python
schema = {
    "type": "object",
    "properties": {
        "task_id": {"type": "string"},
        "user_id": {"type": "string"},
        "title": {"type": "string", "minLength": 1, "maxLength": 200},
        "description": {"type": "string", "maxLength": 2000}
    },
    "required": ["task_id", "user_id"]
}

response = {
    "success": true,
    "data": {
        "task_id": "uuid",
        "title": "Buy almond milk",
        "old_title": "Buy milk"
    },
    "error": null
}
```

**5. delete_task Tool**
```python
schema = {
    "type": "object",
    "properties": {
        "task_id": {"type": "string"},
        "user_id": {"type": "string"}
    },
    "required": ["task_id", "user_id"]
}

response = {
    "success": true,
    "data": {
        "task_id": "uuid",
        "title": "Buy milk",
        "deleted": true
    },
    "error": null
}
```

### Error Taxonomy

| Error Code | Message | HTTP Status |
|------------|---------|-------------|
| TASK_NOT_FOUND | "I couldn't find a task with that ID. Would you like to see your tasks?" | 404 |
| INVALID_TASK_ID | "That doesn't look like a valid task ID." | 400 |
| EMPTY_TITLE | "The task title can't be empty. What would you like the task to say?" | 400 |
| UNAUTHORIZED | "You don't have permission to access this task." | 403 |
| DUPLICATE_FAILED | "A task with this title already exists." | 409 |
| DATABASE_ERROR | "I'm having trouble right now. Please try again." | 500 |

---

## Phase 3: Agent Configuration & Setup

### OpenAI Agents SDK Configuration

```python
# agents/config.py
from openai import OpenAI
from openai_agents import Agent, ToolSet

AGENT_CONFIG = {
    "model": "gpt-4o",
    "temperature": 0.7,  # Balance between creativity and consistency
    "max_tokens": 500,
    "system_prompt": """You are a helpful todo assistant. Help users manage their tasks through natural language.

    Rules:
    - Always confirm successful actions with task details
    - Ask clarifying questions when intent is ambiguous
    - Never invent task IDs or assume task content
    - Use tools for ALL task operations (no direct database access)
    - Maintain friendly, conversational tone
    - Handle errors gracefully with helpful suggestions
    """
}

AGENT_INSTRUCTIONS = """
When users ask to manage tasks, use the appropriate MCP tool:
- "add", "create", "new task" → add_task tool
- "show", "list", "what's on my list" → list_tasks tool
- "complete", "done", "finished" → complete_task tool
- "update", "change", "modify" → update_task tool
- "delete", "remove" → delete_task tool

Before acting, confirm you understand the user's intent. If multiple tasks match a description, list them and ask which one.

After every successful action, confirm with:
- What you did
- The task title and ID
- Relevant details (e.g., "Marked 'Buy milk' as complete ✓")
"""
```

### Agent Runner

```python
# agents/runner.py
class AgentRunner:
    def __init__(self, tools: ToolSet):
        self.client = OpenAI()
        self.agent = Agent(
            config=AGENT_CONFIG,
            instructions=AGENT_INSTRUCTIONS,
            tools=tools
        )

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[dict]
    ) -> str:
        """
        Process user message through agent

        Args:
            user_message: Current user input
            conversation_history: List of {role, content} from database

        Returns:
            Assistant response text
        """
        messages = [
            {"role": "system", "content": AGENT_INSTRUCTIONS}
        ] + conversation_history + [
            {"role": "user", "content": user_message}
        ]

        response = await self.client.chat.completions.create(
            model=AGENT_CONFIG["model"],
            messages=messages,
            tools=self.agent.tools,
            temperature=AGENT_CONFIG["temperature"]
        )

        return response.choices[0].message
```

---

## Phase 4: Stateless Chat Endpoint Implementation

### API Endpoint Design

**Endpoint**: `POST /api/chat/{user_id}`

**Request Schema**:
```json
{
  "message": "Add buy milk to my tasks",
  "conversation_id": "optional-uuid"
}
```

**Response Schema**:
```json
{
  "success": true,
  "data": {
    "response": "I've added 'Buy milk' to your tasks (ID: 123)",
    "conversation_id": "uuid",
    "tool_calls": [
      {"tool": "add_task", "result": {...}}
    ]
  },
  "error": null
}
```

### Request Lifecycle

```python
# routes/chat.py
@router.post("/chat/{user_id}")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Stateless chat endpoint - no server-side memory between requests

    Lifecycle:
    1. Extract user_id from JWT token
    2. Get or create conversation
    3. Load full conversation history from database
    4. Pass to agent for processing
    5. Execute tools via MCP protocol
    6. Store user message and assistant response
    7. Return formatted response
    """

    # Step 1: Validate user (JWT from Phase 2)
    user = get_user(user_id, db)
    if not user:
        raise HTTPException(401, "Unauthorized")

    # Step 2: Get or create conversation
    conversation = get_or_create_conversation(
        user_id,
        request.conversation_id,
        db
    )

    # Step 3: Load conversation history
    history = load_conversation_history(conversation.id, db)

    # Step 4: Process with agent
    agent_runner = AgentRunner(mcp_tools)
    assistant_response = await agent_runner.process_message(
        request.message,
        history
    )

    # Step 5: Store messages
    save_message(conversation.id, "user", request.message, db)
    save_message(conversation.id, "assistant", assistant_response, db)

    # Step 6: Return response
    return ChatResponse(
        success=True,
        data={
            "response": assistant_response,
            "conversation_id": conversation.id,
            "tool_calls": agent_runner.last_tool_calls
        }
    )
```

---

## Phase 5: Conversation Persistence & Retrieval

### History Builder Service

```python
# services/history_builder.py
class ConversationHistoryBuilder:
    @staticmethod
    def build(conversation_id: str, db: Session) -> List[dict]:
        """
        Load full conversation history from database

        Args:
            conversation_id: UUID of conversation
            db: Database session

        Returns:
            List of {role, content, timestamp} messages
        """
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()

        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in messages
        ]
```

### Conversation Service

```python
# services/conversation_svc.py
class ConversationService:
    @staticmethod
    def get_or_create(
        user_id: str,
        conversation_id: Optional[str],
        db: Session
    ) -> Conversation:
        """
        Get existing conversation or create new one

        Args:
            user_id: User UUID
            conversation_id: Optional conversation UUID
            db: Database session

        Returns:
            Conversation object
        """
        if conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()

            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation
```

---

## Phase 6: Frontend ChatKit Integration

### Chat Interface Components

**ChatInterface.tsx** - Main container
```typescript
interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export function ChatInterface({ userId }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string>()

  const sendMessage = async () => {
    setIsLoading(true)

    const response = await fetch(`/api/chat/${userId}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        message: inputValue,
        conversation_id: conversationId
      })
    })

    const data = await response.json()

    setMessages(prev => [
      ...prev,
      {role: 'user', content: inputValue, timestamp: new Date().toISOString()},
      {role: 'assistant', content: data.data.response, timestamp: new Date().toISOString()}
    ])

    setConversationId(data.data.conversation_id)
    setInputValue('')
    setIsLoading(false)
  }

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      <MessageInput
        value={inputValue}
        onChange={setInputValue}
        onSend={sendMessage}
        disabled={isLoading}
      />
    </div>
  )
}
```

---

## Phase 7: Error Handling & Confirmations

### Error Handling Strategy

**1. Tool-Level Errors**
```python
try:
    result = await tool.execute(params)
    if not result["success"]:
        # Format error for AI to explain to user
        return f"I had trouble: {result['error']['message']}"
    return format_success(result)
except Exception as e:
    logger.error(f"Tool execution failed: {e}")
    return "Something went wrong. Please try again."
```

**2. Agent-Level Errors**
```python
if agent_response.tool_calls:
    for tool_call in agent_response.tool_calls:
        try:
            tool_result = await execute_tool(tool_call)
        except ValidationError as e:
            # Ask user for clarification
            return f"{e.message} (e.g., {e.example})"
        except NotFoundError:
            # Offer to show tasks
            return "I couldn't find that. Would you like to see your tasks?"
```

**3. Endpoint-Level Errors**
```python
try:
    response = await process_chat_request(request)
    return response
except HTTPException:
    raise  # Re-raise FastAPI exceptions
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "I'm having trouble right now. Please try again."
            }
        }
    )
```

### Confirmation Patterns

| Action | Confirmation Format |
|--------|-------------------|
| Create task | "I've added '{title}' to your tasks (ID: {id})" |
| Complete task | "Marked '{title}' as complete ✓" |
| Update task | "I've updated task {id}: '{new_title}' (was: '{old_title}')" |
| Delete task | "Deleted '{title}' (ID: {id})" |
| List tasks | "You have {total} tasks. {pending} pending, {completed} completed." |
| Error (not found) | "I couldn't find task {id}. Would you like to see your tasks?" |
| Error (ambiguous) | "Which {thing}? I found: {options}" |

---

## Phase 8: Testing & Validation

### Unit Tests for MCP Tools

```python
# tests/unit/test_add_task_tool.py
@pytest.mark.asyncio
async def test_add_task_creates_task():
    tool = AddTaskTool()
    params = {
        "title": "Buy milk",
        "user_id": "test-user-id"
    }

    result = await tool.execute(params)

    assert result["success"] == True
    assert result["data"]["title"] == "Buy milk"
    assert "task_id" in result["data"]

@pytest.mark.asyncio
async def test_add_task_validates_empty_title():
    tool = AddTaskTool()
    params = {
        "title": "   ",
        "user_id": "test-user-id"
    }

    result = await tool.execute(params)

    assert result["success"] == False
    assert result["error"]["code"] == "EMPTY_TITLE"
```

### Integration Tests for Chat Endpoint

```python
# tests/integration/test_chat_endpoint.py
@pytest.mark.asyncio
async def test_chat_creates_task():
    response = await client.post("/chat/test-user-id", json={
        "message": "Add buy milk"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "added" in data["data"]["response"].lower()

@pytest.mark.asyncio
async def test_chat_maintains_conversation():
    # First message
    response1 = await client.post("/chat/test-user-id", json={
        "message": "Add task 1"
    })
    conversation_id = response1.json()["data"]["conversation_id"]

    # Second message with context
    response2 = await client.post("/chat/test-user-id", json={
        "message": "Add another task",
        "conversation_id": conversation_id
    })

    # Verify both tasks exist
    tasks = await get_user_tasks("test-user-id")
    assert len(tasks) == 2
```

### Statelessness Verification

```python
# tests/integration/test_statelessness.py
@pytest.mark.asyncio
async def test_no_server_state_between_requests():
    """
    Verify server holds no state by:
    1. Sending message
    2. Restarting server (simulate by clearing caches)
    3. Sending second message with conversation_id
    4. Verify conversation resumes correctly
    """
    # Create task
    response1 = await client.post("/chat/user-1", json={
        "message": "Add test task"
    })
    conversation_id = response1.json()["data"]["conversation_id"]

    # Simulate server restart (clear any in-memory state)
    clear_all_caches()

    # Continue conversation (should work without server memory)
    response2 = await client.post("/chat/user-1", json={
        "message": "Show me my tasks",
        "conversation_id": conversation_id
    })

    assert "test task" in response2.json()["data"]["response"]
```

### Agent Intent-to-Tool Mapping Tests

```python
# tests/integration/test_agent_tool_mapping.py
@pytest.mark.asyncio
async def test_agent_maps_create_to_add_task():
    """
    Verify agent correctly interprets "create" intent and calls add_task
    """
    response = await client.post("/chat/test-user", json={
        "message": "Create a task to buy groceries"
    })

    tool_calls = response.json()["data"]["tool_calls"]
    assert len(tool_calls) == 1
    assert tool_calls[0]["tool"] == "add_task"
    assert "groceries" in tool_calls[0]["params"]["title"].lower()

@pytest.mark.asyncio
async def test_agent_handles_ambiguous_delete():
    """
    Verify agent asks for clarification when multiple tasks match
    """
    # Create tasks with similar titles
    await create_task(user_id, "Write report")
    await create_task(user_id, "Review report")

    response = await client.post("/chat/test-user", json={
        "message": "Delete the report task"
    })

    # Agent should ask which one
    assert "which" in response.json()["data"]["response"].lower()
```

### Error Handling Tests

```python
# tests/integration/test_error_handling.py
@pytest.mark.asyncio
async def test_invalid_task_id_error():
    response = await client.post("/chat/test-user", json={
        "message": "Complete task 999999"
    })

    data = response.json()
    assert data["success"] == True  # Agent handles gracefully
    assert "couldn't find" in data["data"]["response"].lower()

@pytest.mark.asyncio
async def test_empty_list_error():
    # User with no tasks
    response = await client.post("/chat/empty-user", json={
        "message": "Show me my tasks"
    })

    data = response.json()
    assert "don't have any tasks" in data["data"]["response"].lower()
```

### Acceptance Tests

```python
# tests/acceptance/test_success_criteria.py
@pytest.mark.asyncio
async def test_sc_001_response_time_under_10s():
    """
    SC-001: Users can complete any task operation in under 10 seconds
    """
    start = time.time()

    response = await client.post("/chat/test-user", json={
        "message": "Add buy milk"
    })

    elapsed = time.time() - start
    assert elapsed < 10.0

@pytest.mark.asyncio
async def test_sc_007_3second_response_time():
    """
    SC-007: 95% of requests complete in under 3 seconds
    """
    times = []

    for _ in range(100):
        start = time.time()
        await client.post("/chat/test-user", json={
            "message": f"Add task {random.randint(1, 1000)}"
        })
        times.append(time.time() - start)

    times.sort()
    p95 = times[94]  # 95th percentile
    assert p95 < 3.0

@pytest.mark.asyncio
async def test_sc_010_user_data_isolation():
    """
    SC-010: 100% of task operations validate user ownership
    """
    # User 1 creates task
    await client.post("/chat/user-1", json={
        "message": "Add secret task"
    })

    # User 2 tries to delete it
    response = await client.post("/chat/user-2", json={
        "message": "Delete task 1"  # Try to delete User 1's task by ID
    })

    # Should fail
    assert "permission" in response.json()["data"]["response"].lower() or \
           "can't" in response.json()["data"]["response"].lower()

@pytest.mark.asyncio
async def test_sc_011_persistence_across_restart():
    """
    SC-011: 100% of conversations persist across server restart
    """
    # Create conversation
    response1 = await client.post("/chat/test-user", json={
        "message": "Add test task"
    })
    conversation_id = response1.json()["data"]["conversation_id"]

    # Simulate server restart
    restart_database_connection()
    clear_all_caches()

    # Resume conversation
    response2 = await client.post("/chat/test-user", json={
        "message": "What did I just ask?",
        "conversation_id": conversation_id
    })

    assert "test task" in response2.json()["data"]["response"].lower()
```

---

## Quality Validation Checklist

### Constitution Compliance

- [ ] Principle 1: All code references specification documents
- [ ] Principle 2: AI uses OpenAI Agents SDK and MCP tools only
- [ ] Principle 8: NO direct database access by AI (100% tool-based)
- [ ] Principle 9: All responses confirm actions and handle errors gracefully

### Implementation Quality

- [ ] All 34 functional requirements implemented
- [ ] All 7 user stories working with acceptance scenarios
- [ ] All 15 success criteria met (measurable and verified)
- [ ] Zero in-memory session state (verified by statelessness tests)
- [ ] 100% of operations go through MCP tools (verified by code review)
- [ ] All errors return user-friendly messages (verified by error tests)

### Performance Validation

- [ ] <3 second response time (95th percentile) verified by load tests
- [ ] <500ms tool execution time verified by unit tests
- [ ] Supports 100 concurrent users verified by stress tests
- [ ] Conversation history loads in <100ms verified by benchmarks

### Data Integrity Validation

- [ ] 100% user ownership validation on all tools
- [ ] Conversation persists across restart (automated test)
- [ ] Zero data loss on concurrent operations (transaction tests)
- [ ] All timestamps stored for auditability (schema validation)

---

## Next Steps

After completing this implementation plan:

1. **Generate Task Breakdown**: Run `/sp.tasks` to create detailed task list
2. **Start Implementation**: Begin with Phase 1 (database models)
3. **Test Incrementally**: Validate each phase before proceeding
4. **Document Decisions**: Create ADRs for any architectural changes
5. **Deploy and Monitor**: Track success criteria metrics in production

---

**Status**: ✅ Plan Complete - Ready for `/sp.tasks`
**Constitution Check**: ✅ Passed (re-validate after Phase 1 design)
**Phase Gates**: All cleared - no blocking violations
