"""
Migration script to add tags column to tasks table
"""
import os
from sqlmodel import create_engine
from sqlalchemy import text

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine
engine = create_engine(DATABASE_URL)

def add_tags_column():
    """Add tags column to the tasks table"""

    with engine.connect() as conn:
        # Check if tags column exists
        if 'sqlite' in DATABASE_URL:
            # For SQLite
            result = conn.execute(text("PRAGMA table_info(tasks)"))
            columns = [row[1] for row in result.fetchall()]

            if 'tags' not in columns:
                print("Adding 'tags' column to tasks table...")
                conn.execute(text("ALTER TABLE tasks ADD COLUMN tags TEXT DEFAULT NULL"))
                conn.commit()
                print("Tags column added successfully!")
            else:
                print("Tags column already exists")

        else:
            # For PostgreSQL
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'tasks' AND column_name = 'tags'
            """))

            if not result.fetchone():
                print("Adding 'tags' column to tasks table...")
                conn.execute(text("ALTER TABLE tasks ADD COLUMN tags TEXT DEFAULT NULL"))
                conn.commit()
                print("Tags column added successfully!")
            else:
                print("Tags column already exists")

if __name__ == "__main__":
    add_tags_column()