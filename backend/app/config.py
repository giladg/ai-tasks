from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All settings can be overridden via .env file.
    """

    # App Configuration
    APP_NAME: str = "AI Task Manager"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./taskmanager.db"

    # Security - JWT
    SECRET_KEY: str  # Required: For JWT signing
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Security - Token Encryption
    ENCRYPTION_KEY: str  # Required: Fernet key for encrypting OAuth tokens

    # Google OAuth
    GOOGLE_CLIENT_ID: str  # Required
    GOOGLE_CLIENT_SECRET: str  # Required
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"
    GOOGLE_SCOPES: List[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/calendar.readonly"
    ]

    # Gemini AI
    GEMINI_API_KEY: str  # Required
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # Background Jobs
    SCHEDULER_TIMEZONE: str = "UTC"
    DAILY_SYNC_HOUR: int = 2  # 2 AM daily sync
    DAILY_SYNC_MINUTE: int = 0

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # Gmail Settings
    GMAIL_LOOKBACK_DAYS: int = 14  # Fetch emails from last 14 days

    # Calendar Settings
    CALENDAR_LOOKBACK_DAYS: int = 7  # Fetch past events from last 7 days
    CALENDAR_LOOKFORWARD_DAYS: int = 14  # Fetch future events for next 14 days

    # Learning Context
    LEARNING_CONTEXT_WEEKS: int = 4  # Use last 4 weeks of edits for learning

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    This ensures we only load the .env file once.
    """
    return Settings()
