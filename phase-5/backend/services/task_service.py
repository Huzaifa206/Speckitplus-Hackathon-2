from typing import List, Optional
from sqlmodel import Session, select
from models.task import Task, TaskRead, TaskUpdate, TaskBase
from models.user import User
from datetime import datetime

def get_tasks_by_user(
    session: Session,
    user_id: str,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None
) -> List[Task]:
    """Get tasks for a specific user with optional filtering and sorting"""
    statement = select(Task).where(Task.user_id == user_id)

    # Apply search filter
    if search:
        statement = statement.where(
            Task.title.contains(search) |
            (Task.description != None) & Task.description.contains(search)
        )

    # Apply priority filter
    if priority and priority != 'all':
        statement = statement.where(Task.priority == priority)

    # Apply sorting
    if sort == 'due_date':
        if order == 'desc':
            statement = statement.order_by(Task.due_date.desc())
        else:
            statement = statement.order_by(Task.due_date.asc())
    elif sort == 'priority':
        if order == 'desc':
            statement = statement.order_by(Task.priority.desc())
        else:
            statement = statement.order_by(Task.priority.asc())
    elif sort == 'title':
        if order == 'desc':
            statement = statement.order_by(Task.title.desc())
        else:
            statement = statement.order_by(Task.title.asc())
    elif sort == 'created_at' or sort is None:
        if order == 'desc':
            statement = statement.order_by(Task.created_at.desc())
        else:
            statement = statement.order_by(Task.created_at.asc())

    tasks = session.exec(statement).all()
    return tasks

def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task

def create_task(session: Session, task_data, user_id: str) -> Task:
    """Create a new task"""
    # Convert task_data to dict and add user_id
    task_dict = task_data.model_dump()
    task_dict['user_id'] = user_id

    # Handle tags conversion if they exist as a list
    if 'tags' in task_dict and isinstance(task_dict['tags'], list):
        import json
        task_dict['tags'] = json.dumps(task_dict['tags'])
    elif 'tags' in task_dict and task_dict['tags'] is None:
        # If tags is None, set it to empty JSON array string
        task_dict['tags'] = '[]'

    # Create the task with the user_id
    db_task = Task(**task_dict)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

def update_task(session: Session, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """Update a task"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        return None

    # Update task fields
    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == 'tags':
            if isinstance(value, list):
                # Convert tags list to JSON string for storage
                import json
                setattr(db_task, field, json.dumps(value))
            elif value is None:
                # Handle None value for tags
                setattr(db_task, field, '[]')
            else:
                # Assume it's already a string
                setattr(db_task, field, value)
        else:
            setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

def delete_task(session: Session, task_id: int, user_id: str) -> bool:
    """Delete a task"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True