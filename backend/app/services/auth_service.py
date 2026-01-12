from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional, Tuple
import secrets

from app.config import get_settings
from app.models.user import User
from app.utils.security import token_encryptor, create_access_token
from app.utils.date_utils import is_token_expired

settings = get_settings()


class AuthService:
    """Service for handling Google OAuth authentication and token management"""

    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            }
        }

    def get_authorization_url(self) -> Tuple[str, str]:
        """
        Generate Google OAuth authorization URL.

        Returns:
            Tuple of (authorization_url, state)
        """
        flow = Flow.from_client_config(
            client_config=self.client_config,
            scopes=settings.GOOGLE_SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )

        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)

        authorization_url, _ = flow.authorization_url(
            access_type='offline',  # Request refresh token
            prompt='consent',  # Force consent screen to always get refresh token
            state=state
        )

        return authorization_url, state

    def exchange_code_for_tokens(self, code: str, state: str) -> dict:
        """
        Exchange authorization code for access and refresh tokens.

        Args:
            code: Authorization code from Google callback
            state: State parameter for CSRF protection

        Returns:
            Dictionary containing tokens and token metadata
        """
        flow = Flow.from_client_config(
            client_config=self.client_config,
            scopes=settings.GOOGLE_SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            state=state
        )

        # Exchange code for tokens
        flow.fetch_token(code=code)

        credentials = flow.credentials

        return {
            'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_expires_at': credentials.expiry,
            'scopes': credentials.scopes
        }

    def get_user_info(self, access_token: str) -> dict:
        """
        Get user info from Google using access token.

        Args:
            access_token: Google OAuth access token

        Returns:
            Dictionary containing user information
        """
        credentials = Credentials(token=access_token)
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()

        return {
            'google_id': user_info.get('id'),
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'picture_url': user_info.get('picture')
        }

    def create_or_update_user(
        self,
        db: Session,
        user_info: dict,
        tokens: dict
    ) -> User:
        """
        Create new user or update existing user with OAuth tokens.

        Args:
            db: Database session
            user_info: User information from Google
            tokens: OAuth tokens (access_token, refresh_token, etc.)

        Returns:
            User object
        """
        # Check if user already exists
        user = db.query(User).filter(User.google_id == user_info['google_id']).first()

        # Encrypt tokens before storing
        encrypted_access_token = token_encryptor.encrypt(tokens['access_token'])
        encrypted_refresh_token = token_encryptor.encrypt(tokens['refresh_token'])

        if user:
            # Update existing user
            user.email = user_info['email']
            user.name = user_info.get('name')
            user.picture_url = user_info.get('picture_url')
            user.access_token = encrypted_access_token
            user.refresh_token = encrypted_refresh_token
            user.token_expires_at = tokens['token_expires_at']
            user.is_active = True
        else:
            # Create new user
            user = User(
                google_id=user_info['google_id'],
                email=user_info['email'],
                name=user_info.get('name'),
                picture_url=user_info.get('picture_url'),
                access_token=encrypted_access_token,
                refresh_token=encrypted_refresh_token,
                token_expires_at=tokens['token_expires_at'],
                is_active=True
            )
            db.add(user)

        db.commit()
        db.refresh(user)

        return user

    def refresh_access_token(self, db: Session, user: User) -> str:
        """
        Refresh OAuth access token using refresh token.

        Args:
            db: Database session
            user: User object with encrypted tokens

        Returns:
            New access token (decrypted)
        """
        # Decrypt refresh token
        refresh_token = token_encryptor.decrypt(user.refresh_token)

        # Create credentials with refresh token
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET
        )

        # Refresh the token
        request = Request()
        credentials.refresh(request)

        # Update user with new tokens
        user.access_token = token_encryptor.encrypt(credentials.token)
        user.token_expires_at = credentials.expiry

        # If refresh token changed (rare), update it
        if credentials.refresh_token:
            user.refresh_token = token_encryptor.encrypt(credentials.refresh_token)

        db.commit()
        db.refresh(user)

        return credentials.token

    def get_valid_access_token(self, db: Session, user: User) -> str:
        """
        Get valid access token for user, refreshing if necessary.

        Args:
            db: Database session
            user: User object

        Returns:
            Valid access token (decrypted)
        """
        # Check if token is expired
        if is_token_expired(user.token_expires_at):
            # Refresh token
            return self.refresh_access_token(db, user)
        else:
            # Token still valid, return decrypted
            return token_encryptor.decrypt(user.access_token)

    def create_jwt_token(self, user: User) -> str:
        """
        Create JWT token for user session.

        Args:
            user: User object

        Returns:
            JWT token string
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "google_id": user.google_id
        }

        return create_access_token(token_data)


# Global service instance
auth_service = AuthService()
