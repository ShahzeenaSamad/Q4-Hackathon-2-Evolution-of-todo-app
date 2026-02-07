"""
Password Security Module
"""
import bcrypt


def hash_password(password: str) -> str:
    """Hash password using bcrypt (salt rounds = 10)"""
    if not password:
        raise ValueError("Password cannot be empty")
    hashed = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hashed password"""
    if not plain_password or not hashed_password:
        return False
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def validate_password_strength(password: str) -> bool:
    """
    Validate password strength:
    - Min 8 chars
    - At least one uppercase, one lowercase, one number, one special char
    """
    if len(password) < 8:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    return has_upper and has_lower and has_number and has_special


def validate_email_format(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
