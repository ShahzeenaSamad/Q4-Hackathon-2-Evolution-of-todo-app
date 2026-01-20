"""
User Service - User CRUD operations
"""
from sqlmodel import Session
from models.user import User


def get_user_by_email(email: str, session: Session) -> User | None:
    """Get user by email"""
    return session.query(User).filter(User.email == email).first()


def create_user(email: str, password: str, name: str = None, session: Session = None) -> User:
    """Create new user with password hashing"""
    import uuid
    from auth.security import (
        hash_password, validate_password_strength,
        validate_email_format
    )

    # Validate email
    if not validate_email_format(email):
        raise ValueError("Invalid email format")

    # Check existing user
    if get_user_by_email(email, session):
        raise ValueError(f"Email {email} already exists")

    # Validate password
    if not validate_password_strength(password):
        raise ValueError("Password must be at least 8 characters with uppercase, lowercase, number, and special character")

    # Hash password
    password_hash = hash_password(password)

    # Generate user ID
    user_id = str(uuid.uuid4())

    user = User(id=user_id, email=email, password_hash=password_hash, name=name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def verify_credentials(email: str, password: str, session: Session) -> User | None:
    """Verify login credentials"""
    user = get_user_by_email(email, session)
    if not user:
        return None

    from auth.security import verify_password
    if not verify_password(password, user.password_hash):
        return None

    return user
