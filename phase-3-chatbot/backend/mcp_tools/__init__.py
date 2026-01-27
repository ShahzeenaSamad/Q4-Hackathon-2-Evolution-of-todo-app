"""
MCP Tools Package
Registry for all Model Context Protocol tools
"""

from .base import MCPTool, MCPToolResponse
from .exceptions import MCPToolError, ValidationError, NotFoundError, OwnershipError

# Import tool implementations
from .add_task import AddTaskTool
from .list_tasks import ListTasksTool
from .complete_task import CompleteTaskTool
from .delete_task import DeleteTaskTool
from .update_task import UpdateTaskTool

# Tool registry - maps tool names to tool instances
_tool_registry = {}


def register_tool(tool: MCPTool) -> None:
    """
    Register an MCP tool in the global registry.

    Args:
        tool: Instance of MCPTool to register
    """
    _tool_registry[tool.name] = tool


def get_tool(name: str) -> MCPTool:
    """
    Get a registered tool by name.

    Args:
        name: Tool name

    Returns:
        MCPTool instance

    Raises:
        KeyError: If tool not found
    """
    if name not in _tool_registry:
        raise KeyError(f"MCP tool '{name}' not found. Available tools: {list(_tool_registry.keys())}")
    return _tool_registry[name]


def list_tools() -> list[str]:
    """
    List all registered tool names.

    Returns:
        List of tool names
    """
    return list(_tool_registry.keys())


def get_all_tools() -> dict[str, MCPTool]:
    """
    Get all registered tools.

    Returns:
        Dictionary mapping tool names to tool instances
    """
    return _tool_registry.copy()


# Auto-register all tools on import
def _register_default_tools():
    """Register all default MCP tools"""
    register_tool(AddTaskTool())
    register_tool(ListTasksTool())
    register_tool(CompleteTaskTool())
    register_tool(DeleteTaskTool())
    register_tool(UpdateTaskTool())


# Register tools when module is imported
_register_default_tools()


# Export main classes and functions
__all__ = [
    "MCPTool",
    "MCPToolResponse",
    "MCPToolError",
    "ValidationError",
    "NotFoundError",
    "OwnershipError",
    "AddTaskTool",
    "ListTasksTool",
    "CompleteTaskTool",
    "DeleteTaskTool",
    "UpdateTaskTool",
    "register_tool",
    "get_tool",
    "list_tools",
    "get_all_tools",
]
