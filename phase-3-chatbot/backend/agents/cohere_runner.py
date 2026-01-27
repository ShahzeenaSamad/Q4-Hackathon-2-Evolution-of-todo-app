"""
Cohere Agent Runner
Orchestrates Cohere AI agent with MCP tools
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
import cohere

from .config import COHERE_MODEL_CONFIG, COHERE_SYSTEM_PROMPT
from mcp_tools import get_all_tools, MCPToolResponse


# Setup logging
logger = logging.getLogger(__name__)


class CohereAgentRunner:
    """
    Runs Cohere AI agent with MCP tools for task management.

    This class orchestrates the interaction between Cohere and MCP tools,
    enabling natural language task management through conversation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Cohere agent runner.

        Args:
            api_key: Cohere API key (defaults to COHERE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")

        self.client = cohere.Client(self.api_key)
        self.model_config = COHERE_MODEL_CONFIG
        self.system_prompt = COHERE_SYSTEM_PROMPT
        self.tools = get_all_tools()

    def format_tools_for_cohere(self) -> List[Dict[str, Any]]:
        """
        Format MCP tools for Cohere function calling.

        Returns:
            List of tool definitions in Cohere format
        """
        cohere_tools = []

        for tool_name, tool in self.tools.items():
            # Get parameters
            params = tool.parameters.get("properties", {})
            required = tool.parameters.get("required", [])

            # Format each parameter for Cohere
            parameter_definitions = {}
            for param_name, param_def in params.items():
                parameter_definitions[param_name] = {
                    "description": param_def.get("description", ""),
                    "type": param_def.get("type", "string"),
                    "required": param_name in required
                }

            tool_def = {
                "name": tool_name,
                "description": tool.description,
                "parameter_definitions": parameter_definitions
            }
            cohere_tools.append(tool_def)

        return cohere_tools

    def run(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        db_session = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Run Cohere agent with message and conversation history.

        Args:
            message: User's message
            conversation_history: List of previous messages
            db_session: Database session to inject into tools
            user_id: User ID for task operations

        Returns:
            Dictionary with response and tool_calls
        """
        # Store user_id for use in tool calls
        self.user_id = user_id

        try:
            logger.info(f"Running Cohere agent with message: {message[:50]}...")

            # Format conversation history for Cohere
            chat_history = self._format_conversation_history(conversation_history)

            # Format tools for Cohere
            tools = self.format_tools_for_cohere()

            # Call Cohere Chat API
            response = self.client.chat(
                message=message,
                chat_history=chat_history,
                preamble=self.system_prompt,
                tools=tools if tools else None,
                model=self.model_config["model"],
                temperature=self.model_config["temperature"],
                max_tokens=self.model_config["max_tokens"]
            )

            # Process response
            if response.tool_calls:
                # Handle tool calls
                return self._handle_tool_calls(response, message, chat_history, db_session)
            else:
                # Direct text response
                return {
                    "response": response.text,
                    "tool_calls": [],
                    "raw_response": response
                }

        except Exception as e:
            logger.error(f"Cohere agent error: {type(e).__name__}: {str(e)}")
            raise

    def _format_conversation_history(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Format conversation history for Cohere API.

        Args:
            history: List of message dictionaries with 'role' and 'content'

        Returns:
            Formatted chat history for Cohere
        """
        formatted = []

        for msg in history:
            # Map roles: user -> USER, assistant -> CHATBOT
            role = "USER" if msg["role"] == "user" else "CHATBOT"
            formatted.append({
                "role": role,
                "message": msg["content"]
            })

        return formatted

    def _handle_tool_calls(
        self,
        response,
        original_message: str,
        chat_history: List[Dict[str, str]],
        db_session
    ) -> Dict[str, Any]:
        """
        Handle tool calls from Cohere response.

        Args:
            response: Cohere API response with tool_calls
            original_message: Original user message
            chat_history: Conversation history
            db_session: Database session

        Returns:
            Dictionary with response and tool_calls
        """
        tool_results = []
        tool_calls_data = []

        for tool_call in response.tool_calls:
            tool_name = tool_call.name
            parameters = tool_call.parameters

            logger.info(f"Executing tool: {tool_name} with params: {parameters}")

            # Execute MCP tool
            try:
                tool = self.tools.get(tool_name)
                if not tool:
                    tool_results.append({
                        "call": tool_call,
                        "status": "FAILED",
                        "error": f"Tool '{tool_name}' not found"
                    })
                    continue

                # Add user_id if not provided or if empty/invalid
                if "user_id" not in parameters or not parameters.get("user_id"):
                    if not self.user_id:
                        raise ValueError("user_id must be provided either in parameters or to agent.run()")
                    parameters["user_id"] = self.user_id

                # Execute tool
                result: MCPToolResponse = tool.execute(session=db_session, **parameters)

                if result.success:
                    tool_results.append({
                        "call": tool_call,
                        "status": "SUCCESS",
                        "result": result.data
                    })
                    tool_calls_data.append({
                        "tool": tool_name,
                        "success": True,
                        "result": result.data
                    })
                else:
                    tool_results.append({
                        "call": tool_call,
                        "status": "FAILED",
                        "error": result.error
                    })
                    tool_calls_data.append({
                        "tool": tool_name,
                        "success": False,
                        "error": result.error
                    })

            except Exception as e:
                logger.error(f"Tool execution error: {e}")
                tool_results.append({
                    "call": tool_call,
                    "status": "FAILED",
                    "error": str(e)
                })
                tool_calls_data.append({
                    "tool": tool_name,
                    "success": False,
                    "error": {"code": "EXCEPTION", "message": str(e)}
                })

        # Generate final response with tool results
        # Always use our natural response generator for tool calls
        # to ensure conversational, user-friendly messages
        if tool_results:
            final_response = self._generate_response_from_tools(tool_results)
        elif response.text:
            # Use Cohere's response only if no tools were called
            final_response = response.text
        else:
            final_response = "Done!"

        return {
            "response": final_response,
            "tool_calls": tool_calls_data,
            "raw_response": response
        }

    def _generate_response_from_tools(self, tool_results: List[Dict[str, Any]]) -> str:
        """
        Generate natural language response from tool results.

        Args:
            tool_results: List of tool execution results

        Returns:
            Natural language response
        """
        import random

        responses = []

        for result in tool_results:
            if result["status"] == "SUCCESS":
                tool_name = result["call"].name
                data = result["result"]

                if tool_name == "add_task":
                    # varied responses for adding tasks
                    confirmations = [
                        f"Got it! I've added '{data['title']}' to your task list.",
                        f"Done! '{data['title']}' is now on your to-do list.",
                        f"Sure thing! I've created the task '{data['title']}' for you.",
                        f"No problem! '{data['title']}' has been added to your tasks.",
                        f"Alright! Task '{data['title']}' is all set up for you."
                    ]
                    responses.append(random.choice(confirmations))

                elif tool_name == "list_tasks":
                    tasks = data.get("tasks", [])
                    if not tasks:
                        messages = [
                            "You're all caught up! No tasks on your list right now.",
                            "Your task list is empty. Would you like to add something?",
                            "Looks like you don't have any tasks yet. What would you like to accomplish?",
                            "Nothing on your to-do list at the moment."
                        ]
                        responses.append(random.choice(messages))
                    else:
                        pending = data.get("pending", 0)
                        completed = data.get("completed", 0)

                        if pending == 0:
                            responses.append(f"Great job! You've completed all {completed} task(s)! 🎉")
                        elif completed == 0:
                            task_preview = ", ".join([f"'{t['title']}'" for t in tasks[:3]])
                            more = f" and {len(tasks) - 3} more" if len(tasks) > 3 else ""
                            responses.append(f"You have {pending} task(s) to do: {task_preview}{more}.")
                        else:
                            responses.append(f"You have {pending} pending and {completed} completed task(s).")

                elif tool_name == "complete_task":
                    # Check if multiple matches or successful completion
                    if data.get("multiple_matches"):
                        responses.append(data.get("message", "Found multiple tasks. Which one should I complete?"))
                    else:
                        confirmations = [
                            f"Awesome work! '{data.get('title', 'that task')}' is marked as complete. ✓",
                            f"Good job! '{data.get('title', 'that task')}' is now done.",
                            f"Great! I've marked '{data.get('title', 'that task')}' as completed.",
                            f"Perfect! '{data.get('title', 'that task')}' has been checked off your list.",
                            f"Well done! '{data.get('title', 'that task')}' is complete."
                        ]
                        responses.append(random.choice(confirmations))

                elif tool_name == "delete_task":
                    # Check if multiple matches or successful deletion
                    if data.get("multiple_matches"):
                        responses.append(data.get("message", "Found multiple tasks. Which one should I delete?"))
                    elif data.get("deleted_count"):
                        # Multiple tasks deleted
                        count = data.get("deleted_count", 0)
                        title = data.get("titles", [""])[0] if data.get("titles") else ""
                        responses.append(f"Done! I've deleted {count} task(s) matching '{title}'.")
                    else:
                        confirmations = [
                            f"Done! I've deleted '{data.get('title', 'that task')}' from your tasks.",
                            f"Got it! '{data.get('title', 'that task')}' has been removed.",
                            f"Sure! '{data.get('title', 'that task')}' is now deleted.",
                            f"Removed! '{data.get('title', 'that task')}' is gone from your list.",
                            f"All set! '{data.get('title', 'that task')}' has been deleted."
                        ]
                        responses.append(random.choice(confirmations))

                elif tool_name == "update_task":
                    if data.get("multiple_matches"):
                        responses.append(data.get("message", "Found multiple tasks. Which one should I update?"))
                    elif data.get("updated_count"):
                        count = data.get("updated_count", 0)
                        new_title = data.get("new_title", "updated")
                        responses.append(f"Done! I've updated {count} task(s) to '{new_title}'.")
                    else:
                        old_title = data.get("old_title", "task")
                        new_title = data.get("title", "updated")
                        confirmations = [
                            f"Done! I've changed '{old_title}' to '{new_title}'.",
                            f"Got it! '{old_title}' has been updated to '{new_title}'.",
                            f"Sure! '{old_title}' is now '{new_title}'.",
                            f"Updated! Changed '{old_title}' to '{new_title}'.",
                            f"All set! '{old_title}' has been renamed to '{new_title}'."
                        ]
                        responses.append(random.choice(confirmations))

                else:
                    responses.append(f"Successfully completed {tool_name}")
            else:
                error = result.get("error", {})
                error_messages = [
                    f"Oops! {error.get('message', 'Something went wrong')}",
                    f"Sorry, I ran into an issue: {error.get('message', 'Unknown error')}",
                    f"Hmm, I couldn't do that. {error.get('message', 'Please try again')}"
                ]
                responses.append(random.choice(error_messages))

        return " ".join(responses) if responses else "Done!"
