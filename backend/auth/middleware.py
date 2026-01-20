"""
JWT Verification Middleware
"""
from fastapi import Request, HTTPException
from typing import Optional
from .jwt import verify_token


async def verify_jwt(request: Request) -> Optional[str]:
    """Extract and verify JWT token from Authorization header"""
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = auth_header.split(" ")[1]
    payload = verify_token(token, "access")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: no user_id")
    request.state.user_id = user_id
    return user_id


def require_auth(request: Request) -> str:
    """FastAPI dependency for authenticated routes"""
    user_id = request.state.user_id if hasattr(request.state, "user_id") else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id
