# MCP Tool Invocation Skill

## Description
Reusable skill for invoking Model Context Protocol (MCP) tools with proper parameter validation, error handling, and response parsing.

## When to Use
- Agent needs to interact with database through MCP tools
- Executing task operations (add/list/complete/update/delete)
- Any operation requiring MCP tool abstraction
- Testing MCP tool functionality

## Capabilities

### 1. Get MCP Tools
```python
from mcp_tools import get_all_tools

def get_tool(tool_name: str):
    """Get MCP tool by name"""
    tools = get_all_tools()
    if tool_name not in tools:
        raise ValueError(f"Tool '{tool_name}' not found")
    return tools[tool_name]
```

### 2. Invoke Tool Safely
```python
def invoke_tool(tool_name: str, session, **kwargs):
    """Invoke MCP tool with error handling"""
    try:
        tool = get_tool(tool_name)
        result = tool.execute(session=session, **kwargs)

        if result.success:
            return {
                "success": True,
                "data": result.data,
                "tool": tool_name
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "tool": tool_name
            }
    except Exception as e:
        return {
            "success": False,
            "error": {"code": "EXCEPTION", "message": str(e)},
            "tool": tool_name
        }
```

### 3. Chain Multiple Tools
```python
def invoke_tool_chain(tool_calls, session):
    """Execute multiple tools in sequence"""
    results = []
    for tool_call in tool_calls:
        result = invoke_tool(
            tool_call["tool"],
            session,
            **tool_call["parameters"]
        )
        results.append(result)

        # Stop on first failure
        if not result["success"]:
            break

    return results
```

## Available MCP Tools

### add_task
```python
invoke_tool(
    "add_task",
    session,
    user_id="user-123",
    title="Buy milk",
    description="Get 2% milk from store"
)
```

### list_tasks
```python
# List all tasks
invoke_tool("list_tasks", session, user_id="user-123")

# Filter by completion status
invoke_tool(
    "list_tasks",
    session,
    user_id="user-123",
    completed=False  # Only pending tasks
)
```

### complete_task
```python
# Complete by task ID
invoke_tool(
    "complete_task",
    session,
    user_id="user-123",
    task_id="123"
)

# Complete by title
invoke_tool(
    "complete_task",
    session,
    user_id="user-123",
    title="Buy milk"
)
```

## Error Handling

### Validation Errors
```python
if not result["success"]:
    error = result["error"]
    if error["code"] == "VALIDATION_ERROR":
        # Handle invalid input
        return f"Invalid input: {error['message']}"
    elif error["code"] == "NOT_FOUND":
        # Handle missing resource
        return f"Resource not found: {error['message']}"
```

### Transaction Safety
```python
def invoke_tool_with_rollback(tool_name, session, **kwargs):
    """Invoke tool with automatic rollback on error"""
    try:
        result = invoke_tool(tool_name, session, **kwargs)
        if not result["success"]:
            session.rollback()
        return result
    except Exception as e:
        session.rollback()
        raise
```

## Tool Response Format

All MCP tools return:
```python
{
    "success": True/False,
    "data": {...},      # On success
    "error": {...},     # On failure
    "tool": "tool_name"
}
```

## Agent Integration

### Mock Agent Pattern
```python
class MockAgentRunner:
    def run(self, message, conversation_history, db_session):
        # Detect intent
        if "add" in message.lower():
            result = invoke_tool("add_task", db_session, user_id=..., title=...)
            return {
                "response": f"I've added '{result['data']['title']}'",
                "tool_calls": [{"tool": "add_task", "status": "success"}]
            }
```

### OpenAI Agent Pattern
```python
# OpenAI will call tools automatically
response = client.chat.completions.create(
    model="gpt-4o",
    messages=conversation_history,
    tools=format_mcp_tools_for_openai()
)

# Execute tool calls
for tool_call in response.tool_calls:
    result = invoke_tool(
        tool_call.function.name,
        db_session,
        **json.loads(tool_call.function.arguments)
    )
```

## Best Practices
1. Always pass `session` parameter for database operations
2. Validate required parameters before invoking tools
3. Handle both success and error cases
4. Log tool calls for debugging
5. Use tool chains for complex operations
6. Check `result["success"]` before accessing `result["data"]`

## Dependencies
- mcp_tools package from phase-3-chatbot/backend
- Database session from db.py
- Exception handling from Python standard lib
