"""
Authentication Routes - Signup, Login, Refresh, Logout
"""
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from sqlmodel import Session
from typing import Optional

from models.user import User
from services.user_service import (
    get_user_by_email, create_user, verify_credentials
)
from auth.security import validate_email_format
from auth.rate_limiter import _rate_limiter
from auth.jwt import (
    create_access_token, create_refresh_token, verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
)

from schemas.auth import SignupRequest, LoginRequest, AuthResponse, UserResponse

from db import get_db


router = APIRouter()


@router.post("/signup")
def signup(http_request: Request, request: SignupRequest, db: Session = Depends(get_db)):
    """
    User Registration Endpoint

    Creates a new user account with email/password.
    Issues JWT tokens (access + refresh) on success.

    Validation Rules (from FR-002, FR-003):
    - Email must be valid format
    - Password must be 8+ characters with uppercase, lowercase, number, special char
    - Email must be unique
    """
    # Check rate limit
    client_ip = http_request.client.host
    if _rate_limiter.is_rate_limited(client_ip):
        return AuthResponse(
            success=False,
            error={"code": "RATE_LIMITED", "message": "Too many attempts. Please try again later."}
        )

    # Create user (service handles validation)
    try:
        user = create_user(
            email=request.email,
            password=request.password,
            name=request.name,
            session=db
        )
    except ValueError as e:
        return AuthResponse(
            success=False,
            error={"code": "VALIDATION_ERROR", "message": str(e)}
        )

    # Generate tokens
    access_token = create_access_token(user.id, user.email)
    refresh_token = create_refresh_token(user.id)

    # Return user + tokens
    return AuthResponse(
        success=True,
        data={
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at.isoformat()
            },
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": f"{ACCESS_TOKEN_EXPIRE_MINUTES}m"
            }
        }
    )


@router.post("/login")
def login(http_request: Request, request: LoginRequest, db: Session = Depends(get_db)):
    """
    User Login Endpoint

    Authenticates user credentials and issues JWT tokens.

    Rate Limiting: 5 failed attempts per 15 min per IP
    """
    # Check rate limit
    client_ip = http_request.client.host
    if _rate_limiter.is_rate_limited(client_ip):
        return AuthResponse(
            success=False,
            error={"code": "RATE_LIMITED", "message": "Too many failed attempts. Please try again later."}
        )

    # Verify credentials
    user = verify_credentials(request.email, request.password, db)

    if not user:
        return AuthResponse(
            success=False,
            error={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}
        )

    # Reset rate limit on successful login
    _rate_limiter.reset_attempts(client_ip)

    # Generate tokens
    access_token = create_access_token(user.id, user.email)
    refresh_token = create_refresh_token(user.id)

    return {
        "success": True,
        "data": {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at.isoformat()
            },
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": f"{ACCESS_TOKEN_EXPIRE_MINUTES}m"
            }
        },
        "error": None
    }


@router.post("/refresh")
def refresh_token(request: Request):
    """
    Token Refresh Endpoint

    Validates refresh token and issues new access token.
    """
    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return AuthResponse(
            success=False,
            error={"code": "MISSING_TOKEN", "message": "Refresh token required"}
        )

    refresh_token = auth_header.split(" ")[1]

    # Verify refresh token
    try:
        payload = verify_token(refresh_token, "refresh")
    except HTTPException:
        return AuthResponse(
            success=False,
            error={"code": "INVALID_REFRESH_TOKEN", "message": "Invalid or expired refresh token"}
        )

    user_id = payload.get("sub")
    email = payload.get("email")

    # Get database session
    session = request.state.session if hasattr(request.state, 'session') else None

    # Verify user still exists
    user = session.get(User, user_id)
    if not user:
        return AuthResponse(
            success=False,
            error={"code": "USER_NOT_FOUND", "message": "User not found"}
        )

    # Issue new access token
    new_access_token = create_access_token(user_id, email)

    return AuthResponse(
        success=True,
        data={
            "tokens": {
                "access_token": new_access_token,
                "token_type": "Bearer",
                "expires_in": f"{ACCESS_TOKEN_EXPIRE_MINUTES}m"
            }
        }
    )


@router.post("/logout")
def logout(request: Request):
    """
    Logout Endpoint

    In production, this would invalidate the refresh token.
    For now, we just return success to indicate logout completed.
    """
    # In production: Invalidate refresh token from token store/database

    # For MVP, just return success
    return AuthResponse(
        success=True,
        data={"message": "Logout successful"}
    )


@router.get("/debug-user")
def debug_user(db: Session = Depends(get_db)):
    """Debug endpoint to check user object"""
    from services.user_service import get_user_by_email

    user = get_user_by_email("testuser@example.com", db)

    # Return all user attributes
    return {
        "user_id": user.id,
        "user_email": user.email,
        "user_name": user.name,
        "user_dict": user.__dict__,
        "id_equals_email": user.id == user.email,
        "type_id": str(type(user.id)),
        "type_email": str(type(user.email))
    }
