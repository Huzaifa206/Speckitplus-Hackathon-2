from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class ConversationBase(SQLModel):
    title: str
    user_id: str
    is_active: bool = True


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    uuid: str
    created_at: datetime
    updated_at: datetime