# Research: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-01-22
**Purpose**: Technical research and decision documentation for Phase 3 implementation

---

## Research Topic 1: OpenAI Agents SDK for Tool-First Architecture

### Question
How to structure agents for tool-first design with GPT-4o while ensuring no direct database access?

### Research Findings
- OpenAI Agents SDK provides native function calling with GPT-4o
- Tools are defined as Python functions with type hints and docstrings
- Agent automatically decides when to call tools based on user input
- No manual prompt engineering required for tool selection

### Decision
**Choice**: Use OpenAI Agents SDK with function calling for MCP tool orchestration

**Rationale**:
- Native tool-calling support in GPT-4o eliminates custom parsing logic
- Agent handles tool chaining automatically
- Type-safe tool definitions prevent errors
- Built-in error handling for failed tool calls

**Alternatives Considered**:
- **LangChain**: Rejected due to excessive abstraction and complexity
- **Custom Agent**: Rejected because it would require reinventing wheel
- **Direct Prompt Engineering**: Rejected because less reliable than function calling

### Implementation Notes
```python
from openai_agents import Agent
from mcp_tools import AddTaskTool, ListTasksTool, etc.

agent = Agent(
    model="gpt-4o",
    tools=[AddTaskTool(), ListTasksTool(), ...],
    instructions="Use tools for ALL task operations"
)
```

---

## Research Topic 2: MCP (Model Context Protocol) Implementation

### Question
How to define and implement MCP tools in Python for AI agent integration?

### Research Findings
- MCP is an open protocol for AI tool interfaces
- Official MCP Python SDK provides tool registration and execution
- Tools expose JSON-RPC interface with JSON schema definitions
- Tools must be stateless (all state passed as parameters)

### Decision
**Choice**: Use official MCP SDK with JSON-RPC tool interface

**Rationale**:
- Industry standard for AI tool integration
- Language-agnostic protocol (future-proofing)
- Built-in tool discovery and validation
- Clear separation between tool definition and execution

**Alternatives Considered**:
- **OpenAPI/Swagger**: Rejected because designed for HTTP APIs, not AI tools
- **Custom Tool Protocol**: Rejected because proprietary and non-standard
- **GraphQL**: Rejected because overkill for simple tool operations

### Implementation Notes
```python
from mcp import Tool, ToolRegistry

@tool(name="add_task")
def add_task(title: str, user_id: str, description: str = None) -> dict:
    """Create a new task for the user"""
    # Tool implementation
    return {"success": True, "data": {...}}
```

---

## Research Topic 3: Conversation History Management in Stateless Architecture

### Question
How to handle conversation context efficiently without server-side memory?

### Research Findings
- Stateless architecture requires loading history per request
- Full history ensures no context loss
- Conversation summarization reduces token usage for long conversations
- Database queries must be optimized for performance

### Decision
**Choice**: Load full conversation history per request, implement summarization at 50 messages

**Rationale**:
- Simplicity: No complex state synchronization
- Reliability: No data loss on restart
- Performance: <100ms query time with proper indexing
- Flexibility: Easy to add features like conversation export

**Trade-offs**:
- Slightly slower than in-memory (acceptable within <3s budget)
- Higher database load (mitigated by connection pooling from Phase 2)

**Alternatives Considered**:
- **In-Memory Session State**: Rejected (violates constitution Principle 8)
- **Sliding Window (last N messages)**: Rejected (loses early context)
- **Distributed Cache (Redis)**: Rejected (adds complexity, single point of failure)

### Performance Optimization
```python
# Database indexes for fast history loading
CREATE INDEX idx_message_conversation_created
ON Message(conversation_id, created_at);

# Query optimization
SELECT * FROM Message
WHERE conversation_id = ?
ORDER BY created_at ASC
LIMIT 1000;  -- Prevent excessive loads
```

---

## Research Topic 4: WebSocket vs HTTP for Chat Interface

### Question
Should the chat interface use WebSocket (persistent connection) or HTTP (request/response)?

### Research Findings
- WebSocket: Real-time bidirectional communication, server complexity
- HTTP: Simpler stateless model, easier scaling, matches constitution
- User experience: Both feel instantaneous for text chat
- Deployment: HTTP works better with serverless platforms (Vercel)

### Decision
**Choice**: HTTP POST for MVP (Phase 3), WebSocket option for future real-time sync

