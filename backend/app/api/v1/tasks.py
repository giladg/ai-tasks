from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import date, datetime
from typing import Optional, List

from app.database import get_db
from app.schemas.task import Task as TaskSchema, TaskUpdate, TaskList, TaskCreate
from app.models.task import Task, PriorityEnum, SourceTypeEnum
from app.models.task_edit import TaskEdit, EditTypeEnum
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks")


def log_task_edit(
    db: Session,
    task: Task,
    edit_type: EditTypeEnum,
    old_value: Optional[str] = None,
    new_value: Optional[str] = None
):
    """
    Log a task edit to the task_edits table for learning purposes.

    Args:
        db: Database session
        task: Task that was edited
        edit_type: Type of edit
        old_value: Old value (optional)
        new_value: New value (optional)
    """
    task_edit = TaskEdit(
        task_id=task.id,
        user_id=task.user_id,
        edit_type=edit_type,
        old_value=old_value,
        new_value=new_value
    )
    db.add(task_edit)
    db.commit()


@router.get("", response_model=TaskList)
async def get_tasks(
    date_filter: Optional[date] = Query(None, alias="date", description="Filter by due date"),
    extracted_date: Optional[date] = Query(None, description="Filter by extraction date (YYYY-MM-DD)"),
    latest_only: Optional[bool] = Query(False, description="Show only tasks from latest extraction"),
    is_done: Optional[bool] = Query(None, description="Filter by completion status"),
    is_ai_error: Optional[bool] = Query(None, description="Filter by AI error flag"),
    priority: Optional[PriorityEnum] = Query(None, description="Filter by priority"),
    source_type: Optional[SourceTypeEnum] = Query(None, description="Filter by source type"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get tasks for the current user with optional filters.

    Args:
        date_filter: Filter by due date
        extracted_date: Filter by extraction date
        latest_only: Show only tasks from the latest extraction date
        is_done: Filter by completion status
        is_ai_error: Filter by AI error flag
        priority: Filter by priority level
        source_type: Filter by source type (gmail/calendar)
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of tasks matching the filters
    """
    # Build query
    query = db.query(Task).filter(Task.user_id == current_user.id)

    # Apply filters
    if date_filter is not None:
        query = query.filter(Task.due_date == date_filter)

    if latest_only:
        # Get the latest extraction date for this user
        latest_task = db.query(Task).filter(
            Task.user_id == current_user.id
        ).order_by(Task.extracted_at.desc()).first()

        if latest_task:
            # Filter to tasks extracted on the same date as the latest task
            latest_date = latest_task.extracted_at.date()
            query = query.filter(
                func.date(Task.extracted_at) == latest_date
            )
    elif extracted_date is not None:
        # Filter by specific extraction date
        query = query.filter(
            func.date(Task.extracted_at) == extracted_date
        )

    if is_done is not None:
        query = query.filter(Task.is_done == is_done)

    if is_ai_error is not None:
        query = query.filter(Task.is_ai_error == is_ai_error)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    if source_type is not None:
        query = query.filter(Task.source_type == source_type)

    # Execute query
    tasks = query.order_by(Task.due_date.asc(), Task.priority.desc()).all()

    return TaskList(
        tasks=[TaskSchema.model_validate(task) for task in tasks],
        total=len(tasks)
    )


@router.get("/extraction-dates", response_model=List[date])
async def get_extraction_dates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of unique extraction dates for user's tasks.
    Allows frontend to show date navigation for different extraction batches.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of dates (YYYY-MM-DD) when tasks were extracted, sorted newest first
    """
    # Query distinct extraction dates
    dates = db.query(
        func.date(Task.extracted_at).label('extraction_date')
    ).filter(
        Task.user_id == current_user.id
    ).distinct().order_by(
        func.date(Task.extracted_at).desc()
    ).all()

    # Convert to list of date objects
    return [d.extraction_date for d in dates]


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a single task by ID.

    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Task details
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskSchema.model_validate(task)


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task and log the edit for learning purposes.

    Args:
        task_id: Task ID
        task_update: Updated task data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated task
    """
    # Get task
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Track changes for learning
    if task_update.priority is not None and task_update.priority != task.priority:
        log_task_edit(
            db, task,
            EditTypeEnum.priority_changed,
            old_value=task.priority.value,
            new_value=task_update.priority.value
        )
        task.priority = task_update.priority

    if task_update.is_done is not None and task_update.is_done != task.is_done:
        if task_update.is_done:
            log_task_edit(db, task, EditTypeEnum.marked_done)
        else:
            log_task_edit(db, task, EditTypeEnum.unmarked_done)
        task.is_done = task_update.is_done

    if task_update.is_ai_error is not None and task_update.is_ai_error != task.is_ai_error:
        if task_update.is_ai_error:
            log_task_edit(db, task, EditTypeEnum.marked_ai_error)
        else:
            log_task_edit(db, task, EditTypeEnum.unmarked_ai_error)
        task.is_ai_error = task_update.is_ai_error

    # Update other fields without logging
    if task_update.description is not None:
        task.description = task_update.description

    if task_update.due_date is not None:
        task.due_date = task_update.due_date

    db.commit()
    db.refresh(task)

    return TaskSchema.model_validate(task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task.

    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}


@router.post("/trigger-sync")
async def trigger_sync(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger data sync for current user (for testing).
    This will run the sync job in the background.

    Args:
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    from app.jobs.daily_sync import sync_user_data

    # Run sync in background
    background_tasks.add_task(sync_user_data, current_user.id)

    return {"message": "Sync job queued for execution"}
