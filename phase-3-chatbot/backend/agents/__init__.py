"""
Agents Package
Multi-provider AI agent configuration and execution for Phase 3
Supports: Mock, Cohere, OpenAI
"""

import os
from .config import (
    OPENAI_MODEL_CONFIG,
    COHERE_MODEL_CONFIG,
    AGENT_SYSTEM_PROMPT,
    COHERE_SYSTEM_PROMPT,
    BEHAVIOR_RULES
)
from .runner import AgentRunner
from .mock_runner import MockAgentRunner
from .cohere_runner import CohereAgentRunner

# =============================================================================
# Agent Selection Configuration
# =============================================================================

# Get agent type from environment variable
# Options: 'mock', 'cohere', 'openai'
AI_AGENT_TYPE = os.getenv("AI_AGENT_TYPE", "mock").lower()

# Legacy support for USE_MOCK_AGENT
USE_MOCK_AGENT_LEGACY = os.getenv("USE_MOCK_AGENT", "true").lower() == "true"

# If legacy variable is set and AI_AGENT_TYPE is not explicitly set
if AI_AGENT_TYPE == "mock" and not USE_MOCK_AGENT_LEGACY:
    AI_AGENT_TYPE = "cohere"  # Default to Cohere if USE_MOCK_AGENT is false


def get_agent():
    """
    Get the appropriate agent instance based on AI_AGENT_TYPE.

    Returns:
        Agent instance (MockAgentRunner, CohereAgentRunner, or AgentRunner)
    """
    if AI_AGENT_TYPE == "mock":
        return MockAgentRunner
    elif AI_AGENT_TYPE == "cohere":
        return CohereAgentRunner
    elif AI_AGENT_TYPE == "openai":
        return AgentRunner
    else:
        # Default to mock for safety
        print(f"Warning: Unknown AI_AGENT_TYPE '{AI_AGENT_TYPE}'. Defaulting to mock agent.")
        return MockAgentRunner


# Legacy compatibility
USE_MOCK_AGENT = (AI_AGENT_TYPE == "mock")


__all__ = [
    # Agent classes
    "AgentRunner",
    "MockAgentRunner",
    "CohereAgentRunner",
    "get_agent",

    # Configuration
    "USE_MOCK_AGENT",
    "USE_MOCK_AGENT_LEGACY",
    "AI_AGENT_TYPE",

    # Model configs
    "OPENAI_MODEL_CONFIG",
    "COHERE_MODEL_CONFIG",

    # Prompts
    "AGENT_SYSTEM_PROMPT",
    "COHERE_SYSTEM_PROMPT",

    # Behavior rules
    "BEHAVIOR_RULES",
]
