"""
JWT Authentication Middleware and Utilities
"""

from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from os import getenv
from datetime import datetime, timedelta

# JWT Configuration
JWT_SECRET = getenv("JWT_SECRET", "my-super-secret-jwt-key-for-development-min-32-chars")
JWT_ALGORITHM = "HS256"

if JWT_SECRET == "my-super-secret-jwt-key-for-development-min-32-chars":
    print("WARNING: Using default JWT secret. Set JWT_SECRET in production!")


def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    """Create a JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_jwt(request: Request):
    """
    Middleware to verify JWT token and extract user_id
    Attaches user_id to request.state
    """
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = auth_header.split(" ")[1]

    try:
        # Verify token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user_id"
            )

        # Attach user_id to request state
        request.state.user_id = user_id
        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )


# Dependency for protected routes
async def get_current_user(request: Request):
    """Get current authenticated user from JWT token"""
    user_id = verify_jwt(request)
    return user_id
