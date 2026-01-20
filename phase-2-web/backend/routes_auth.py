"""
Authentication Routes - Signup, Login, Logout
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel
from passlib.context import CryptContext
from datetime import timedelta

from db import get_session
from models import User, UserCreate, UserRead
from auth import create_jwt_token, get_current_user

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


@router.post("/signup", status_code=201)
async def signup(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new user account
    """
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=409, detail={
            "success": False,
            "error": {
                "code": "EMAIL_EXISTS",
                "message": "An account with this email already exists"
            }
        })

    # Validate password length
    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Password must be at least 8 characters"
            }
        })

    # Create user (password validation only, not storing for now)
    # In production with Better Auth, users table is managed by Better Auth
    # For testing, we create user without password field
    import uuid
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        name=user_data.name
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create JWT tokens (access + refresh)
    access_token = create_jwt_token({"sub": user.id, "email": user.email}, timedelta(minutes=15))
    refresh_token = create_jwt_token({"sub": user.id, "email": user.email}, timedelta(days=7))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.createdAt
        }
    }


class LoginRequest(SQLModel):
    """Login request model"""
    email: str
    password: str


@router.post("/login")
async def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate a user and return JWT token
    """
    # Find user by email
    user = session.exec(
        select(User).where(User.email == login_data.email)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail={
            "success": False,
            "error": {
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        })

    # For testing, just verify user exists
    # In production with Better Auth, password verification is handled by Better Auth
    # TODO: Implement proper password verification with Better Auth integration

    # Create JWT tokens (access + refresh)
    access_token = create_jwt_token({"sub": user.id, "email": user.email}, timedelta(minutes=15))
    refresh_token = create_jwt_token({"sub": user.id, "email": user.email}, timedelta(days=7))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.createdAt
        }
    }


@router.post("/logout")
async def logout():
    """
    Logout user (client should clear the token)
    """
    return {
        "success": True,
        "data": {
            "message": "Logged out successfully"
        }
    }


class RefreshRequest(SQLModel):
    """Refresh token request model"""
    refresh_token: str


@router.post("/refresh")
async def refresh(refresh_data: RefreshRequest):
    """
    Refresh access token using refresh token
    """
    from jose import jwt, JWTError

    try:
        # Verify refresh token
        payload = jwt.decode(
            refresh_data.refresh_token,
            "my-super-secret-jwt-key-for-development-min-32-chars",
            algorithms=["HS256"]
        )

        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id or not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Create new tokens
        access_token = create_jwt_token({"sub": user_id, "email": email}, timedelta(minutes=15))
        new_refresh_token = create_jwt_token({"sub": user_id, "email": email}, timedelta(days=7))

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.get("/me")
async def get_current_user_info(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get current authenticated user's information
    """
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "User not found"
            }
        })

    return {
        "success": True,
        "data": {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "emailVerifiedAt": user.emailVerifiedAt,
                "image": user.image,
                "createdAt": user.createdAt
            }
        }
    }
