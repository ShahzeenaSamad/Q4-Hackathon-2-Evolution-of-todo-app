"""
MCP Tool Exception Classes
Custom exceptions for MCP tool operations
"""


class MCPToolError(Exception):
    """Base exception for MCP tool errors"""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class ValidationError(MCPToolError):
    """Raised when input validation fails"""

    def __init__(self, message: str):
        super().__init__("VALIDATION_ERROR", message)


class NotFoundError(MCPToolError):
    """Raised when a resource is not found"""

    def __init__(self, message: str):
        super().__init__("NOT_FOUND", message)


class OwnershipError(MCPToolError):
    """Raised when user doesn't own the resource"""

    def __init__(self, message: str):
        super().__init__("OWNERSHIP_ERROR", message)
