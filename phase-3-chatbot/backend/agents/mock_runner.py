"""
Mock Agent Runner
Simulates OpenAI agent responses using reusable skills
"""

import re
import logging
from typing import List, Dict, Any, Optional

# Database Session Management Skill
from db import SessionLocal

# MCP Tool Invocation Skill
from mcp_tools import get_all_tools, MCPToolResponse

# Error Handling Skill
from mcp_tools.exceptions import ValidationError, NotFoundError, OwnershipError

# Setup logging
logger = logging.getLogger(__name__)


class MockAgentRunner:
    """
    Mock agent that simulates OpenAI GPT-4o responses.

    Uses skills for:
    - Intent Detection (keyword-based)
    - MCP Tool Invocation
    - Error Handling & Recovery
    - Conversation Management

    Perfect for testing without OpenAI API billing.
    """

    # Intent keywords (from Agent Intent Detection skill)
    INTENT_PATTERNS = {
        "add_task": ["add", "create", "new task", "remind me to", "need to", "i have to"],
        "list_tasks": ["what", "show", "list", "my tasks", "todo", "need to do", "pending"],
        "complete_task": ["done", "finished", "completed", "complete", "mark as done"]
    }

    def __init__(self, use_tools: bool = True):
        """
        Initialize mock agent.

        Args:
            use_tools: Whether to actually call MCP tools or just simulate
        """
        self.tools = get_all_tools()
        self.use_tools = use_tools

    def run(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        db_session = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Run mock agent with message and conversation history.

        Args:
            message: User's message
            conversation_history: List of previous messages
            db_session: Database session to inject into tools
            user_id: User ID for task operations

        Returns:
            Dictionary with response and tool_calls
        """
        # Store user_id for use in tool invocations
        self.user_id = user_id
        try:
            # Intent Detection Skill
            intent = self._detect_intent(message)

            logger.info(f"Detected intent: {intent['intent']} (confidence: {intent['confidence']})")

            # Route to appropriate handler
            if intent["intent"] == "add_task":
                return self._handle_add_task(message, intent, db_session)
            elif intent["intent"] == "list_tasks":
                return self._handle_list_tasks(db_session)
            elif intent["intent"] == "complete_task":
                return self._handle_complete_task(message, intent, db_session)
            else:
                # General conversation
                return self._handle_general_conversation(message)

        except Exception as e:
            # Error Handling Skill
            logger.error(f"Agent error: {type(e).__name__}: {str(e)}")
            return self._format_error_response(e, message)

    def _detect_intent(self, message: str) -> Dict[str, Any]:
        """
        Detect intent using keyword patterns (Intent Detection Skill)

        Returns:
            Dict with intent, confidence, and entities
        """
        message_lower = message.lower().strip()

        # Check each intent pattern
        for intent_name, keywords in self.INTENT_PATTERNS.items():
            if any(keyword in message_lower for keyword in keywords):
                result = {
                    "intent": intent_name,
                    "confidence": 0.8,
                    "entities": {}
                }

                # Extract entities based on intent
                if intent_name == "add_task":
                    result["entities"]["title"] = self._extract_task_title(message)
                elif intent_name == "complete_task":
                    result["entities"]["reference"] = self._extract_task_reference(message)

                return result

        # Default: general conversation
        return {
            "intent": "general",
            "confidence": 0.5,
            "entities": {}
        }

    def _handle_add_task(
        self,
        message: str,
        intent: Dict[str, Any],
        db_session
    ) -> Dict[str, Any]:
        """Handle add task intent using MCP Tool Invocation skill"""
        task_title = intent["entities"].get("title", "")

        # Validation (Error Handling Skill)
        if not task_title or len(task_title) < 2:
            return {
                "response": "What task would you like me to add? Please provide a task title.",
                "tool_calls": [],
                "raw_response": None
            }

        # MCP Tool Invocation
        return self._invoke_tool_safely(
            "add_task",
            db_session,
            title=task_title,
            description=None
        )

    def _handle_list_tasks(self, db_session) -> Dict[str, Any]:
        """Handle list tasks intent using MCP Tool Invocation skill"""
        # MCP Tool Invocation
        return self._invoke_tool_safely(
            "list_tasks",
            db_session
        )

    def _handle_complete_task(
        self,
        message: str,
        intent: Dict[str, Any],
        db_session
    ) -> Dict[str, Any]:
        """Handle complete task intent using MCP Tool Invocation skill"""
        task_ref = intent["entities"].get("reference", "")

        # Validation
        if not task_ref:
            return {
                "response": "Which task would you like me to mark as complete? You can tell me the task name or ID.",
                "tool_calls": [],
                "raw_response": None
            }

        # MCP Tool Invocation
        return self._invoke_tool_safely(
            "complete_task",
            db_session,
            title=task_ref
        )

    def _handle_general_conversation(self, message: str) -> Dict[str, Any]:
        """Handle general conversation"""
        return {
            "response": f"I didn't understand that. You said: '{message}'. Could you please rephrase?",
            "tool_calls": [],
            "raw_response": None
        }

    def _invoke_tool_safely(
        self,
        tool_name: str,
        db_session,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Invoke MCP tool with error handling (MCP Tool Invocation + Error Handling Skills)

        Args:
            tool_name: Name of MCP tool to invoke
            db_session: Database session
            **kwargs: Tool parameters

        Returns:
            Formatted response dictionary
        """
        if not db_session or not self.use_tools:
            # Mock response without actual tool call
            return self._format_mock_response(tool_name, **kwargs)

        tool = self.tools.get(tool_name)
        if not tool:
            return {
                "response": f"Tool '{tool_name}' not available",
                "tool_calls": [],
                "raw_response": None
            }

        try:
            # Add user_id if not provided or if empty/invalid
            if "user_id" not in kwargs or not kwargs.get("user_id"):
                if not self.user_id:
                    raise ValueError("user_id must be provided either in parameters or to agent.run()")
                kwargs["user_id"] = self.user_id

            # Invoke tool
            result: MCPToolResponse = tool.execute(session=db_session, **kwargs)

            if result.success:
                # Format success response
                return self._format_success_response(tool_name, result.data)
            else:
                # Format business logic error (user-friendly)
                return self._format_business_error(tool_name, result.error)

        except ValidationError as e:
            # Validation error (user input problem)
            return self._format_validation_error(e)
        except NotFoundError as e:
            # Not found error (resource doesn't exist)
            return self._format_not_found_error(e, tool_name.replace("_", " "))
        except OwnershipError as e:
            # Ownership error (unauthorized access)
            return {
                "response": "I can't let you access that task. It belongs to another user.",
                "tool_calls": [{"tool": tool_name, "success": False, "error": str(e)}],
                "raw_response": None
            }
        except Exception as e:
            # Unexpected error (Error Handling Skill)
            logger.error(f"Unexpected error in {tool_name}: {type(e).__name__}: {e}")
            return self._format_error_response(e, tool_name)

    def _format_success_response(self, tool_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format successful tool result into natural language"""
        if tool_name == "add_task":
            response = f"I've added '{data.get('title', 'task')}' to your tasks (ID: {data.get('task_id', 'N/A')})"
        elif tool_name == "list_tasks":
            tasks = data.get("tasks", [])
            if not tasks:
                response = "You don't have any tasks yet!"
            else:
                task_list = "\n".join([
                    f"- {t.get('title', 'task')}" + (" ✓" if t.get('completed') else "")
                    for t in tasks[:10]  # Limit to 10 tasks
                ])
                response = f"You have {data.get('total', len(tasks))} task(s):\n{task_list}"
                if data.get('total', 0) > 10:
                    response += f"\n(... and {data.get('total', 0) - 10} more)"
        elif tool_name == "complete_task":
            if data.get("multiple_matches"):
                response = data.get("message", "Found multiple tasks. Which one should I complete?")
            else:
                response = f"Marked '{data.get('title', 'task')}' as complete ✓"
        elif tool_name == "delete_task":
            if data.get("multiple_matches"):
                response = data.get("message", "Found multiple tasks. Which one should I delete?")
            elif data.get("deleted_count"):
                count = data.get("deleted_count", 0)
                response = f"Deleted {count} task(s)!"
            else:
                response = f"Deleted '{data.get('title', 'task')}' from your tasks"
        elif tool_name == "update_task":
            if data.get("multiple_matches"):
                response = data.get("message", "Found multiple tasks. Which one should I update?")
            elif data.get("updated_count"):
                count = data.get("updated_count", 0)
                new_title = data.get("new_title", "updated")
                response = f"Updated {count} task(s) to '{new_title}'!"
            else:
                old_title = data.get("old_title", "task")
                new_title = data.get("title", "updated")
                response = f"Changed '{old_title}' to '{new_title}'!"
        else:
            response = f"Done! ({tool_name})"

        return {
            "response": response,
            "tool_calls": [{
                "tool": tool_name,
                "success": True,
                "result": data
            }],
            "raw_response": None
        }

    def _format_business_error(self, tool_name: str, error: Dict[str, Any]) -> Dict[str, Any]:
        """Format business logic error (from tool)"""
        message = error.get("message", "Something went wrong")

        # Make it more user-friendly
        if "not found" in message.lower():
            message = f"I couldn't find what you're looking for. Would you like to see your tasks?"
        elif "already completed" in message.lower():
            message = f"That task is already marked as complete."
        else:
            message = f"Sorry, I couldn't do that. {message}"

        return {
            "response": message,
            "tool_calls": [{
                "tool": tool_name,
                "success": False,
                "error": error
            }],
            "raw_response": None
        }

    def _format_validation_error(self, error: ValidationError) -> Dict[str, Any]:
        """Format validation error"""
        messages = {
            "empty_title": "The task title can't be empty. What would you like the task to say?",
            "invalid_user_id": "I couldn't identify your account.",
        }

        user_message = messages.get(error.code, error.message)

        return {
            "response": user_message,
            "tool_calls": [],
            "raw_response": None
        }

    def _format_not_found_error(self, error: NotFoundError, context: str) -> Dict[str, Any]:
        """Format not found error with helpful suggestion"""
        base_msg = f"I couldn't find that {context}."
        suggestion = "Would you like to see your tasks?"

        return {
            "response": f"{base_msg} {suggestion}",
            "tool_calls": [],
            "raw_response": None
        }

    def _format_error_response(self, error: Exception, context: str) -> Dict[str, Any]:
        """Format general error (Error Handling Skill)"""
        error_msg = str(error).lower()

        if "database" in error_msg or "connection" in error_msg:
            message = "I'm having trouble connecting to the database. Please try again."
        elif "timeout" in error_msg:
            message = "That took too long. Please try again."
        else:
            message = f"Something went wrong. Please try again."

        return {
            "response": message,
            "tool_calls": [],
            "raw_response": None
        }

    def _format_mock_response(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Format mock response when not using actual tools"""
        if tool_name == "add_task":
            title = kwargs.get("title", "new task")
            response = f"[MOCK] I've added '{title}' to your tasks"
            data = {"task_id": "mock-123", "title": title, "completed": False}
        elif tool_name == "list_tasks":
            response = "[MOCK] You have 0 tasks"
            data = {"tasks": [], "total": 0, "pending": 0, "completed": 0}
        elif tool_name == "complete_task":
            title = kwargs.get("title", "task")
            response = f"[MOCK] Marked '{title}' as complete"
            data = {"title": title, "completed": True}
        else:
            response = f"[MOCK] {tool_name} completed"
            data = {}

        return {
            "response": response,
            "tool_calls": [{
                "tool": tool_name,
                "success": True,
                "result": data
            }],
            "raw_response": None
        }

    def _extract_task_title(self, message: str) -> str:
        """
        Extract task title from message (Entity Extraction - Intent Detection Skill)

        Patterns:
        - "Add buy milk" -> "buy milk"
        - "Remind me to call mom" -> "call mom"
        - "I need to buy groceries" -> "buy groceries"
        """
        message_lower = message.lower()

        # Remove trigger words
        triggers = ["add ", "create ", "new task: ", "remind me to ", "i need to ", "i have to "]
        for trigger in triggers:
            if trigger in message_lower:
                parts = message_lower.split(trigger)
                if len(parts) > 1:
                    title = parts[1].strip().capitalize()
                    return title if len(title) > 1 else ""

        # Fallback: return everything after first word
        words = message.split()
        if len(words) > 1:
            return " ".join(words[1:]).capitalize()

        return ""

    def _extract_task_reference(self, message: str) -> str:
        """
        Extract task reference from message (Entity Extraction - Intent Detection Skill)

        Patterns:
        - "Complete buy milk" -> "buy milk"
        - "I finished buying milk" -> "buying milk"
        - "Done with groceries" -> "groceries"
        """
        message_lower = message.lower()

        # Remove trigger words
        triggers = ["done with ", "finished ", "completed ", "complete ", "mark as done "]
        for trigger in triggers:
            if trigger in message_lower:
                parts = message_lower.split(trigger)
                if len(parts) > 1:
                    ref = parts[1].strip().capitalize()
                    return ref if len(ref) > 1 else ""

        # Fallback: return last word
        words = message.split()
        if words:
            return words[-1].capitalize()

        return ""
