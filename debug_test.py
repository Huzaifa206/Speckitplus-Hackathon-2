"""
Debug script to test the backend functionality
"""

def test_database_connection():
    """Test database connection and basic operations"""
    try:
        from backend.core.database import get_session, create_db_and_tables
        from backend.services.user_service import create_user, get_user_by_email

        # Create tables
        create_db_and_tables()

        # Test creating a user
        with get_session() as session:
            user = create_user(session, "test@example.com", "Test User", "password123")
            print(f"Created user: {user.email}, ID: {user.id}")

            # Try retrieving the user
            retrieved_user = get_user_by_email(session, "test@example.com")
            print(f"Retrieved user: {retrieved_user.email if retrieved_user else 'None'}")

        print("[OK] Database operations successful!")
        return True
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_models():
    """Test that models can be imported and instantiated"""
    try:
        from backend.models.user import User
        from backend.models.task import Task, TaskBase
        from backend.schemas.task import TaskCreate

        # Test creating a basic task
        task_base = TaskBase(
            title="Test Task",
            description="Test Description",
            user_id="test-user-id"
        )

        print(f"[OK] Models import and instantiation successful: {task_base.title}")
        return True
    except Exception as e:
        print(f"[ERROR] Model error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing backend functionality...\n")

    print("Testing models:")
    models_ok = test_models()

    print("\nTesting database operations:")
    db_ok = test_database_connection()

    print(f"\nResults:")
    print(f"- Models: {'[OK]' if models_ok else '[ERROR]'}")
    print(f"- Database: {'[OK]' if db_ok else '[ERROR]'}")

    if models_ok and db_ok:
        print("\n[SUCCESS] Backend is functioning correctly!")
    else:
        print("\n[FAILURE] Backend has issues that need to be fixed.")