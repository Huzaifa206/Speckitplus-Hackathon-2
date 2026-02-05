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

@router.get("/")
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

    # Convert tasks to proper format with parsed tags
    import json
    formatted_tasks = []
    for task in tasks:
        # Parse tags from JSON string if they exist
        tags_list = []
        if task.tags:
            try:
                tags_list = json.loads(task.tags)
            except (json.JSONDecodeError, TypeError):
                tags_list = []

        # Create a dict with the proper format
        task_dict = task.dict()
        task_dict['tags'] = tags_list
        formatted_tasks.append(task_dict)

    return formatted_tasks


@router.get("/{task_id}")
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

    # Parse tags from JSON string if they exist
    import json
    tags_list = []
    if task.tags:
        try:
            tags_list = json.loads(task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_list = []

    # Create a dict with the proper format
    task_dict = task.dict()
    task_dict['tags'] = tags_list

    return task_dict


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

    # Parse tags from JSON string if they exist
    import json
    tags_list = []
    if created_task.tags:
        try:
            tags_list = json.loads(created_task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_list = []

    # Create a dict with the proper format
    task_dict = created_task.dict()
    task_dict['tags'] = tags_list

    return task_dict


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

    # Parse tags from JSON string if they exist
    import json
    tags_list = []
    if updated_task.tags:
        try:
            tags_list = json.loads(updated_task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_list = []

    # Create a dict with the proper format
    task_dict = updated_task.dict()
    task_dict['tags'] = tags_list

    return task_dict


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