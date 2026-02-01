from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    role: MessageRole
    content: str
    conversation_id: int
    tool_calls: Optional[str] = None
    tool_results: Optional[str] = None


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime