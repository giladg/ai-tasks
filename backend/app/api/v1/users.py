from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserProfile, UserUpdate
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserProfile)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's full profile.

    Args:
        current_user: Current authenticated user

    Returns:
        User profile with extended information
    """
    return UserProfile.model_validate(current_user)


@router.patch("/me", response_model=UserProfile)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile.

    Args:
        user_update: Updated user data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user profile
    """
    # Update user fields
    if user_update.name is not None:
        current_user.name = user_update.name

    db.commit()
    db.refresh(current_user)

    return UserProfile.model_validate(current_user)
