from typing import Optional
from sqlmodel import Session, select
from backend.models.user import User, UserRead
from backend.core.security import get_password_hash, verify_password

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """Get a user by ID"""
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()

import uuid

def create_user(session: Session, email: str, name: str, password: str) -> User:
    """Create a new user"""
    # For now, we'll use a simple string ID - in a real app with Better Auth,
    # this would come from the auth provider
    user_id = str(uuid.uuid4())

    db_user = User(
        id=user_id,
        email=email,
        name=name,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user"""
    # In a real Better Auth integration, we would verify with the external service
    # For this simulation, we'll just check if the user exists
    # since we don't store passwords in our local DB with Better Auth
    user = get_user_by_email(session, email)
    if not user:
        # User doesn't exist
        return None

    # In a real implementation, we'd verify the credentials with Better Auth
    # For this example, we'll assume the user exists and return it
    return user