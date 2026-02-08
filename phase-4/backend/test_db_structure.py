"""
Test script to verify database structure
"""
from core.database import engine
from sqlalchemy import text

def test_table_structure():
    """Test the structure of the tasks table"""

    with engine.connect() as conn:
        if 'sqlite' in str(engine.url):
            # For SQLite
            result = conn.execute(text("PRAGMA table_info(tasks)"))
            columns = result.fetchall()

            print("Tasks table structure:")
            for col in columns:
                print(f"  Column: {col[1]}, Type: {col[2]}, Not Null: {col[3]}, Default: {col[4]}")

            # Check if tags column exists
            column_names = [col[1] for col in columns]
            if 'tags' in column_names:
                print("\n✓ Tags column exists!")
            else:
                print("\n✗ Tags column missing!")
        else:
            # For PostgreSQL
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'tasks'
                ORDER BY ordinal_position
            """))

            columns = result.fetchall()
            print("Tasks table structure:")
            for col in columns:
                print(f"  Column: {col[0]}, Type: {col[1]}, Nullable: {col[2]}, Default: {col[3]}")

            # Check if tags column exists
            column_names = [col[0] for col in columns]
            if 'tags' in column_names:
                print("\n✓ Tags column exists!")
            else:
                print("\n✗ Tags column missing!")

if __name__ == "__main__":
    test_table_structure()