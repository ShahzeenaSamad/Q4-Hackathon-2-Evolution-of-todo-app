"""
Base MCP Tool Class
Defines the standard interface for all MCP tools
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class MCPToolResponse(BaseModel):
    """Standardized response format for all MCP tools"""

    success: bool
    data: Any = None
    error: Dict[str, str] = None  # {code: str, message: str}

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"task_id": "abc-123", "title": "Buy milk"},
                "error": None
            }
        }


class MCPTool(ABC):
    """Base class for all MCP tools"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name (e.g., 'add_task')"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for the AI agent"""
        pass

    @property
    def parameters(self) -> Dict[str, Any]:
        """Tool parameter schema (optional, defaults to empty)"""
        return {}

    @abstractmethod
    def execute(self, **kwargs) -> MCPToolResponse:
        """Execute the tool with given parameters"""
        pass
