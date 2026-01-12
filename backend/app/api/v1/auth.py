from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import urllib.parse

from app.database import get_db
from app.schemas.auth import TokenResponse, GoogleAuthURL, LogoutResponse
from app.schemas.user import User as UserSchema
from app.services.auth_service import auth_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth")


@router.get("/google/login", response_model=GoogleAuthURL)
async def google_login():
    """
    Initiate Google OAuth flow.
    Returns authorization URL to redirect user to Google consent screen.
    """
    authorization_url, state = auth_service.get_authorization_url()

    return GoogleAuthURL(authorization_url=authorization_url)


@router.get("/google/callback")
async def google_callback(
    code: str = Query(..., description="Authorization code from Google"),
    state: str = Query(..., description="State parameter for CSRF protection"),
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback.
    Exchanges authorization code for tokens, creates/updates user, and redirects to frontend.

    Args:
        code: Authorization code from Google
        state: State parameter for CSRF protection
        db: Database session

    Returns:
        Redirect to frontend with JWT token
    """
    try:
        # Exchange code for tokens
        tokens = auth_service.exchange_code_for_tokens(code, state)

        # Get user info from Google
        user_info = auth_service.get_user_info(tokens['access_token'])

        # Create or update user in database
        user = auth_service.create_or_update_user(db, user_info, tokens)

        # Create JWT token for session
        jwt_token = auth_service.create_jwt_token(user)

        # Redirect to frontend with token and user data
        frontend_url = f"http://localhost:5173/auth/callback"
        redirect_url = f"{frontend_url}?token={jwt_token}"

        return RedirectResponse(url=redirect_url)

    except Exception as e:
        # Redirect to frontend with error
        error_message = urllib.parse.quote(str(e))
        return RedirectResponse(
            url=f"http://localhost:5173/login?error={error_message}"
        )


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.

    Args:
        current_user: Current user from JWT token

    Returns:
        User information
    """
    return UserSchema.model_validate(current_user)


@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user.
    Note: Since we're using JWT, actual logout happens on the client side
    by removing the token. This endpoint is mainly for completeness.

    Args:
        current_user: Current user from JWT token

    Returns:
        Logout confirmation message
    """
    return LogoutResponse(message="Logged out successfully")


@router.post("/refresh")
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually refresh OAuth access token.
    This is mainly for testing - token refresh happens automatically
    when needed in the background job and API calls.

    Args:
        current_user: Current user from JWT token
        db: Database session

    Returns:
        Success message
    """
    try:
        auth_service.refresh_access_token(db, current_user)
        return {"message": "Token refreshed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token refresh failed: {str(e)}"
        )
