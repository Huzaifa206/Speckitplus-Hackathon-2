from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskOperation(str, Enum):
    ADD = "add"
    LIST = "list"
    COMPLETE = "complete"
    DELETE = "delete"


class TaskCommand(BaseModel):
    """Structured output for task management commands"""
    operation: TaskOperation = Field(..., description="The operation to perform: add, list, complete, or delete")
    task_id: Optional[int] = Field(None, description="Task ID for complete/delete operations")
    title: Optional[str] = Field(None, description="Task title for add operations")
    description: Optional[str] = Field(None, description="Task description for add operations")
    priority: Optional[TaskPriority] = Field(None, description="Task priority for add operations")
    due_date: Optional[str] = Field(None, description="Due date in YYYY-MM-DD or DD-MM-YYYY format")
    tags: Optional[List[str]] = Field(None, description="List of tags for the task")
    status_filter: Optional[str] = Field(None, description="Status filter for list operations: all, completed, pending")
    priority_filter: Optional[str] = Field(None, description="Priority filter for list operations: all, high, medium, low")
    search_term: Optional[str] = Field(None, description="Search term for list operations")


class TaskResponse(BaseModel):
    """Structured output for task responses"""
    success: bool
    message: str
    task_id: Optional[int] = None
    tasks: Optional[List[dict]] = None


# Function definitions for OpenAI function calling
FUNCTION_DEFINITIONS = [
    {
        "name": "add_task",
        "description": "Add a new task",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description"},
                "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "Task priority"},
                "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD or DD-MM-YYYY format"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "List of tags for the task"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "List tasks with optional filters",
        "parameters": {
            "type": "object",
            "properties": {
                "status_filter": {"type": "string", "enum": ["all", "completed", "pending"], "description": "Status filter"},
                "priority_filter": {"type": "string", "enum": ["all", "high", "medium", "low"], "description": "Priority filter"},
                "search_term": {"type": "string", "description": "Search term to filter tasks"}
            }
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as completed",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "ID of the task to complete"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "ID of the task to delete"}
            },
            "required": ["task_id"]
        }
    }
]