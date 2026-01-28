from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.api.deps import get_current_admin_user
from app.models.user import User
from app.models.task import Task
from app.models.task_edit import TaskEdit
from app.schemas.user import User as UserSchema
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])


# Schemas
class UserListItem(BaseModel):
    id: int
    email: str
    name: Optional[str]
    is_active: bool
    is_admin: bool
    has_data_access: bool
    task_count: int
    last_sync_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class UserDetail(BaseModel):
    id: int
    email: str
    name: Optional[str]
    picture_url: Optional[str]
    is_active: bool
    is_admin: bool
    has_data_access: bool
    last_sync_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    task_count: int
    pending_tasks: int
    completed_tasks: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class SystemStats(BaseModel):
    total_users: int
    active_users: int
    admin_users: int
    users_with_data_access: int
    total_tasks: int
    pending_tasks: int
    completed_tasks: int
    tasks_created_today: int
    tasks_created_this_week: int


# Endpoints
@router.get("/users", response_model=List[UserListItem])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_admin: Optional[bool] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all users with optional filters.
    Admin only.
    """
    query = db.query(User)

    # Apply filters
    if search:
        query = query.filter(
            (User.email.ilike(f"%{search}%")) |
            (User.name.ilike(f"%{search}%"))
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)

    # Get users with task count
    users = query.offset(skip).limit(limit).all()

    result = []
    for user in users:
        task_count = db.query(Task).filter(Task.user_id == user.id).count()
        result.append(UserListItem(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            is_admin=user.is_admin,
            has_data_access=user.has_data_access,
            task_count=task_count,
            last_sync_at=user.last_sync_at,
            created_at=user.created_at
        ))

    return result


@router.get("/users/{user_id}", response_model=UserDetail)
async def get_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific user.
    Admin only.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get task counts
    total_tasks = db.query(Task).filter(Task.user_id == user_id).count()
    pending_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_done == False,
        Task.is_ai_error == False
    ).count()
    completed_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_done == True
    ).count()

    return UserDetail(
        id=user.id,
        email=user.email,
        name=user.name,
        picture_url=user.picture_url,
        is_active=user.is_active,
        is_admin=user.is_admin,
        has_data_access=user.has_data_access,
        last_sync_at=user.last_sync_at,
        created_at=user.created_at,
        updated_at=user.updated_at,
        task_count=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks
    )


@router.patch("/users/{user_id}", response_model=UserDetail)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update user settings (activate/deactivate, grant/revoke admin).
    Admin only.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent admin from deactivating or removing admin from themselves
    if user.id == current_admin.id:
        if user_update.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate your own account"
            )
        if user_update.is_admin is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove admin privileges from yourself"
            )

    # Update fields
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    if user_update.is_admin is not None:
        user.is_admin = user_update.is_admin

    db.commit()
    db.refresh(user)

    # Return updated user details
    return await get_user(user_id, current_admin, db)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user and all their data.
    Admin only.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent admin from deleting themselves
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    # Delete user (cascade will delete tasks and task_edits)
    db.delete(user)
    db.commit()

    return {"message": f"User {user.email} deleted successfully"}


@router.post("/users/{user_id}/sync")
async def trigger_user_sync(
    user_id: int,
    background_tasks: BackgroundTasks,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger sync for a specific user.
    Admin only.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.has_data_access:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has not authorized Gmail/Calendar access"
        )

    # Trigger sync in background
    from app.jobs.daily_sync import sync_user_data
    background_tasks.add_task(sync_user_data, user_id)

    return {"message": f"Sync queued for user {user.email}"}


@router.get("/stats", response_model=SystemStats)
async def get_system_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get system-wide statistics.
    Admin only.
    """
    # User stats
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    admin_users = db.query(User).filter(User.is_admin == True).count()
    users_with_data_access = db.query(User).filter(User.has_data_access == True).count()

    # Task stats
    total_tasks = db.query(Task).count()
    pending_tasks = db.query(Task).filter(
        Task.is_done == False,
        Task.is_ai_error == False
    ).count()
    completed_tasks = db.query(Task).filter(Task.is_done == True).count()

    # Tasks created today
    today = datetime.utcnow().date()
    tasks_today = db.query(Task).filter(
        func.date(Task.created_at) == today
    ).count()

    # Tasks created this week
    week_ago = datetime.utcnow() - timedelta(days=7)
    tasks_this_week = db.query(Task).filter(
        Task.created_at >= week_ago
    ).count()

    return SystemStats(
        total_users=total_users,
        active_users=active_users,
        admin_users=admin_users,
        users_with_data_access=users_with_data_access,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        tasks_created_today=tasks_today,
        tasks_created_this_week=tasks_this_week
    )
