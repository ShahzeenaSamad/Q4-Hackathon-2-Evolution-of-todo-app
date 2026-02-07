"""
User Service - User CRUD operations
"""
from sqlmodel import Session
from models.user import User
import logging

logger = logging.getLogger(__name__)


def get_user_by_email(email: str, session: Session) -> User | None:
    """Get user by email"""
    try:
        return session.query(User).filter(User.email == email).first()
    except Exception as e:
        logger.error(f"Error fetching user by email {email}: {str(e)}")
        raise


def create_user(email: str, password: str, name: str = None, session: Session = None) -> User:
    """Create new user with password hashing"""
    import uuid
    from auth.security import (
        hash_password, validate_password_strength,
        validate_email_format
    )

    try:
        # Validate email
        if not validate_email_format(email):
            raise ValueError("Invalid email format")

        # Check existing user
        existing_user = get_user_by_email(email, session)
        if existing_user:
            logger.warning(f"Attempt to create duplicate user: {email}")
            raise ValueError(f"Email {email} already exists")

        # Validate password
        if not validate_password_strength(password):
            raise ValueError("Password must be at least 8 characters with uppercase, lowercase, number, and special character")

        # Hash password
        logger.info(f"Creating user: {email}")
        password_hash = hash_password(password)

        # Generate user ID
        user_id = str(uuid.uuid4())

        user = User(id=user_id, email=email, password_hash=password_hash, name=name)
        session.add(user)
        session.commit()
        session.refresh(user)

        logger.info(f"User created successfully: {email} (ID: {user_id})")
        return user

    except ValueError:
        # Re-raise validation errors as-is
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        error_msg = str(e).lower()
        logger.error(f"Failed to create user {email}: {str(e)}", exc_info=True)

        # Handle database-specific errors
        if "unique constraint" in error_msg or "duplicate key" in error_msg:
            raise ValueError(f"Email {email} already exists")
        elif "connection" in error_msg or "timeout" in error_msg:
            raise ValueError("Database connection error. Please try again.")
        else:
            raise ValueError(f"Failed to create account: {str(e)}")


def verify_credentials(email: str, password: str, session: Session) -> User | None:
    """Verify login credentials"""
    user = get_user_by_email(email, session)
    if not user:
        return None

    from auth.security import verify_password
    if not verify_password(password, user.password_hash):
        return None

    return user
