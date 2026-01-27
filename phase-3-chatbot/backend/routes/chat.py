"""
Chat Endpoint
POST /api/v1/chat/{user_id}
Main chat interface for AI-powered task management

Uses skills:
- Conversation Management (create/add/get conversations)
- Database Session Management (proper session handling)
- Error Handling & Recovery (graceful error responses)
- MCP Tool Invocation (via agents)
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlmodel import Session

# Database Session Management Skill
from db import get_db

# Conversation Management Skill
from services import ConversationService, HistoryBuilder

# Agents (use MCP Tool Invocation skill internally)
from agents import get_agent, AI_AGENT_TYPE, MockAgentRunner

# Error Handling Skill
from mcp_tools.exceptions import ValidationError, NotFoundError, OwnershipError


router = APIRouter(prefix="/api/v1", tags=["Chat"])
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""

    message: str = Field(..., min_length=1, max_length=5000, description="User's natural language message")
    conversation_id: Optional[str] = Field(None, description="Resume existing conversation")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""

    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "response": "I've added 'Buy milk' to your tasks (ID: 123)",
                    "conversation_id": "abc-123",
                    "tool_calls": [
                        {
                            "tool": "add_task",
                            "success": True,
                            "result": {"task_id": "123", "title": "Buy milk"}
                        }
                    ]
                },
                "error": None
            }
        }


@router.post("/chat/{user_id}", response_model=ChatResponse)
async def send_message(user_id: str, request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process a natural language message through the AI agent.

    ## Pipeline (Conversation Management Skill):
    1. Validate user authentication (user_id from path)
    2. Get or create conversation
    3. Load conversation history from database
    4. Pass to AI agent with MCP tools
    5. Store user message and assistant response
    6. Return formatted response

    ## Statelessness:
    - No server-side state between requests
    - Full conversation loaded from database each request
    - All state persisted to database immediately

    ## Tool Usage:
    - Agent automatically calls MCP tools based on intent
    - All task operations go through tools (Principle 8)
    - User sees confirmations for all actions

    ## Error Handling:
    - Validation errors return user-friendly messages
    - Database errors handled gracefully
    - Agent errors caught and formatted
    """

    try:
        logger.info(f"Chat request from user {user_id}: {request.message[:50]}...")

        # Initialize services (Conversation Management Skill)
        conversation_svc = ConversationService()
        history_builder = HistoryBuilder()

        # Get or create conversation
        conversation_id = await _get_or_create_conversation(
            conversation_svc,
            user_id,
            request.conversation_id,
            db
        )

        if not conversation_id:
            return ChatResponse(
                success=False,
                error={"code": "NOT_FOUND", "message": "Conversation not found"}
            )

        # Load conversation history (limit to last 10 for speed)
        full_history = history_builder.build_history(conversation_id, db)
        history = full_history[-10:]  # Only last 10 messages
        logger.info(f"Loaded {len(history)} messages from history (total: {len(full_history)})")

        # Store user message
        conversation_svc.add_message(conversation_id, "user", request.message, db)
        logger.info(f"Stored user message")

        # Run AI agent with MCP tools
        agent_result = await _run_agent(
            request.message,
            history,
            db,
            user_id
        )

        logger.info(f"Agent response: {agent_result['response'][:100]}...")
        logger.info(f"Tool calls: {len(agent_result['tool_calls'])}")

        # Store assistant response
        conversation_svc.add_message(
            conversation_id,
            "assistant",
            agent_result['response'],
            db
        )

        # Return formatted response
        return ChatResponse(
            success=True,
            data={
                "response": agent_result['response'],
                "conversation_id": conversation_id,
                "tool_calls": agent_result['tool_calls']
            }
        )

    except ValidationError as e:
        # Validation error (user input problem)
        logger.error(f"Validation error: {str(e)}")
        return ChatResponse(
            success=False,
            error=_format_validation_error(e)
        )
    except NotFoundError as e:
        # Resource not found
        logger.error(f"Not found error: {str(e)}")
        return ChatResponse(
            success=False,
            error=_format_not_found_error(e, "conversation")
        )
    except Exception as e:
        # Unexpected error (Error Handling Skill)
        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
        return ChatResponse(
            success=False,
            error=_format_general_error(e)
        )


async def _get_or_create_conversation(
    conversation_svc,
    user_id: str,
    conversation_id: Optional[str],
    db: Session
) -> Optional[str]:
    """
    Get existing conversation or create new one (Conversation Management Skill)

    Returns:
        Conversation ID or None if not found
    """
    if not conversation_id:
        # Create new conversation
        new_conv_id = conversation_svc.create_conversation(user_id, db)
        logger.info(f"Created new conversation {new_conv_id}")
        return new_conv_id
    else:
        # Verify conversation exists and belongs to user
        conversation = conversation_svc.get_conversation(conversation_id, user_id, db)
        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
            return None
        return conversation_id


async def _run_agent(
    message: str,
    history: List[Dict[str, str]],
    db: Session,
    user_id: str = None
) -> Dict[str, Any]:
    """
    Run AI agent with error recovery (Error Handling Skill)

    Args:
        message: User message
        history: Conversation history
        db: Database session
        user_id: User ID for task operations

    Returns:
        Agent result dictionary with response and tool_calls
    """
    try:
        # Get agent class based on AI_AGENT_TYPE configuration
        AgentClass = get_agent()
        agent_name = AI_AGENT_TYPE.upper()

        logger.info(f"Using {agent_name} Agent")

        # Instantiate agent with appropriate parameters
        if AI_AGENT_TYPE == "mock":
            agent = AgentClass(use_tools=True)
        else:
            agent = AgentClass()

        # Run agent
        result = agent.run(
            message=message,
            conversation_history=history,
            db_session=db,
            user_id=user_id
        )

        return result

    except Exception as e:
        # Fallback to mock agent if real agent fails (Error Handling Skill)
        if AI_AGENT_TYPE != "mock":
            logger.warning(f"{AI_AGENT_TYPE.upper()} agent failed: {e}. Falling back to mock agent.")
            agent = MockAgentRunner(use_tools=True)
            return agent.run(message, history, db, user_id=user_id)
        else:
            # Re-raise if already using mock agent
            raise


def _format_validation_error(error: ValidationError) -> Dict[str, str]:
    """Format validation error into user-friendly response (Error Handling Skill)"""
    messages = {
        "empty_title": "The message can't be empty.",
        "invalid_user_id": "I couldn't identify your account. Please log in again.",
    }

    user_message = messages.get(error.code, error.message)

    return {
        "code": "VALIDATION_ERROR",
        "message": user_message
    }


def _format_not_found_error(error: NotFoundError, context: str) -> Dict[str, str]:
    """Format not found error with helpful suggestion (Error Handling Skill)"""
    base_msg = f"I couldn't find what you're looking for."
    suggestion = "Would you like to start a new conversation?"

    return {
        "code": "NOT_FOUND",
        "message": f"{base_msg} {suggestion}"
    }


def _format_general_error(error: Exception) -> Dict[str, str]:
    """Format general error into user-friendly response (Error Handling Skill)"""
    error_msg = str(error).lower()

    if "database" in error_msg or "connection" in error_msg:
        message = "I'm having trouble connecting to the database. Please try again."
    elif "timeout" in error_msg:
        message = "That took too long. Please try again."
    elif "openai" in error_msg or "api" in error_msg:
        message = "The AI service is having issues. Using basic mode instead."
    else:
        message = "Something went wrong. Please try again."

    return {
        "code": "INTERNAL_ERROR",
        "message": message
    }
