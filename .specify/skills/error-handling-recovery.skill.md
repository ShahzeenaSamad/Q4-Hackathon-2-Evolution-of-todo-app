# Error Handling & Recovery Skill

## Description
Reusable skill for handling errors gracefully in agent-MCP tool interactions with user-friendly messages and recovery strategies.

## When to Use
- Any MCP tool invocation
- Agent response generation
- Database operations
- API calls to external services

## Error Categories

### 1. Validation Errors
**Causes:** Missing/invalid parameters, empty fields, wrong data types

```python
def handle_validation_error(error: ValidationError) -> str:
    """Return user-friendly validation error message"""
    messages = {
        "empty_title": "The task title can't be empty. What would you like the task to say?",
        "invalid_user_id": "I couldn't identify your account. Please log in again.",
        "invalid_task_id": "That doesn't look like a valid task ID. Task IDs are numbers.",
        "missing_required": "Some required information is missing. Please provide all details."
    }
    return messages.get(error.code, f"Validation error: {error.message}")
```

### 2. Not Found Errors
**Causes:** Task doesn't exist, conversation not found, user not found

```python
def handle_not_found_error(error: NotFoundError, context: str = "") -> str:
    """Return helpful not found error with suggestions"""
    base_msg = f"I couldn't find what you're looking for."

    suggestions = {
        "task": "Would you like to see your tasks?",
        "conversation": "This conversation may have been deleted. Starting a new one...",
        "user": "Your account wasn't found. Please check if you're logged in."
    }

    suffix = suggestions.get(context, "")
    return f"{base_msg} {suffix}".strip()
```

### 3. Ownership Errors
**Causes:** User trying to access another user's resources

```python
def handle_ownership_error(error: OwnershipError) -> str:
    """Handle unauthorized access attempts"""
    return "I can't let you access that task. It belongs to another user."
```

### 4. Database Errors
**Causes:** Connection failures, transaction errors, constraint violations

```python
def handle_database_error(error: Exception) -> str:
    """Handle database-related errors"""
    error_msg = str(error).lower()

    if "connection" in error_msg or "timeout" in error_msg:
        return "I'm having trouble connecting to the database. Please try again in a moment."

    if "foreign key" in error_msg or "constraint" in error_msg:
        return "There's a data consistency issue. The technical team has been notified."

    if "duplicate" in error_msg:
        return "This item already exists. Would you like to update it instead?"

    # Generic database error
    return "Something went wrong while saving your data. Please try again."
```

### 5. API Errors (OpenAI)
**Causes:** Rate limits, quota exceeded, network issues

```python
def handle_openai_error(error: Exception) -> str:
    """Handle OpenAI API errors"""
    error_type = type(error).__name__

    if "RateLimitError" in error_type or "429" in str(error):
        return "I'm receiving too many requests right now. Please wait a moment and try again."

    if "InsufficientQuotaError" in error_type or "quota" in str(error).lower():
        return "The AI service is currently unavailable. Using basic mode instead."

    if "timeout" in str(error).lower():
        return "The AI service is taking too long to respond. Please try again."

    return "I'm having trouble with the AI service. Please try again later."
```

## Error Response Format

```python
def format_error_response(error: Exception, context: str = "") -> dict:
    """Format any error into standardized response"""
    error_type = type(error).__name__

    # Determine error category
    if hasattr(error, 'code'):
        # Custom exception (ValidationError, NotFoundError, etc.)
        if error.code.startswith("VALIDATION"):
            message = handle_validation_error(error)
        elif error.code == "NOT_FOUND":
            message = handle_not_found_error(error, context)
        elif error.code == "OWNERSHIP":
            message = handle_ownership_error(error)
        else:
            message = str(error)
    else:
        # Standard exception
        if "database" in context or "sql" in str(error).lower():
            message = handle_database_error(error)
        elif "openai" in context:
            message = handle_openai_error(error)
        else:
            message = f"An error occurred: {str(error)}"

    return {
        "success": False,
        "error": {
            "type": error_type,
            "message": message,
            "recoverable": is_recoverable(error)
        },
        "user_message": message  # User-friendly version
    }
```

## Recovery Strategies

### Retry Logic
```python
import time

def retry_on_failure(operation, max_retries=3, delay=1.0):
    """Retry operation with exponential backoff"""
    last_error = None

    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            last_error = e
            if not is_recoverable(e):
                break

            # Exponential backoff
            wait_time = delay * (2 ** attempt)
            time.sleep(wait_time)

    # All retries failed
    raise last_error
```

