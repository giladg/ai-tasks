from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model representing a registered user.
    Stores Google OAuth credentials (encrypted) for accessing Gmail and Calendar.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255))
    picture_url = Column(Text)

    # OAuth tokens (stored encrypted using Fernet)
    # Nullable because user might log in without authorizing Gmail/Calendar access initially
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)

    # Track if user has authorized Gmail/Calendar data access
    has_data_access = Column(Boolean, default=False)

    # Sync metadata
    last_sync_at = Column(DateTime, nullable=True)  # Last successful data collection

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    task_edits = relationship("TaskEdit", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"
