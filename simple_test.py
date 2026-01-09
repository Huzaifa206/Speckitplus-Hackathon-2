"""
Simple test to verify the application structure and imports
"""

def test_backend_imports():
    """Test that all backend modules can be imported without errors"""
    try:
        # Test core modules
        print("Testing core imports...")
        from backend.core.database import get_session, create_db_and_tables
        print("[OK] Database imports successful")

        from backend.core.security import create_access_token, verify_token
        print("[OK] Security imports successful")

        # Test models
        print("\nTesting model imports...")
        from backend.models.user import User, UserBase
        print("[OK] User model imports successful")

        from backend.models.task import Task, TaskBase, PriorityEnum
        print("[OK] Task model imports successful")

        # Test services
        print("\nTesting service imports...")
        from backend.services.user_service import get_user_by_email, create_user
        print("[OK] User service imports successful")

        from backend.services.task_service import get_tasks_by_user, create_task
        print("[OK] Task service imports successful")

        # Test API routes
        print("\nTesting API imports...")
        from backend.api.auth import router as auth_router
        print("[OK] Auth API imports successful")

        from backend.api.tasks import router as tasks_router
        print("[OK] Tasks API imports successful")

        # Test main app
        print("\nTesting main app import...")
        from backend.main import app
        print("[OK] Main app import successful")

        print("\n[OK] All backend modules imported successfully")
        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Testing application structure...\n")

    test_backend_imports()