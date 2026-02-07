# Agent Intent Detection Skill

## Description
Reusable skill for detecting user intents from natural language messages. Supports both keyword-based (mock) and AI-based (OpenAI) intent detection.

## When to Use
- Agent needs to understand what user wants to do
- Routing user messages to appropriate MCP tools
- Building conversational agents
- Testing intent detection logic

## Capabilities

### 1. Keyword-Based Intent Detection
```python
def detect_intent_keywords(message: str) -> dict:
    """Detect intent using keyword patterns (fast, no API needed)"""
    message_lower = message.lower().strip()

    # Add task intents
    if any(keyword in message_lower for keyword in
           ["add", "create", "new task", "remind me to", "need to"]):
        return {
            "intent": "add_task",
            "confidence": 0.8,
            "entities": extract_task_title(message)
        }

    # List task intents
    elif any(keyword in message_lower for keyword in
             ["what are my tasks", "list", "show tasks", "what do i need", "my todo"]):
        return {
            "intent": "list_tasks",
            "confidence": 0.9
        }

    # Complete task intents
    elif any(keyword in message_lower for keyword in
             ["done", "finished", "completed", "marked off"]):
        return {
            "intent": "complete_task",
            "confidence": 0.8,
            "entities": extract_task_reference(message)
        }

    # Default: general conversation
    else:
        return {
            "intent": "general",
            "confidence": 0.5
        }
```

### 2. AI-Based Intent Detection (GPT-4o)
```python
from openai import OpenAI

def detect_intent_ai(message: str, client: OpenAI) -> dict:
    """Detect intent using OpenAI GPT-4o (more accurate)"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a task management intent detector.
                Classify user messages into intents: add_task, list_tasks, complete_task, update_task, delete_task, general.
                Return JSON with intent and confidence score."""
            },
            {"role": "user", "content": message}
        ],
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)
```

### 3. Entity Extraction
```python
def extract_task_title(message: str) -> dict:
    """Extract task title from message"""
    # Remove common task creation phrases
    phrases = ["add", "create", "new task", "remind me to", "need to", "i need to"]
    title = message.lower()

    for phrase in phrases:
        if phrase in title:
            title = title.replace(phrase, "").strip()
            break

    return {"title": title.capitalize()}

def extract_task_reference(message: str) -> dict:
    """Extract task reference (ID or title) from message"""
    # Look for task ID (number)
    import re
    numbers = re.findall(r'\b\d+\b', message)
    if numbers:
        return {"task_id": numbers[0]}

    # Otherwise extract title
    return {"title": message.strip()}
```

## Intent Categories

### add_task
**Triggers:**
- "add buy milk"
- "create task for groceries"
- "remind me to call mom"
- "need to finish report"

**Entities:**
- title: task name (required)
- description: optional details

### list_tasks
**Triggers:**
- "what are my tasks"
- "show me my todo list"
- "what do I need to do"
- "list all pending tasks"

**Entities:**
- completed: filter by status (optional)
- limit: max tasks to show (optional)

### complete_task
**Triggers:**
- "I finished buying milk"
- "done with the report"
- "completed task 123"
- "marked off groceries"

**Entities:**
- task_id: exact task ID (optional)
- title: task title to match (optional)

### update_task
**Triggers:**
- "change task title"
- "update task 123"
- "modify buy milk task"

**Entities:**
- task_id: task to update (required)
- new_title: updated title (optional)
- new_description: updated description (optional)

### delete_task
**Triggers:**
- "delete task 123"
- "remove buy milk"
- "get rid of that task"

**Entities:**
- task_id: task to delete (required)

### general
**Triggers:**
- Greetings ("hello", "hi")
- Questions ("how does this work")
- Small talk

**Action:** Respond conversationally

## Intent-to-Tool Mapping

```python
INTENT_TO_TOOL = {
    "add_task": "add_task",
    "list_tasks": "list_tasks",
    "complete_task": "complete_task",
    "update_task": "update_task",  # Not implemented yet
    "delete_task": "delete_task"   # Not implemented yet
}

def route_to_tool(intent: dict, db_session):
    """Route detected intent to appropriate MCP tool"""
    tool_name = INTENT_TO_TOOL.get(intent["intent"])

    if not tool_name:
        return None

    from mcp_tools import get_all_tools
    tools = get_all_tools()

    if tool_name in tools:
        tool = tools[tool_name]

        # Merge entities with required parameters
        params = {"user_id": "current_user_id"}
        params.update(intent.get("entities", {}))

        return tool.execute(session=db_session, **params)

    return None
```

## Mock Agent Implementation

```python
class MockAgentRunner:
    def __init__(self, use_tools: bool = True):
        self.use_tools = use_tools

    def run(self, message: str, conversation_history: list, db_session):
        # Detect intent
        intent = detect_intent_keywords(message)

        # Route to tool
        if self.use_tools and intent["intent"] != "general":
            result = route_to_tool(intent, db_session)

            if result and result.success:
                return {
                    "response": self.format_success_response(intent, result.data),
                    "tool_calls": [{"tool": intent["intent"], "status": "success"}]
                }

        # Fallback to general response
        return {
            "response": self.format_general_response(message),
            "tool_calls": []
        }

    def format_success_response(self, intent: dict, data: dict):
        """Format successful tool result into natural language"""
        if intent["intent"] == "add_task":
            return f"I've added '{data['title']}' to your tasks (ID: {data['task_id']})"
        elif intent["intent"] == "list_tasks":
            return f"You have {data['total']} tasks: {', '.join([t['title'] for t in data['tasks']])}"
        elif intent["intent"] == "complete_task":
            return f"Marked '{data['title']}' as complete ✓"
        return "Done!"

    def format_general_response(self, message: str):
        """Format general conversational response"""
        return f"I understand you said: '{message}'. How can I help with your tasks?"
```

## Testing

### Test Intent Detection
```python
def test_intent_detection():
    test_cases = [
        ("Add buy milk", "add_task"),
        ("What are my tasks?", "list_tasks"),
        ("I finished buying milk", "complete_task"),
        ("Hello there", "general")
    ]

    for message, expected_intent in test_cases:
        detected = detect_intent_keywords(message)
        assert detected["intent"] == expected_intent
        print(f"✅ '{message}' -> {detected['intent']}")
```

## Best Practices
1. Use keyword detection for simple cases (fast, free)
2. Use AI detection for complex/ambiguous cases (accurate, costs)
3. Provide confidence scores for all intents
4. Extract entities with intents when possible
5. Handle general conversation gracefully
6. Test with diverse phrasing patterns

## Dependencies
- OpenAI client (for AI-based detection)
- Regular expressions (for entity extraction)
- MCP tools (for routing)
