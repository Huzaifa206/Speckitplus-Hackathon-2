from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str

class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[str] = Field(default=None, primary_key=True)  # Using string ID to match with Better Auth
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserRead(UserBase):
    id: str
    created_at: datetime