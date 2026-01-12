from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class EditTypeEnum(str, enum.Enum):
    """Types of task edits tracked for learning"""
    priority_changed = "priority_changed"
    marked_done = "marked_done"
    marked_ai_error = "marked_ai_error"
    unmarked_done = "unmarked_done"
    unmarked_ai_error = "unmarked_ai_error"


class TaskEdit(Base):
    """
    TaskEdit model representing user edits to tasks.
    Used to build learning context for improving Gemini task extraction.
    Tracks changes to priority, completion status, and AI error flags.
    """

    __tablename__ = "task_edits"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Edit details
    edit_type = Column(Enum(EditTypeEnum), nullable=False)
    old_value = Column(Text, nullable=True)  # JSON or simple value
    new_value = Column(Text, nullable=True)  # JSON or simple value

    # Timestamp
    created_at = Column(DateTime, server_default=func.now(), index=True)

    # Relationships
    task = relationship("Task", back_populates="edits")
    user = relationship("User", back_populates="task_edits")

    def __repr__(self):
        return f"<TaskEdit(id={self.id}, task_id={self.task_id}, edit_type={self.edit_type})>"
