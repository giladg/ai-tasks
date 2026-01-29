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
from app.config import get_settings

router = APIRouter(prefix="/auth")
settings = get_settings()


@router.get("/google/login", response_model=GoogleAuthURL)
async def google_login():
    """
    Initiate Google OAuth flow for basic login (authentication only).
    User will need to separately authorize Gmail/Calendar access.
    Returns authorization URL to redirect user to Google consent screen.
    """
    authorization_url, state = auth_service.get_authorization_url(flow_type='login')

    return GoogleAuthURL(authorization_url=authorization_url)


@router.get("/google/callback")
async def google_callback(
    code: str = Query(..., description="Authorization code from Google"),
    state: str = Query(..., description="State parameter for CSRF protection"),
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback for initial login (authentication only).
    Creates user account without Gmail/Calendar access.

    Args:
        code: Authorization code from Google
        state: State parameter for CSRF protection
        db: Database session

    Returns:
        Redirect to frontend with JWT token
    """
    try:
        # Exchange code for tokens (login flow only gets basic profile info)
        tokens = auth_service.exchange_code_for_tokens(code, state, flow_type='login')

        # Get user info from Google
        user_info = auth_service.get_user_info(tokens['access_token'])

        # Create or update user WITHOUT data access tokens
        user = auth_service.create_or_update_user(db, user_info, tokens=None)

        # Create JWT token for session
        jwt_token = auth_service.create_jwt_token(user)

        # Redirect to frontend with token
        frontend_callback = f"{settings.FRONTEND_URL}/auth/callback"
        redirect_url = f"{frontend_callback}?token={jwt_token}"

        return RedirectResponse(url=redirect_url)

    except Exception as e:
        # Redirect to frontend with error
        error_message = urllib.parse.quote(str(e))
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/login?error={error_message}"
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


@router.get("/google/authorize-data", response_model=GoogleAuthURL)
async def google_authorize_data(current_user: User = Depends(get_current_user)):
    """
    Initiate Gmail and Calendar data authorization flow.
    User must be logged in to authorize data access.

    Args:
        current_user: Current authenticated user

    Returns:
        Authorization URL for Gmail/Calendar access
    """
    # Pass user's email and ID - email for login_hint, ID embedded in state for callback
    authorization_url, state = auth_service.get_authorization_url(
        flow_type='data',
        user_email=current_user.email,
        user_id=current_user.id
    )

    return GoogleAuthURL(authorization_url=authorization_url)


@router.get("/google/data-callback")
async def google_data_callback(
    code: str = Query(..., description="Authorization code from Google"),
    state: str = Query(..., description="State parameter for CSRF protection"),
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback for Gmail/Calendar data authorization.
    Updates existing user with data access tokens.

    Args:
        code: Authorization code from Google
        state: State parameter with embedded user_id
        db: Database session

    Returns:
        Redirect to frontend dashboard
    """
    try:
        # Decode state to get user_id
        state_data = auth_service.decode_state_token(state)
        if not state_data or 'user_id' not in state_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid state parameter"
            )

        user_id = state_data['user_id']

        # Get user from database
        current_user = db.query(User).filter(User.id == user_id).first()
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Exchange code for tokens (data flow gets Gmail/Calendar access)
        tokens = auth_service.exchange_code_for_tokens(code, state, flow_type='data')

        # Get user info to verify identity
        user_info = auth_service.get_user_info(tokens['access_token'])

        # Verify that the authorized account matches the logged-in user
        if user_info['email'] != current_user.email:
            error_message = urllib.parse.quote(
                f"Account mismatch: You are logged in as {current_user.email} but authorized {user_info['email']}. "
                f"Please authorize with the correct account."
            )
            return RedirectResponse(
                url=f"{settings.FRONTEND_URL}/dashboard?error={error_message}"
            )

        # Update user with data access tokens
        user = auth_service.create_or_update_user(db, user_info, tokens=tokens)

        # Redirect to frontend dashboard
        redirect_url = f"{settings.FRONTEND_URL}/dashboard?authorized=true"

        return RedirectResponse(url=redirect_url)

    except HTTPException:
        raise
    except Exception as e:
        # Redirect to frontend with error
        error_message = urllib.parse.quote(str(e))
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/dashboard?error={error_message}"
        )


@router.get("/status")
async def auth_status(current_user: User = Depends(get_current_user)):
    """
    Check user's authorization status.
    Returns whether user has authorized Gmail/Calendar access.

    Args:
        current_user: Current authenticated user

    Returns:
        Authorization status
    """
    has_data_access = auth_service.has_valid_data_access(current_user)

    return {
        "authenticated": True,
        "has_data_access": has_data_access,
        "email": current_user.email,
        "name": current_user.name
    }
