"""
Agent Configuration for AI-powered Todo Management
"""
from typing import Dict, Any


# =============================================================================
# OpenAI Configuration (Legacy - Not Recommended)
# =============================================================================

OPENAI_MODEL_CONFIG: Dict[str, Any] = {
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 500,
    "timeout": 30.0,
}


# =============================================================================
# Cohere Configuration (New - Default)
# =============================================================================

# Cohere Command Model Settings (Optimized for Speed)
COHERE_MODEL_CONFIG: Dict[str, Any] = {
    "model": "command-r-plus-08-2024",  # Latest stable model (Aug 2024)
    "temperature": 0.3,         # Lower temperature for faster, more consistent responses
    "max_tokens": 80,           # Much shorter responses = 2x faster
    "timeout": 15.0,            # 15 second timeout
}


# =============================================================================
# System Prompts (Shared across all AI providers)
# =============================================================================

# Agent System Prompt (Optimized for Speed - 60% shorter)
AGENT_SYSTEM_PROMPT = """Task assistant. Tools: add_task(title), list_tasks(), complete_task(title), update_task(title, new_title), delete_task(title).
Users speak English-Urdu mixed.
Actions: Add/Create→add_task, Show/List→list_tasks, Complete/Done→complete_task, Delete/Remove→delete_task, Edit/Change→update_task.
Special: "all"/"sare"→delete all matches, "ko X bana do"→update to X.
Examples: "Add workout"→add_task, "show tasks"→list_tasks, "workout complete"→complete_task, "delete workout"→delete_task
"""


# Alias for Cohere
COHERE_SYSTEM_PROMPT = AGENT_SYSTEM_PROMPT


# =============================================================================
# Agent Behavior Rules (Shared)
# =============================================================================

BEHAVIOR_RULES = {
    "clarification_over_assumption": True,
    "confirm_all_operations": True,
    "no_hallucination": True,
    "friendly_errors": True,
}
