from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: PriorityEnum = PriorityEnum.medium
    user_id: str = Field(foreign_key="users.id", index=True)
    due_date: Optional[datetime] = None
    is_recurring: bool = False
    recurring_interval: Optional[str] = None  # daily, weekly, etc.
    tags: Optional[str] = None  # Store tags as JSON string for now

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskRead(TaskBase):
    id: int
    created_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurring_interval: Optional[str] = None
    tags: Optional[str] = None  # Store as JSON string