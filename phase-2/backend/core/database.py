from sqlmodel import create_engine, Session
from typing import Generator
import os
from contextlib import contextmanager

# Database URL - defaults to a local SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=False)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Create tables
def create_db_and_tables():
    from models.user import User
    from models.task import Task
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)