**Rationale**:
- **Statelessness**: HTTP aligns with constitution Principle 8
- **Simplicity**: No connection management complexity
- **Scaling**: Stateless requests scale horizontally
- **Deployment**: Works with existing Phase 2 infrastructure
- **User Experience**: <500ms response time feels instant for text

**Trade-offs**:
- No real-time updates (acceptable for MVP)
- Slightly higher latency (acceptable within <3s budget)

**Alternatives Considered**:
- **WebSocket**: Rejected for MVP due to complexity and statefulness requirements
- **Server-Sent Events (SSE)**: Rejected because unidirectional (client-to-server needed)

### Future Enhancement Path
If real-time sync becomes a priority (e.g., multi-device collaboration):
1. Add WebSocket endpoint for message streaming
2. Keep HTTP for statelessness compliance
3. Use WebSocket for notifications only (not primary chat)

---

## Research Topic 5: Frontend Chat UI Framework

### Question
Which frontend framework/library for chat interface?

### Research Findings
- ChatKit: Opinionated, heavy dependency
- Stream: Expensive, over-engineered for simple chat
- Custom React Components: Full control, reuses Phase 2 structure
- Next.js App Router: Already used in Phase 2

### Decision
**Choice**: Custom React components with Next.js (reusing Phase 2 structure)

**Rationale**:
- **Consistency**: Matches Phase 2 frontend stack
- **Control**: Full customization for conversational UI
- **Lightweight**: No heavy external dependencies
- **Learning**: Demonstrates React best practices

**Alternatives Considered**:
- **ChatKit**: Rejected (too opinionated, heavy)
- **Stream**: Rejected (expensive, overkill for MVP)
- **Vue/Angular**: Rejected (inconsistent with Phase 2)

---

## Decision Summary Table

| Topic | Decision | Key Rationale | Alternatives Rejected |
|-------|----------|---------------|----------------------|
| AI Framework | OpenAI Agents SDK | Native tool calling, GPT-4o support | LangChain, Custom |
| Tool Protocol | MCP SDK | Industry standard, stateless | OpenAPI, Custom |
| Conversation State | Full history load | Simplicity, reliability | In-memory, Redis cache |
| Chat Protocol | HTTP POST | Stateless, scalable | WebSocket (MVP only) |
| Frontend UI | Custom React | Control, consistency | ChatKit, Stream |
| Database | PostgreSQL (Phase 2) | Reuse existing infrastructure | MongoDB, Redis |
| Authentication | JWT (Phase 2) | Reuse existing auth system | OAuth2, SAML |
| Deployment | Vercel (serverless) | Stateless architecture compatible | Self-hosted VM |

---

## Performance Benchmarks

Based on research and Phase 2 performance data:

| Operation | Target | Phase 2 Baseline | Phase 3 Goal |
|-----------|--------|------------------|--------------|
| Database query | <50ms | ~30ms | <50ms ✅ |
| Tool execution | <200ms | N/A | <200ms |
| AI processing | <2s | N/A | <2s |
| Total response | <3s | N/A | <3s (95th percentile) |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI API rate limits | Medium | High | Implement retry with exponential backoff |
| Slow AI response | Low | Medium | Set 2.5s timeout, use faster model if needed |
| Database connection exhaustion | Low | High | Use Phase 2 connection pooling (20+30 overflow) |
| Token limit with long conversations | Medium | Low | Summarize at 50 messages |
| Ambiguous user intent | High | Low | Agent asks clarifying questions |
| Concurrent modifications | Low | Medium | Database transactions with optimistic locking |

---

## Open Questions Resolved

### Q1: How to handle conversation history length?
**Answer**: Load full history, implement summarization at 50 messages

### Q2: Automatic or explicit tool chaining?
**Answer**: Automatic (AI decides when to chain tools)

### Q3: How to structure error messages?
**Answer**: User-friendly, actionable, non-technical

### Q4: Duplicate task titles?
**Answer**: Allow duplicates, use task IDs for disambiguation

### Q5: Strategy for ambiguous commands?
**Answer**: Agent asks clarifying questions (Constitution Principle 9)

### Q6: Retry behavior on failures?
**Answer**: Idempotent tools with database-level constraints

### Q7: MCP tool response format?
**Answer**: Standardized JSON: `{success, data, error}`

---

**Status**: ✅ Research Complete - All NEEDS CLARIFICATION resolved
**Next Phase**: Proceed to data model and API contracts
