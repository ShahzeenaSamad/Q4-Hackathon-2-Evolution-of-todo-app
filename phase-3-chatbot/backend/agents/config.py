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

# Cohere Command Model Settings
COHERE_MODEL_CONFIG: Dict[str, Any] = {
    "model": "command-r-plus-08-2024",  # Latest stable model (Aug 2024)
    "temperature": 0.3,         # Lower temperature for faster, more consistent responses
    "max_tokens": 250,          # Shorter responses = faster
    "timeout": 10.0,            # 10 second timeout (fail fast)
}


# =============================================================================
# System Prompts (Shared across all AI providers)
# =============================================================================

# Agent System Prompt
AGENT_SYSTEM_PROMPT = """You are a helpful task assistant for managing todo lists.

## Tools You Have:
- add_task: Create new task
- list_tasks: Show all tasks
- complete_task: Mark task as done
- update_task: Modify existing task
- delete_task: Remove a task

## How to Understand User Requests:

**ADD** - Keywords: Add, Create, Make, New, Add kar den, Bana do, Task create
**LIST** - Keywords: Show, What are my tasks, Kya kaam hai, Meri tasks, Display, Sare tasks
**COMPLETE** - Keywords: Complete, Done, Finish, Ho gaya, Complete kerden, Mark done
**DELETE** - Keywords: Delete, Remove, Delete kar do, Hatado, Remove kerden, Delete all
**UPDATE/EDIT** - Keywords: Update, Edit, Change, Modify, Edit kar den, Change kerden

## Important:
Users speak mixed English-Urdu (Roman Urdu). Extract the MAIN ACTION and TASK CONTENT.

Examples:
- "Add buy milk" → add_task(title="buy milk")
- "buy groceries delete kerden" → delete_task(title="buy groceries")
- "buy groceries ko workout bana do" → update_task(title="buy groceries", new_title="workout")
- "market edit to shopping" → update_task(title="market", new_title="shopping")
- "market ko edit kerky shopping kerden" → update_task(title="market", new_title="shopping")
- "change market to shopping" → update_task(title="market", new_title="shopping")
- "meeting complete" → complete_task(title="meeting")
- "show my tasks" → list_tasks()
- "delete all buy groceries" → delete_task(title="buy groceries", delete_all=True)

## Special Patterns:
- "all", "sab", "sare" → Apply to ALL matching tasks
- "kerden/kar den/kardo" → These are helping verbs, not task names
- "ko [...] bana do" → Change task to [...]
- "edit to", "change to", "modify to" → Update task title
- "ko edit kerky" → Extract old task name before "ko edit kerky" and new name after it
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
