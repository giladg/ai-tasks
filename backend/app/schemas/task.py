from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from app.models.task import PriorityEnum, SourceTypeEnum


class TaskBase(BaseModel):
    """Base task schema with common fields"""
    description: str
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[date] = None


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    source_type: SourceTypeEnum
    source_link: Optional[str] = None
    source_id: Optional[str] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[date] = None
    is_done: Optional[bool] = None
    is_ai_error: Optional[bool] = None


class Task(TaskBase):
    """Schema for task response"""
    id: int
    user_id: int
    source_type: SourceTypeEnum
    source_link: Optional[str] = None
    source_id: Optional[str] = None
    extracted_at: datetime
    is_done: bool
    is_ai_error: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    """Schema for list of tasks with pagination"""
    tasks: list[Task]
    total: int


class TaskFilter(BaseModel):
    """Schema for task filtering parameters"""
    date: Optional[date] = None
    is_done: Optional[bool] = None
    is_ai_error: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    source_type: Optional[SourceTypeEnum] = None
