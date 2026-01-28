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

    def get_authorization_url(self, flow_type: str = 'login') -> Tuple[str, str]:
        """
        Generate Google OAuth authorization URL.

        Args:
            flow_type: 'login' for initial authentication, 'data' for Gmail/Calendar access

        Returns:
            Tuple of (authorization_url, state)
        """
        if flow_type == 'data':
            scopes = settings.GOOGLE_LOGIN_SCOPES + settings.GOOGLE_DATA_SCOPES
            redirect_uri = settings.GOOGLE_DATA_REDIRECT_URI
        else:
            scopes = settings.GOOGLE_LOGIN_SCOPES
            redirect_uri = settings.GOOGLE_REDIRECT_URI

        flow = Flow.from_client_config(
            client_config=self.client_config,
            scopes=scopes,
            redirect_uri=redirect_uri
        )

        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)

        authorization_url, _ = flow.authorization_url(
            access_type='offline',  # Request refresh token
            prompt='consent' if flow_type == 'data' else 'select_account',  # Force consent for data access
            state=state
        )

        return authorization_url, state

    def exchange_code_for_tokens(self, code: str, state: str, flow_type: str = 'login') -> dict:
        """
        Exchange authorization code for access and refresh tokens.

        Args:
            code: Authorization code from Google callback
            state: State parameter for CSRF protection
            flow_type: 'login' for initial authentication, 'data' for Gmail/Calendar access

        Returns:
            Dictionary containing tokens and token metadata
        """
        if flow_type == 'data':
            scopes = settings.GOOGLE_LOGIN_SCOPES + settings.GOOGLE_DATA_SCOPES
            redirect_uri = settings.GOOGLE_DATA_REDIRECT_URI
        else:
            scopes = settings.GOOGLE_LOGIN_SCOPES
            redirect_uri = settings.GOOGLE_REDIRECT_URI

        flow = Flow.from_client_config(
            client_config=self.client_config,
            scopes=scopes,
            redirect_uri=redirect_uri,
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
        tokens: Optional[dict] = None
    ) -> User:
        """
        Create new user or update existing user.
        For initial login, tokens can be None (user just authenticates).
        For data authorization, tokens contain Gmail/Calendar access.

        Args:
            db: Database session
            user_info: User information from Google
            tokens: Optional OAuth tokens (for data access)

        Returns:
            User object
        """
        # Check if user already exists
        user = db.query(User).filter(User.google_id == user_info['google_id']).first()

        if user:
            # Update existing user
            user.email = user_info['email']
            user.name = user_info.get('name')
            user.picture_url = user_info.get('picture_url')
            user.is_active = True

            # Update tokens if provided (data authorization flow)
            if tokens:
                user.access_token = token_encryptor.encrypt(tokens['access_token'])
                user.refresh_token = token_encryptor.encrypt(tokens['refresh_token'])
                user.token_expires_at = tokens['token_expires_at']
                user.has_data_access = True
        else:
            # Create new user
            user_data = {
                'google_id': user_info['google_id'],
                'email': user_info['email'],
                'name': user_info.get('name'),
                'picture_url': user_info.get('picture_url'),
                'is_active': True,
                'has_data_access': False
            }

            # Add tokens if provided
            if tokens:
                user_data['access_token'] = token_encryptor.encrypt(tokens['access_token'])
                user_data['refresh_token'] = token_encryptor.encrypt(tokens['refresh_token'])
                user_data['token_expires_at'] = tokens['token_expires_at']
                user_data['has_data_access'] = True

            user = User(**user_data)
            db.add(user)

        db.commit()
        db.refresh(user)

        return user

    def has_valid_data_access(self, user: User) -> bool:
        """
        Check if user has valid Gmail/Calendar data access.

        Args:
            user: User object

        Returns:
            True if user has authorized and has valid tokens
        """
        if not user.has_data_access or not user.refresh_token:
            return False

        # If access token exists and not expired, we have access
        if user.access_token and user.token_expires_at:
            if not is_token_expired(user.token_expires_at):
                return True

        # If we have a refresh token, we can get a new access token
        return bool(user.refresh_token)

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
