"""
MCP (Model Context Protocol) Tools for Task Management
These tools allow the AI assistant to interact with the task management system
"""

from typing import Dict, Any, Optional
from sqlmodel import Session, select
from models.task import Task, TaskBase, TaskUpdate
from models.user import User
from core.database import get_db_session
from datetime import datetime


def add_task(title: str, description: Optional[str] = None, priority: str = "medium",
             due_date: Optional[str] = None, tags: Optional[list] = None, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Create a new task for the user
    """
    try:
        print(f"DEBUG: add_task called with user_id: {user_id}, title: {title}, due_date: {due_date}")

        with get_db_session() as session:
            # Parse due_date if provided
            parsed_due_date = None
            if due_date:
                try:
                    # Try ISO format first (YYYY-MM-DD)
                    parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    try:
                        # Try YYYY-MM-DD format (without time)
                        parsed_due_date = datetime.strptime(due_date, '%Y-%m-%d')
                    except ValueError:
                        try:
                            # Try DD-MM-YYYY format (as mentioned in the example)
                            parsed_due_date = datetime.strptime(due_date, '%d-%m-%Y')
                        except ValueError:
                            # If all formats fail, log and continue without date
                            print(f"Warning: Could not parse date format: {due_date}")
                            parsed_due_date = None

            print(f"DEBUG: parsed_due_date: {parsed_due_date}")

            # Create task object
            task_data = TaskBase(
                title=title,
                description=description,
                priority=priority.lower(),
                user_id=user_id,
                due_date=parsed_due_date
            )

            print(f"DEBUG: Creating task with data: {task_data}")

            task = Task(**task_data.dict())
            session.add(task)
            session.commit()
            session.refresh(task)

            print(f"DEBUG: Task created successfully with ID: {task.id}")

            return {
                "success": True,
                "task_id": task.id,
                "message": f"Task '{task.title}' created successfully"
            }
    except Exception as e:
        print(f"ERROR: Failed to create task: {str(e)}")
        import traceback
        print(f"TRACEBACK: {traceback.format_exc()}")
        return {
            "success": False,
            "message": f"Failed to create task: {str(e)}"
        }


def list_tasks(status: str = "all", priority: str = "all", search: Optional[str] = None,
               limit: Optional[int] = None, offset: Optional[int] = 0, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Retrieve user's tasks with optional filtering
    """
    try:
        with get_db_session() as session:
            statement = select(Task).where(Task.user_id == user_id)

            # Apply filters
            if status != "all":
                if status == "completed":
                    statement = statement.where(Task.completed == True)
                elif status == "pending":
                    statement = statement.where(Task.completed == False)

            if priority != "all":
                statement = statement.where(Task.priority == priority.lower())

            if search:
                statement = statement.where(Task.title.contains(search))

            if limit:
                statement = statement.limit(limit).offset(offset)

            tasks = session.exec(statement).all()

            # Format the tasks
            formatted_tasks = []
            for task in tasks:
                formatted_tasks.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                })

            return {
                "success": True,
                "tasks": formatted_tasks,
                "total_count": len(formatted_tasks),
                "message": f"Retrieved {len(formatted_tasks)} tasks"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to list tasks: {str(e)}",
            "tasks": [],
            "total_count": 0
        }


def complete_task(task_id: int, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Mark a task as completed
    """
    try:
        with get_db_session() as session:
            # Get the task
            task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found or doesn't belong to user"
                }

            # Update the task
            task.completed = True
            session.add(task)
            session.commit()

            return {
                "success": True,
                "message": f"Task '{task.title}' marked as completed"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to complete task: {str(e)}"
        }


def delete_task(task_id: int, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Remove a task
    """
    try:
        with get_db_session() as session:
            # Get the task
            task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found or doesn't belong to user"
                }

            # Delete the task
            session.delete(task)
            session.commit()

            return {
                "success": True,
                "message": f"Task '{task.title}' deleted successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to delete task: {str(e)}"
        }