from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: PriorityEnum = PriorityEnum.medium
    user_id: str
    due_date: Optional[datetime] = None
    is_recurring: bool = False
    recurring_interval: Optional[str] = None  # daily, weekly, etc.
    tags: Optional[List[str]] = []  # Add tags field

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None
    is_recurring: bool = False
    recurring_interval: Optional[str] = None  # daily, weekly, etc.
    tags: Optional[List[str]] = []  # Add tags field

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurring_interval: Optional[str] = None
    tags: Optional[List[str]] = None

class TaskFilterParams(BaseModel):
    search: Optional[str] = None
    priority: Optional[str] = None
    sort: Optional[str] = None
    order: Optional[str] = None