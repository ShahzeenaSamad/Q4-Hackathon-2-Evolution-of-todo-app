"""
Agent Runner
Orchestrates OpenAI agent with MCP tools
"""

import os
from openai import OpenAI
from typing import List, Dict, Any, Optional
from .config import OPENAI_MODEL_CONFIG, AGENT_SYSTEM_PROMPT
from mcp_tools import get_all_tools, MCPToolResponse


class AgentRunner:
    """
    Runs OpenAI agent with MCP tools for task management.

    This class orchestrates the interaction between GPT-4o and MCP tools,
    enabling natural language task management through conversation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize agent runner.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=self.api_key)
        self.model_config = OPENAI_MODEL_CONFIG
        self.system_prompt = AGENT_SYSTEM_PROMPT
        self.tools = get_all_tools()

    def format_tools_for_openai(self) -> List[Dict[str, Any]]:
        """
        Format MCP tools for OpenAI function calling.

        Returns:
            List of tool definitions in OpenAI format
        """
        openai_tools = []

        for tool_name, tool in self.tools.items():
            tool_def = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            openai_tools.append(tool_def)

        return openai_tools

    def run(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        db_session = None
    ) -> Dict[str, Any]:
        """
        Run agent with message and conversation history.

        Args:
            message: User's message
            conversation_history: List of previous messages (role, content)
            db_session: Database session to inject into tools

        Returns:
            Dictionary with:
                - response: Agent's text response
                - tool_calls: List of tool executions
                - raw_response: Full OpenAI response
        """
        # Build messages array
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        # Add conversation history
        messages.extend(conversation_history)

        # Add current message
        messages.append({"role": "user", "content": message})

        # Get tools for function calling
        tools = self.format_tools_for_openai()

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model_config["model"],
            messages=messages,
            tools=tools if tools else None,
            tool_choice="auto" if tools else None,
            temperature=self.model_config.get("temperature", 0.7),
            max_tokens=self.model_config.get("max_tokens", 500),
        )

        # Extract response
        assistant_message = response.choices[0].message

        # Process tool calls if any
        tool_calls = []
        if assistant_message.tool_calls:
            tool_calls = self._execute_tool_calls(assistant_message.tool_calls, db_session)

        # Get text response
        text_response = assistant_message.content or ""

        return {
            "response": text_response,
            "tool_calls": tool_calls,
            "raw_response": assistant_message
        }

    def _execute_tool_calls(self, tool_calls, db_session) -> List[Dict[str, Any]]:
        """
        Execute tool calls from OpenAI response.

        Args:
            tool_calls: OpenAI tool_calls objects
            db_session: Database session to inject

        Returns:
            List of executed tool results
        """
        results = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = eval(tool_call.function.arguments)  # Parse JSON args

            try:
                # Get tool and execute with session injection
                tool = get_all_tools()[function_name]

                # Inject session into tool execution
                if db_session is not None:
                    result: MCPToolResponse = tool.execute(session=db_session, **function_args)
                else:
                    result: MCPToolResponse = tool.execute(**function_args)

                results.append({
                    "tool": function_name,
                    "success": result.success,
                    "result": result.data if result.success else result.error,
                    "tool_call_id": tool_call.id
                })

            except Exception as e:
                results.append({
                    "tool": function_name,
                    "success": False,
                    "result": {"code": "EXECUTION_ERROR", "message": str(e)},
                    "tool_call_id": tool_call.id
                })

        return results