### Fallback to Mock Agent
```python
def run_agent_with_fallback(message, history, db_session):
    """Try real agent, fallback to mock on failure"""
    try:
        from agents.runner import AgentRunner
        agent = AgentRunner()
        return agent.run(message, history, db_session)
    except Exception as e:
        logger.warning(f"Real agent failed: {e}. Using mock agent.")
        from agents.mock_runner import MockAgentRunner
        agent = MockAgentRunner(use_tools=True)
        return agent.run(message, history, db_session)
```

### Graceful Degradation
```python
def invoke_tool_with_graceful_failure(tool_name, session, **kwargs):
    """Invoke tool with graceful failure handling"""
    try:
        result = invoke_tool(tool_name, session, **kwargs)
        return result
    except Exception as e:
        logger.error(f"Tool {tool_name} failed: {e}")

        # Return error response but don't crash
        return {
            "success": False,
            "error": {
                "code": "TOOL_ERROR",
                "message": f"I couldn't complete that operation. {get_suggestion(tool_name)}"
            },
            "tool": tool_name
        }

def get_suggestion(tool_name: str) -> str:
    """Provide helpful suggestion based on failed tool"""
    suggestions = {
        "add_task": "Would you like to try a different task title?",
        "list_tasks": "Would you like me to try showing your tasks again?",
        "complete_task": "Could you tell me which task you completed by its title or ID?"
    }
    return suggestions.get(tool_name, "Please try again.")
```

## Error Recovery Examples

### MCP Tool Error Wrapper
```python
def safe_tool_invoke(tool_name: str, session, **kwargs):
    """Wrap MCP tool invocation with error handling"""
    try:
        tool = get_tool(tool_name)
        result = tool.execute(session=session, **kwargs)

        if result.success:
            return {
                "success": True,
                "data": result.data,
                "user_message": format_success_message(tool_name, result.data)
            }
        else:
            # Tool returned business logic error
            error = result.error
            return {
                "success": False,
                "error": error,
                "user_message": format_business_error(error)
            }

    except ValidationError as e:
        return format_error_response(e, "validation")
    except NotFoundError as e:
        return format_error_response(e, "task")
    except OwnershipError as e:
        return format_error_response(e, "ownership")
    except Exception as e:
        logger.exception(f"Unexpected error in {tool_name}")
        return format_error_response(e, "database")
```

### Agent Error Handler
```python
def handle_agent_error(error: Exception, user_message: str) -> str:
    """Convert agent error to user-friendly message"""
    error_type = type(error).__name__

    if "openai" in error_type.lower() or "api" in error_type.lower():
        return f"{handle_openai_error(error)} You said: '{user_message}'. Could you rephrase that?"

    if "timeout" in str(error).lower():
        return f"I'm taking too long to respond. Let me try a simpler approach. You said: '{user_message}'"

    return f"I'm having trouble understanding that. Could you say it differently? You said: '{user_message}'"
```

## Logging Errors

```python
import logging

logger = logging.getLogger(__name__)

def log_error(error: Exception, context: dict):
    """Log error with context for debugging"""
    logger.error(
        f"Error in {context.get('operation', 'unknown')}: "
        f"{type(error).__name__}: {str(error)}",
        extra={
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "recoverable": is_recoverable(error)
        }
    )
```

## Testing Error Handling

```python
def test_error_scenarios():
    """Test various error scenarios"""
    # Test validation error
    try:
        Task(title="")  # Empty title
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        msg = handle_validation_error(e)
        assert "can't be empty" in msg

    # Test not found error
    try:
        get_task(task_id=99999)  # Non-existent task
        assert False, "Should have raised NotFoundError"
    except NotFoundError as e:
        msg = handle_not_found_error(e, "task")
        assert "couldn't find" in msg

    print("✅ All error scenarios handled correctly")
```

## Best Practices
1. Always catch specific exceptions before generic ones
2. Provide actionable error messages with suggestions
3. Log errors with context for debugging
4. Use graceful degradation for non-critical failures
5. Implement retry logic for transient errors
6. Never expose internal implementation details to users
7. Test error paths alongside happy paths
8. Use recovery strategies appropriate to error type

## Dependencies
- Custom exceptions from mcp_tools/exceptions.py
- Logging module from Python standard lib
- Exception handling from Python standard lib
