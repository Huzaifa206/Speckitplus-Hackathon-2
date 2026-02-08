from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True