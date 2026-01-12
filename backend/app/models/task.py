from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class PriorityEnum(str, enum.Enum):
    """Task priority levels"""
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class SourceTypeEnum(str, enum.Enum):
    """Source of task extraction"""
    gmail = "gmail"
    calendar = "calendar"


class Task(Base):
    """
    Task model representing an actionable item extracted from emails or calendar.
    Tasks are linked to a user and can be edited (priority, completion status).
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Task details
    description = Column(Text, nullable=False)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.medium, nullable=False)
    due_date = Column(Date, nullable=True)

    # Source information
    source_type = Column(Enum(SourceTypeEnum), nullable=False)
    source_link = Column(Text, nullable=True)  # URL to Gmail thread or Calendar event
    source_id = Column(String(255), nullable=True)  # Gmail thread ID or Calendar event ID

    # Extraction metadata
    extracted_at = Column(DateTime, nullable=False, server_default=func.now())

    # User actions
    is_done = Column(Boolean, default=False)
    is_ai_error = Column(Boolean, default=False)  # Marked as "not really a task"

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="tasks")
    edits = relationship("TaskEdit", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task(id={self.id}, user_id={self.user_id}, description='{self.description[:50]}...', priority={self.priority})>"
