from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.utils.security import decode_access_token

# HTTP Bearer token security scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token.

    Args:
        credentials: HTTP Authorization credentials (Bearer token)
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Extract token
    token = credentials.credentials

    # Decode JWT
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user ID from payload
    user_id: Optional[int] = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to get current user if authenticated, otherwise None.
    Useful for endpoints that work with or without authentication.

    Args:
        credentials: Optional HTTP Authorization credentials
        db: Database session

    Returns:
        User object or None
    """
    if credentials is None:
        return None

    try:
        # Extract token
        token = credentials.credentials

        # Decode JWT
        payload = decode_access_token(token)

        if payload is None:
            return None

        # Get user ID from payload
        user_id: Optional[int] = payload.get("sub")

        if user_id is None:
            return None

        # Get user from database
        user = db.query(User).filter(User.id == int(user_id)).first()

        if user is None or not user.is_active:
            return None

        return user

    except Exception:
        return None


def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to verify current user is an admin.
    Use this for admin-only endpoints.

    Args:
        current_user: Current authenticated user

    Returns:
        User object (if admin)

    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user
