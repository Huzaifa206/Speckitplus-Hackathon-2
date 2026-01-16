from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from core.database import get_session
from core.security import get_current_user
from schemas.task import TaskCreate, TaskCreateRequest, TaskRead, TaskUpdate
from services.task_service import (
    get_tasks_by_user,
    get_task_by_id,
    create_task,
    update_task,
    delete_task
)

router = APIRouter(prefix="/users/{user_id}/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user),
    search: Optional[str] = Query(None, description="Search in title and description"),
    priority: Optional[str] = Query(None, description="Filter by priority (high, medium, low, all)"),
    sort: Optional[str] = Query(None, description="Sort by (due_date, priority, title, created_at)"),
    order: Optional[str] = Query(None, description="Sort order (asc, desc)")
):
    """Get all tasks for a specific user with optional filtering and sorting"""
    # Verify that the user is requesting their own tasks
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    tasks = get_tasks_by_user(
        session=session,
        user_id=user_id,
        search=search,
        priority=priority,
        sort=sort,
        order=order
    )
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
async def read_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """Get a specific task by ID"""
    # Verify that the user is requesting their own task
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskRead)
async def create_new_task(
    user_id: str,
    task: TaskCreateRequest,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """Create a new task for a user"""
    # Verify that the user is creating a task for themselves
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create the task with the authenticated user's ID
    created_task = create_task(session=session, task_data=task, user_id=user_id)
    return created_task


@router.put("/{task_id}", response_model=TaskRead)
async def update_existing_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """Update a specific task"""
    # Verify that the user is updating their own task
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    updated_task = update_task(
        session=session,
        task_id=task_id,
        user_id=user_id,
        task_update=task_update
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
async def delete_existing_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """Delete a specific task"""
    # Verify that the user is deleting their own task
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user's tasks"
        )

    success = delete_task(session=session, task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}